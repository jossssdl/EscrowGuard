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