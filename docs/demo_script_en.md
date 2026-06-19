# EscrowGuard - Demo Video Script (English)

**Target Duration:** ~4.5 minutes (under 5 minutes)
**Visual Style:** Screen recording of the Landing Page, Login, and Operator Dashboard Portal, paired with dynamic voiceover.

---

### Part 1: Intro & The Problem (0:00 - 0:45)

* **Visual:** Close-up of the **EscrowGuard** landing page, showing the title, dynamic HUD stats ("Active Pools: 12", "Secured Vol: $4.2M"), and the connection toggle set to **Live API**.
* **Audio (Voiceover):** 
  > "Securing escrow deposits and ensuring compliance in high-value transactions is a massive operational headache. Identity fraud, money laundering, and list screening often lead to costly transaction delays or severe regulatory risk.
  > 
  > Introducing **EscrowGuard**—an intelligent, autonomous multi-agent escrow platform that automates compliance, secures deposits, and bridges agent execution with human supervision under the Human-in-the-Loop paradigm."

---

### Part 2: The Landing Page Simulator (0:45 - 1:45)

* **Visual:** Scroll down to the interactive simulator on the landing page. Select the **Limpio** preset (`cliente_limpio.pdf`) and click **Iniciar Simulación de Depósito**. The nodes light up from Extractor AI to Banco Mock, OSINT Risk, and finally automatic Approval.
* **Audio (Voiceover):**
  > "Right on our landing page, clients can test the system in real time. We are using our Live API, running on Gemini 2.5 Flash.
  > 
  > Let's run a clean transaction. The **Extractor AI** parses the passport PDF, the **Banco Escrow** locks the funds preventively, and the **OSINT Risk** agent scans international sanctions databases. 
  > 
  > Since this buyer is clean, the syndicate automatically approves the escrow and releases the funds. Complete, hands-free automation."

---

### Part 3: Secure Login Flow (1:45 - 2:15)

* **Visual:** Click the "Iniciar sesión" (Sign In) link in the header. Show the secure login screen. The email `compliance@escrowguard.mx` and password `EscrowGuard2026` are preloaded. Click **Entrar al sistema**.
* **Audio (Voiceover):**
  > "But what happens behind the scenes when a risk is flagged? Let’s log into the operator dashboard. 
  > 
  > Using preloaded credentials for our Compliance Officer, we enter the secure operational center."

---

### Part 4: The Operator Portal & AI Agents (2:15 - 3:00)

* **Visual:** Show the main dashboard page (`dashboard.html`). Hover over the metrics ($4.2M Protected Funds, 12 Active Operations, 99.8% PLD Accuracy, 2 Human Reviews pending). Go to the **Agentes** tab in the sidebar and show the operational status, latencies, and connection tests of the 4 agents.
* **Audio (Voiceover):**
  > "This is the EscrowGuard Operator Portal. Here, compliance officers have an overview of protected funds, active escrows, and pending human reviews. 
  > 
  > Under the **Agents** tab, we can monitor the health, latencies, and connection statuses of our cooperative AI agents: Extractor AI, Banco Escrow, OSINT Risk, and Compliance HITL. They are all up and operational."

---

### Part 5: HITL Case Resolution (3:00 - 4:15)

* **Visual:** Click on the **Cumplimiento** (Compliance) tab. Show the pending queue (Carlos Ávila PEP match and SAT 69-B match). Select **Carlos Ávila**. Read the details: evaluated name "Carlos Ávila Dircio" vs PEP list "JOSÉ CRISTIAN AVILA DIRCIO" (DOB difference). Type a note in the resolution box: *"Birthdate checked. Validated as a false positive. Releasing funds."* Click **Aprobar falso positivo**. Show the toast notification and watch the pending queue count drop from 2 to 1.
* **Audio (Voiceover):**
  > "Now, let's resolve a pending case in our Compliance Queue. 
  > 
  > We select the case of Carlos Ávila. The system has flagged a potential PEP homonym match. However, looking at the biometric data, the evaluated buyer has a different birthdate than the sanctioned PEP. It is a false positive.
  > 
  > We type our audit resolution note, click 'Approve False Positive', and the system instantly instructs the Banco Escrow to release the funds. The case is resolved, and the transaction is fully audited in the ledger."

---

### Part 6: Multilingual Capabilities & Outro (4:15 - 4:45)

* **Visual:** Click the **EN** button in the language switch to instantly toggle the entire dashboard, sidebar, metrics, and case descriptions to English. End on the main dashboard screen.
* **Audio (Voiceover):**
  > "Finally, the entire portal supports instant localization. With one click, the interface switches between Spanish and English, making it ready for global compliance operations.
  > 
  > EscrowGuard bridges autonomous agents with human compliance rules, securing high-value transactions with zero friction.
  > 
  > EscrowGuard: The Future of Autonomous, Compliant Asset Custody. Thank you."
