# Importando la librería que nos permite enviar correos y manejar pdf's
import secrets
import ssl
import string
import smtplib
import pandas as pd
from fpdf import FPDF, HTMLMixin
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
# Importando modulo para manejo de base de datos.
from dbConnect import obtnerProductosMinimosDiponible

# Datos cuenta envío de correos.
gmail_user = 'almsaicmotors@gmail.com'
gmail_password = 'Soporte2021*'

alphabet = string.ascii_letters + string.digits

columns_dict = {'nombre_producto': 'Nombre del producto', 'cantidad_minima':'Cantidad requerida',
                'nombre_proveedor':'Nombre del proveedor', 'cantidad_disponible':'Cantidad disponible'}
columns_list = ['nombre_producto', 'cantidad_minima', 'nombre_proveedor', 'cantidad_disponible']

class PDF(FPDF, HTMLMixin):
    pass
    def logo(self, name, x, y, w, h):
        self.image(name, x, y, w, h)                
        
    def texts(self, root="static/messages/notification.txt", x=10.0, y=80.0, msg=""):
        if msg =="":
            with open(root, 'rb') as msg:
                msg = msg.read().decode('utf-8')
                
        self.set_xy(x, y)
        self.set_text_color(103, 98, 97)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, msg)
    
    def titles(self, title):
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', "B", 16)        
        self.set_text_color(11, 11, 54)
        self.cell(w=210, h=60, align='C', txt=title, border=0)
        
    def msj_settings(self, usuario):
        
        saludo = f"""Estimado(a) {usuario}"""
        despedida = """Saludos, Equipo Saic Motor."""

        return saludo, despedida
    
def emailInventario(cuentaCorreo, nombreUsuario, pdf_ruta="static/messages/reporte.pdf"):
    """ Preparar los datos para el envío del correo de reporte de inventario.

    Este verifica si existe el usuario en la base de datos.

    Parameters

    cuentaCorreo -- Es la cuenta del usuario en la base de datos.
    """

    # Datos de la cuenta
    sent_from = gmail_user

    # Datos del correo
    to = cuentaCorreo

    subject = 'Reporte de inventario - Saic Motor S.A.'
    body = """

Estimado(a) %s

Se procede a enviar adjunto el reporte de inventario faltante.

¿No reconoces esta actividad?

Revisa ahora los dispositivos que has utilizado recientemente. Si no hiciste estos cambios o si crees que alguien ha accedido a tu cuenta sin autorización, deberás cambiar tu contraseña de acceso inmediatamente con tu cuenta en Saic Motor.

No respondas a este correo ya que solamente es informativo, recuerda que es generado de manera automática y no es un canal oficial de comunicación de Saic Motor.


Saludos.

Equipo Saic Motor

Este es un correo de carácter informativo, favor de no responderlo.

    """ % (nombreUsuario)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, to, subject, body)

    mensaje = MIMEMultipart()
    mensaje['From'] = sent_from
    mensaje['To'] = to
    mensaje['Subject'] = subject
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(body, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(pdf_ruta, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % "reporte.pdf")
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    argumentosEmail = (sent_from, to, mensaje)
    
    return argumentosEmail


def enviarCorreo(argumentosEmail):
    """ Envío del correo de reporte de inventario.

    Este método recibe los parámetros (desde, hacia, cuerpo del mensaje y adjunto) del correo para realizar el envío

    Parameters

    argumentosEmail -- Es una tupla que contiene los datos del correo.
    pdf_ruta -- Ruta en la que se aloja el archivo generado con los reportes de inventario.
    """

    try:
 
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(argumentosEmail[0], argumentosEmail[1], argumentosEmail[2].as_string())
        server.close()
    except Exception as e:
        return e

def create_pdf(usuario, cuentacorreo):
    
    table = pd.DataFrame(obtnerProductosMinimosDiponible())
    if len(table) > 0:
        table = table[columns_list]
        table = table.rename(columns=columns_dict)
        data = table.columns.tolist()
        table = table.values.tolist()
        table.insert(0, data)

        pdf=PDF()
        saludo, despedida = pdf.msj_settings(usuario)
        pdf.add_page() 
        pdf.logo('static/images/Logo-login.png', 10, 0, 30, 30)
        pdf.texts(y=50 ,msg=saludo)
        pdf.texts()
        pdf.ln()
        
        line_height = pdf.font_size * 2.5
        col_width = 48  # distribute content evenly
        for row in table:
            for datum in row:
                pdf.cell(col_width, line_height, str(datum), border=1, align="C")
            pdf.ln(line_height)
    
        pdf.texts(y=250, msg=despedida)
        pdf.titles("Reporte de inventario")
        pdf.set_author("saicmot")
        pdf.output("static/messages/reporte.pdf", "F")
        
        enviarCorreo(emailInventario(cuentacorreo,usuario))
    else:
        pass
    