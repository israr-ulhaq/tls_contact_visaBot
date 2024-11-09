# tls_contact_visaBot

**tls_contact_visaBot** is a Telegram bot designed to assist users with the TLS contact visa application process. The bot automates interactions with the TLS contact website using a web driver, providing a seamless user experience.

## Features
1. Automates TLS contact visa application interactions.
2. Provides real-time updates on the application status.
3. User-friendly interface via Telegram.

## Prerequisites
Before setting up and running the bot, ensure you have the following:

1. **Telegram Bot Token**: You need to create a bot in Telegram and obtain a bot token. Follow the [Telegram Bot API instructions](https://core.telegram.org/bots) to create a bot and obtain the token.
2. **Chrome WebDriver**: Install the Chrome WebDriver that matches your installed version of Chrome. You can download it from the [official Chrome WebDriver site](https://sites.google.com/chromium.org/driver/).

## Setup
Follow these steps to set up the bot:

### 1. Clone the Repository
   - Clone this repository to your local machine using the following command:

     ```bash
     git clone https://github.com/yourusername/tls_contact_visaBot.git
     ```

### 2. Install Dependencies
   - Navigate to the project directory and install the required Python packages using pip:

     ```bash
     cd tls_contact_visaBot
     pip install -r requirements.txt
     ```

### 3. Configure Bot Token
   - Add your Telegram bot token to the code. You can do this by modifying the `config.py` file (or the relevant section of the main script) with your bot token:

     ```python
     TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
     ```

### 4. Set Up WebDriver
   - Ensure the Chrome WebDriver executable is located in a directory that is part of your system's PATH. Alternatively, specify the path to the WebDriver in the code:

     ```python
     CHROME_DRIVER_PATH = '/path/to/chromedriver'
     ```

### 5. Verify Environment
   - Confirm that the required environment variables are set up correctly, and that both Python and pip are accessible from your terminal. You can check this with:

     ```bash
     python --version
     pip --version
     ```

### 6. Run Initial Tests
   - Run a quick test to ensure all dependencies and configurations are correct. Start the bot with:

     ```bash
     python main.py
     ```

   - Verify that the bot connects to Telegram and responds to basic commands. This will ensure that setup was successful.

## Usage
To start the bot, run the main script:

```bash
python main.py

## Disclaimer
This bot is intended for personal, educational, and non-commercial use only. It is designed to assist users with automating interactions with the TLS contact visa application process for convenience. 

Please note:
- This bot is not affiliated with or endorsed by TLScontact or any visa application service.
- Use of the bot may be subject to the terms and conditions of the TLScontact website or applicable visa authorities.
- Users are responsible for ensuring compliance with all applicable laws and website terms.
