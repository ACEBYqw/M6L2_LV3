import discord
from discord import File
from AIGenerator import FusionBrainAPI
from config import API_KEY, SECRET_KEY

API_URL = "https://api-key.fusionbrain.ai/"
ai_api = FusionBrainAPI(API_URL, API_KEY, SECRET_KEY)

PREFIX = "!generate" 

async def handle_message(message):
    """
    Discord mesajlarını işleyen ana fonksiyon.
    """
    if message.author.bot:
        return 

    if message.content.startswith(PREFIX):
        prompt = message.content[len(PREFIX):].strip()

        if not prompt:
            await message.channel.send(
                f"Lütfen bir istek girin! Kullanım: **`{PREFIX} [istediğiniz görselin açıklaması]`**"
            )
            return

        try:
            loading_message = await message.channel.send(
                f"⌛ **'{prompt}'** isteğiniz işleniyor. Lütfen bekleyin..."
            )

            image_binary = ai_api.get_image_binary(prompt)

            if image_binary:
                discord_file = File(image_binary, filename='generated_image.png')
                
                await loading_message.edit(
                    content=f"✨ İşte **'{prompt}'** isteğiniz için oluşturulan görsel:"
                )
                
                await message.channel.send(file=discord_file)
                
            else:
                await loading_message.edit(
                    content="❌ Üzgünüm, görüntü oluşturulamadı. Lütfen isteği kontrol edin."
                )

        except Exception as e:
            print(f"❌ Mesaj işlenirken bir hata oluştu: {e}")
            await message.channel.send("Sunucu tarafında bir hata oluştu.")
