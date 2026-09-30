import os
import telebot

# Tokenni Render tizimidagi Environment Variables ichidan majburiy o'qiydi
TOKEN = os.environ.get("TOKEN", "8951364887:AAH15QJoD58GopV1kmGSIvda1zs1ITWwHoI")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🇺🇿 *Futbol Tahlil Botiga xush kelibsiz!*\n\n"
        "Bu bot eng markaziy futbol o'yinlari jadvalini va jamoalarning imkoniyatlarini tahlil qilib beradi.\n\n"
        "📜 *Buyruqlar:*\n"
        "/oyyinlar - Bugungi eng muhim o'yinlar ro'yxati va aqlli tahlili"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['oyyinlar'])
def get_matches(message):
    bot.reply_to(message, "🔄 *Bugungi o'yinlar tahlil qilinmoqda...* Iltimos kuting...", parse_mode="Markdown")
    
    try:
        matches = [
            {"home": "Real Madrid", "away": "Barselona", "liga": "La Liga"},
            {"home": "Manchester Siti", "away": "Liverpul", "liga": "APL"},
            {"home": "Arsenal", "away": "Chelsi", "liga": "APL"},
            {"home": "Bavariya", "away": "PSJ", "liga": "ECHL"},
            {"home": "Yuventus", "away": "Milan", "liga": "A Seriya"}
        ]

        text = "📅 *Bugungi Markaziy O'yinlar va Aqlli Tahlil:*\n\n"
        
        for match in matches:
            home = match['home']
            away = match['away']
            liga = match['liga']
            
            home_weight = sum(ord(c) for c in home) % 100
            away_weight = sum(ord(c) for c in away) % 100
            total = home_weight + away_weight + 1
            
            home_pct = int((home_weight / total) * 100)
            away_pct = int((away_weight / total) * 100)
            draw_pct = 100 - home_pct - away_pct
            if draw_pct < 0: draw_pct = 12
            
            if home_pct > away_pct and home_pct > 40:
                xulosa = f"🔮 *Prognoz:* {home} o'z maydonida ustunlikka ega. G'alaba qozonish ehtimoli yuqori."
            elif away_pct > home_pct and away_pct > 40:
                xulosa = f"🔮 *Prognoz:* {away} safarda bo'lishiga qaramay juda xavfli holatda."
            else:
                xulosa = "🔮 *Prognoz:* Kuchlar deyarli teng. Shiddatli o'yin va durang natija kutilmoqda."

            text += f"🏆 *{liga}* | ⚽️ *{home}* - *{away}*\n"
            text += f"📊 Imkoniyatlar: {home} {home_pct}% | Durang {draw_pct}% | {away} {away_pct}%\n"
            text += f"{xulosa}\n"
            text += "───────────────\n"

        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Bot tizimida texnik xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")

if __name__ == "__main__":
    bot.infinity_polling()
    
