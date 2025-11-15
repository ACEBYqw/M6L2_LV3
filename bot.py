import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from logic import handle_message
import random 

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None) 

@bot.event
async def on_ready():
    """Bot başlatıldığında çalışır."""
    print(f'✅ Bot giriş yaptı: {bot.user.name} (ID: {bot.user.id})')
    print('----------------------------------')

@bot.command(name='start', aliases=['help', 'h'])
async def start_command(ctx):
    """Botun açıklamasını ve kullanımını içeren komut."""
    PREFIX = "!generate" 
    
    help_message = (
        "👋 Merhaba! Ben metin komutlarınızdan **yapay zeka görselleri** oluşturan bir botum.\n\n"
        "**Nasıl kullanılır?**\n"
        f"Görsel oluşturmak için `{PREFIX}` komutunu kullanın ve arkasına istediğiniz görselin açıklamasını yazın.\n\n"
        f"**Örnek:**\n"
        f"```{PREFIX} uzay giysili bir kedi, dijital sanat```\n\n"
        "Görseliniz 🖼️ **FusionBrain API** tarafından oluşturulur ve size anında sunulur. İyi eğlenceler!"
    )
    
    await ctx.send(help_message)

@bot.command(name='sing', aliases=['şarkı', 'söyle'])
async def sing_command(ctx):
    """Botun rastgele bir şarkı sözü söylemesi."""
    songs = [
        "🎶 Benim adım bot, benim adım bot! İşimi yaparım, yorulmam hiç! 🤖",
        "🌟 'Twinkle, twinkle, little star, how I wonder what you are!' ✨",
        "💻 Kodlarım akıyor, disklerim dönüyor... 🎵 Mükemmel bir algoritmayım!",
        "🌈 Gökkuşağı gibi parlıyorum, yapay zekanın gücü bende! ✨"
    ]
    
    await ctx.reply(random.choice(songs))


@bot.event
async def on_message(message):
    await handle_message(message)
    await bot.process_commands(message) 

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("❌ HATA: Geçersiz Bot Token'ı.")
    except Exception as e:
        print(f"❌ BOT BAŞLATILAMADI: {e}")
