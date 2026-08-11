import os
import discord
from dotenv import load_dotenv
from easy_pil import Editor, Font, load_image_async
from flask import Flask
from threading import Thread

# Configurações do bot
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))

# Servidor Flask falso para manter o Render gratuito ligado
app = Flask(__name__)
@app.route('/')
def home():
    return "O bot está online!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Inicia o servidor web em uma thread separada
Thread(target=run_web_server).start()

# Configuração do bot
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online!")

@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL_ID)
    if not channel: return
    
    try:
        background = Editor("wcbg.jpeg")
        profile_image = await load_image_async(str(member.display_avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()
        
        poppins_big = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=30, variant="regular")
        
        background.paste(profile, (325, 70))
        background.text((400, 240), "BEM-VINDO(A)", color="white", font=poppins_big, align="center")
        background.text((400, 305), f"{member.name}", color="white", font=poppins_small, align="center")
        
        file = discord.File(fp=background.image_bytes, filename="welcome.png")
        await channel.send(f"Olá {member.mention}! Seja bem-vindo(a)!", file=file)
    except Exception as e:
        print(f"Erro: {e}")

client.run(TOKEN)
