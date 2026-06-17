# Documentos Mock de Prueba (EscrowGuard)

## 🏢 Script Hunters

Este directorio está destinado a almacenar los archivos de pasaportes y documentos de identidad simulados en formato PDF para realizar las pruebas locales de extracción e integración.

### 📋 Archivos Esperados:
1. `pasaporte_valido.pdf`: Representará a un comprador con datos limpios que no dispare alertas en listas de sanciones.
2. `pasaporte_sospechoso.pdf`: Representará a un comprador que comparte nombre con un registro sancionado en la OFAC, disparando el flujo de falso positivo e intervención humana (DPO).

*Nota: Estos archivos serán provistos e implementados por el **Dev 2 (Mock Services)** en la fase correspondiente.*
