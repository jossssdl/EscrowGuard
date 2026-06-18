Este submódulo contiene la infraestructura de datos simulada y los entornos de prueba para el proyecto EscrowGuard. Proporciona las respuestas estructuradas y los documentos necesarios para que los agentes de IA y el Frontend interactúen con escenarios financieros y regulatorios reales de México.

Estructura de Archivos
services/sanction_mock.py: Motor de validación de Prevención de Lavado de Dinero (PLD). Simula consultas a las listas negras de la UIF y el SAT 

services/bank_mock.py: Sistema de fideicomiso en memoria. Simula la retención preventiva y liberación de fondos generando claves de rastreo SPEI
