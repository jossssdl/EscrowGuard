# EscrowGuard - Guion para Video Demo (Español)

**Duración Objetivo:** ~4 minutos (menos de 5 minutos)
**Estilo Visual:** Grabación de pantalla del dashboard combinada con narración (voz en off).

---

### Parte 1: El Gancho y el Problema (0:00 - 0:45)

* **Visual:** Comienza con un plano general del dashboard de **EscrowGuard**, mostrando el indicador pulsante de "AI Shield Active" y las tarjetas de Threat Intelligence (99.9% de precisión PLD) y latencia de API.
* **Audio (Voz en off):** 
  > "Cada día, millones de dólares se aseguran en transacciones de depósito en garantía o escrows. Sin embargo, garantizar el cumplimiento legal y financiero es una pesadilla administrativa. Las plataformas tradicionales sufren para validar identidades, prevenir lavado de dinero y gestionar revisiones manuales, provocando fraudes o costosos retrasos.
  > 
  > Les presentamos **EscrowGuard**—el sindicato multiagente autónomo definitivo, diseñado para asegurar activos digitales y fideicomisos con cumplimiento de nivel bancario, impulsado por LangGraph, PydanticAI y CrewAI."

---

### Parte 2: El Sindicato de Agentes (0:45 - 1:30)

* **Visual:** Desplazamiento hacia la sección de "El Sindicato de Agentes Inteligentes", pasando el cursor por los cuatro agentes clave:
  1. *Extractor AI* (PydanticAI)
  2. *Banco Fideicomiso* (SPEI Mock)
  3. *OSINT Risk* (CrewAI)
  4. *Human HITL* (DPO Portal)
* **Audio (Voz en off):**
  > "EscrowGuard opera mediante un sindicato cooperativo de agentes de inteligencia artificial que gestionan todo el ciclo de vida de la transacción:
  > - Primero, el **Extractor AI** lee los documentos de identidad y valida la información.
  > - Segundo, el **Banco Fideicomiso** interactúa con la capa bancaria para bloquear preventivamente los fondos mediante un SPEI simulado.
  > - Tercero, el agente de **OSINT Risk** analiza bases de datos de sanciones internacionales y nacionales (OFAC, SAT, PEP).
  > - Y cuarto, si se detecta un posible riesgo, el agente de **Human HITL** pausa el flujo de ejecución, notificando al Oficial de Cumplimiento (DPO) para una resolución manual."

---

### Parte 3: Demostración en Vivo - Flujo Limpio (1:30 - 2:30)

* **Visual:** Regresa al panel HUD interactivo. Cambia el modo de conexión a **Live API**. Haz clic en el preset **Limpio**, cargando la plantilla `cliente_limpio.pdf`. Haz clic en **Iniciar Simulación de Depósito**. Observa los logs en la consola en tiempo real y la iluminación secuencial de los nodos: A -> B -> C -> D -> E (todos en verde).
* **Audio (Voz en off):**
  > "Veámoslo en acción. Conectados directamente a nuestra Live API de FastAPI, cargamos el escenario limpio e iniciamos la simulación.
  > 
  > Inmediatamente, el Extractor AI analiza el PDF del pasaporte y extrae la información del comprador. El Banco retiene preventivamente los $1.2M MXN. El agente OSINT de CrewAI realiza la investigación web y confirma que el comprador no tiene antecedentes ni coincide con listas OFAC.
  > 
  > Al estar limpio, el sistema aprueba automáticamente la transacción y libera los fondos al vendedor de forma instantánea. Fluido, seguro y rápido."

---

### Parte 4: Demostración en Vivo - Pasaporte Personalizado y DPO HITL (2:30 - 3:45)

* **Visual:** Arrastra y suelta un pasaporte personalizado (ej. `Pasaporte (1).pdf`), mostrando cómo se sube al servidor. Escribe en el nombre del comprador **YAEL OSCAR AVILA CAMARGO** y nacimiento **15/09/2003**. Haz clic en **Iniciar Simulación de Depósito**. Los nodos avanzan y, al llegar al Nodo D (Compliance), parpadea en color ámbar y emerge el modal de decisión del DPO detallando la coincidencia de apellidos con el PEP `JOSÉ CRISTIAN AVILA DIRCIO`. Haz clic en **Aprobar Falso Positivo (DPO)**. El Nodo E se ilumina en verde.
* **Audio (Voz en off):**
  > "Ahora probemos el verdadero poder de EscrowGuard: el cumplimiento dinámico y el descarte inteligente de homónimos. Arrastramos un pasaporte personalizado. El frontend lo sube a nuestro servidor mediante la API, e ingresamos el nombre: Yael Oscar Avila Camargo.
  > 
  > Al iniciar la simulación, el agente OSINT detecta que el comprador comparte el apellido 'Avila' con un PEP sancionado en listas de riesgo.
  > 
  > En lugar de bloquear la transacción injustificadamente o dejarla pasar sin control, EscrowGuard activa la revisión interactiva. Emerge el modal del DPO mostrando la discrepancia biométrica: el comprador tiene 23 años, pero el PEP sancionado tiene 46.
  > 
  > El oficial revisa, hace clic en 'Aprobar Falso Positivo' y los fondos se liberan de inmediato. El backend registra y audita toda la resolución en tiempo real."

---

### Parte 5: Cierre y Propuesta de Valor (3:45 - 4:00)

* **Visual:** Muestra los logs finales en verde indicando que el fideicomiso se completó de forma ultra-segura. Termina con el dashboard principal en pantalla.
* **Audio (Voz en off):**
  > "Al conectar sistemas multiagente autónomos con criterios y decisiones humanas de cumplimiento, EscrowGuard mitiga fraudes, reduce las cargas operativas de cumplimiento en un 90% y brinda total certeza jurídica y financiera.
  > 
  > EscrowGuard: El futuro de la custodia de activos inteligente y en cumplimiento. Muchas gracias."
