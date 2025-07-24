"""

© abilash-dev | https://github.com/abilash-dev/AdvancedContactFormPy

"""

from flask import Flask, render_template, request, redirect, flash, session, url_for
import smtplib, uuid, random, json
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json
import shutil
import sys

if not os.path.exists('.env'):
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        os.remove('.env.example')
        print("\n---------- [ IMPORTANT ] ----------\n")
        print("Successfully created .env file.")
        print("Please open the new .env file and fill in the required values before running the app again.")
        sys.exit(1)
    else:
        print("\n---------- [ IMPORTANT ] ----------\n")
        print(".env.example file not found.")
        print("Please create it from: https://github.com/abilash-dev/AdvancedContactFormPy#installation")
        print("Or re-clone the repository properly to make sure all files are present.")
        sys.exit(1)
        

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("app_secret_key")

# MAIL CONFIG
SMTP_SERVER = os.getenv("smtp_server")
SMTP_PORT = os.getenv("smtp_port")
NO_REPLY_EMAIL = os.getenv("no_reply_mail")
NO_REPLY_EMAIL_PSW = os.getenv("no_reply_mail_psw")
CONTACT_EMAIL = os.getenv("contact_mail")
CONTACT_EMAIL_PSW = os.getenv("contact_mail_psw")

#DISCORD CONFIG
DISCORD_CLIENT_ID = os.getenv("discord_bot_client_id")
DISCORD_CLIENT_SECRET = os.getenv("discord_bot_client_secret")
DISCORD_REDIRECT_URI = os.getenv("discord_redirect_uri")

#OTHER CONFIG
GOOGLE_CLIENT_ID = os.getenv("google_client_id")
IS_MAIL_ENABLED = os.getenv("manual_mail_enabled")
IS_GOOGLE_ENABLED = os.getenv("google_login_enabled")
IS_DISCORD_ENABLED = os.getenv("discord_login_enabled")

MAIL_ALLOWED_DOMAINS = json.loads(os.getenv("manual_mail_allowed_domains",'[]'))

@app.route("/")
def home():
    return "Your contact form is running in /contact"

@app.route("/contact")
def contact():
    discord_user = session.get("discord_user")
    mail = False
    google = False
    discord = False
    if IS_MAIL_ENABLED == "True":
        mail = True
    if IS_GOOGLE_ENABLED == "True":
        google = True
    if IS_DISCORD_ENABLED == "True":
        discord = True
    if mail == False and google == False and discord == False:
        mail = True
        google = True
        discord = True
    return render_template("contact.html", discord_user=discord_user, google_client_id = GOOGLE_CLIENT_ID, mail_enabled = mail, google_enabled = google, discord_enabled = discord)


@app.route("/login/discord")
def login_discord():
    discord_auth_url = (
        f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code&scope=identify email"
    )
    return redirect(discord_auth_url)

@app.route("/callback")
def callback_discord():
    code = request.args.get("code")
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'scope': 'identify email'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    token_res = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    token_json = token_res.json()
    access_token = token_json.get('access_token')

    user_res = requests.get('https://discord.com/api/users/@me',
                            headers={'Authorization': f'Bearer {access_token}'})
    user_json = user_res.json()

    session['discord_user'] = {
        'name': user_json.get('username'),
        'email': user_json.get('email'),
        'id': user_json.get('id')
    }

    return redirect(url_for("contact"))




