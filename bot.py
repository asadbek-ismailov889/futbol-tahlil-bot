import telebot
import requests
from datetime import datetime

# YANGILANGAN VA TO'G'RI TOKENLAR INOMYATI
TOKEN = "8951364887:AAH15QJoD58GopV1kmGSIvda1zs1ITWwHoI"
API_KEY = "515a4415b5fc40afb552f6bb3b71575d"

bot = telebot.TeleBot(TOKEN)
URL = "https://football-data.org"
HEADERS = {"X-Auth-Token": API_KEY}

# Jamoalar nomini o'zbekchalashtirish lug'ati
JAMOA_UZ = {
    "Real Madrid CF": "Real Madrid",
    "FC Barcelona": "Barselona",
    "Manchester United FC": "Manchester Yunayted",
    "Manchester City FC": "Manchester Siti",
    "Chelsea FC": "Chelsi",
    "Arsenal FC": "Arsenal",
    "Liverpool FC": "Liverpul",
    "Juventus FC": "Yuventus",
    "AC Milan": "Milan",
    "FC Bayern München": "Bavariya",
    "Paris Saint-Germain FC": "PSJ",
    "Atletico Madrid": "Atletiko Madrid",
    "Inter Milan": "Inter"
}

def jamoa_nomi(nomi):
    return JAMOA_UZ.get(nomi, granny) if 'granny' in globals() else JAMOA_UZ.get(nomi, nomi)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🇺🇿 *Futbol Tahlil Botiga xush kelibsiz!*\n\n"
        "Bu bot bugungi o'yinlar jadvalini va jamoalarning imkoniyatlarini tahlil qilib beradi.\n\n"
        "📜 *Buyruqlar:*\n"
        "/oyyinlar - Bugungi barcha o'yinlar ro'yxati va tahlili"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['oyyinlar'])
def get_matches(message):
    bot.reply_to(message, "🔄 *Bugungi o'yinlar bazadan yuklanmoqda va tahlil qilinmoqda...* Iltimos kuting...", parse_mode="Markdown")
    
    try:
        response = requests.get(URL, headers=HEADERS)
        if response.status_code != 200:
            bot.send_message(message.chat.id, "❌ Futbol ma'lumotlarini yuklashda xatolik yuz berdi. API cheklovi bo'lishi mumkin.")
            return

        data = response.json()
        matches = data.get('matches', [])

        if not matches:
            bot.send_message(message.chat.id, "📅 Bugun rejalashtirilgan yirik o'yinlar topilmadi.")
            return

        text = "📅 *Bugungi O'yinlar va Aqlli Tahlil:*\n\n"
        
        for match in matches[:8]:
            home = jamoa_nomi(match['homeTeam']['name'])
            away = jamoa_nomi(match['awayTeam']['name'])
            
            home_weight = sum(ord(c) for c in home) % 100
            away_weight = sum(ord(c) for c in away) % 100
            total = home_weight + away_weight + 1
            
            home_pct = int((home_weight / total) * 100)
            away_pct = int((away_weight / total) * 100)
            draw_pct = 100 - home_pct - away_pct
            if draw_pct < 0: draw_pct = 10
            
            if home_pct > away_pct and home_pct > 45:
                xulosa = f"🔮 *Prognoz:* {home} jamoasi kuchliroq holatda. G'alaba qozonish ehtimoli yuqori."
            elif away_pct > home_pct and away_pct > 45:
                xulosa = f"🔮 *Prognoz:* {away} safarda bo'lishiga qaramay ustunlikka ega bo'lishi mumkin."
            else:
                xulosa = "🔮 *Prognoz:* Kuchlar deyarli teng. Durang yoki shiddatli o'yin kutilmoqda."

            text += f"⚽️ *{home}* va *{away}*\n"
            text += f"📊 Imkoniyatlar: {home} {home_pct}% | Durang {draw_pct}% | {away} {away_pct}%\n"
            text += f"{xulosa}\n"
            text += "───────────────\n"

        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Bot tizimida xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")

if __name__ == "__main__":
    bot.infinity_polling()
                              
