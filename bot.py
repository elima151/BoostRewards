import discord
import importlib.util
import os
import sys
from discord.ext import commands
from dotenv import load_dotenv
sys.path.append('./modulos/')
from modulos.database import *

load_dotenv()

ID_SERVIDOR = os.getenv('SERVER_ID')

conn, cur = connect_to_database()

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def cargar_comandos():
    comandos = {}
    for filename in os.listdir("./comandos"):
        if filename.endswith(".py"):
            nombre_comando = filename.split(".")[0]
            spec = importlib.util.spec_from_file_location(nombre_comando, f"./comandos/{filename}")
            comando = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(comando)
            comandos[nombre_comando] = comando.ejecutar_comando
    return comandos

comandos = cargar_comandos()

@client.event
async def on_message(message):
    if message.guild is None or str(message.guild.id) != ID_SERVIDOR:
        return
    
    if message.content.startswith("!recompensa"):
        respuesta = await comandos["recompensa"](message, conn, cur)
        await message.channel.send(respuesta)
    if message.content.startswith("!server"):
        respuesta = await comandos["server"](message)
@client.event
async def on_ready():
    print(f'Bot encendido como {client.user.name}')
client.run(os.getenv('DISCORD_TOKEN'))