@app.route("/submit", methods=["POST"])
def submit_form():
    if request.method == "POST":
        name = request.form.get("name-hidden")
        email = request.form.get("email-hidden")
        message = request.form.get("message")

        if not name:
            name = request.form.get("manual-name")
        if not email:
            email = request.form.get("manual-email")
            if len(MAIL_ALLOWED_DOMAINS)>0 and not any(email.endswith(domain) for domain in MAIL_ALLOWED_DOMAINS):
                flash(f"Email should end with one of the following: {', '.join(MAIL_ALLOWED_DOMAINS)}", "warning")
                return redirect("/contact")
        
        if name and email and message:
            unique_id = random.randint(10000000, 99999999)
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            session['email'] = email  
            session['name'] = name  
            session['message'] = message  
            session['unique_id'] = unique_id  

            try:
                subject_to_user = f"Contact Form ID - {unique_id}"
                headers = f"From: {NO_REPLY_EMAIL}\r\nTo: {email}\r\n"
                headers += "MIME-Version: 1.0\r\n"
                headers += "Content-Type: text/html; charset=utf-8\r\n"
                headers += f"Subject: {subject_to_user}\r\n"
                headers += f"Reply-To: {email}\r\n\r\n"
                
                email_content_to_user = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; color: #333;">
                        <h3>Hello {name},</h3>
                        <h2 style="color: #f90000;">Use the following one-time password (OTP) to complete the verification.</h2>
                        <p><strong>Your Contact Form ID:</strong> {unique_id}</p>
                        <p><strong>OTP for verification:</strong> {otp}</p>  
                        <hr style="border: 1px solid #ddd;">
                        <footer style="font-size: 12px; color: #888;">
                            <p>This is an automated reply from our website.</p>
                            <p>&copy; abilash-dev | https://github.com/abilash-dev/AdvancedContactFormPy</p>
                        </footer>
                    </body>
                </html>
                """
                
                email_content = headers + email_content_to_user

                with smtplib.SMTP(SMTP_SERVER, 587) as server:
                    server.ehlo()
                    server.starttls()  
                    server.ehlo()  
                    server.login(NO_REPLY_EMAIL, NO_REPLY_EMAIL_PSW)
                    
                    server.sendmail(NO_REPLY_EMAIL, email, email_content)


                flash(f"Please check {email} for the OTP.", "success")
                return render_template("contact.html", otp_sent=True)
            except smtplib.SMTPException as e:
                flash("Failed to send otp due to an mail server error.", "danger")
                print(f"SMTP error: {e}")
            except Exception as e:
                flash("Failed to send otp, Please try again later.", "danger")
                print(f"Error: {e}")

            return redirect("/contact")
        else:
            flash("All fields are required.", "warning")
            return redirect("/contact")


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    user_otp = request.form.get("otp")

    if user_otp and not user_otp.isdigit():
        flash("Invalid OTP. Please try again.", "danger")
        return redirect("/contact")
    
    if user_otp and int(user_otp) == session.get('otp'):
        try:
            name = session.get('name')
            email = session.get('email')
            message = session.get('message')
            unique_id = session.get('unique_id')

            subject_to_user = f"Contact Form ID - {unique_id}"
            headers = f"From: {CONTACT_EMAIL}\r\nTo: {email}\r\n"
            headers += "MIME-Version: 1.0\r\n"
            headers += "Content-Type: text/html; charset=utf-8\r\n"
            headers += f"Subject: {subject_to_user}\r\n"
            headers += f"Reply-To: {email}\r\n\r\n"
            
            email_content_to_user = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h3>Hello {name},</h3>
                    <h2 style="color: #f90000;">Confirmation of Your Contact Form Submission</h2>
                    <p>We have received your message and will get back to you shortly.</p>
                    <p><strong>Your Contact Form ID:</strong> {unique_id}</p>
                    <hr style="border: 1px solid #ddd;">
                    <p><strong>Your Message:</strong></p>
                    <pre style="margin-left: 30px; color: #555; font-size: 14px;">{message}</pre>
                    <hr style="border: 1px solid #ddd;">
                    <footer style="font-size: 12px; color: #888;">
                        <p>This is an automated reply from our website.</p>
                        <p>&copy; abilash-dev | https://github.com/abilash-dev/AdvancedContactFormPy</p>
                    </footer>
                    <p style="font-size: 12px; color: #555;">
                    Kind Regards,<br>
                    <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><br>
                    </p>
                </body>
            </html>
            """
            
            email_content = headers + email_content_to_user

            with smtplib.SMTP(SMTP_SERVER, 587) as server:
                server.ehlo()
                server.starttls()  
                server.ehlo()  
                server.login(CONTACT_EMAIL, CONTACT_EMAIL_PSW)

                recipients = [email, CONTACT_EMAIL]

                server.sendmail(CONTACT_EMAIL, recipients, email_content)
                
                

            flash("OTP verified successfully! Your message has been submitted.", "success")
            session.pop('otp', None)  
            session.pop('email', None)  
            session.pop('name', None)  
            session.pop('message', None)  
            session.pop('unique_id', None)  
            session.pop('discord_user',None)
        except smtplib.SMTPException as e:
            flash("Failed to send confirmation email due to an mail server error.", "danger")
            print(f"SMTP error: {e}")
        except Exception as e:
            flash("Failed to send confirmation email, Try again later.", "danger")
            print(f"Error: {e}")

        return redirect("/contact")
    else:
        flash("Invalid OTP. Please try again.", "danger")
        return redirect("/contact")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    session.clear()
    print("Running")