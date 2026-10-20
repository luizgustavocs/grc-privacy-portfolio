# Evidence Collector (compliance as code)

Small Python tool that runs **read-only** checks and produces a Markdown evidence report, mapping each check to an **ISO/IEC 27002:2022** control. It shows how GRC evidence collection can be automated instead of gathered by screenshots.

Standard library only: no installation needed beyond Python 3.10+.

## Checks

| Check | Source | ISO/IEC 27002 control |
|---|---|---|
| TLS 1.2+ negotiated | Website | 8.24 Use of cryptography |
| Certificate valid for more than 15 days | Website | 8.24 Use of cryptography |
| HSTS header | Website | 8.24 Use of cryptography |
| Content-Security-Policy, X-Content-Type-Options, X-Frame-Options | Website | 8.28 Secure coding |
| Referrer-Policy | Website | 5.34 Privacy and protection of PII |
| Server version not disclosed | Website | 8.9 Configuration management |
| Branch protection and required pull request review | GitHub | 8.32 Change management |
| Dependabot vulnerability alerts enabled | GitHub | 8.8 Management of technical vulnerabilities |

## Usage

```bash
python collector.py --url https://your-site.example
```

```bash
GITHUB_TOKEN=<token> python collector.py --url https://your-site.example --repo owner/repo --branch main
```

The report is printed and saved to `evidence-report.md`.

**Only run it against sites and repositories you own or are authorised to assess.**

## Example output

| Check | Status | Evidence | ISO/IEC 27002 control |
|---|---|---|---|
| TLS version | PASS | Negotiated TLSv1.3 | 8.24 Use of cryptography |
| Header: HSTS | PASS | max-age=63072000; includeSubDomains | 8.24 Use of cryptography |
| Header: Referrer-Policy | PASS | no-referrer | 5.34 Privacy and protection of PII |

## Roadmap

- [ ] Cloud checks (storage buckets not public, MFA on root account, logging enabled)
- [ ] JSON output for import into CISO Assistant
- [ ] Scheduled run in GitHub Actions with the report stored as an artifact (continuous evidence)
