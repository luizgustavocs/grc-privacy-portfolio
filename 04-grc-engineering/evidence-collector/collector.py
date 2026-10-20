"""Evidence collector: automated checks mapped to ISO/IEC 27002:2022 controls.

Runs read-only checks against:
  * a website you own or are authorised to assess (HTTPS and security headers);
  * GitHub repositories you administer (branch protection, Dependabot alerts).

Writes a Markdown report with the result, the evidence and the mapped control.
Standard library only (no dependencies).

Usage:
  python collector.py --url https://example.com
  python collector.py --url https://example.com --repo owner/name --branch main
  (GitHub checks need a token with admin read access in the GITHUB_TOKEN environment variable)
"""

import argparse
import datetime as dt
import json
import os
import ssl
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

SECURITY_HEADERS = {
    "strict-transport-security": ("HSTS", "8.24 Use of cryptography"),
    "content-security-policy": ("Content Security Policy", "8.28 Secure coding"),
    "x-content-type-options": ("X-Content-Type-Options", "8.28 Secure coding"),
    "x-frame-options": ("X-Frame-Options (or CSP frame-ancestors)", "8.28 Secure coding"),
    "referrer-policy": ("Referrer-Policy", "5.34 Privacy and protection of PII"),
}


def result(check, status, evidence, control):
    return {"check": check, "status": status, "evidence": evidence, "control": control}


def check_website(url):
    out = []
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        out.append(result("HTTPS in use", "FAIL", f"URL scheme is {parsed.scheme}", "8.24 Use of cryptography"))
        return out

    # TLS version and certificate expiry
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((parsed.hostname, parsed.port or 443), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=parsed.hostname) as tls:
                version = tls.version()
                cert = tls.getpeercert()
        expires = dt.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days = (expires - dt.datetime.utcnow()).days
        out.append(result("TLS version", "PASS" if version in ("TLSv1.2", "TLSv1.3") else "FAIL",
                          f"Negotiated {version}", "8.24 Use of cryptography"))
        out.append(result("Certificate validity", "PASS" if days > 15 else "WARN",
                          f"Expires {expires:%Y-%m-%d} ({days} days)", "8.24 Use of cryptography"))
    except (OSError, ssl.SSLError, KeyError, ValueError) as exc:
        out.append(result("TLS handshake", "FAIL", f"Error: {exc}", "8.24 Use of cryptography"))

    # Security headers
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "evidence-collector/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.URLError as exc:
        out.append(result("HTTP response", "FAIL", f"Error: {exc}", "8.28 Secure coding"))
        return out

    for name, (label, control) in SECURITY_HEADERS.items():
        value = headers.get(name)
        if name == "x-frame-options" and not value and "frame-ancestors" in headers.get("content-security-policy", ""):
            value = "covered by CSP frame-ancestors"
        out.append(result(f"Header: {label}", "PASS" if value else "FAIL",
                          value[:120] if value else "Missing", control))

    server = headers.get("server", "")
    exposes_version = any(ch.isdigit() for ch in server)
    out.append(result("Server version not disclosed", "WARN" if exposes_version else "PASS",
                      f"Server: {server or '(not sent)'}", "8.9 Configuration management"))
    return out


def github_get(path, token):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "evidence-collector/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read()
            return resp.status, (json.loads(body) if body else None)
    except urllib.error.HTTPError as exc:
        return exc.code, None


def check_github(repo, branch, token):
    out = []
    status, data = github_get(f"/repos/{repo}/branches/{branch}/protection", token)
    if status == 200:
        reviews = (data or {}).get("required_pull_request_reviews") or {}
        approvals = reviews.get("required_approving_review_count", 0)
        out.append(result(f"Branch protection on {branch}", "PASS",
                          f"Enabled; required approvals: {approvals}", "8.32 Change management"))
        out.append(result("Pull request review required", "PASS" if approvals >= 1 else "FAIL",
                          f"Required approvals: {approvals}", "8.32 Change management"))
    else:
        out.append(result(f"Branch protection on {branch}", "FAIL",
                          f"Not enabled or not readable (HTTP {status})", "8.32 Change management"))

    status, _ = github_get(f"/repos/{repo}/vulnerability-alerts", token)
    out.append(result("Dependabot vulnerability alerts", "PASS" if status == 204 else "FAIL",
                      "Enabled" if status == 204 else f"Disabled or not readable (HTTP {status})",
                      "8.8 Management of technical vulnerabilities"))
    return out


def to_markdown(target, results):
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "WARN", "FAIL")}
    lines = [f"# Evidence report: {target}", "",
             f"Generated: {now} | PASS: {counts['PASS']} | WARN: {counts['WARN']} | FAIL: {counts['FAIL']}", "",
             "| Check | Status | Evidence | ISO/IEC 27002 control |", "|---|---|---|---|"]
    for r in results:
        evidence = r["evidence"].replace("|", "\\|")
        lines.append(f"| {r['check']} | {r['status']} | {evidence} | {r['control']} |")
    lines += ["", "> Automated, read-only checks. They support, but do not replace, a full control assessment."]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", help="HTTPS URL of a site you own or are authorised to assess")
    parser.add_argument("--repo", help="GitHub repository owner/name you administer")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--out", default="evidence-report.md")
    args = parser.parse_args()
    if not args.url and not args.repo:
        parser.error("use --url and/or --repo")

    results = []
    if args.url:
        results += check_website(args.url)
    if args.repo:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN is not set (needed for GitHub checks)")
        results += check_github(args.repo, args.branch, token)

    report = to_markdown(args.url or args.repo, results)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(report + "\n")
    print(report)


if __name__ == "__main__":
    main()
