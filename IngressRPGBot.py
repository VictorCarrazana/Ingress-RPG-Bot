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


TOKEN = os.getenv("BOT_TOKEN")



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

        response += f"AGENTE: {player_data['Agent Name']}\n"
        response += f"FACTION: {player_data['Agent Faction']}\n\n"

        response += f"CLASE PRINCIPAL: {main_class}\n"
        response += f"SUBCLASE: {sub_class}\n\n"

        for name, score in sorted_results:
            response += f"{name}: {score}%\n"

        await update.message.reply_text(response)

    except Exception as e:

        await update.message.reply_text(
            f"Error procesando stats:\n{e}"
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

print("Bot iniciado...")

app.run_polling()