from despedida import despedida
from servicios.detalle import detalle_de_la_deuda
from servicios.recibo import solicitar_recibo
from servicios.formas_y_lugares import formas_y_lugares_de_pago

function_calling = {
    "detalle_de_la_deuda": detalle_de_la_deuda,
    "solicitar_recibo": solicitar_recibo,
    "formas_y_lugares_de_pago": formas_y_lugares_de_pago,
    "despedida": despedida
}