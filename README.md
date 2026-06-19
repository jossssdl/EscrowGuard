# EscrowGuard - Multi-Agent Compliance System for High-Value Escrows

## 🏢 Desarrollado por **Script Hunters** para el Hackathon **Band of Agents** 🚀

EscrowGuard es una plataforma multiagente inteligente y segura diseñada para mitigar y resolver la fricción operativa ocasionada por falsos positivos en verificaciones de cumplimiento regulatorio (OFAC, PEP y prevención de lavado de dinero) en transacciones financieras de custodia (escrow) de alto valor.

Este repositorio está organizado con una arquitectura **Frontend / Backend** desacoplada para admitir despliegues independientes y un escalamiento modular idóneo para producción.

---

## 🛠️ Arquitectura Completa del Sistema

EscrowGuard integra agentes LLM autónomos y cooperativos, una máquina de estados segura (LangGraph), servicios bancarios simulados y un portal interactivo para oficiales de cumplimiento (DPO) en un ecosistema unificado:

```mermaid
graph TD
    subgraph Frontend Client (SPA)
        UI[Landing Page & Dashboard]
        Portal[DPO Compliance Portal]
        Engine[Sandbox Simulation Engine]
        Controller[JS API Orchestrator]
    end
    
    subgraph Backend Core (FastAPI Server)
        API[FastAPI REST Endpoints]
        Listener[EscrowRoomListener]
        Store[(In-Memory Session Store)]
    end
    
    subgraph Sindicato de Agentes & Servicios
        LG[LangGraph Orchestrator]
        Ext[Extractor Agent - PydanticAI]
        OS[OSINT Agent - CrewAI]
        Bank[SPEI / Escrow Bank Mock]
        DB[OFAC / PEP Sanctions DB]
    end
    
    subgraph Plataforma Externa
        Band[Band.ai SDK / Chat Room]
    end

    UI --> Engine
    UI --> Controller
    Portal --> Controller
    Controller <-- HTTP / CORS --> API
    API --> LG
    API <-- Read/Write --> Store
    Listener <-- WebSockets / Events --> Band
    Listener --> LG
    Listener <-- Read/Write --> Store
    
    LG --> Ext
    LG --> OS
    LG --> Bank
    OS --> DB
    
    classDef client fill:#4f46e5,stroke:#c0c1ff,stroke-width:2px,color:#fff;
    classDef server fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef agents fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef ext fill:#78350f,stroke:#fbbf24,stroke-width:2px,color:#fff;
    
    class UI,Portal,Engine,Controller client;
    class API,Listener,Store server;
    class LG,Ext,OS,Bank,DB agents;
    class Band ext;
```

---

## 📁 Estructura del Directorio del Proyecto

El espacio de trabajo está segmentado para separar la interfaz de usuario de los motores de procesamiento lógico en Python:

```text
escrow-guard/
├── docs/                               # Guías técnicas y scripts de demostración
│   ├── dev1_integration.md             # Especificación de Integración y API de FastAPI
│   ├── dev3_extractor_integration.md   # Documentación del Agente Extractor (PydanticAI)
│   ├── dev6_frontend_simulator.md      # Especificación del simulador y diseño visual
│   ├── demo_script_es.md               # Script de demostración paso a paso (Español)
│   └── demo_script_en.md               # Script de demostración paso a paso (Inglés)
├── frontend/                           # Aplicación Web del Cliente (Dev 6)
│   ├── index.html                      # Landing Page principal y Simulador Sandbox
│   ├── index.css                       # Estilos CSS Glassmorphic refinados para el simulador
│   ├── login.html                      # Portal de inicio de sesión para el Oficial DPO
│   ├── dashboard.html                  # Panel interactivo de auditoría DPO para escrows
│   └── portal.css                      # Hojas de estilo dedicadas para las interfaces del portal
├── backend/                            # Servidor Backend de Python
│   ├── main.py                         # API REST de FastAPI y Listener de Band.ai (Dev 1)
│   ├── requirements.txt                # Dependencias del servidor de Python
│   ├── .env.example                    # Plantilla de variables de entorno requeridas
│   ├── agents/                         # Agentes del Sindicato Inteligente
│   │   ├── __init__.py
│   │   ├── extractor.py                # Extractor de PDF biométrico (PydanticAI - Dev 3)
│   │   ├── osint.py                    # Investigador OSINT Web (CrewAI/LiteLLM - Dev 4)
│   │   └── escrow.py                   # Orquestador del Flujo de Estados (LangGraph - Dev 5)
│   ├── services/                       # Servicios e integraciones externas simuladas (Dev 2)
│   │   ├── __init__.py
│   │   ├── bank_mock.py                # Banco Mock de Fideicomisos y SPEI de Banxico
│   │   └── sanction_mock.py            # Base de datos mock de PEPs y sanciones de OFAC
│   └── mock_docs/                      # Documentos de identidad y payloads de prueba (Dev 2)
│       ├── README.md                   # Guía de uso de los documentos de prueba
│       ├── cliente_limpio.pdf          # Pasaporte limpio (Aprueba automáticamente)
│       ├── solicitud_sat.pdf           # Pasaporte sospechoso (Genera Alerta / Falso Positivo)
│       ├── empresa_fantasma.pdf        # Pasaporte bloqueado (Gatilla Rechazo)
│       ├── Pasaporte (1).pdf           # Ejemplo adicional de pasaporte
│       └── sample_payloads.json        # Archivo JSON con payloads de ejemplo para pruebas API
├── LICENSE                             # Licencia de uso del código
└── README.md                           # Documentación principal del repositorio
```

