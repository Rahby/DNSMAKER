# Telegram VPN Bot 🤖🔐

This is a Telegram bot written in Python that helps users get DNS, WireGuard, and OpenVPN configuration files. It also includes a subscription system for managing user access.

## Features ✨

- ✅ Random IPv4 and IPv6 DNS generation per country
- ✅ Weekly tested DNS (IPv4)
- ✅ Auto-generated WireGuard config
- ✅ Auto-generated OpenVPN config with username/password
- ✅ Inline admin panel for activating user subscriptions
- ✅ User validation system based on subscription expiry
- ✅ Telegram UI with Inline Keyboard Buttons

## Getting Started 🚀

### 1. Clone the repository

```bash`
git clone https://github.com/yourusername/telegram-vpn-bot.git
cd telegram-vpn-bot ```

### 2. Install Requirements
- Python 3.7+
``` pip install pyTelegramBotAPI ```
### 3. Set up the bot
-In the Python file, replace the following variables:
TOKEN = ''           # Your Telegram bot token (inside quotes)
OWNER_ID = 123456789 # Your Telegram numeric user ID (as admin)
SUPPORT_LINK = 'https://t.me/example'  # Telegram link for subscription support
### 4. Run the bot
```python bot.py```
### Bot Commands 📚
Command	Description
```/start```	Starts the bot
```/panel```	Admin panel to activate users

### Admin Panel Functionality 🛠
- Send user ID to activate a 30-day subscription

- Users receive private confirmation

- Subscription expiration is checked automatically

### WireGuard & OpenVPN Config Generation 🔐
- WireGuard configs use randomly generated keys

- OpenVPN config includes embedded random credentials

- Server IP is hardcoded to 10.202.10.10 (change as needed)

### File Structure 📁
- users.json: Stores user subscription expiration timestamps

- wireguard_config.conf: Generated and sent to the user, then deleted

- openvpn_config.ovpn: Same as above for OpenVPN

### To-Do / Improvements 🧠
 - Store generated VPN credentials securely

- Add more country-specific DNS logic

 - Improve error handling and logging

- Add multi-admin support

### Disclaimer ⚠️
This project is for educational purposes only. Using VPN or DNS configurations to bypass restrictions may violate the terms of service of some platforms or legal regulations in your country.

