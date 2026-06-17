# EscrowGuard - Multi-Agent Compliance System for High-Value Escrows

## 🏢 Script Hunters - Hackathon Project (Band of Agents)

EscrowGuard is a multi-agent platform designed to mitigate and resolve the operational friction caused by false positives in regulatory compliance checks (OFAC, PEP, and Anti-Money Laundering) in high-value escrow financial transactions.

This repository contains the base structure for the development of the project, focusing on platform integration, the simulation REST API, and the collaborative chat SDK corresponding to the **Dev 1 (Platform, API, and SDK Integrator)** section.

---

## 📁 Project Directory Structure

The organization of the project folders and the function of each within the EscrowGuard ecosystem are detailed below:

```text
HACKATHON_BAND_OF_AGENTS/
├── docs/                               # Technical documentation of the project
│   └── dev1_integration.md             # Integration technical specification and API (Dev 1)
├── escrow-guard/                       # Root directory of the application code
│   ├── agents/                         # Syndicate of intelligent agents
│   │   ├── __init__.py
│   │   ├── extractor.py                # Extractor Agent (PydanticAI - Dev 3)
│   │   ├── osint.py                    # OSINT / Investigator Agent (CrewAI - Dev 4)
│   │   └── escrow.py                   # State Graph (LangGraph - Dev 5)
│   ├── services/                       # Simulation services and mocks (Dev 2)
│   │   ├── __init__.py
│   │   ├── bank_mock.py                # Escrow bank mock service
│   │   └── sanction_mock.py            # OFAC sanctions database mock
│   ├── mock_docs/                      # Sample PDF test documents (Dev 2)
│   ├── .env.example                    # Template for environment variables
│   ├── requirements.txt                # Core dependencies of the solution
│   └── main.py                         # Application entry point and event listener (Dev 1)
├── LICENSE                             # MIT Distribution License
└── README.md                           # Main repository documentation
```

---

## 👤 Responsibilities and Deliverables of Dev 1

**Dev 1** acts as the integration core of the project, connecting the agent modules and simulated infrastructure with external platforms (Band Pro SDK) and the user interface (FastAPI).

### 🛠️ Key Tasks
1. **Environment and Base Setup:** Establish the `requirements.txt` dependency file and define the `.env.example` configuration template.
2. **Development of `main.py`:**
   - Configure the local API using FastAPI, enabling Cross-Origin Resource Sharing (CORS) to interact with the Landing Page and the interactive simulator.
   - Design the `POST /api/simulate` endpoint to invoke the LangGraph state machine synchronously or asynchronously.
   - Implement the chat listener using the `EscrowRoomListener(RoomListener)` class from the `band-sdk` package.
   - Coordinate the interactive Human-in-the-Loop (HITL) approval flow by reacting to key input ("APROBAR" / "RECHAZAR") from the Compliance Officer (DPO) in the Band Pro room.
