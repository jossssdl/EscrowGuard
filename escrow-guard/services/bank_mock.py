# -*- coding: utf-8 -*-
"""
Servicio de simulación bancaria para la cuenta de depósito en garantía (Escrow).
Desarrollado por el equipo Script Hunters.
"""

from typing import Dict, Any, Optional
import uuid

class BankEscrowService:
    """
    Clase simulada para gestionar transacciones y retención preventivas en cuentas de Escrow.
    """
    def __init__(self):
        # Almacenamiento en memoria de las transacciones de custodia
        # Clave: transaction_id, Valor: dict con detalles
        self._transacciones: Dict[str, Dict[str, Any]] = {}

    def crear_deposito(self, monto: float, comprador: str) -> Dict[str, Any]:
        """
        Registra preventivamente un depósito y bloquea los fondos en estado RETENIDO.
        """
        transaction_id = f"ESC-{str(uuid.uuid4())[:8].upper()}"
        transaccion = {
            "transaction_id": transaction_id,
            "monto": monto,
            "comprador": comprador,
            "estado": "RETENIDO",
            "historial": ["FONDOS_RETENIDOS_PREVENTIVAMENTE"]
        }
        self._transacciones[transaction_id] = transaccion
        return transaccion

    def obtener_deposito(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles de un depósito existente.
        """
        return self._transacciones.get(transaction_id)

    def liberar_fondos(self, transaction_id: str) -> bool:
        """
        Libera los fondos retenidos para que sean transferidos al vendedor.
        """
        if transaction_id in self._transacciones:
            transaccion = self._transacciones[transaction_id]
            if transaccion["estado"] == "RETENIDO":
                transaccion["estado"] = "LIBERADO"
                transaccion["historial"].append("FONDOS_LIBERADOS_AL_VENDEDOR")
                return True
        return False

    def reembolsar_fondos(self, transaction_id: str) -> bool:
        """
        Devuelve los fondos retenidos al comprador en caso de rechazo.
        """
        if transaction_id in self._transacciones:
            transaccion = self._transacciones[transaction_id]
            if transaccion["estado"] == "RETENIDO":
                transaccion["estado"] = "REEMBOLSADO"
                transaccion["historial"].append("FONDOS_REEMBOLSADOS_AL_COMPRADOR")
                return True
        return False
