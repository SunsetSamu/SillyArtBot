from discord.ext import commands
import random
from constants import TEMATICAS, PERSONAJES

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def topic(self, ctx):
        """Genera una temática aleatoria"""
        await ctx.send(f"🎨 Temática sugerida: **{random.choice(TEMATICAS)}**")
        pass

    @commands.command()
    async def character(self, ctx):
        """Genera un personaje aleatorio"""
        idea = (
            f"**{random.choice(PERSONAJES)}** "
        )
        await ctx.send(f"🎨 Personaje sugerido:\n{idea}")
        pass

    @commands.command()
    async def help(self,ctx):
        await ctx.send(
        f"**Comanditos:**\n"
        f"```markdown\n"
        f"> El prefix del bot es []\n\n"
        f"# Generales:\n"
        f"[]topic: _Elige una temática aleatoria de la base de datos._\n"
        f"[]character: _Elige un personaje aleatorio de la base de datos._\n"
        f"~POR AÑADIR~ []database (characters/topics): _Muestra la base de datos completa\nde personajes o temáticas._\n"
        f"[]help: _Muestra este mensaje._\n\n"
        f"# Administración del bot:\n"
        f"[]setchallenge (canal_anuncios/canal_entradas): _Configura los canales necesarios\npara que el bot funcione en el servidor._\n"
        f"[]startchallenge (+ tema personalizado): _Empieza el reto semanal sin importar el\ndia de la semana o programa el siguiente con la tematica que quieras. []sc_\n"
        f"[]endchallenge: _Termina el reto semanal actual y fuerza sacar los resultados. []ec_\n"
        f"[]checkconfig: _Muestra la configuración actual del servidor. []cc_\n"
        f"[]linkmsg: _Encuentra el link del anuncio al reto actual. []la_\n"
        f"```\n"
        f"*Bot creado por _@SunsetSamu_*\n"
        f"sunsetsamu.github.io\n"
        )
    
async def setup(bot):
    await bot.add_cog(UserCommands(bot))