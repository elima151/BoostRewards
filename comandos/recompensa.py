import sys
import subprocess
sys.path.append('./modulos/')
from modulos.database import *
from dotenv import load_dotenv
load_dotenv()

ROLE_ID = int(os.getenv('ROLE_ID'))

async def recompensa(message, conn, cur):
    conexion, cursor = conn, cur
    if not any(role.id == ROLE_ID for role in message.author.roles):
        return "No tienes el rol requerido para usar este comando."

    args = message.content.split()[1:]
    if not args:
        return "Debes proporcionar un nick para otorgar la recompensa. Ejemplo: `!recompensa Imanol151`"

    resultado = None
    cursor.execute("SELECT * FROM usos_recompensa WHERE usuario_id = %s", (message.author.id,))
    resultado = cursor.fetchone()
    if resultado is not None:
        return "Ya has usado este comando antes."

    cursor.execute("INSERT INTO usos_recompensa (usuario_id) VALUES (%s)", (message.author.id,))
    conexion.commit()

    comando = f"python test.py {args[0]}"
    subprocess.run(["screen", "-S", "Survi", "-p", "0", "-X", "stuff", f"{comando}\n"])
    
    return f"¡Recompensa otorgada a {args[0]}!"

async def ejecutar_comando(message, conn, cur):
    if message.content.startswith("!recompensa"):
        return await recompensa(message, conn, cur)

    return None

