import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")

# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY

APP_NAME = "RCLH S16 Rugby App"
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://s16-nine.vercel.app")
# By default, Brevo sends from the account owner's email if not specified
SENDER_EMAIL = os.getenv("FROM_EMAIL", "adriserrajime@gmail.com") 

def send_password_reset_email(to_email: str, token: str, user_name: str = "amigo"):
    """
    Sends a premium HTML password reset email using Brevo (Sendinblue) API.
    """
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"
    
    subject = f"Restablece tu contraseña de {APP_NAME} 🔑"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Inter', -apple-system, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #eee; border-radius: 12px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ width: 80px; height: auto; }}
            .content {{ padding: 0 20px; }}
            .greeting {{ font-size: 18px; font-weight: 600; margin-bottom: 15px; }}
            .message {{ margin-bottom: 25px; color: #555; }}
            .button-wrapper {{ text-align: center; margin: 35px 0; }}
            .button {{ 
                background-color: #003366; 
                color: white !important; 
                padding: 14px 28px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: bold; 
                display: inline-block;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .security-note {{ font-size: 12px; color: #888; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }}
            .footer {{ text-align: center; font-size: 12px; color: #aaa; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://tyqyixwqoxrrfvoeotax.supabase.co/storage/v1/object/public/imagenes/Escudo_Hospi_3D-removebg-preview.png" alt="RCLH Logo" class="logo">
            </div>
            <div class="content">
                <div class="greeting">Hola, {user_name}</div>
                <div class="message">
                    Hemos recibido una solicitud para restablecer la contraseña de tu cuenta asociada a este correo electrónico. ¡No te preocupes! Estas cosas pasan hasta en las mejores melés.
                </div>
                <div class="button-wrapper">
                    <a href="{reset_link}" class="button">Restablecer Contraseña</a>
                </div>
                <div class="message">
                    <b>¿No has sido tú?</b><br>
                    Si no solicitaste este cambio, puedes ignorar este mensaje con total seguridad. Tu contraseña actual seguirá funcionando y no se realizará ningún cambio.
                </div>
                <div class="security-note">
                    <b>Nota de seguridad:</b><br>
                    Este enlace caducará en las próximas 24 horas. Por tu seguridad, nunca compartas este correo con nadie.
                </div>
            </div>
            <div class="footer">
                <p>¡Nos vemos pronto en la app!</p>
                <p>El equipo de <b>{APP_NAME}</b></p>
                <p style="font-size: 10px; opacity: 0.8;">RC L'Hospitalet • Carrer de la Residència, s/n • L'Hospitalet de Llobregat, Barcelona</p>
            </div>
        </div>
    </body>
    </html>
    """

    if not BREVO_API_KEY:
        print(f"WARNING: BREVO_API_KEY missing. Cannot send email to {to_email}.")
        print(f"DEBUG: Password Reset Link: {reset_link}")
        return False

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": user_name}],
        reply_to={"email": SENDER_EMAIL, "name": APP_NAME},
        headers={"Some-Custom-Name": "unique-id-1234"},
        html_content=html_content,
        sender={"email": SENDER_EMAIL, "name": APP_NAME},
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"INFO: Email sent via Brevo. Response: {api_response}")
        return True
    except ApiException as e:
        print(f"ERROR: Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
        # Fallback to logging the link
        print(f"DEBUG: Password Reset Link for {to_email}: {reset_link}")
        return False
    except Exception as e:
        print(f"ERROR: General error sending email via Brevo to {to_email}: {e}")
        print(f"DEBUG: Password Reset Link for {to_email}: {reset_link}")
        return False
