# AdvancedContactFormPy

**Best SMTP-based multi-login contact form for your website – with OTP security and flexible login options!**

---

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Screenshot](#screenshot)
- [Contributing](#contributing)
- [Donation](#donation)
- [Contact](#contact)
- [License](#license)
- [Copyright](#copyright)

---

## Description

**AdvancedContactFormPy** is a powerful and user-friendly SMTP-based contact form solution for websites. It allows site visitors to reach the website owner through multiple login options: **Google**, **Discord**, or **manual email** login.

To reduce spam, **OTP verification** also included in the form. For manual email logins, access **can be restricted** to **specific email domains**.

Each submission generates a **unique form ID**, making it easy to track conversations. The website owner can **reply directly via email** and has the flexibility to **enable or disable** any of the login methods as needed.

---

## Features

- **SMTP-based email sending**  
- **Multiple authentication methods:**  
  - Google Login  
  - Discord Login  
  - Manual email login (with domain restriction option)  
- **OTP verification** for increased security and spam prevention  
- **Unique contact form ID** per submission  
- **HTML-based emails**  
- **User-friendly interface**  
- **Owner can reply directly from mail**  
- **Enable/disable login methods** with environment variables  
- **Flexible domain restriction** for manual email login  

---

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/abilash-dev/AdvancedContactFormPy.git
    cd AdvancedContactFormPy
    ```

2. **Set up the `.env` file**

    Copy the below template and fill it with your credentials:

    ```env
    discord_bot_client_id = "" # DISCORD BOT CLIENT ID/BOT ID/DEVELOPER ID
    discord_bot_client_secret = "" # DISCORD BOT CLIENT SECRET
    discord_redirect_uri = "<domain/localhost>/callback" # ADD THE REDIRECT URI IN DEVELOPER PORTAL
    # https://discord.com/developers/applications/1084622004801503344/oauth2 

    google_client_id = "<client_id>.apps.googleusercontent.com" # COPY PASTE THE CLIENT ID
    # https://console.cloud.google.com/apis/credentials

    smtp_server = "smtp.<mail_server>" # SMTP SERVER 
    smtp_port = 587 # SMTP PORT
    no_reply_mail = "" # MAIL ID TO SEND OTP
    no_reply_mail_psw = "" # MAIL PASSWORD OF no_reply_mail
    contact_mail = "" # MAIL ID TO SEND FINAL CONTACT FORM
    contact_mail_psw = "" # MAIL PASSWORD OF contact_mail
    app_secret_key = "" # APP SECRET FOR YOUR FLASK WEB APP
    manual_mail_allowed_domains = [] # FORMAT - ["@gmail.com","@abilash.link"]
    # Leave empty ([]) to allow all domains

    manual_mail_enabled = "True" # True/False
    google_login_enabled = "True" # True/False
    discord_login_enabled = "True" # True/False
    # At least one login method must be enabled
    ```

    Fill all fields and save the file as `.env` in the project root.

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**

    ```bash
    python app.py
    ```

> ⚠️ Requires **Python 3.11+**

---

## Configuration

All configuration is handled via the `.env` file as described above.

---

## Usage

After running `app.py`, access your contact form at:

```
http://<your-domain-or-localhost>/contact
```

Visitors can contact you via Google, Discord, or manual email login (based on your enabled settings). Each submission is verified via OTP and delivered to your configured contact email.

---

## Screenshot

![Contact Form Example](https://abilash.link/api/uploads/image(17).png)

---

## Contributing

We welcome and encourage contributions!  
If you want to help improve this project:

1. **Fork** the repository.
2. **Clone** your fork.
3. **Create a new branch** for your feature or fix.
4. **Make your changes** and commit.
5. **Push** your branch to your fork.
6. **Open a Pull Request** describing your changes.

_Star ⭐ the project if you like it!_

---

## Donation

If you found this project useful and want to support development, feel free to donate. 

- **LTC (LTC Network): LVViYLmm2yayhYC82HTLHgiLmFM55CkVsj**  
- **BTC/ETH/SOL (BEP20): 0xdd13b3d0e6ea8760afcbd137a5cc02f5d353c584** 
- **Binance ID: 496966292**  

*[Contact Abilash](#contact) for more payment methods.*
---

## Contact

- **Author:** Abilash  
- **Website:** [abilash.link](https://abilash.link)  
- **Discord:** [abilash.](https://abilash.link/discord)
- **Email:** contact@abilash.link  

---

## License

_This project is licensed under the [MIT License](LICENSE)._

---

## Copyright

&copy; 2025 abilash-dev
