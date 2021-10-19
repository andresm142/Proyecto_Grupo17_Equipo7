# Importando la librería que nos permite enviar correos
import secrets
import smtplib

# Importando modulo para manejo de base de datos.
import dbConnect

# Datos cuenta envío de correos.
gmail_user = 'saicmotorsa@gmail.com'
gmail_password = 'Sm1234567'


def prepararEmail(cuentaCorreo, nombreUsuario, idUsuario):
    """ Preparar los datos para el envío del correo de restablecimiento de claves.

    Este método después de recibir la petición de restablecimiento de contraseña,
    verifica si existe el usuario en la base de datos. Si es un correo válido, envía la nueva clave.

    Parameters

    cuentaCorreo -- Es la cuenta a la que se le enviará el correo de restablecimiento.
    """

    # Datos de la cuenta
    sent_from = gmail_user

    # Datos del correo
    to = [cuentaCorreo]
    password = secrets.token_hex(8)
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

    """ % (nombreUsuario, password)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    #dbConnect.recuperarContrasena(cuentaCorreo, idUsuario, password)
    argumentosEmail = (sent_from, to, email_text)

    print("Ingrese a los datos para preparar correo " + cuentaCorreo + " " + nombreUsuario + " " + idUsuario)
    # Enviar el correo electrónico de restablecimiento de contraseña.
    return argumentosEmail
    

def enviarCorreo(argumentosEmail):
    """ Envío del correo de restablecimiento de claves.

    Este método recibe los parámetros (desde, hacia, cuerpo del mensaje) del correo para realizar el envío

    Parameters

    argumentosEmail -- Es una tupla que contiene los datos del correo.
    """

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('saicmotorsa@gmail.com', 'Sm1234567')
        #server.sendmail('saicmotorsa@gmail.com', argumentosEmail[1], argumentosEmail[2]('utf-8'))
        server.sendmail(argumentosEmail[0], argumentosEmail[1], argumentosEmail[2].encode('utf-8'))
        server.close()
        return 'Email enviado'
    except Exception as e:
        return e
