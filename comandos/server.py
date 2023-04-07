import discord
import requests
import datetime
import os
import base64
import asyncio
from io import BytesIO
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

color_hex = os.getenv('EMBED_COLOR')
color = discord.Color(int(color_hex[1:], 16))

async def server(message):
    response = requests.get(f"https://api.mcsrvstat.us/2/{os.getenv('MC_IP')}")

    if response.status_code == 200 and response.json()['online']:
        server_info = response.json()

        banner_base64 = server_info.get('icon', None)
        if banner_base64:
            banner_bytes = base64.b64decode(banner_base64[22:])
            banner_img = BytesIO(banner_bytes)
        else:
            banner_img = None

        embed = discord.Embed(title=f"**Estado {os.getenv('MC_NAME')}**", color=color)
        embed.add_field(name="__Estado__", value=f"Online")
        embed.add_field(name="__Conectados__", value=f"{server_info['players']['online']}/{server_info['players']['max']}")
        embed.add_field(name="__Version__", value=f"{server_info['version']}")
        embed.add_field(name="__IP del Servidor__", value=f"{os.getenv('MC_IP')}")
        embed.add_field(name="__IP Numerica__", value=f"{server_info['ip']}")
        embed.add_field(name="__Puerto__", value=f"{server_info['port']}")
        embed.add_field(name="__IP Bedrock__", value=f"{os.getenv('BD_IP')}")
        embed.set_image(url=f"{os.getenv('MC_BANNER')}")
        embed.timestamp = datetime.datetime.now()

        if banner_img:
            embed.set_thumbnail(url="attachment://thumbnail.png")

        embed.set_footer(text=f"Copyright © {os.getenv('MC_NAME')}")

        msg = await message.channel.send(embed=embed, file=discord.File(banner_img, filename="thumbnail.png") if banner_img else None)
    else:
        embed = discord.Embed(title="Servidor fuera de línea",
                              description="Lo siento, el servidor se encuentra cerrado o en mantenimiento.",
                              color=discord.Color.red())
        msg = await message.channel.send(embed=embed)
        await asyncio.sleep(300)
        await msg.delete()

    return msg

async def ejecutar_comando(message):
    await server(message)
