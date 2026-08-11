import discord
import os
from dotenv import load_dotenv
from easy_pil import Editor, load_image_async, Font

# Carrega as variáveis do arquivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))

# Configurando os 'intents' para o bot conseguir ver quem entra
intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'O bot {client.user} está online e pronto para receber membros!')

@client.event
async def on_member_join(member):
    # Procura o canal pelo ID configurado no .env
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return

    try:
        # Carrega a imagem de fundo (certifique-se de ter a pasta assets e a imagem wcbg.jpeg)
        background = Editor("assets/wcbg.jpeg")
        
        # Pega a foto de perfil do usuário no Discord
        profile_image = await load_image_async(str(member.display_avatar.url))
        
        # Redimensiona a foto de perfil para 150x150 e corta em círculo
        profile = Editor(profile_image).resize((150, 150)).circle_image()
        
        # Configura as fontes (a biblioteca já traz a fonte Poppins por padrão)
        poppins_big = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=30, variant="regular")
        
        # Cola a foto de perfil no meio da imagem 
        background.paste(profile, (325, 90)) 
        
        # Escreve o texto de Bem-Vindo e o Nome do Usuário
        background.text((400, 260), "BEM-VINDO(A)", color="white", font=poppins_big, align="center")
        background.text((400, 325), f"{member.name}", color="white", font=poppins_small, align="center")
        
        # Converte a imagem pronta para um formato que o Discord aceita
        file = discord.File(fp=background.image_bytes, filename="welcome.png")
        
        # Envia a mensagem com a imagem no canal
        await channel.send(f"Olá {member.mention}! Seja muito bem-vindo(a) ao servidor!", file=file)
        
    except Exception as e:
        print(f"Ocorreu um erro ao gerar a imagem: {e}")

# Inicia o bot
client.run(TOKEN)
