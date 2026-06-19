# EscrowGuard - Demo Video Script (English)

**Target Duration:** ~4 minutes (under 5 minutes)
**Visual Style:** Screen recording of the dashboard combined with voiceover.

---

### Part 1: The Hook & The Problem (0:00 - 0:45)

* **Visual:** Open with a close-up of the **EscrowGuard** landing page/dashboard, showing the "AI Shield Active" badge pulsing, and highlight cards like Threat Intelligence (99.9% PLD accuracy) and API Latency.
* **Audio (Voiceover):** 
  > "Every single day, millions of dollars are locked in escrow transactions. But securing these funds is a compliance nightmare. Traditional platforms struggle with identity validation, money laundering checks, and manual reviews, leading to severe fraud or costly delays.
  > 
  > Meet **EscrowGuard**—the ultimate autonomous multi-agent syndicate built to secure digital assets and escrows with bank-grade compliance, powered by LangGraph, PydanticAI, and CrewAI."

---

### Part 2: The Agent Syndicate (0:45 - 1:30)

* **Visual:** Scroll down to the "Sindicato de Agentes Inteligentes" section, hovering over the four key agents:
  1. *Extractor AI* (PydanticAI)
  2. *Banco Fideicomiso* (SPEI Mock)
  3. *OSINT Risk* (CrewAI)
  4. *Human HITL* (DPO Portal)
* **Audio (Voiceover):**
  > "EscrowGuard operates using a cooperative syndicate of AI agents that manage the entire transaction lifecycle:
  > - First, the **Extractor AI** parses document text and validates identity fields.
  > - Second, the **Banco Fideicomiso** interacts with the financial layer to securely lock the funds via simulated SPEI.
  > - Third, the **OSINT Risk** agent scans international sanctions list database (OFAC, SAT, PEP).
  > - And fourth, when a potential risk is flagged, the **Human HITL** agent pauses the loop, notifying the Data Protection Officer for manual resolution."

---

### Part 3: Live Demo - Clean Flow (1:30 - 2:30)

* **Visual:** Scroll back to the interactive HUD. Set connection mode to **Live API**. Click on the **Limpio** preset, loading the `cliente_limpio.pdf` template. Click **Iniciar Simulación de Depósito**. Show the console log updating in real-time, nodes lighting up: A -> B -> C -> D -> E (green).
* **Audio (Voiceover):**
  > "Let's see it in action. We are connected directly to our FastAPI live backend. We load a clean scenario and click 'Start Escrow Simulation'.
  > 
  > Instantly, the Extractor AI reads the PDF passport and extracts the buyer's metadata. Next, the Bank Mock locks the $1.2M MXN preventively. The OSINT CrewAI agent runs a deep search and verifies that the buyer has no negative record or matches in OFAC.
  > 
  > Because it's completely clean, the system automatically approves the transaction and disperses the funds to the seller. Seamless, secure, and fast."

---

### Part 4: Live Demo - Custom Passport & DPO HITL (2:30 - 3:45)

* **Visual:** Drag and drop a custom passport (e.g. `Pasaporte (1).pdf`), showing it uploads to the server. Change the name input to **YAEL OSCAR AVILA CAMARGO** with DOB **15/09/2003**. Click **Iniciar Simulación de Depósito**. The nodes scale up. When Node D is reached, it flashes amber yellow, and the DPO modal pops up with details matching the PEP `JOSÉ CRISTIAN AVILA DIRCIO` but highlighting the DOB discrepancy. Click **Aprobar Falso Positivo (DPO)**. Node E lights up green.
* **Audio (Voiceover):**
  > "Now, let’s test the true power of EscrowGuard: dynamic compliance and homonym checks. We drag and drop a custom passport. The frontend uploads it to our secure API, and we enter the name: Yael Oscar Avila Camargo.
  > 
  > When we start the simulation, the OSINT crew flags a warning. The buyer shares the surname 'Avila' with a sanctioned PEP. 
  > 
  > Instead of blocking the transaction completely or letting it slip, EscrowGuard triggers a Human-in-the-Loop review. The DPO Review Modal pops up, showing the birthdate discrepancy: the buyer is 23 years old, but the sanctioned PEP is 46. 
  > 
  > The officer reviews, clicks 'Approve False Positive', and the funds are instantly released. The backend processes the resolution dynamically, keeping the transaction records fully audited."

---

### Part 5: Outro & Value Proposition (3:45 - 4:00)

* **Visual:** Show the logs finishing successfully. End on the dashboard home screen showing the real-time syndicate status.
* **Audio (Voiceover):**
  > "By bridging cutting-edge multi-agent systems with human compliance guardrails, EscrowGuard prevents fraud, reduces manual workload by 90%, and ensures absolute transaction security.
  > 
  > EscrowGuard: The Future of Autonomous, Compliant Asset Custody. Thank you."
