# VitaClin (fictitious company)

> **Fictitious.** VitaClin does not exist. It is the scenario used for every exercise in this portfolio.

## Profile

| Item | Description |
|---|---|
| Business | Health-tech SaaS: online scheduling, electronic health records and telemedicine for small clinics |
| Headquarters | Brasília, Brazil |
| Markets | Brazil (main) and Spain (pilot with 3 clinics in Madrid) |
| Size | 60 employees; about 400 client clinics; about 250,000 patients in the platform |
| Role under LGPD / GDPR | **Processor** (operador) for clinic patient data; **controller** for its own employees, leads and clinic users |
| Infrastructure | Web app (Next.js), API (Node.js), PostgreSQL, file storage for exams and recordings, hosted on a public cloud in São Paulo; backups replicated to the EU region for the Spanish clients |
| Third parties | Cloud provider, payment gateway, email/SMS provider, video-call provider for telemedicine, CRM, analytics |

## Data in scope

- **Patients:** name, CPF/DNI, date of birth, contact, health records, exam files, telemedicine recordings (**sensitive data**, art. 11 LGPD / art. 9 GDPR), including **children** (art. 14 LGPD / art. 8 GDPR).
- **Clinic users:** name, professional registration (CRM/CRO), login, access logs.
- **Employees:** HR data, payroll, health certificates.
- **Leads and marketing:** name, email, phone, website behaviour (cookies).

## Upcoming changes that trigger the exercises

1. Launch of **telemedicine with recorded consultations** (needs a DPIA / RIPD).
2. Expansion to **Spain** (GDPR, international transfers, EU representative).
3. Large hospital client requires **ISO/IEC 27001 certification** in 12 months (gap analysis, risk register, policies).
4. Marketing wants to use patient app data for **campaigns** (legitimate interest assessment).