---

## 👤 Roles de Desarrollo y Entregables del Equipo

El proyecto **EscrowGuard** fue desarrollado colaborativamente distribuyendo el alcance técnico entre 6 ingenieros especializados:

### 🛠️ Dev 1: Integración de API, Listener y Pasarela del SDK
* **Responsabilidades:**
  - Desarrollo de la API REST utilizando **FastAPI** con políticas CORS dinámicas.
  - Implementación de los endpoints `POST /api/simulate`, `GET /api/transaction/{id}` y `POST /api/transaction/{id}/resolve`.
  - Integración del listener de salas de chat en tiempo real mediante el **Band Pro SDK**, permitiendo el envío de alertas automáticas y la recepción interactiva de comandos (`APROBAR` / `RECHAZAR`) por parte de oficiales humanos.

### 💰 Dev 2: Servicios de Simulación y Activos de Prueba
* **Responsabilidades:**
  - Programación de la lógica del banco de fideicomisos (`bank_mock.py`), soportando congelamiento de fondos preventivos, reembolsos SPEI y dispersión final al vendedor.
  - Creación del motor de base de datos de sanciones (`sanction_mock.py`) basado en la lista OFAC/PEP.
  - Generación de pasaportes PDF reales con metadatos específicos para simular escenarios Limpios, Falsos Positivos y de Riesgo Crítico.

### 🔍 Dev 3: Agente Extractor de Cumplimiento Biométrico
* **Responsabilidades:**
  - Desarrollo del extractor de texto estructurado utilizando **PydanticAI** y **PyPDF2** para parsear PDFs directamente a esquemas de tipo seguro `EntidadesExtraidas`.
  - Diseño de fallbacks estáticos basados en patrones del nombre del archivo para asegurar ejecuciones resilientes ante ausencias de conexión de LLM.
  - Configuración robusta tolerante a fallas en variables de entorno.

### 🌐 Dev 4: Agente Investigador OSINT Financiero
* **Responsabilidades:**
  - Configuración del agente inteligente en **CrewAI** para realizar minería web de noticias adversas, alertas del SAT Art. 69-B e historiales UIF.
  - Integración con **LiteLLM** y la API de Gemini (2.5 Flash / 3.5 Flash) y Groq como motores cognitivos del agente.
  - Generación automatizada de reportes consolidados de inteligencia financiera formateados en Markdown.

### ⛓️ Dev 5: Orquestador del Grafo de Estados
* **Responsabilidades:**
  - Diseño del grafo secuencial utilizando **LangGraph** para trazar la lógica de negocio del fideicomiso.
  - Gestión del ciclo de vida de la transacción en nodos: *Extracción*, *Retención Bancaria*, *Búsqueda OSINT*, *Pausa de Cumplimiento (DPO)* y *Liquidación/Dispersión*.
  - Configuración del estado suspendido para soportar la intervención de Human-in-the-Loop (HITL) sin bloquear recursos.

### 🎨 Dev 6: Simulador Web UX y Portales de Cumplimiento
* **Responsabilidades:**
  - Diseño de una SPA moderna y glassmorphic bajo los lineamientos visuales del Stitch Design System.
  - Creación de un simulador dual (Modo **Sandbox** local en cliente / Modo **Live** conectado a FastAPI).
  - Implementación de drag-and-drop de archivos PDF, visualizadores dinámicos del estado de los nodos mediante SVG e interfaces de portal dedicadas para el DPO (`login.html` y `dashboard.html`).

---

## 🚀 Instrucciones de Configuración y Ejecución Local

### 1. Inicialización del Backend
1. Navega a la carpeta del backend:
   ```bash
   cd backend
   ```
2. Crea tu archivo de configuración `.env` tomando como base el archivo `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Asegúrate de configurar las variables principales:
   * `GEMINI_API_KEY` (Utilizada por LiteLLM / Gemini 2.5 Flash)
   * `GROK_API_KEY` (Opcional, mapeada para inicializar Groq en CrewAI)
   * `BAND_API_KEY` y `BAND_ROOM_ID` (Opcional, requeridas si vas a conectar el bot real a salas de Band.ai)

3. Activa tu entorno virtual e instala las dependencias:
   ```bash
   source ../.venv/bin/activate
   pip install -r requirements.txt
   ```
4. Inicia el servidor web FastAPI:
   ```bash
   python main.py
   ```
   El backend se ejecutará en [http://localhost:8000](http://localhost:8000).

### 2. Inicialización del Frontend
1. Entra a la carpeta del frontend:
   ```bash
   cd ../frontend
   ```
2. Levanta un servidor de archivos estáticos para evitar bloqueos por políticas CORS:
   ```bash
   python3 -m http.server 8080
   ```
3. Abre [http://localhost:8080](http://localhost:8080) en tu navegador.
4. Explora las vistas del Portal DPO abriendo `login.html` y `dashboard.html` directamente en tu servidor local.
