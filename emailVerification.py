import os
import random
import string
import ssl
import urllib3
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# load environment variables
load_dotenv()

# disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# completely disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

def generate_verification_code(length=6):
    """
    generate a random verification code of specified length
    
    parameters:
        length: the length of the verification code, default is 6
    returns:
        a random verification code string
    """
    # use digits to generate the verification code
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(to_email, subject="Email Verification", code=None):
    """
    send a verification email
    
    parameters:
        to_email: the email address of the recipient
        subject: the subject of the email, default is "Email Verification"
        code: the verification code, if None, a random code will be generated
    returns:
        a tuple of (success status, message, verification code)
        success status: True means the email is sent successfully, False means the email is not sent
        message: the detailed information of the success or the failure
        verification code: the verification code sent to the recipient
    """
    # get the SendGrid API key
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        return False, "SendGrid API key is not set", None
    
    # if the verification code is not provided, generate a random one
    if not code:
        code = generate_verification_code()
    
    # build the email content
    from_email = "yinghu9991@gmail.com"  # replace with your sender email
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
        <h2 style="color: #333;">Email Verification Code</h2>
        <p>Hello,</p>
        <p>Your verification code is:</p>
        <div style="background-color: #f5f5f5; padding: 10px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
            {code}
        </div>
        <p>The verification code is valid for 10 minutes. Please do not share the verification code with others.</p>
        <p>If you did not request this verification code, please ignore this email.</p>
        <p>Thank you,</p>
        <p>BudgetManager Team</p>
        <p style="color: #999; font-size: 12px; margin-top: 30px;">This email is automatically sent by the system. Please do not reply.</p>
    </div>
    """
    
    # create the email object
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        # create the SendGrid client
        sg = SendGridAPIClient(api_key)
        
        # disable SSL verification
        sg.client.session.verify = False
            
        # send the email
        response = sg.send(message)
        
        # check the sending status
        if response.status_code >= 200 and response.status_code < 300:
            return True, f"The verification code has been sent to {to_email}", code
        else:
            return False, f"Failed to send the email: status code {response.status_code}", None
            
    except Exception as e:
        return False, f"Failed to send the email: {str(e)}", None