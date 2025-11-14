import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from logic import handle_message

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents) 

@bot.event
async def on_ready():
    """Bot başlatıldığında çalışır."""
    print(f'✅ Bot giriş yaptı: {bot.user.name} (ID: {bot.user.id})')
    print('----------------------------------')

@bot.event
async def on_message(message):
    await handle_message(message)
    # Komutları da işlemek için gerekli
    await bot.process_commands(message) 

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("❌ HATA: Geçersiz Bot Token'ı.")
    except Exception as e:
        print(f"❌ BOT BAŞLATILAMADI: {e}")