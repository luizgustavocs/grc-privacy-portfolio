# DevSecOps Lab: secure software supply chain

[![DevSecOps pipeline](https://github.com/luizgustavocs/grc-privacy-portfolio/actions/workflows/devsecops.yml/badge.svg)](https://github.com/luizgustavocs/grc-privacy-portfolio/actions/workflows/devsecops.yml)

A small API from **VitaClin** (the fictitious health-tech used across this portfolio) delivered through a pipeline that builds security into every stage. Each stage is mapped to the ISO/IEC 27002:2022 control and the NIST SSDF (SP 800-218) practice it produces evidence for, so the pipeline is also a source of **continuous audit evidence**.

## Pipeline

```
push / pull request
   |
   +-- Secret scanning (Gitleaks)
   +-- SAST (Semgrep: Python, Dockerfile and GitHub Actions rules)
   +-- Dependency audit (pip-audit) and tests (pytest)
   |
   +-- Build image -> Dockerfile misconfiguration scan -> image vulnerability scan (Trivy) -> SBOM (CycloneDX)
   |
   +-- main only: push to GHCR -> Cosign keyless signature (OIDC) -> SBOM attestation -> signature verification
```

Workflow: [`.github/workflows/devsecops.yml`](../.github/workflows/devsecops.yml)

## Control mapping

| Stage | What it prevents | ISO/IEC 27002:2022 | NIST SSDF |
|---|---|---|---|
| Gitleaks | Credentials committed to the repository | 5.17 Authentication information, 8.4 Access to source code | PS.1 |
| Semgrep | Insecure code patterns, Dockerfile and workflow misconfigurations | 8.28 Secure coding, 8.29 Security testing | PW.7 |
| pip-audit and Trivy image scan | Components with known vulnerabilities (fails on fixable HIGH and CRITICAL) | 8.8 Management of technical vulnerabilities | PW.4, RV.1 |
| Trivy config scan | Container misconfiguration (root user, missing healthcheck) | 8.9 Configuration management | PW.9 |
| Unit and security tests | Regressions in input validation, security headers and disabled API docs | 8.29 Security testing | PW.8 |
| SBOM (CycloneDX) | Not knowing which components are in production | 5.21 ICT supply chain security, 5.9 Inventory of assets | PS.3 |
| Cosign keyless signature and attestation | Running an image that was not built by this pipeline | 5.21 ICT supply chain security, 8.32 Change management | PS.2 |
| Actions pinned by SHA, least-privilege permissions, OIDC instead of stored keys | Compromised third-party actions and stolen long-lived secrets | 5.21, 8.2 Privileged access rights | PO.3 |

## Privacy by design in the application

- `patient_ref` only accepts a **pseudonymised reference** (`P-000123`); a CPF or a name is rejected (LGPD art. 6, III, minimisation; GDPR art. 25).
- Logs record only the technical identifier of the appointment, never patient data.
- API documentation endpoints are disabled in production and security headers are set on every response.
- The container runs as a non-root user and ships only the runtime dependencies (multi-stage build).

## Verify the published image yourself

```bash
cosign verify ghcr.io/luizgustavocs/vitaclin-appointments-api:<commit-sha> \
  --certificate-identity-regexp "^https://github.com/luizgustavocs/grc-privacy-portfolio/.github/workflows/devsecops.yml@" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

## Run locally

```bash
cd 06-devsecops/app
pip install -r requirements-dev.txt
python -m pytest -q
docker build -t vitaclin-api .
docker run --rm -p 8000:8000 vitaclin-api
```

## Roadmap

- [ ] Terraform for the cloud resources, scanned with Checkov in the pipeline
- [ ] GitHub to AWS authentication with OIDC (no access keys)
- [ ] Kubernetes deployment (kind) with hardened `securityContext`
- [ ] Kyverno policies: non-root only, no `latest` tag, only images signed by this pipeline
- [ ] DAST with OWASP ZAP against the running container
