import time
import logging
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Fideicomiso_Banxico")

cuentas_puente_activas = {}

def retener_fondos_fideicomiso(id_contrato: str, monto_mxn: float) -> dict:
    logger.info(f"Procesando retencion de fondos via SPEI. Contrato: {id_contrato}, Monto: ${monto_mxn} MXN")
    
    time.sleep(1.5)
    
    # Generar una Clave de Rastreo estilo SPEI (15 caracteres despues del prefijo)
    clave_rastreo_spei = f"BNX{str(uuid.uuid4().int)[:15]}"
    fecha_operacion = time.strftime("%Y-%m-%d %H:%M:%S")
    
    cuentas_puente_activas[clave_rastreo_spei] = {
        "id_contrato": id_contrato,
        "monto_mxn": monto_mxn,
        "estado_stps": "FONDOS_ASEGURADOS_EN_FIDEICOMISO",
        "fecha_fondeo": fecha_operacion
    }
    
    logger.info(f"Operacion exitosa. Fondos asegurados. Clave de Rastreo SPEI: {clave_rastreo_spei}")
    return {
        "exito": True,
        "clave_rastreo": clave_rastreo_spei,
        "mensaje": "Los fondos han sido retenidos en la cuenta concentradora del fideicomiso."
    }

def liquidar_pago_vendedor(clave_rastreo: str) -> dict:
    logger.info(f"Recibida instruccion de liquidacion para la operacion: {clave_rastreo}")
    
    time.sleep(1.0)
    
    if clave_rastreo not in cuentas_puente_activas:
        logger.error(f"Fallo en la liquidacion. La clave {clave_rastreo} no existe en el registro.")
        return {
            "exito": False,
            "mensaje": "Clave de rastreo no valida."
        }
        
    estado_actual = cuentas_puente_activas[clave_rastreo]["estado_stps"]
    if estado_actual == "LIQUIDADO_AL_VENDEDOR":
        logger.error(f"Fallo operativo. Los fondos de la operacion {clave_rastreo} ya habian sido dispersados.")
        return {
            "exito": False,
            "mensaje": "La transferencia SPEI ya fue ejecutada previamente."
        }
        
    cuentas_puente_activas[clave_rastreo]["estado_stps"] = "LIQUIDADO_AL_VENDEDOR"
    cuentas_puente_activas[clave_rastreo]["fecha_liquidacion"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info(f"Liquidacion completada. Dispersando fondos a la CLABE del vendedor.")
    return {
        "exito": True,
        "mensaje": "Transferencia SPEI enviada al beneficiario final con exito.",
        "comprobante_electronico_pago": cuentas_puente_activas[clave_rastreo]
    }

class BankEscrowService:
    """
    Clase que encapsula el servicio de fideicomiso y depósito en garantía.
    """
    def __init__(self):
        pass

    def crear_deposito(self, monto: float, nombre_comprador: str) -> dict:
        """
        Crea un registro de retención preventiva en el fideicomiso.
        """
        id_contrato = f"ESC-{str(uuid.uuid4().int)[:8]}"
        res = retener_fondos_fideicomiso(id_contrato, monto)
        return {
            "transaction_id": res["clave_rastreo"],
            "id_contrato": id_contrato,
            "monto": monto,
            "comprador": nombre_comprador,
            "estado": "HELD"
        }

    def liberar_fondos(self, tx_id: str) -> bool:
        """
        Libera los fondos y los liquida al vendedor.
        """
        res = liquidar_pago_vendedor(tx_id)
        return res["exito"]

    def reembolsar_fondos(self, tx_id: str) -> bool:
        """
        Reembolsa los fondos devueltos al comprador.
        """
        if tx_id in cuentas_puente_activas:
            cuentas_puente_activas[tx_id]["estado_stps"] = "REEMBOLSADO_AL_COMPRADOR"
            cuentas_puente_activas[tx_id]["fecha_reembolso"] = time.strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Reembolso completado para la transaccion {tx_id}.")
            return True
        return False

    def obtener_deposito(self, tx_id: str) -> dict:
        """
        Obtiene el estado actual del depósito en garantía.
        """
        if tx_id in cuentas_puente_activas:
            dep = cuentas_puente_activas[tx_id]
            return {
                "transaction_id": tx_id,
                "comprador": dep.get("id_contrato"), # fallback to contract id/name
                "monto": dep.get("monto_mxn"),
                "estado": dep.get("estado_stps")
            }
        return None