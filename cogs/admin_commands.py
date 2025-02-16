import discord
from discord.ext import commands
from utils.views import ConfirmationView
from utils.sc_conditions import conditions
from utils.data_manager import DataManager
import random
from constants import TEMATICAS

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchats(self, ctx, tipo: str):
        """Configura los canales del reto (A!challenge c1/c2)"""
        if "c1" in tipo: # Canal de anuncios
            self.bot.guild_data[str(ctx.guild.id)] = {
                'announcement_channel': ctx.channel.id,
                'submission_channel': None,
                'current_challenge': None
            }
        elif "c2" in tipo: # Canal de envíos
            if str(ctx.guild.id) in self.bot.guild_data:
                self.bot.guild_data[str(ctx.guild.id)]['submission_channel'] = ctx.channel.id
        self.bot.save_data()
        try:
            await ctx.send("✅ Configuración actualizada!")
        except discord.Forbidden:
            await ctx.send("❌ No tengo permisos para enviar mensajes en este canal.")

        pass


    @commands.command(aliases=["cc"])
    @commands.has_permissions(administrator=True)
    async def checkconfig(self, ctx):
        """Muestra la configuración actual del servidor"""
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.guild_data:
            data = self.bot.guild_data[guild_id]
            announcement_channel = self.bot.get_channel(data['announcement_channel'])
            submission_channel = self.bot.get_channel(data['submission_channel'])
            current_challenge_id = data.get('last_announcement_id', 'No hay desafío activo')
            next_theme = self.bot.guild_data[guild_id]['current_challenge'].get('next_theme', 'No hay tema siguiente')

            await ctx.send(
                f"📋 **Configuración del servidor**:\n"
                f"---------------------------------------------\n"
                f"**ID del servidor:** {guild_id}\n"
                f"**Canal de anuncios:** {announcement_channel.mention if announcement_channel else 'No configurado'}\n"
                f"**Canal de envíos:** {submission_channel.mention if submission_channel else 'No configurado'}\n"
                f"**Desafío actual:** {current_challenge_id}\n"
                f"**Siguiente tema:** {next_theme}"
                )
        else:
            await ctx.send("❌ No hay configuración guardada para este servidor.")
        pass

    @commands.command(aliases=["ec"])
    @commands.has_permissions(administrator=True)
    async def endchallenge(self, ctx):
        """Fuerza el final del reto actual"""
        async def action(ctx):
            guild_id = str(ctx.guild.id)
            if guild_id in self.bot.guild_data:
                data = self.bot.guild_data[guild_id]
                announcement_channel = self.bot.get_channel(data['announcement_channel'])
                submission_channel = self.bot.get_channel(data['submission_channel'])

                if not announcement_channel or not submission_channel:
                    await ctx.send("❌ Los canales de anuncios o envíos no están configurados.")
                    return

                await self.bot.process_winner(guild_id, submission_channel, announcement_channel)

                await ctx.send("✅ El reto ha sido finalizado (forzado)")
                

                # Anunciar el siguiente reto, uncomment when ready
                # await self.bot.announce_weekly_challenge(guild_id, data)
            else:
                await ctx.send("❌ No hay configuración guardada para este servidor.")

        view = ConfirmationView(ctx, action)
        await ctx.send("⚠️ ¿Estás seguro de que deseas finalizar el reto actual?", view=view)
        pass


    @commands.command(aliases=["sc"])
    @commands.has_permissions(administrator=True)
    async def startchallenge(self, ctx, *, tema: str = None):
        # Fuerza el inicio de un nuevo reto con una temática personalizada
        async def action(ctx):
            guild_id = str(ctx.guild.id)

            if guild_id in self.bot.guild_data:
                data = self.bot.guild_data[guild_id]

                """
                if data.get('last_announcement_id') is not None and data.get('current_challenge', {}).get('next_theme') is None and tema is not None:
                    # si hay un reto activo pero no hay una tematica para el siguiente y el input contiene una tematica
                    data['current_challenge']['next_theme'] = tema
                    self.bot.save_data()
                    await ctx.send("⚠️ Ya hay un reto activo. La temática se guardará para el siguiente reto.")

                elif data.get('last_announcement_id') is not None and data.get('current_challenge', {}).get('next_theme') is not None and tema is not None:
                    # si hay un reto activo y hay una tematica para el siguiente y el input contiene una tematica
                    data['current_challenge']['next_theme'] = tema
                    self.bot.save_data()
                    await ctx.send("⚠️ Ya hay un reto activo y ya habías configurado una temática para el siguiente reto.\nSe ha reemplazado la temática anterior.")

                elif data.get('last_announcement_id') is None and data.get('current_challenge', {}).get('next_theme') is not None and tema is None:
                    # si no hay un reto activo y hay una tematica para el siguiente y el input no contiene una tematica
                    await self.bot.announce_weekly_challenge(guild_id, data)
                    await ctx.send(f"✅ Un nuevo reto ha sido iniciado (forzado) con la temática: {data['current_challenge']['theme']}")
                    
                else:
                    # si no hay un reto activo y no hay una tematica para el siguiente y el input contiene una tematica
                    await self.bot.announce_weekly_challenge(guild_id, data)
                    await ctx.send(f"✅ Un nuevo reto ha sido iniciado (forzado) con la temática: {data['current_challenge']['theme']}")
                    """
                await conditions(self, ctx, tema)

            else:
                await ctx.send("❌ No hay configuración guardada para este servidor.")

        view = ConfirmationView(ctx, action)
        await ctx.send("⚠️ ¿Estás seguro de que deseas iniciar un nuevo reto?", view=view)
        pass

    @commands.command(aliases=["la"])
    @commands.has_permissions(administrator=True)
    async def linkmsg(self, ctx, message_id: int = None):
        """Links the announcement_id to a specific message in the chat"""
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.guild_data:
            data = self.bot.guild_data[guild_id]
            announcement_channel = self.bot.get_channel(data['announcement_channel'])

            if not announcement_channel:
                await ctx.send("❌ El canal de anuncios no está configurado.")
                return
            
            if data.get('last_announcement_id') is None:
                await ctx.send("❌ Message ID doesn't really exist.")
                return
            
            try:
                last_announcement_id = data.get('last_announcement_id')
                if last_announcement_id is None:
                    await ctx.send("❌ No hay ID de anuncio guardado.")
                    return
                    
                try:
                    message = await announcement_channel.fetch_message(last_announcement_id)
                    await ctx.send(f"ANNOUNCEMENT LINKED: {message.jump_url}")

                except discord.NotFound:
                    await ctx.send("❌ No se encontró ningún mensaje con ese ID en el canal de anuncios.")
            
            except discord.NotFound:
                await ctx.send("❌ No se encontró ###########")
        else:
            await ctx.send("❌ No hay configuración guardada para este servidor.")



async def setup(bot):
    await bot.add_cog(AdminCommands(bot))