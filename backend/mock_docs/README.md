# Mock Test Documents (EscrowGuard)

## 🏢 Script Hunters

This directory is designated to store simulated passport and identity documents in PDF format to conduct local extraction and integration tests.

### 📋 Expected Files:
1. `pasaporte_valido.pdf`: Represents a buyer with clean records that will not trigger any sanction list alerts.
2. `pasaporte_sospechoso.pdf`: Represents a buyer sharing a name with an OFAC-sanctioned individual, triggering the false-positive workflow and requiring human intervention (DPO).

*Note: These files will be provided and implemented by **Dev 2 (Mock Services)** during the corresponding phase.*
