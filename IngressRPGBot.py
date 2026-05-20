from flask import Flask
import threading
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

from parser import parse_stats
from calculator import calculate_profiles


# ==========================================
# TOKEN
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")


# ==========================================
# FLASK WEB SERVER
# ==========================================

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Ingress RPG Bot Online"


# ==========================================
# TELEGRAM MESSAGE HANDLER
# ==========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    try:

        player_data = parse_stats(text)

        results = calculate_profiles(player_data)

        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1],
            reverse=True
        )

        main_class = sorted_results[0][0]
        sub_class = sorted_results[1][0]

        response = ""

        response += "━━━━━━━━━━━━━━\n"
        response += f"AGENTE: {player_data['Agent Name']}\n"
        response += f"FACTION: {player_data['Agent Faction']}\n"
        response += "━━━━━━━━━━━━━━\n\n"

        response += f"CLASE PRINCIPAL\n{main_class}\n\n"
        response += f"SUBCLASE\n{sub_class}\n\n"

        response += "📊 ATRIBUTOS\n\n"

        for name, score in sorted_results:

            bar = "█" * int(score / 10)

            response += f"{name}: {bar} {score}%\n"

        response += "\n━━━━━━━━━━━━━━"

        await update.message.reply_text(response)

    except Exception as e:

        await update.message.reply_text(
            f"Error procesando stats:\n{e}"
        )


# ==========================================
# TELEGRAM BOT
# ==========================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

print("Bot iniciado...")


# ==========================================
# THREAD BOT
# ==========================================

def run_web():

    PORT = int(os.environ.get("PORT", 10000))

    web_app.run(
        host="0.0.0.0",
        port=PORT
    )


web_thread = threading.Thread(target=run_web)

web_thread.start()


# Ejecutar bot en hilo principal
app.run_polling()
