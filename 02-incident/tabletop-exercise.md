# Tabletop Exercise: Leaked Telemedicine Recordings

**Scenario (fictitious):** on a Monday at 09:10, a security researcher emails VitaClin saying that a public storage bucket contains about 3,000 telemedicine recordings, including consultations with children. The bucket was created for a migration test two weeks earlier.

## Injects (reveal one at a time)

| Time | Inject | Decisions to record |
|---|---|---|
| T+0 | Researcher's email arrives at the support inbox | Who is called? Is the incident confirmed? |
| T+1h | Logs show the bucket was accessed by unknown IPs | Containment steps; evidence preservation |
| T+4h | 400 recordings belong to the 3 Spanish clinics | Which laws and authorities apply? Who notifies (controller or processor)? |
| T+24h | A journalist asks for comment | Communication line; who speaks |
| T+48h | Root cause: no review of storage permissions in the change process | Corrective actions; which ISO 27002 controls failed |

## Expected outputs

- [ ] Timeline of decisions with the reasoning
- [ ] Notification decision (ANPD, AEPD via the Spanish clinics, data subjects, clients)
- [ ] Draft messages (filled templates)
- [ ] Lessons learned: controls to add (for example 5.23 cloud services, 8.9 configuration management, 8.32 change management) and new risks in the risk register
