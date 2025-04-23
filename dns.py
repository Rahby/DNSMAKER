import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import socket
import json
import time
import os
import threading

TOKEN = '' #داخل کوتیشن توکن ربات رو میزاید
OWNER_ID = 123456789 #اینجا ایدی عددی خودت یا کسی که میخوای ادمین باشه رو قرار میدی
SUPPORT_LINK = 'https://t.me/ffelz'
DATA_FILE = 'users.json'

bot = telebot.TeleBot(TOKEN)

# بارگذاری کاربران
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(user_data, f)

def is_user_valid(user_id):
    expiry = user_data.get(str(user_id), 0)
    return time.time() < expiry

def generate_random_ipv4():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def generate_random_ipv6():
    return ":".join([f"{random.randint(0, 65535):x}" for _ in range(8)])

def check_ipv4(dns):
    try:
        socket.gethostbyaddr(dns)
        return True
    except:
        return False

def check_ipv6(ipv6):
    try:
        socket.getaddrinfo(ipv6, None, socket.AF_INET6)
        return True
    except:
        return False

# DNS تست ذخیره‌شده
weekly_test_dns = "8.8.8.8"

def update_weekly_dns():
    global weekly_test_dns
    for _ in range(30):
        ip = generate_random_ipv4()
        if check_ipv4(ip):
            weekly_test_dns = ip
            break
    threading.Timer(604800, update_weekly_dns).start()  # هر هفته

update_weekly_dns()

# تولید کلید خصوصی وایرگارد
def generate_wireguard_private_key():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))

# تولید کلید عمومی وایرگارد
def generate_wireguard_public_key(private_key):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))

# تولید کانفیگ وایرگارد
def generate_wireguard_config():
    private_key = generate_wireguard_private_key()
    public_key = generate_wireguard_public_key(private_key)

    server_ip = "10.202.10.10"  # IP سرور ربات
    config = f"""
[Interface]
PrivateKey = {private_key}
Address = 10.0.0.2/24
DNS = {server_ip}

[Peer]
PublicKey = {public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {server_ip}:51820
PersistentKeepalive = 25
"""
    return config.strip()

# تولید کانفیگ OpenVPN
def generate_openvpn_config():
    username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

    config = f"""
client
dev tun
proto udp
remote 10.202.10.10 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
remote-cert-tls server
cipher AES-256-CBC
auth SHA256
compress lz4
verb 3
<auth-user-pass>
{username}
{password}
</auth-user-pass>
"""
    return config.strip()

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    if is_user_valid(user_id):
        show_country_selection(message.chat.id)
    else:
        bot.send_message(message.chat.id, "برای خرید اشتراک، لطفاً به پشتیبانی مراجعه کنید:",
                         reply_markup=InlineKeyboardMarkup().add(
                             InlineKeyboardButton("خرید اشتراک", url=SUPPORT_LINK),
                             InlineKeyboardButton("تست DNS", callback_data="test_dns")))
#بخش مخصوص ادمین 
@bot.message_handler(commands=['panel'])
def admin_panel(message):
    if message.from_user.id == OWNER_ID:
        bot.send_message(message.chat.id, "آیدی عددی کاربر را ارسال کنید:")
        bot.register_next_step_handler(message, receive_user_id)
    else:
        bot.send_message(message.chat.id, "شما به این بخش دسترسی ندارید.")

def receive_user_id(message):
    try:
        target_id = int(message.text.strip())
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("فعالسازی اشتراک 30 روزه", callback_data=f"activate_{target_id}"))
        bot.send_message(message.chat.id, f"کاربر {target_id} انتخاب شد.", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "آیدی نامعتبر است.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("activate_"))
def handle_activation(call):
    if call.from_user.id == OWNER_ID:
        user_id = call.data.split("_")[1]
        user_data[str(user_id)] = time.time() + (30 * 24 * 3600)
        save_data()
        bot.send_message(call.message.chat.id, f"اشتراک برای کاربر {user_id} فعال شد.")
        try:
            bot.send_message(int(user_id), "اشتراک شما توسط مدیر فعال شد و به مدت 30 روز معتبر است.")
        except:
            pass
    else:
        bot.answer_callback_query(call.id, "دسترسی ندارید.")

def show_country_selection(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Turkey", callback_data="Turkey"),
        InlineKeyboardButton("Germany", callback_data="Germany"),
        InlineKeyboardButton("UAE", callback_data="UAE")
    )
    markup.add(
        InlineKeyboardButton("خرید اشتراک", url=SUPPORT_LINK),
        InlineKeyboardButton("تست DNS", callback_data="test_dns"),
        InlineKeyboardButton("WireGuard", callback_data="WireGuard"),
        InlineKeyboardButton("OpenVPN", callback_data="OpenVPN")
    )
    bot.send_message(chat_id, "کشور مورد نظر رو انتخاب کن:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "test_dns")
def handle_test_dns(call):
    text = f"DNS تست هفتگی IPv4:\n\n{weekly_test_dns}"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data in ["Turkey", "Germany", "UAE"])
def handle_dns(call):
    country = call.data
    ipv4_dns, ipv6_dns = "یافت نشد", "یافت نشد"

    for _ in range(20):
        ipv4 = generate_random_ipv4()
        if check_ipv4(ipv4):
            ipv4_dns = ipv4
            break

    for _ in range(20):
        ipv6 = generate_random_ipv6()
        if check_ipv6(ipv6):
            ipv6_dns = ipv6
            break

    text = f"DNS برای {country}:\n\nIPv4: {ipv4_dns}\nIPv6: {ipv6_dns}"
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)

@bot.callback_query_handler(func=lambda call: call.data == "WireGuard")
def handle_wireguard(call):
    config = generate_wireguard_config()
    file_name = "wireguard_config.conf"
    with open(file_name, "w") as f:
        f.write(config)
    bot.send_document(call.message.chat.id, open(file_name, 'rb'))
    os.remove(file_name)

@bot.callback_query_handler(func=lambda call: call.data == "OpenVPN")
def handle_openvpn(call):
    config = generate_openvpn_config()
    file_name = "openvpn_config.ovpn"
    with open(file_name, "w") as f:
        f.write(config)
    bot.send_document(call.message.chat.id, open(file_name, 'rb'))
    os.remove(file_name)

bot.infinity_polling()
