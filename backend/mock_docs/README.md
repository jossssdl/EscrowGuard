# Documentos de Prueba (EscrowGuard)

## 🏢 Script Hunters

Esta carpeta almacena los documentos de identidad simulados (PDF) que alimentan tanto
la extracción local (modo Live con LLM) como los escenarios de la demo. El contenido real
de cada PDF está **alineado** con los presets del simulador frontend, con el fallback
estático del agente extractor y con la base mock de sanciones (`services/sanction_mock.py`).

### 📋 Archivos y escenarios canónicos

| Archivo | Escenario | Persona (contenido real del PDF) | Fecha nac. | Resultado del flujo |
| :--- | :--- | :--- | :--- | :--- |
| `cliente_limpio.pdf` | **Limpio** | Credencial INE de **JIMÉNEZ FILOMENO EDMUNDO** | 1990-08-14 | `APPROVED` (no figura en listas) |
| `solicitud_sat.pdf` | **Falso Positivo (HITL)** | Pasaporte de **CARLOS AVILA DIRCIO** | 1992-07-14 | `SANCTION_FLAGGED` → revisión DPO |
| `empresa_fantasma.pdf` | **Sanción Exacta** | Pasaporte de **JOSE CRISTIAN AVILA DIRCIO** | 1985-08-20 | `REJECTED` (coincidencia exacta) |

### 🔎 Lógica del falso positivo

- El PEP sancionado de referencia es **JOSÉ CRISTIAN AVILA DIRCIO** (UIF, nacido `1985-08-20`).
- `CARLOS AVILA DIRCIO` **comparte apellidos** con el PEP pero tiene **otra fecha de nacimiento**
  (`1992-07-14`), por lo que el grafo de LangGraph lo marca como posible homonimia y solicita
  intervención humana (Human-in-the-Loop) en lugar de rechazarlo automáticamente.
- `JOSE CRISTIAN AVILA DIRCIO` coincide en nombre **y** fecha de nacimiento con la lista, por lo
  que el sistema lo rechaza de forma directa.

> Los PDFs se generan como documentos de texto simples (extraíbles por PyPDF2). Si necesitas
> regenerarlos, recrea documentos con los mismos nombres y datos de la tabla anterior.
