from contextlib import asynccontextmanager
import os
import openai
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

openai.api_key=os.getenv('API_KEY')

class UserData(BaseModel):
    message: str

def similitud(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
asignaciones = {}
def message_embedding():

    text = [
        "¿Quiénes son las autoridades de Garantizar?",
        "¿Quiénes son los Directores Corporativos de Garantizar?",
        "¿Quiénes lideran Garantizar y cuáles son sus roles?",
        "¿Cuál es la función de los Directores Corporativos en Garantizar?",
        "No puedo cargar la documentación.",
        "No recibí el contrato digital.",
        "Quiero cancelar mi solicitud",
        "Se bloqueó mi usuario. ¿Cómo continúo?",
        "¿Cuáles son los beneficios específicos de acceder a la Garantía Comercial de Garantizar?",
        "¿Cuáles son los beneficios específicos del Pagaré Bursátil para las PyMEs exportadoras?",
        "¿Qué bonificaciones y convenios ofrece Garantizar en relación con las Garantías Bancarias?",
        "Alta, baja o modificación de domicilio y otros datos",
        "¿Qué certificaciones tiene Garantizar?",
        "¿Cuáles son las calificaciones de Garantizar?",
        "¿Por qué las calificaciones del sistema SGR son importantes para Garantizar?",
        "¿Cómo afectan las condiciones del mercado y las actualizaciones internas a las garantías bancarias de Garantizar?",
        "¿Cómo afectan las condiciones del mercado y las actualizaciones internas a los montos máximos para el descuento de cheques?",
        "Después de seleccionar la línea y banco, ¿qué sigue?",
        "¿Cómo funciona el Descuento de Cheques de Pago Diferido para emprendedores?",
        "¿Cómo puedo acceder al Descuento de Cheques de Pago Diferido y cuáles son las tasas que ofrece?",
        "Explícame cómo funciona la calificación global y la asignación de la línea de descuento en el servicio de Descuento de Cheques de Pago Diferido.",
        "¿Cuáles son las características clave del Descuento de Cheques de Pago Diferido y cómo puedo acceder a este servicio?",
        "Si utilizo el Descuento de Cheques de Pago Diferido, ¿afecta mi capacidad para obtener otras soluciones de Garantizar al mismo tiempo?",
        "¿Cómo se realiza la calificación global para el Descuento de Cheques de Pago Diferido y cómo se establecen los topes de línea?",
        "¿Cómo se determinan los topes de línea en el Descuento de Cheques de Pago Diferido y qué papel juegan los parámetros de venta?",
        "¿Cómo funciona el Descuento de Cheques de Pagos Diferidos?",
        "Cuéntame sobre el Descuento de Cheques de Pagos Diferidos de Garantizar.",
        "¿Cómo se establece el monto de las Obligaciones Negociables PyME?",
        "¿Cómo puedo obtener el certificado PyME?",
        "¿Cómo puedo solicitar mis comprobantes de pago?",
        "¿Qué documentación se requiere para la emisión de Obligaciones Negociables PyME y cuáles son los plazos asociados?",
        "Explícame el servicio E-CHEQ de Garantizar.",
        "¿Cómo se determina el monto del E-cheq y qué papel juega el perfil crediticio del tomador?",
        "¿Cómo funciona el proceso de emisión y recepción del E-cheq en Garantizar?",
        "¿Cuál es la ventaja principal en términos de rapidez al acceder al financiamiento a través del E-cheq?",
        "¿Cómo se comparan las tasas del E-cheq con las ofrecidas por los bancos tradicionales?",
        "Explícame el funcionamiento del E-CHEQ de Garantizar.",
        "Explícame la opción de E-CHEQ para emprendedores y sus características clave.",
        "¿Qué soluciones ofrece Garantizar?",
        "¿Cómo puedo solicitar una garantía?",
        "¿Cómo funciona el descuento de cheques?",
        "¿Cómo puedo simular el descuento de mis cheques con Garantizar?",
        "¿Cuál es la comisión de Garantizar?",
        "Explícame la Garantía Bancaria para PyMEs.",
        "Cuéntame sobre la Garantía Bancaria para emprendedores, sus usos y condiciones.",
        "Explícame cómo funciona la Garantía Bancaria Digital y cuáles son sus características clave.",
        "¿Cómo puedo acceder a la Garantía Bancaria Digital y cuáles son sus beneficios destacados?",
        "¿Cuáles son los detalles y requisitos específicos para obtener la Garantía Bancaria Digital de Garantizar?",
        "¿Cómo funciona el proceso de firma digital en la Garantía Bancaria Digital y de qué manera simplifica los trámites administrativos?",
        "¿Cómo funciona el proceso de renovación de la Garantía Bancaria Digital y cuáles son las ventajas específicas que ofrece?",
        "¿Cuáles son las opciones disponibles para la renovación de la Garantía Bancaria Digital y cuáles son las ventajas específicas asociadas?",
        "¿Cuáles son las condiciones de la Garantía Bancaria de hasta $160.000.000 para capital de trabajo?",
        "Háblame sobre la Garantía Bancaria de hasta $500.000.000 para proyectos de inversión y/o compra de bienes de capital.",
        "Háblame sobre la Garantía Comercial de Garantizar.",
        "Explícame las características de la Garantía Comercial de Garantizar.",
        "Háblame sobre la Garantía Comercial Digital para emprendedores y cómo puede ampliar la cuenta corriente para clientes.",
        "¿Cómo puedo acceder a la Garantía Comercial Digital y cómo se gestiona?",
        "¿Existen acuerdos de financiamiento en el marco del vínculo de Garantizar con el aliado comercial (gran empresa)?",
        "¿Cuál es el paso a paso para obtener la Garantía Comercial Digital y dónde puedo encontrar más información al respecto?",
        "¿Cómo se determinan las tasas en la Garantía Comercial Digital y dónde puedo encontrar las ofertas bancarias vigentes?",
        "¿Qué ofrece la garantía en la Cadena de Valor?",
        "¿Cuál es el destino principal de estos fondos?",
        "¿Hay un límite establecido en el monto?",
        "¿Qué tipo de contragarantía se requiere?",
        "¿En qué consiste la solución Cadena de Valor?",
        "¿Cuáles son los canales de trabajo disponibles?",
        "¿Cómo se determina el monto de asistencia?",
        "¿Es posible combinar distintas soluciones?",
        "¿Qué beneficios ofrece este enfoque de cadena?",
        "¿Cuál es el propósito de las garantías en la Cadena de Valor?",
        "¿Qué sectores de la empresa abarcan estas garantías?",
        "¿Cuáles son las necesidades específicas que buscan cubrir estas garantías?",
        "¿Cómo se gestionan estas garantías?",
        "¿Se requiere contragarantía para acceder a estas garantías?",
        "¿Cuál es el propósito de las garantías en la Cadena de Valor?",
        "¿A quiénes están destinadas estas garantías?",
        "¿Cuáles son las áreas que cubren estas garantías?",
        "¿Cómo funciona el Descuento de Cheques de Pago Diferido para emprendedores?",
        "¿Cómo aprovechar la opción de E-Cheq para emprendedores?",
        "¿Cómo solicitar la Garantía Bancaria para emprendedores?",
        "¿Cómo obtener la Garantía Bancaria Digital para emprendedores?",
        "¿Cómo solicitar la Garantía Comercial Digital para emprendedores?",
        "Háblame sobre las garantías específicas para emprendedores que ofrece Garantizar.",
        "¿Cuáles son las opciones de garantías para PyMEs que ofrece Garantizar?",
        "¿Quiénes somos?",
        "¿Puedes proporcionar más detalles sobre la Sociedad de Garantía Recíproca?",
        "¿Cuáles son los beneficios de invertir en Garantizar?",
        "¿Qué es el fondo de riesgo de Garantizar?",
        "¿Cuáles son los requisitos para ser Socio Protector?",
        "¿Cómo me convierto en Socio Protector?",
        "¿Cuál es la misión de Garantizar?",
        "¿Cuál es la visión de Garantizar?",
        "¿Cómo Garantizar cumple su misión de facilitar el acceso al financiamiento?",
        "¿Cómo Garantizar busca lograr la inclusión financiera para las MiPyMEs?",
        "¿Cuál es el monto máximo que puedo obtener con la garantía digital y a qué tipo de crédito puedo acceder?",
        "¿Qué implica la gestión de Obligaciones Negociables PyME?",
        "Háblame sobre las Obligaciones Negociables PyME de Garantizar.",
        "¿Cómo puedo obtener una garantía digital para acceder a un crédito?",
        "¿Cómo puedo conocer el paso a paso para obtener mi Garantía Digital?",
        "Levantamiento de hipoteca/ liberación de prenda.",
        "Otras consultas.",
        "Cuéntame sobre el Pagaré Bursátil de Garantizar.",
        "Cuéntame acerca del Pagaré Bursátil de Garantizar.",
        "¿Cómo puedo contactar a Garantizar para obtener más información?",
        "¿Cuáles son los próximos eventos o novedades de Garantizar?",
        "¿Para quién están diseñadas las soluciones para Emprendedores?",
        "¿Para quién están diseñadas las soluciones para PyMEs?",
        "¿Qué premios y reconocimientos ha recibido Garantizar?",
        "Háblame más sobre los premios recibidos, especialmente el Premio ALIDE y el Premio Microsoft Al+Tour.",
        "¿Cuánto demora el banco en otorgarme el crédito?",
        "¿Cómo puedo saber en qué estado se encuentra mi solicitud?",
        "¿Qué documentación necesito para solicitar una garantía digital?",
        "¿Qué bancos otorgan los créditos respaldados por una garantía digital? ¿Qué características tienen estos créditos?",
        "¿Qué sucede si obtuve la garantía pero decido no adquirir el crédito?",
        "El banco aún no se comunicó conmigo",
        "Firmé el contrato y no sé cómo seguir",
        "Mi solicitud fue rechazada, ¿por qué?",
        "Si no pago IIBB, ¿qué debo hacer al presentar la documentación?",
        "¿Cómo se lleva a cabo la emisión de una ON y qué implica tener un bono de deuda privada en el mercado de capitales?",
        "¿Cómo me registro y selecciono la línea crediticia junto al banco monetizador?",
        "¿Qué soluciones financieras ofrece Garantizar para PyMEs?",
        "¿Cuáles son las garantías disponibles para PyMEs?",
        "¿Qué opciones ofrece Garantizar para emprendedores?",
        "¿Qué implica la garantía bancaria digital para emprendedores?",
        "¿Cuáles son las opciones de garantías para aliados comerciales?",
        "¿Qué acciones puedo realizar en la Sucursal Virtual de Garantizar?",
        "¿Cómo puedo consultar y descargar mis comprobantes de pago en la Sucursal Virtual?",
        "¿Cómo gestiono mi garantía comercial en la Sucursal Virtual para ampliar el crédito con mi comunidad de clientes y proveedores?",
        "¿Cómo puedo contactar a Garantizar o seguir sus novedades en redes sociales?",
        "¿Cuáles son los pasos para acceder a un crédito bancario a través de la Garantía Digital en la Sucursal Virtual?",
        "¿Qué es la Sucursal virtual? ¿Qué productos puedo gestionar en la sucursal virtual?",
        "¿Cómo me registro en la sucursal virtual? ¿Cómo completo mi solicitud?",
        "¿Cómo realizo la carga de documentación?",
        "¿Cómo valido mi celular? ¿Cómo valido mi DNI en la Sucursal virtual para obtener una garantía digital?",
        "¿Dónde están ubicadas sus sucursales?",
        "¿Cómo puedo ubicar la sucursal más cercana?",
        "¿Ofrecen atención a nivel nacional?",
        "¿Puedo solicitar asesoramiento a domicilio?",
        "¿Cuántas sucursales tiene Garantizar en Salta?",
        "¿Cómo me contacto con la sucursal de Garantizar en Salta?",
        "¿Dónde está la sucursal de Garantizar en Chaco?",
        "¿Cuál es el correo electrónico de la sucursal de Garantizar en Misiones?",
        "¿En qué dirección está ubicada la sucursal de Garantizar en Catamarca?",
        "¿Hay alguna sucursal de Garantizar en Tucumán?",
        "¿Cuántas sucursales tiene Garantizar en Santa Fe?",
        "¿Dónde encuentro la sucursal de Garantizar en Reconquista?",
        "¿En qué dirección está la sucursal de Garantizar en Rosario?",
        "¿Hay una sucursal de Garantizar en Venado Tuerto?",
        "¿Dónde está la sucursal de Garantizar en La Rioja?",
        "¿Cuál es el teléfono de la sucursal de Garantizar en San Juan?",
        "¿Cuántas sucursales tiene Garantizar en Córdoba?",
        "¿En qué dirección está la sucursal de Garantizar en Río Cuarto?",
        "¿Cuál es el teléfono de la sucursal de Garantizar en San Francisco?",
        "¿Dónde está la sucursal de Garantizar en Villa María?",
        "¿Hay una sucursal de Garantizar en San Luis?",
        "¿Dónde está la sucursal de Garantizar en Mendoza?",
        "¿En qué dirección se encuentra la sucursal de Garantizar en Concordia?",
        "¿Dónde está la sucursal de Garantizar en Paraná?",
        "¿Cuántas sucursales tiene Garantizar en CABA?",
        "¿Dónde está la sucursal de Garantizar en Avellaneda?",
        "¿En qué dirección está la sucursal de Garantizar en San Isidro?",
        "¿Cómo me contacto con la sucursal de Garantizar en San Justo?",
        "¿Hay una sucursal de Garantizar en La Plata?",
        "¿Cuál es el teléfono de la sucursal de Garantizar en Bahía Blanca?",
        "¿Dónde está la sucursal de Garantizar en Junín?",
        "¿En qué dirección está la sucursal de Garantizar en Mar del Plata?",
        "¿Cuál es el teléfono de la sucursal de Garantizar en Pilar?",
        "¿Dónde está la sucursal de Garantizar en Tandil?",
        "¿Hay una sucursal de Garantizar en Santa Rosa, La Pampa?",
        "¿Cómo se determina la tasa del Pagaré Bursátil y cuál es el plazo disponible?",
        "¿Cómo se establecen los topes de línea para el descuento de cheques y la calificación global de la PyME?",
        "¿Cuáles son las ventajas de utilizar el E-CHEQ de Garantizar?",
        "¿Dónde está la sucursal de Garantizar en Neuquén?",
        "¿Cuáles son los beneficios que obtengo con mis aportes?",
        "¿Cómo se generan los rendimientos financieros en el fondo?",
        "¿Cuál es el beneficio impositivo específico para los socios protectores?",
        "¿Cómo el fondo respalda a la cadena de valor?",
        "¿Cuáles son los requisitos para ser Socio Protector?",
        "¿Cómo puedo invertir en el Fondo de Garantizar?",
        "¿Con qué bancos trabaja Garantizar para facilitar los servicios financieros?",
        "Quiero iniciar sesión, ¿cómo puedo hacerlo?"
    ]

    first_categorias = [
        "Autoridades de empresa Garantizar",
        "Ayuda y Soporte",
        "Beneficios de la Garantía Comercial",
        "Beneficios para PyMEs Exportadoras",
        "Bonificaciones y Convenios",
        "Cambio de Datos Personales",
        "Certificaciones y Calificaciones",
        "Condiciones y Actualizaciones",
        "Confirmación y Finalización",
        "Descuento de Cheques de Pago Diferido",
        "Descuento de Cheques de Pago Diferido - Acceso y Tasas",
        "Descuento de Cheques de Pago Diferido - Calificación Global y Línea de Descuento",
        "Descuento de Cheques de Pago Diferido - Características y Acceso",
        "Descuento de Cheques de Pago Diferido - Interacción con Otras Soluciones",
        "Descuento de Cheques de Pago Diferido - Proceso de Calificación y Topes de Línea",
        "Descuento de Cheques de Pago Diferido - Topes de Línea y Parámetros de Venta",
        "Descuento de Cheques de Pagos Diferidos",
        "Determinación del Monto",
        "Documentación y Certificados",
        "Documentación y Plazos",
        "E-CHEQ",
        "E-cheq - Monto y Perfil Crediticio",
        "E-cheq - Proceso de Emisión y Recepción",
        "E-cheq - Rapidez en el Acceso al Financiamiento",
        "E-cheq - Tasas Comparativas",
        "E-CHEQ de Garantizar",
        "E-CHEQ para Emprendedores",
        "Financiamiento y Soluciones",
        "Garantía Bancaria",
        "Garantía Bancaria Digital",
        "Garantía Bancaria Digital - Acceso y Beneficios",
        "Garantía Bancaria Digital - Detalles y Requisitos",
        "Garantía Bancaria Digital - Firma Digital y Proceso Simplificado",
        "Garantía Bancaria Digital - Renovación y Ventajas Específicas",
        "Garantía Bancaria para Capital de Trabajo",
        "Garantía Bancaria para Proyectos de Inversión o Compra de Bienes de Capital",
        "Garantía Comercial",
        "Garantía Comercial de Garantizar",
        "Garantía Comercial Digital",
        "Garantía Comercial Digital - Acceso y Gestión",
        "Garantía Comercial Digital - Financiamiento y Vínculo con Aliado Comercial",
        "Garantía Comercial Digital - Proceso de Solicitud",
        "Garantía Comercial Digital - Tasas y Ofertas Bancarias",
        "Garantías para Aliados Comerciales - Cadena de Valor",
        "Garantías para Emprendedores - Descuento de Cheques de Pago Diferido",
        "Garantías para Emprendedores - E-Cheq",
        "Garantías para Emprendedores - Garantía Bancaria",
        "Garantías para Emprendedores - Garantía Bancaria Digital",
        "Garantías para Emprendedores - Garantía Comercial Digital",
        "Garantías para Emprendedores de Garantizar",
        "Garantías para PyMEs",
        "Información Institucional",
        "Inversiones y Socios Protectores",
        "Misión y Visión",
        "Monto y Crédito Asociado",
        "Obligaciones Negociables PyME",
        "Obligaciones Negociables PyME de Garantizar",
        "Obtención de Garantía Digital",
        "Obtención de Garantía Digital - Instrucciones",
        "Otras Consultas",
        "Pagaré Bursátil",
        "Pagaré Bursátil de Garantizar",
        "Preguntas Generales",
        "Premios y Reconocimientos",
        "Proceso de Crédito y Estado de Solicitud",
        "Proceso de Emisión y Deuda Privada",
        "Proceso de Registro y Selección",
        "Soluciones Financieras",
        "Sucursal Virtual - Acceso y Funciones",
        "Sucursal Virtual - Consulta y Descarga de Comprobantes de Pago",
        "Sucursal Virtual - Garantía Comercial y Ampliación de Crédito",
        "Sucursal Virtual - Información de Contacto y Redes Sociales",
        "Sucursal Virtual - Pasos para Acceder al Crédito con Garantía Digital",
        "Sucursal Virtual y Gestión Online",
        "Sucursales y Cobertura Nacional",
        "Tasa y Plazo",
        "Topes y Calificación Global",
        "Ventajas del E-CHEQ",
        "Aportes y Beneficios",
        "Rendimientos Financieros",
        "Beneficios Impositivos",
        "Respaldo para la Cadena de Valor",
        "Requisitos de Inversión",
        "Proceso de Inversión"
    ]

    categorias = [

'Nuestro Consejo de Administración está liderado por el Presidente Gabriel Omar González y el Vicepresidente Guillermo Moretti. Además, contamos con Consejeros Titulares y Suplentes, una Comisión Fiscalizadora y Directores Corporativos en áreas clave como Operaciones, Comercial, Servicios Corporativos, Finanzas, Asuntos Jurídicos, y Estrategia, Tecnología y Nuevos Negocios. 🤝👥',

'Contamos con un equipo de Directores Corporativos liderados por Mariano González Alayes (Operaciones), Pablo Daniel Perazzo (Comercial), Giselle Duarte (Servicios Corporativos), José Belli (Finanzas), Ramiro G. Fernández (Asuntos Jurídicos), y Patricio Connolly (Estrategia, Tecnología y Nuevos Negocios). 🎯👤',

'Nuestro presidente es Gabriel Omar González y el vicepresidente es Guillermo Moretti. Contamos con Consejeros, una Comisión Fiscalizadora y Directores Corporativos en áreas clave. ¿Te gustaría saber más sobre sus roles específicos? 🤝👤',

'Los Directores Corporativos lideran áreas clave como Operaciones, Comercial, Finanzas, Asuntos Jurídicos, entre otros. ¿Hay algún área específica que te interese conocer más a fondo? 🎯👥',

'Consulta los instructivos para conocer el paso a paso de la carga de documentación. Si aún no puedes cargarlos, contactanos acá para que podamos asesorarte. ❓🖱️',

'Verifica tu carpeta de correo no deseado o spam. Si no lo encuentras, contactanos acá para que podamos enviártelo. 📧❓',

'Ingresa a la sucursal virtual, selecciona la solicitud vigente y presiona "Dar de baja". Para consultas, contactanos acá. 📉🔒',

'Espera 30 minutos para desbloquear tu usuario o solicita cambio de contraseña. Asegúrate de que la contraseña cumpla con los requisitos alfanuméricos informados. 🔐🕒',

'Al obtener la Garantía Comercial, tendrás acceso a mayores volúmenes de compra y plazos de pago mejorados. ¿Hay algo en particular que te interese saber sobre los beneficios o el proceso de solicitud? 💼🛍️',

'Este producto es una solución interesante para PyMEs exportadoras, ya que permite financiarse en moneda extranjera. La tasa está sujeta al mercado, y el plazo puede llegar hasta 1 año y medio. ¿Necesitas más información sobre cómo aplicar o los beneficios detallados? 🚢📊',

'Ofrecemos bonificaciones de gastos administrativos para proyectos comprometidos con el cuidado ambiental y la sustentabilidad. Además, garantizamos acceso a tasas, plazos y períodos de gracia competitivos gracias a convenios con los principales bancos públicos y privados del país. ¿Quieres más detalles sobre estas bonificaciones y convenios? 🌿🤝',

'Para cambios de domicilio u otros datos personales, contactanos acá para que podamos realizar la gestión. 🏠🔧',

'Contamos con las mejores calificaciones del sistema SGR, consolidando nuestro liderazgo y compromiso con el crecimiento productivo e industrial. Entre ellas, la Certificación ISO 9001:2015 para los procesos de otorgamiento de garantías. 🏆📊',

'Calificación Nacional de Largo Plazo: AA-(arg) y Calificación Nacional de Corto Plazo: A1 (arg). Además, somos AAA con perspectiva estable por UNTREF. 📈✅',

'Las calificaciones refuerzan nuestro compromiso con el crecimiento industrial. ¿Necesitas más detalles sobre cómo impacta en nuestro respaldo a las MiPyMEs? 📈✨',

'Las condiciones están sujetas al mercado y a actualizaciones internas de los montos máximos a garantizar. ¿Necesitas información adicional sobre cómo estas condiciones pueden afectar tu solicitud? 📊🔄',

'Las condiciones están sujetas al mercado y a actualizaciones internas de los montos máximos a garantizar. ¿Necesitas más detalles sobre cómo estas condiciones pueden influir en tu solicitud de descuento de cheques? 📈🔄',

'Después de la selección, recibirás un correo de confirmación y habrás completado el proceso. ¿Hay algo más que te gustaría saber sobre la confirmación o los siguientes pasos? 📧✅',

'Este servicio se gestiona en sucursal, está destinado a capital de trabajo, y no tiene un tope definido en el monto. Requiere a sola firma como contragarantía. ¿Hay algo más que te gustaría saber sobre esta opción? 📃💵',

'El Descuento de Cheques de Pago Diferido te brinda acceso a crédito a través del mercado de capitales de corto plazo, con tasas competitivas. ¿Quieres conocer más detalles sobre cómo acceder a este servicio o tienes alguna pregunta específica sobre las tasas ofrecidas? 🔄💰',

'En el Descuento de Cheques de Pago Diferido, realizamos una calificación global de tu PyME y te asignamos una línea de descuento válida por un año y medio. ¿Te gustaría más información sobre este proceso o sobre la duración de la línea asignada? 📊🔄',

'El Descuento de Cheques de Pago Diferido te proporciona acceso a crédito a través del mercado de capitales de corto plazo, con tasas competitivas. Es importante destacar que el descuento de cheques no afecta tu capacidad de obtener otras soluciones de Garantizar simultáneamente. Realizamos una calificación global de tu PyME y asignamos una línea de descuento de cheques válida por un año y medio, estableciendo topes de acuerdo a los parámetros de venta. ¿Hay algo más específico que te gustaría conocer sobre este servicio? 📈💳',

'No, el Descuento de Cheques de Pago Diferido no resta cupo para obtener otras soluciones de Garantizar en paralelo. ¿Hay algo más que te gustaría saber sobre la compatibilidad de este servicio con otras soluciones? 🔄💼',

'En el Descuento de Cheques de Pago Diferido, realizamos una calificación global de tu PyME para asignar una línea de descuento válida por un año y medio. Los topes de línea se determinan según los parámetros de venta de tu empresa. ¿Quieres más detalles sobre el proceso de calificación o cómo se establecen los topes de línea? 🔄📊',

'Los topes de línea para el descuento de cheques se establecen de acuerdo a los parámetros de venta de tu empresa. ¿Quisieras más detalles sobre cómo se determinan estos topes o alguna otra información sobre el proceso? 📈🔄',

'Ideal para financiar capital de trabajo, su monto es acorde a la realidad de cada PyME, con contragarantía requerida a sola firma. ¿Necesitas más información sobre la gestión en sucursal u otros detalles? 🔄💵',

'El descuento de cheques de pagos diferidos de Garantizar ofrece montos de hasta $50.000.000 para cheques propios y hasta $120.000.000 para cheques de terceros. Los topes se establecen según los parámetros de venta y no restan cupo para otras soluciones de Garantizar simultáneamente. ¿Necesitas más detalles sobre cómo funciona o los requisitos para acceder? 🔄💵',

'El monto se establece de acuerdo a la capacidad de repago de la empresa. ¿Quieres saber más sobre los factores que influyen en la determinación del monto o si hay requisitos específicos? 📊💼',

'El certificado PyME es obligatorio para gestionar tu garantía. Descarga el instructivo en PDF para obtenerlo paso a paso. 📄📥',

'Visualiza y descarga los comprobantes de pago de tus garantías vigentes. Consulta el instructivo en PDF para obtenerlos fácilmente. 💳💻',

'La documentación mínima se presenta ante la Comisión Nacional de Valores (CNV) y el Mercado Argentino de Valores (MAV). Además, se ofrecen plazos extendidos con la posibilidad de realizar múltiples emisiones. ¿Necesitas más detalles sobre la documentación o los plazos? 📑📅',

'Se gestiona de forma online para financiar capital de trabajo sin tope definido. La contragarantía requerida es a sola firma. ¿Tienes preguntas específicas sobre la gestión online u otros aspectos? 💻💰',

'El monto del E-cheq se establece de acuerdo al perfil crediticio del tomador. ¿Quisieras más información sobre cómo se determina este monto o alguna otra característica del proceso? 📈🔄',

'El E-cheq se emite desde el homebanking y es recibido en la cuenta bancaria del beneficiario. ¿Tienes alguna pregunta específica sobre el proceso de emisión o recepción del E-cheq? 🔄🏦',

'El E-cheq proporciona una mayor rapidez en el acceso al financiamiento en comparación con otras opciones. ¿Hay algo más específico que te gustaría saber sobre la velocidad del proceso? 🚀💳',

'Las tasas promedio del mercado de capitales para el E-cheq suelen ser más favorables que las de los bancos tradicionales. ¿Te gustaría conocer más detalles sobre las ventajas en tasas que ofrece el E-cheq? 📊💸',

'El E-CHEQ se libra desde el homebanking y es recibido en la cuenta bancaria del destinatario. ¿Tienes preguntas específicas sobre el proceso de emisión o recepción? 💻💰',

'El E-CHEQ se gestiona online, tiene como destino el capital de trabajo, y no tiene un tope definido en el monto. Requiere a sola firma como contragarantía. ¿Necesitas más información sobre cómo solicitarlo o sus beneficios? 💻💰',

'En Garantizar facilitamos el acceso al financiamiento para tu micro, pequeña o mediana empresa. Con el respaldo de nuestro fondo de riesgo, otorgamos garantías que mejoran tus condiciones de financiamiento. Estas garantías respaldan diversas operaciones financieras. Descubre más en nuestra sección Soluciones. ¿Querés hacer crecer tu negocio? Garantizar es para vos. 🚀',

'Contamos con más de 30 puntos de atención en todo el país. Encuentra el más cercano en nuestra sección Sucursales. También, puedes gestionar una garantía digital de forma segura y ágil en nuestra Sucursal virtual. ¡Estamos para ayudarte! 📍💻',

'En Simulá tus cheques, calcula el saldo de una operación de descuento. Garantizamos cheques de pago diferido propios y de terceros, físicos o electrónicos (ECHEQ). Realizamos una calificación global de tu PyME y asignamos una línea de descuento válida por un año y medio. 💵🔄',

'¡Es fácil! Con nuestras Garantías Bursátiles, respaldamos tus cheques de pago diferido propios y de terceros, ya sean físicos o electrónicos. Esto te permite descontarlos en el mercado de capitales y obtener financiamiento por hasta 360 días. ¿Querés empezar a operar? 😊',

'Nuestra comisión es un porcentaje sobre el monto de la operación por cada 12 meses de vigencia del contrato. Contáctanos para detalles sobre una solución específica. 📊📞',

'Es una opción para financiar capital de trabajo, inversión o compra de bienes de capital con un monto de hasta $500.000.000. Se requiere contragarantía de bienes muebles, inmuebles o prenda según la garantía y montos solicitados. ¿Necesitas más detalles sobre la gestión en sucursal u otros aspectos? 🏦📊',

'La Garantía Bancaria para emprendedores se gestiona en sucursal, puede destinarse a capital de trabajo, inversión, y compra de bienes de capital. Ofrece un monto de hasta $3.000.000 y no requiere contragarantía. ¿Necesitas más información o el procedimiento para obtenerla? 🏦🔄',

'La Garantía Bancaria Digital se gestiona de forma digital, tiene como destino el capital de trabajo, ofrece un monto de hasta $3.000.000, y no requiere contragarantía. ¿Quieres más detalles o el paso a paso para aplicar? 🖥️💸',

'La Garantía Bancaria Digital brinda acceso las 24/7 desde cualquier lugar del país. Para obtenerla, se requiere documentación como constancia de monotributo o RRI, certificado PyME, DNI digitalizado, y constancia de IIBB si es aplicable. Los beneficios incluyen una tasa fija y cuotas fijas según la oferta bancaria vigente, firma digital del contrato, posibilidad de renovación con el 70% del plazo cumplido, créditos bancarios con tasa preferencial para mujeres emprendedoras, y simplificación de los gastos administrativos. ¿Hay algo más específico que te gustaría saber sobre el acceso o los beneficios? 🌐💡',

'La Garantía Bancaria Digital de Garantizar ofrece acceso las 24/7 desde cualquier lugar del país. La documentación requerida incluye constancia de monotributo o RRI, certificado PyME, DNI digitalizado, y constancia de IIBB si es necesario. La tasa y las cuotas son fijas según la oferta bancaria vigente, con la posibilidad de firma digital del contrato. Además, existe la opción de renovar la garantía con el 70% del plazo cumplido. También se ofrecen créditos bancarios con tasa preferencial para mujeres emprendedoras y se simplifican los gastos administrativos. ¿Te gustaría saber más detalles o tienes alguna pregunta específica sobre este servicio? 🏦💻',

'La Garantía Bancaria Digital ofrece un proceso de firma digital en el contrato, agilizando y simplificando los trámites administrativos. ¿Te gustaría saber más sobre cómo funciona la firma digital o alguna otra característica del proceso? 📝🔒',

'La Garantía Bancaria Digital permite renovación con el 70% del plazo cumplido. Además, proporciona créditos bancarios con tasa preferencial para mujeres emprendedoras y simplificación de los gastos administrativos. ¿Tienes alguna pregunta sobre el proceso de renovación o quieres conocer más detalles sobre estas ventajas específicas? 🔄💳',

'La renovación de la Garantía Bancaria Digital es posible con el 70% del plazo cumplido, ofreciendo flexibilidad en el proceso. Las ventajas específicas incluyen acceso a créditos bancarios con tasas preferenciales para mujeres emprendedoras y la simplificación de los gastos administrativos. ¿Quieres más detalles sobre las opciones de renovación o alguna otra ventaja específica? 🔄💡',

'La garantía es para capital de trabajo con un monto de hasta $160.000.000. El plazo varía según la oferta bancaria, desde 1 hasta 3 años. ¿Hay algo más específico que te gustaría conocer sobre esta garantía? 💼💰',

'Esta garantía es para proyectos de inversión o compra de bienes de capital con un monto de hasta $500.000.000. El plazo también varía según la oferta bancaria, con 7 años y períodos de gracia competitivos. ¿Necesitas más detalles sobre las condiciones o beneficios adicionales? 📈🏭',

'Esta garantía busca ampliar la cuenta corriente con proveedores, con un monto de hasta $60.000.000. La contragarantía incluye bienes muebles, inmuebles o prenda según la garantía y montos solicitados. ¿Quieres conocer más detalles sobre su gestión en sucursal u otros aspectos? 📈🤝',

'La Garantía Comercial proporciona acceso a crédito comercial para aumentar el volumen de compra con plazos de pago mejorados. El plazo está establecido en 1 año. ¿Necesitas más detalles o información sobre cómo solicitarla? 🔄💳',

'Esta garantía se gestiona de manera digital, se destina a la ampliación de la cuenta corriente para tus clientes, ofrece un monto de hasta $3.000.000, y no requiere contragarantía. ¿Te gustaría conocer más detalles o el procedimiento para obtenerla? 🌐📊',

'La Garantía Comercial Digital ofrece gestión 24/7 desde cualquier lugar del país para PyMEs miembros de la cadena de valor del aliado comercial (gran empresa). ¿Necesitas más información sobre el proceso de acceso o gestión? 🔄💻',

'Sí, la Garantía Comercial Digital ofrece acuerdos de financiamiento en el marco del vínculo de Garantizar con el aliado comercial (gran empresa). ¿Te gustaría obtener más información sobre estos acuerdos o algún otro aspecto relacionado? 💼🤝',

'Puedes conocer el paso a paso detallado para obtener tu Garantía Comercial Digital haciendo clic en este enlace: Cómo Completar Solicitud Garantía Comercial Digital. ¿Tienes alguna pregunta específica sobre el proceso? 🔄💻',

'Las tasas en la Garantía Comercial Digital se basan en ofertas bancarias vigentes y están disponibles en la sucursal virtual. ¿Quieres conocer más detalles sobre cómo se determinan estas tasas o dónde encontrar las ofertas? 📊🌐',

'Las garantías en la Cadena de Valor están diseñadas para ampliar el crédito entre la gran empresa y su comunidad de PyMEs clientes y proveedoras. Buscan cubrir necesidades de capital de trabajo e inversiones, sin un tope definido en el monto.',

'El destino principal es el financiamiento de proyectos relacionados con el capital de trabajo e inversiones dentro de la cadena de valor, fortaleciendo las relaciones comerciales.',

'No, estas garantías no tienen un límite definido en el monto, adaptándose a las exigencias y oportunidades del mercado en el que opera la cadena de valor.',

'La contragarantía puede ser a sola firma y/o contar con una contragarantía adicional, dependiendo de los requisitos y acuerdos comerciales establecidos en cada situación.',

'🌐 La solución Cadena de Valor está diseñada para respaldar el financiamiento de todas las PyMEs vinculadas a la empresa, incluyendo tanto a clientes como proveedores.',

'🔄 Hay dos canales de trabajo: 1) Analizando el perfil de riesgo del aliado comercial (gran empresa) para fijar un monto global de asistencia y establecer topes máximos por cada PyME de la cadena. 2) Estableciendo un vínculo comercial directo con las PyMEs de la cadena de valor.',

'💰 El monto se establece analizando el perfil de riesgo del aliado comercial y fijando un monto global de asistencia. Además, se definen topes máximos por cada PyME de la cadena de valor. Esta evaluación busca respaldar financieramente a todas las PyMEs involucradas en la cadena.',

'🤝 Sí, existe la posibilidad de combinar soluciones en el marco de la Cadena de Valor, adaptándose a las necesidades específicas de cada PyME y las condiciones del mercado. Esto ofrece flexibilidad y opciones personalizadas para respaldar el crecimiento y desarrollo de las empresas involucradas.',

'🚀 La cadena de valor brinda un respaldo financiero integral a todas las PyMEs vinculadas, fortaleciendo las relaciones comerciales. Al analizar el riesgo global y establecer vínculos directos, se busca potenciar el crecimiento de todas las empresas involucradas en la cadena comercial.',

'🌐 Las garantías en la Cadena de Valor tienen como objetivo ampliar el crédito entre la gran empresa y su comunidad de PyMEs clientes y proveedoras. Se diseñan para cubrir necesidades de capital de trabajo e inversiones, sin un tope definido en el monto.',

'🔄 Estas garantías abarcan toda la comunidad de PyMEs vinculadas a la empresa, incluyendo tanto a clientes como a proveedores. El enfoque es brindar respaldo financiero de manera integral, fortaleciendo las relaciones comerciales y contribuyendo al crecimiento sostenible de todas las empresas involucradas.',

'💼 Las garantías en la Cadena de Valor buscan cubrir necesidades de capital de trabajo e inversiones. Al no tener un tope definido en el monto, se adaptan a las distintas realidades y requerimientos financieros de las PyMEs, brindando flexibilidad para respaldar proyectos y operaciones comerciales.',

'🔄 La gestión de estas garantías se realiza en sucursal, facilitando el acceso y la tramitación para las PyMEs involucradas en la Cadena de Valor. Esto busca simplificar los procesos y agilizar la obtención de garantías, permitiendo a las empresas concentrarse en sus operaciones y proyectos comerciales.',

'🔐 Sí, se puede requerir a sola firma y/o contragarantía adicional según la evaluación y las condiciones específicas de cada PyME. Esto busca establecer un equilibrio entre la accesibilidad a las garantías y la necesidad de respaldo para garantizar transacciones comerciales seguras y sostenibles en la Cadena de Valor.',

'💼 Las garantías en la Cadena de Valor tienen como objetivo ampliar el crédito entre la gran empresa y su comunidad de PyMEs clientes y proveedoras. Se enfocan en cubrir necesidades de capital de trabajo e inversiones, sin un tope definido en el monto.',

'🌐 Están diseñadas para PyMEs que forman parte de la cadena comercial de la gran empresa aliada. Esto incluye tanto a clientes como a proveedores, abarcando a todas las empresas vinculadas que buscan respaldo financiero para sus necesidades de crédito, capital de trabajo e inversiones.',

'📈 Las garantías en la Cadena de Valor buscan cubrir diversas áreas financieras, desde necesidades de capital de trabajo hasta inversiones estratégicas. No tienen un tope definido en el monto, ofreciendo flexibilidad para adaptarse a las distintas dimensiones y requerimientos de las PyMEs.',

'El Descuento de Cheques de Pago Diferido es una solución para obtener capital de trabajo. La gestión se realiza en sucursal, con un monto sin tope definido y sin restar cupo para otras soluciones de Garantizar. Realizamos una calificación global de tu PyME y asignamos una línea válida por un año y medio. ¿Tienes alguna pregunta específica sobre esta opción? 💳📊',

'El E-Cheq permite liberar cheques de forma digital, ofreciendo tasas promedio más favorables que las de los bancos. La gestión es online, sin tope definido en el monto, y la rapidez en el acceso al financiamiento es mayor. ¿Quieres explorar esta alternativa para tu emprendimiento? 🌐💰',

'La Garantía Bancaria para emprendedores es una opción para financiar capital de trabajo, inversión y compra de bienes de capital. La gestión se realiza en sucursal, sin requerir contragarantía y con un monto de hasta $3.000.000. ¿Quieres conocer más detalles o iniciar el proceso de solicitud? 🛠💡',

'La Garantía Bancaria Digital es una solución para acceder a créditos de hasta $3.000.000 destinados al capital de trabajo. La gestión es totalmente digital, sin requerir contragarantía, y se puede completar a través de nuestra plataforma online. Conoce el paso a paso aquí. ¿Necesitas más información sobre esta garantía? 🚀💻',

'La Garantía Comercial Digital es una opción para ampliar la cuenta corriente con clientes. La gestión es digital, sin requerir contragarantía, y el monto puede llegar hasta $3.000.000. Conoce el paso a paso aquí. ¿Necesitas más detalles o asistencia en el proceso? 🌐💼',

'Garantizar proporciona diversas opciones de garantías para emprendedores, incluyendo la Garantía Bancaria Digital, Garantía Bancaria, Descuento de Cheques de Pago Diferido, E-CHEQ, y Garantía Comercial Digital. ¿Te gustaría más información sobre alguna de estas opciones o cómo solicitarlas? 💼🌐',

'Ofrecemos diversas opciones, como garantías bancarias, garantías comerciales, descuento de cheques de pagos diferidos, E-CHEQ, obligaciones negociables PyME y pagarés bursátiles. ¿En qué área específica necesitas respaldo financiero para tu PyME? 💼💰',

'Somos la Sociedad de Garantía Recíproca líder del país, respaldando el crecimiento de todos los sectores productivos e industriales. Acompañamos a las MiPyMEs para que accedan a un financiamiento competitivo y seguro, potenciando un sistema virtuoso de crecimiento en todos los niveles. 🌐📈',

'Claro, somos líderes en el país, respaldando el crecimiento de sectores productivos. ¿Hay algo específico que te interese saber? 🤔🌐',

'Con el fondo más grande y sólido del sistema SGR, al invertir en Garantizar obtienes rendimientos financieros, beneficios impositivos y contribuyes al fortalecimiento de los sectores productivos del país. Descubre más en nuestra sección Inversiones. 📈💰',

'El fondo de riesgo, formado por aportes de Socios Protectores, respalda las operaciones de las PyMEs. Representa una oportunidad de diversificación de la inversión para personas físicas o jurídicas. 🤝💼',

'Pueden ser Socios Protectores personas físicas o jurídicas que cumplan con el monto mínimo de aporte y plazo de permanencia. Descarga el documento en PDF para obtener más información sobre nuestras oportunidades de inversión. 📄🔐',

'Contacta con nosotros desde nuestra sección Inversiones para conocer cómo convertirte en Socio Protector. 🤔📞',

'Ofrecer los mejores instrumentos para que las MiPyMEs accedan al financiamiento en la banca pública, privada y el mercado de capitales. 💼💰',

'Garantizar la inclusión financiera a las MiPyMEs de todos los sectores productivos del país. 🌍💳',

'Ofrecemos instrumentos para que las MiPyMEs accedan a financiamiento en la banca pública y privada. ¿Necesitas información detallada sobre los instrumentos? 💼💡',

'Nuestra visión es incluir financieramente a MiPyMEs de todos los sectores. ¿Te gustaría conocer iniciativas específicas que respalden esta visión? 🌍💳',

'Con la garantía digital, puedes acceder a un crédito de hasta $3.000.000. ¿Te gustaría conocer más sobre las condiciones del crédito o algún otro detalle? 💰🏦',

'Se realiza en sucursal y está destinada a inversiones, sin tope definido. La contragarantía puede ser a sola firma y/o adicional. ¿Quieres más información sobre este tipo de garantía o su gestión en sucursal? 📈🤝',

'La emisión de una ON genera una reputación positiva en el mercado de capitales para la PyME. ¿Te gustaría conocer más detalles sobre cómo funciona este tipo de financiamiento? 🌐💳',

'Obtener una garantía digital es fácil y rápido. Sigue estos 3 simples pasos: \n\nPaso 0: Regístrate o ingresa si ya eres socio. \nPaso 1: Selecciona la línea crediticia y el banco monetizador. \nPaso 2: Recibe el correo de confirmación ¡y listo! ¿Necesitas más detalles sobre cada paso o tienes alguna pregunta específica? 📑💻',

'¡Claro! Para conocer detalladamente el paso a paso de cómo obtener tu Garantía Digital, puedes acceder al siguiente enlace: Cómo Completar Solicitud Garantía Financiera Digital. ¿Hay algo más en lo que pueda ayudarte? 📑💻',

'Inicia el trámite de liberación solicitando el Certificado de Garantía en el banco que te otorgó el préstamo. Envía una nota formal con la solicitud de liberación de la contragarantía a Garantizar. 🏦📄',

'Si no encontraste la consulta que querés hacer, contactanos acá para que podamos asesorarte. ❓📞',

'Gestionado en sucursal, es para capital de trabajo o inversión sin tope definido. La contragarantía puede ser a sola firma y/o adicional. ¿Necesitas detalles específicos sobre su gestión o características? 📑💼',

'El Pagaré Bursátil ofrece financiamiento en pesos o dólares y es especialmente interesante para PyMEs exportadoras que manejan un flujo de financiamiento en moneda extranjera. ¿Tienes preguntas específicas sobre esta opción de financiamiento? 💸🌐',

'Puedes contactarnos a través de nuestros canales de atención. ¿Necesitas información de contacto específica? 📞📧',

'Mantente actualizado visitando nuestra sección de noticias o eventos en nuestro sitio web. ¿Buscas información sobre algún evento en particular? 📆📰',

'Diseñadas exclusivamente para profesionales y autónomos, especialmente aquellos que son Monotributistas y Responsables Inscriptos (RI). Estas soluciones buscan proporcionar garantías y facilitar el acceso a créditos bancarios, brindando opciones adaptadas a las necesidades financieras y características de este segmento empresarial. 🚀💼',

'Dirigidas a pequeñas y medianas empresas (PyMEs) que buscan financiamiento y garantías para impulsar su crecimiento. Estas soluciones abarcan desde satisfacer necesidades de capital de trabajo hasta facilitar inversiones o adquisiciones de bienes de capital. Diseñadas para respaldar a las PyMEs en diferentes aspectos financieros, proporcionando acceso a créditos, garantías y herramientas que fortalezcan su posición en el mercado y contribuyan a su desarrollo sostenible. 🌱💰',

'Hemos sido galardonados con el Premio ALIDE por "Gestión y modernización tecnológica" y el Premio Microsoft Al+Tour Argentina por la innovación tecnológica en autogestión de garantías bancarias. También, hemos sido reconocidos como uno de los "Mejores lugares para trabajar en Argentina". 🏆🌟',

'Claro, ALIDE reconoció nuestra gestión tecnológica y Microsoft premió nuestra innovación en garantías bancarias. ¿Quieres detalles sobre cómo logramos esto? 🏆🚀',

'Tras obtener nuestra garantía, el banco suele demorar entre 15 y 30 días en otorgar el crédito. Contacta al banco seleccionado para más información. ⌛🏦',

'Ingresa el número de ticket enviado por correo electrónico en el formulario para conocer el estado de tu trámite. 📨🔍',

'Necesitas foto de tu DNI, constancia de inscripción a AFIP e Ingresos Brutos, y certificado PyME vigente. Consulta el instructivo en PDF para obtener tu certificado PyME. 📄📷',

'Con nuestras garantías digitales, accede a créditos del Banco Nación y Banco Ciudad. Consulta características y detalles contactándote con el banco seleccionado. 🏦💳',

'Si decides no adquirir el crédito, cancelaremos la garantía y solicitaremos al banco la carta de baja. 📉🔒',

'Garantizar envió tu contrato al banco. Si han pasado más de 30 días y no te contactaron, comunícate con la sucursal correspondiente. 📞❓',

'Tras firmar el contrato, espera el contacto del banco para la apertura de cuenta. Ingresa el número de ticket en el formulario para más información. 📑🔍',

'Lamentablemente, no podemos avanzar si no cumples con los requisitos. El otorgamiento está sujeto a condiciones de calificación. Consulta las condiciones en la normativa correspondiente. ❌📄',

'Carga una nota escrita a mano y firmada en la que declares no pagar IIBB. 📝✋',

'En el proceso, se emite un bono de deuda privada en el mercado de capitales, y otras empresas pueden adquirirlo. Las tasas y plazos son asignados por el mercado, y el financiamiento es a largo plazo. ¿Tienes preguntas específicas sobre el proceso de emisión o características del bono? 📈💰',

'El registro es el primer paso. Luego, seleccionas la línea crediticia y el banco monetizador. ¿Necesitas instrucciones detalladas sobre el registro o la selección de la línea y banco? 🌐👤',

'Ofrecemos diversas opciones como garantías para proyectos de inversión, capital de trabajo, bienes de capital, pagarés bursátiles, cheques de pago diferido y obligaciones negociables PyME. ¿En qué área necesitas respaldo financiero? 💼💰',

'PyMEs pueden acceder a garantías bancarias, pagarés bursátiles, cheques de pago diferido y obligaciones negociables. ¿Necesitas detalles específicos sobre alguna de estas garantías? 📄✅',

'Para emprendedores, ofrecemos garantías para acceder a créditos bancarios exclusivamente para profesionales y autónomos, incluyendo opciones como garantía bancaria y garantía bancaria digital. ¿En qué podemos apoyar tu emprendimiento? 🚀💡',

'La garantía bancaria digital es una opción para acceder a créditos bancarios de forma ágil y exclusiva para monotributistas y responsables inscriptos. ¿Necesitas más información sobre este servicio? 💻📈',

'Ofrecemos garantías para ampliar el crédito entre grandes empresas y su red de PyMEs clientes y proveedoras. Esto incluye opciones como cadena de valor y garantía comercial digital. ¿Cómo podemos fortalecer tu cadena de valor? 🤝💼',

'En la Sucursal Virtual de Garantizar, puedes acceder a un crédito bancario mediante la Garantía Digital, gestionar tu garantía comercial para ampliar el crédito con tu comunidad de clientes y proveedores, y consultar y descargar tus comprobantes de pago. ¿Necesitas más detalles sobre alguna de estas funciones? 🏦💼',

'En la Sucursal Virtual, puedes consultar y descargar tus comprobantes de pago. ¿Tienes alguna pregunta específica sobre cómo realizar esta acción o necesitas asistencia? 🔄📄',

'En la Sucursal Virtual, puedes gestionar tu garantía comercial para ampliar el crédito con tu comunidad de clientes y proveedores. ¿Te gustaría conocer más detalles sobre este proceso o necesitas ayuda en algún aspecto específico? 🔄📊',

'Puedes encontrar la información de contacto y seguir las novedades de Garantizar en las siguientes redes sociales: LinkedIn, Facebook, Instagram, Twitter, y YouTube. ¿Necesitas información adicional o quieres conectarte con nosotros? 🌐🤝',

'Para acceder a un crédito bancario con Garantía Digital, sigue estos pasos: 1. Accede a la Sucursal Virtual. 2. Selecciona la línea crediticia y el banco monetizador. 3. Recibe el correo de confirmación. ¿Necesitas más información sobre este proceso? 🔄💳',

'La Sucursal virtual es la plataforma de autogestión de Garantizar. Obtén garantías digitales, visualiza comprobantes y simula cheques. Regístrate para conectar con las oportunidades de crecimiento. 💻🔒',

'Regístrate de forma sencilla. Consulta los instructivos en PDF para completar la solicitud de garantía financiera y comercial digital. 📝🔧',

'Sigue consejos útiles para cargar rápidamente la documentación en nuestra Sucursal virtual. Consulta el instructivo en PDF para detalles. 📂🖱️',

'Ingresa tu número de celular y CUIT para validación. Consulta los requisitos para acceder a la garantía digital. 📱🔐',

'🗺️ Contamos con una cobertura nacional, con más de 30 puntos de atención distribuidos estratégicamente en todo el país. ¡Encontrá la sucursal más cercana para recibir asesoramiento personalizado y acceder a nuestras soluciones financieras!',

'📍 Utiliza nuestro mapa interactivo para encontrar fácilmente la sucursal Garantizar más próxima a tu ubicación. Estamos comprometidos con el desarrollo productivo en todo el territorio, por lo que estamos accesibles en múltiples puntos del país.',

'🌐 Sí, estamos en todo el país. Nuestra red de sucursales y asesores comerciales está diseñada para brindar soluciones financieras adaptadas a las necesidades de las PyMEs en cada rincón, apoyando el desarrollo productivo de manera federal.',

'🏡 ¡Sí! Contamos con la flexibilidad de visitarte donde te encuentres. Ya sea en nuestras sucursales o en tu propio establecimiento, adaptamos nuestros servicios para que elijas la opción más conveniente y recibas la solución financiera que necesitas.',

'Garantizar cuenta con una sucursal en Salta, ubicada en Zuviría 120, CP 4400.',

'Puedes comunicarte con la sucursal de Salta llamando al +54 11 4012 1040 o escribiendo a salta@garantizar.com.ar.',

'La sucursal de Garantizar en Chaco se encuentra en Resistencia, en 9 de Julio 264, CP 3500.',

'Para contactar a la sucursal en Misiones, puedes escribir a misiones@garantizar.com.ar o llamar al +54 376 44 8329.',

'La sucursal en Catamarca tiene su ubicación en Rivadavia 567, CP 4700.',

'Sí, Garantizar tiene una sucursal en San Miguel de Tucumán, en 24 de Septiembre 1002, CP 4000.',

'Garantizar cuenta con varias sucursales en Santa Fe: Falucho 2568, CP 3000; Iturraspe 161, CP 3560; Entre Ríos 874, CP 2000; Chacabuco 716, CP 2600.',

'La sucursal en Reconquista está ubicada en Iturraspe 161, CP 3560.',

'Garantizar tiene una sucursal en Rosario, situada en Entre Ríos 874, CP 2000.',

'Sí, Garantizar tiene una sucursal en Venado Tuerto, en Chacabuco 716, CP 2600.',

'La sucursal de Garantizar en La Rioja está en Rivadavia 621, CP 5300.',

'Puedes contactar a la sucursal en San Juan llamando al +54 11 4012 2875.',

'Garantizar cuenta con varias sucursales en Córdoba: Ituzaingó 72, CP 5000; 25 de Mayo 75, CP 5800; Bv. 9 de Julio 1703, CP 2400.',

'La sucursal en Río Cuarto se encuentra en 25 de Mayo 75, CP 5800.',

'Puedes comunicarte con la sucursal de San Francisco llamando al +54 3564 68 4016.',

'La sucursal de Garantizar en Villa María tiene su ubicación en CP 5900.',

'Sí, Garantizar tiene una sucursal en San Luis, en Colón 926, CP 5700.',

'La sucursal en Mendoza está ubicada en San Martin 815, CP 5500.',

'Puedes encontrar la sucursal en Concordia en CP 3200.',

'La sucursal en Paraná está ubicada en Buenos Aires 212, CP 3100.',

'Garantizar cuenta con dos sucursales en CABA: Sarmiento 543, CP 1041; Maipú 73, CP 1084.',

'La sucursal de Garantizar en Avellaneda se encuentra en Av. Mitre 485, CP 1870.',

'Puedes encontrar la sucursal en San Isidro en Av. Santa Fe 1592, CP 1640.',

'Puedes comunicarte con la sucursal de San Justo llamando al +54 11 4012 1060.',

'Sí, Garantizar tiene una sucursal en La Plata, ubicada en Calle 49, nro 550, esq. 6, CP 1900.',

'Para contactar a la sucursal en Bahía Blanca, puedes llamar al +54 291 451 2132.',

'La sucursal en Junín está en Benito de Miguel 31, CP 6000.',

'La sucursal en Mar del Plata está ubicada en San Martín 3060 local 3, CP 7600.',

'Puedes contactar a la sucursal de Pilar llamando al +54 11 4012 2936.',

'La sucursal en Tandil tiene su ubicación en Sarmiento 530, CP 7000.',

'Sí, Garantizar tiene una sucursal en Santa Rosa, en Pellegrini 250, CP 6300.',

'La tasa depende del mercado, y el plazo puede extenderse hasta 1 año y medio. ¿Hay algo más que te gustaría saber sobre la determinación de tasas o los plazos disponibles? 📈⏳',

'Los topes de línea se establecen según los parámetros de venta, y desde Garantizar realizamos una calificación global de tu PyME para asignarte una línea de descuento de cheques. Esta línea, otorgada a través de una única calificación, es válida por un año y medio. ¿Quieres más información sobre estos procesos o condiciones? 📊✅',

'El E-CHEQ ofrece tasas promedio del mercado de capitales, generalmente más favorables que las de los bancos. El monto se establece según el perfil crediticio del tomador, y brinda mayor rapidez en el acceso al financiamiento. ¿Necesitas más detalles sobre estas ventajas o el proceso de aplicación? 🚀📊',

'La sucursal de Garantizar en Neuquén está en Santa Fe 283, CP 8300.',

'Con tus aportes al Fondo de Garantizar, obtienes rendimientos financieros, beneficios impositivos (100% de desgravación del impuesto a las ganancias) y respaldo para tu cadena de valor mediante la oportunidad de financiar a tus proveedores y clientes.',

'Los rendimientos financieros se generan mediante la reinversión de los aportes realizados, convirtiéndolos en rentabilidad periódica para los Socios Protectores.',

'Los socios protectores disfrutan del 100% de desgravación del impuesto a las ganancias, proporcionando beneficios impositivos significativos.',

'El Fondo de Garantizar brinda respaldo a la cadena de valor al ofrecer la oportunidad de financiar a proveedores y clientes, contribuyendo al fortalecimiento de la cadena de pago.',

'Los requisitos incluyen una inversión mínima de $3.000.000 y la condición de no estar vinculado a Garantizar como socio partícipe.',

'Para invertir, se requiere una inversión mínima de $3.000.000. Si estás interesado, puedes derivar a un ejecutivo para obtener asesoramiento y completar el proceso de inversión.',

'Garantizar tiene alianzas estratégicas con varios bancos líderes en Argentina para ofrecer servicios financieros de calidad. Algunos de los bancos con los que colaboramos incluyen Banco Nación, Banco Argentino de Desarrollo, Banco Ciudad, Galicia, Supervielle, Santander, Banco Provincia, Banco Patagonia, BBVA, Macro, HSBC, ICBC, Itaú, Banco Credicoop, Banco Hipotecario, Banco Comafi, entre otros. Esta red de asociaciones nos permite brindar soluciones financieras diversificadas y adaptadas a las necesidades de nuestros clientes.',

'¡Claro! Para iniciar sesión, simplemente dirígete al siguiente  [enlace](https://idp.garantizar.com.ar/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSucuVirtual%26redirect_uri%3Dhttps%253A%252F%252Fdigital.garantizar.com.ar%252Fsignin-oidc%26response_type%3Dcode%2520id_token%26scope%3Dopenid%2520profile%2520nosis_api%2520sga_api%26response_mode%3Dform_post%26nonce%3D638380936114441357.MWRjY2YwNzUtNjEyNy00N2Y4LWExN2EtMWU4ODU0NDRiYjAzYTA4ODhhNjUtOGViMi00MTUxLTlkYjYtNDNkMWI1YTA5ODkw%26state%3DCfDJ8MFnyWylvl1AtmeABfrn5Zg8b1ROlNVolNsvEcYyjc44hyocOZ_EFIQ9monTVbbhha1HbdeXBK3x4p-5SrxL1G8Qf6DaEqgdwm-Dx_ctvCXbT3Ea7em_K6AV9aNcIX1vWrvGWV88pzbZSSjED2D1vfaN4zbVEHTXa-TX7Uivu55EZLbWZdCkHgvpgOImob6OAPI8_JKgOV46yp_sGY0bSs3zt1NEpFGYjQn-fbVue5NRoBbPN21iJui_Bd-iYw2Q12cEmc_mwcXjzcZdd_ZLD0h-d2RhRPIXdvO6dtIQp13c65JfETbkeO_srzFYWJXwn5kVy83LEwKO55Oo23nFnSEtAfJvxKFe-2p51Sfox3kp%26x-client-SKU%3DID_NETSTANDARD1_4%26x-client-ver%3D5.2.0.0). ¡Listo para acceder! 🚀. ¡Listo para acceder! 🚀',

    ]

    embeddings = {}
    for texto in text + categorias:
        embeddings[texto] = openai.embeddings.create(input=[texto], model="text-embedding-ada-002").data[0].embedding

    # Asignar a categoría más similar 
 
    for texto, embedding in embeddings.items():
        if texto in categorias: continue
    
        # Guardar máxima similitud por categoría
        similitudes = {categoria: 0 for categoria in categorias}
    
        for categoria in categorias:
            sim = similitud(embedding, embeddings[categoria])
            
            if sim > similitudes[categoria]:
                similitudes[categoria] = sim

        # Asignar a categoría con máxima similitud    
        categoria_asignada = max(similitudes, key=similitudes.get)
        asignaciones[texto] = categoria_asignada

    return asignaciones

def message_embeddingv2():

    text = [
        "¿Quiénes son las autoridades de Garantizar?",
        "¿Quiénes son los Directores Corporativos de Garantizar?"
    ]

    categorias = [
        "Autoridades",
        "Ayuda y Soporte",
    ]

    embeddings = {}
    for texto in text + categorias:
        embeddings[texto] = openai.embeddings.create(input=[texto], model="text-embedding-ada-002").data[0].embedding

    # Asignar a categoría más similar 
    asignaciones = {}
    for texto, embedding in embeddings.items():
        if texto in categorias: continue
    
        # Guardar máxima similitud por categoría
        similitudes = {categoria: 0 for categoria in categorias}
    
        for categoria in categorias:
            sim = similitud(embedding, embeddings[categoria])
            
            if sim > similitudes[categoria]:
                similitudes[categoria] = sim

        # Asignar a categoría con máxima similitud    
        categoria_asignada = max(similitudes, key=similitudes.get)
        asignaciones[texto] = categoria_asignada

    return asignaciones

app.add_event_handler("startup", message_embedding)

@asynccontextmanager
@app.post('/chat')
async def message_to_embedding(user_data: UserData):
    return asignaciones[user_data.message]