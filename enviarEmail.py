# Importando la librería que nos permite enviar correos
import smtplib

# Importando modulo para manejo de base de datos.
import dbConnect

# Datos de la cuenta
gmail_user = 'saicmotorsa@gmail.com'
gmail_password = 'Sm1234567'
sent_from = gmail_user


def prepararEmail(cuentaCorreo):
    """ Preparar los datos para el envío del correo de restablecimiento de claves.

    Este método después de recibir la petición de restablecimiento de contraseña,
    verifica si existe el usuario en la base de datos. Si es un correo válido, envía la nueva clave.

    Parameters

    cuentaCorreo -- Es la cuenta a la que se le enviará el correo de restablecimiento.
    """
    

    # Instanciar y crear la conexión hacia la base de datos.
    conn = dbConnect
    conn.crearConexion()

    # Validar si la cuenta de correo existe en la base de datos.
    if conn.validarUsuario(cuentaCorreo):
        # Datos del correo
        to = [cuentaCorreo]
        subject = 'Solicitud cambio de contraseña - Saic Motor S.A.'
        body = """
                
        Estimado(a) %s

        Tu contraseña temporal es: %s

        ¿No reconoces esta actividad?

        Revisa ahora los dispositivos que has utilizado recientemente. Si no hiciste estos cambios o si crees que alguien ha accedido a tu cuenta sin autorización, deberás cambiar tu contraseña de acceso inmediatamente con tu cuenta en Saic Motor.

        No respondas a este correo ya que solamente es informativo, recuerda que es generado de manera automática y no es un canal oficial de comunicación de Saic Motor.


        Saludos.

        Equipo Saic Motor

        Este es un correo de carácter informativo, favor de no responderlo.

        """ % ("Prueba de nombre", "Nueva Contraseña")

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        argumentosEmail = (sent_from, to, email_text)
    

def enviarEmail(argumentosEmail):
    """ Envío del correo de restablecimiento de claves.

    Este método recibe los parámetros (desde, hacia, cuerpo del mensaje) del correo para realizar el envío

    Parameters

    argumentosEmail -- Es una tupla que contiene los datos del correo.
    """

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(argumentosEmail[0], argumentosEmail[1], argumentosEmail[2]('utf-8'))
        server.close()
        return 'Email enviado'
    except Exception as e:
        return e + 'Fallo en conexión'
