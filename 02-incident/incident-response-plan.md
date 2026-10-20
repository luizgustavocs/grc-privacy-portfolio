# Security and Personal Data Incident Response Plan

**Organisation:** VitaClin (fictitious) | **Version:** `<v1.0>` | **Owner:** CISO / DPO | **Approved by:** `<board>`

References: NIST SP 800-61; ISO/IEC 27001 controls 5.24 to 5.28; LGPD art. 48 and the ANPD incident reporting regulation; GDPR arts. 33 and 34.

## 1. Roles

| Role | Responsibility | Name / backup |
|---|---|---|
| Incident manager | Coordinates the response and decisions | |
| Technical lead | Containment, investigation, recovery | |
| DPO / Encarregado | Assesses risk to data subjects; decides and prepares notifications | |
| Legal | Contracts, liability, law enforcement | |
| Communication | Messages to clients, data subjects and press | |
| Executive sponsor | Approves notifications and budget | |

## 2. Severity classification

| Level | Criteria | Example | Activation |
|---|---|---|---|
| Low | No personal data or no relevant risk | Phishing email blocked | Technical team |
| Medium | Limited personal data, low risk | Email sent to wrong recipient with name and phone | Incident manager + DPO |
| High | Sensitive data, large volume or relevant risk | Unauthorised access to health records | Full team + executive |
| Critical | Service unavailable or mass exposure of sensitive data | Ransomware on production database | Full team, external support |

## 3. Phases

1. **Preparation:** contacts, tools, backups tested, logs retained, playbooks.
2. **Detection and analysis:** record date and time of awareness; what happened, which data, how many data subjects, which systems.
3. **Containment:** isolate systems, revoke credentials, preserve evidence (chain of custody).
4. **Eradication and recovery:** remove the cause, restore from clean backups, monitor.
5. **Notification decision:** see section 4.
6. **Lessons learned:** report within `<x days>`, update risks, controls and this plan.

## 4. Notification decision (DPO)

| Question | Answer |
|---|---|
| Does the incident involve personal data? | |
| Can it cause **relevant risk or damage** to data subjects (sensitive data, children, financial data, large scale, data that enables fraud)? | |
| Was the data protected (encryption with uncompromised key)? | |
| **Brazil:** notify ANPD and data subjects within the deadline set by the ANPD regulation (check the current text) | |
| **EU:** notify the authority within **72 hours** of awareness (GDPR art. 33); data subjects without undue delay if high risk (art. 34) | |
| Contractual duties to notify clients (VitaClin is a processor for the clinics) | |

Every incident, notified or not, goes into the **incident register** with the reasoning of the decision.

## 5. Templates

- [ANPD notification](anpd-notification-template.md)
- Notice to data subjects
- Notice to client clinics (controllers)
