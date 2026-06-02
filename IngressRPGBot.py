
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
from radar_chart import create_radar_chart
from rarity import calculate_rarity


# ==========================================
# TOKEN
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")


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
        from subclasses import SUBCLASSES
        
        rpg_subclass = SUBCLASSES.get(
            (main_class, sub_class),
            sub_class
            )
        rarity = calculate_rarity(results)

        response = ""
        response = ""

        # ==========================================
        # HEADER
        # ==========================================

        response += "╔══════════════════╗\n"
        response += "      INGRESS RPG\n"
        response += "╚══════════════════╝\n\n"

        response += f"🧑 AGENTE: {player_data['Agent Name']}\n"
        response += f"🔷 FACCIÓN: {player_data['Agent Faction']}\n"
        response += f"⭐ NIVEL: {player_data.get('Level', 0)}\n\n"

# ==========================================
# CLASE PRINCIPAL
# ==========================================

        response += "━━━━━━━━━━━━━━━━━━\n"
        response += "⚔️ PERFIL PRINCIPAL\n"
        response += "━━━━━━━━━━━━━━━━━━\n\n"

        response += f"🏆 Clase: {main_class}\n"

# ==========================================
# SUBCLASE RPG
# ==========================================

        if isinstance(rpg_subclass, dict):

            subclass_name = rpg_subclass["translation"]

            subclass_desc = rpg_subclass["description"]

        else:

            subclass_name = str(rpg_subclass)

            subclass_desc = ""

        response += f"🧩 Subclase: {subclass_name}\n"

        if subclass_desc:

            response += f"📖 {subclass_desc}\n"

# ==========================================
# RAREZA
# ==========================================

        response += "\n━━━━━━━━━━━━━━━━━━\n"
        response += "💎 RAREZA\n"
        response += "━━━━━━━━━━━━━━━━━━\n\n"

        response += f"🌟 {rarity['name']}\n"
        response += f"📜 {rarity['description']}\n"

# ==========================================
# TOP PERFILES
# ==========================================
        response += "\n━━━━━━━━━━━━━━━━━━\n"
        response += "📊 PERFILES\n"
        response += "━━━━━━━━━━━━━━━━━━\n\n"

        for i, (name, score) in enumerate(sorted_results):

         filled = int(score / 10)

         empty = 10 - filled

         bar = "█" * filled + "░" * empty

         medal = ""

         if i == 0:
              medal = "🥇"

         elif i == 1:
           medal = "🥈"

         elif i == 2:
              medal = "🥉"

         response += f"{medal} {name:<12} {bar} {score}%\n"
        

# ==========================================
# FOOTER
# ==========================================

        response += "\n━━━━━━━━━━━━━━━━━━\n"

        response += "📡 Perfil generado automáticamente\n"
        response += "por Ingress RPG Bot\n"

        await update.message.reply_text(response)
        # generar radar chart
        chart_path = create_radar_chart(
    results,
    player_data['Agent Name']
    )
        # enviar imagen
        await update.message.reply_photo(
    photo=open(chart_path, "rb")
    )
      
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


# Ejecutar bot en hilo principal
app.run_polling()
