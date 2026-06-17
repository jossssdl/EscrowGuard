# EscrowGuard - Sistema Multiagente de Cumplimiento Normativo en Garantías

## 🏢 Script Hunters - Proyecto de Hackathon (Band of Agents)

EscrowGuard es una plataforma multiagente diseñada para mitigar y resolver la fricción operativa ocasionada por los falsos positivos en verificaciones de cumplimiento normativo (OFAC, PEP y prevención de lavado de dinero) en transacciones financieras de custodia y garantía (_Escrow_) de alto valor.

Este repositorio contiene la estructura base para el desarrollo del proyecto, enfocándose en la integración de la plataforma, la API REST de simulación y el SDK de chat colaborativo correspondientes a la sección de **Dev 1 (Integrador de Plataforma, API y SDK)**.

---

## 📁 Estructura del Directorio del Proyecto

A continuación se detalla la organización de carpetas del proyecto y la función de cada una de ellas dentro del ecosistema de EscrowGuard:

```text
HACKATHON_BAND_OF_AGENTS/
├── docs/                               # Documentación técnica del proyecto
│   └── dev1_integration.md             # Especificación técnica de integración y API (Dev 1)
├── escrow-guard/                       # Directorio raíz del código de la aplicación
│   ├── agents/                         # Sindicato de agentes inteligentes
│   │   ├── __init__.py
│   │   ├── extractor.py                # Agente Extractor (PydanticAI - Dev 3)
│   │   ├── osint.py                    # Agente OSINT / Investigador (CrewAI - Dev 4)
│   │   └── escrow.py                   # Grafo de Estados (LangGraph - Dev 5)
│   ├── services/                       # Servicios de simulación y mocks (Dev 2)
│   │   ├── __init__.py
│   │   ├── bank_mock.py                # Mock del servicio de depósito bancario
│   │   └── sanction_mock.py            # Mock de base de datos de sanciones OFAC
│   ├── mock_docs/                      # Documentos de prueba en formato PDF (Dev 2)
│   ├── .env.example                    # Plantilla de configuración de variables de entorno
│   ├── requirements.txt                # Dependencias generales de la solución
│   └── main.py                         # Punto de entrada de la aplicación y escucha de eventos (Dev 1)
├── distribucion_equipo.md              # Distribución general de roles
└── plan_de_implementacion.md           # Plan de implementación detallado del hackathon
```

---

## 👤 Responsabilidades y Entregables del Dev 1

El **Dev 1** actúa como el núcleo de integración del proyecto, conectando los módulos de agentes e infraestructura simulada con las plataformas externas (Band Pro SDK) y la interfaz de usuario (FastAPI).

### 🛠️ Tareas Principales

1. **Configuración del Entorno y Base:** Establecer el archivo de dependencias `requirements.txt` y definir el archivo de configuración `.env.example`.
2. **Desarrollo de `main.py`:**
   - Configurar la API local con FastAPI, habilitando el intercambio de recursos de origen cruzado (CORS) para interactuar con la Landing Page y el simulador interactivo.
   - Diseñar el endpoint POST `/api/simulate` para invocar el grafo de LangGraph de manera síncrona o asíncrona.
   - Implementar el listener de chat mediante la clase `EscrowRoomListener(RoomListener)` de `band-sdk`.
   - Coordinar el flujo interactivo de aprobación humana (_Human-in-the-Loop_) reaccionando a las palabras clave del Oficial de Cumplimiento (DPO) en la sala de Band Pro.

---
