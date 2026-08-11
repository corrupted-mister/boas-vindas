import os
import discord
from dotenv import load_dotenv
from easy_pil import Editor, Font, load_image_async

# Carrega as variáveis de ambiente (Token e ID do Canal)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))

# Configurando os 'intents' para o bot conseguir detectar novos membros
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"O bot {client.user} está online e pronto para receber membros!")


@client.event
async def on_member_join(member):
  # Procura o canal pelo ID configurado nas variáveis de ambiente
  channel = client.get_channel(CHANNEL_ID)
  if not channel:
    return

  try:
    # Carrega a imagem de fundo da raiz do projeto
    background = Editor("wcbg.jpeg")

    # Pega a foto de perfil do usuário no Discord
    profile_image = await load_image_async(str(member.display_avatar.url))

    # Redimensiona a foto de perfil para 150x150 e corta em círculo
    profile = Editor(profile_image).resize((150, 150)).circle_image()

    # Configura as fontes padrão da biblioteca easy-pil
    poppins_big = Font.poppins(size=50, variant="bold")
    poppins_small = Font.poppins(size=30, variant="regular")

    # Cola a foto de perfil centralizada no topo
    background.paste(profile, (325, 70))

    # Escreve o texto de Bem-Vindo e o Nome do Usuário perfeitamente centralizados
    background.text(
        (400, 240),
        "BEM-VINDO(A)",
        color="white",
        font=poppins_big,
        align="center",
    )
    background.text(
        (400, 305),
        f"{member.name}",
        color="white",
        font=poppins_small,
        align="center",
    )

    # Converte a imagem pronta para um formato aceito pelo Discord
    file = discord.File(fp=background.image_bytes, filename="welcome.png")

    # Envia a mensagem mencionando o usuário com a imagem anexada
    await channel.send(
        f"Olá {member.mention}! Seja muito bem-vindo(a) ao servidor!", file=file
    )

  except Exception as e:
    print(f"Ocorreu um erro ao gerar a imagem: {e}")


# Inicia o bot utilizando o token de segurança
client.run(TOKEN)
