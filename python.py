import telebot
import requests

BOT_TOKEN = "7602854348:AAG5QTYO5441Pver3YGcVidn7XWAMT9CqHA"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def chat_with_llama3(message):
    prompt = message.text
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        res.raise_for_status()  # Raises HTTPError for bad responses
        reply = res.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        reply = f"⚠️ API Error: {res.status_code} - {res.text}"
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    bot.reply_to(message, reply)

