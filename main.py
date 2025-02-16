from datetime import datetime, timedelta, timezone
import json
import random
from discord.ext import commands
from utils.data_manager import DataManager

import discord
import os
from constants import TEMATICAS, PERSONAJES
from dotenv import load_dotenv

class ArtBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        super().__init__(command_prefix='[]', intents=intents)
        self.guild_data = DataManager.load_data()

        self.remove_command("help")

    async def setup_hook(self):
        await self.load_extension('cogs.admin_commands')
        await self.load_extension('cogs.user_commands')
        await self.load_extension('cogs.tasks')

    async def on_ready(self):
        print(
            f'------------------------------------\n'
            f'Logged in as {self.user}\n'
            f'------------------------------------')
        if not self.get_cog('ChallengeTasks').weekly_challenge.is_running():
            self.get_cog('ChallengeTasks').weekly_challenge.start()

    def save_data(self):
        DataManager.save_data(self.guild_data)


    async def announce_weekly_challenge(self, guild_id, data):
        announcement_channel = self.get_channel(data['announcement_channel'])
        submission_channel = self.get_channel(data['submission_channel'])
        
        if not announcement_channel or not submission_channel:
            print("Missing announcement or submission channel.")
            return
        
        
        if data.get('current_challenge', {}).get('next_theme') is not None:
            tema = data['current_challenge']['next_theme']
        elif 'theme' in data.get('current_challenge', {}) and data['current_challenge']['theme'] is not None:
            tema = data['current_challenge']['theme']
        else:
            tema = random.choice(TEMATICAS)
        
        start_date = datetime.now(timezone.utc)
        end_date = start_date + timedelta(hours=23, minutes=30)
        
        mensaje = (
            f"🎨 **Reto semanal de dibujos** 🎨\n"
            f"---------------------------------------------\n"
            f"Del {start_date.strftime('%d/%m')} al <t:{int(end_date.timestamp())}:F>\n"
            f"Temática: **{tema}**\n\n"
            f"Sube tus obras a {submission_channel.mention}!\n"
        )
        
        announcement_message = await announcement_channel.send(mensaje)

        
        self.guild_data[guild_id]['last_announcement_id'] = announcement_message.id
        self.guild_data[guild_id]['current_challenge'] = {
            'start': start_date.isoformat(),
            'end': end_date.isoformat(),
            'theme': tema,
            'next_theme': None,
            'active_challenge': True
        }
        self.save_data()

    async def process_winner(self, guild_id, submission_channel, announcement_channel):
        data = self.guild_data.get(guild_id, {})
        submission_channel = self.get_channel(data.get('submission_channel'))
        challenge = data.get('current_challenge')
        next_ch = data.get('current_challenge', {}).get('next_theme')
        
        if not challenge:
            return
        
        submissions = []
        start = datetime.fromisoformat(challenge['start'])
        end = datetime.fromisoformat(challenge['end'])
        
        async for message in submission_channel.history(limit=100, oldest_first=True):
            if message.created_at > end:
                continue
            if message.created_at < start:
                break
            if message.attachments:
                # Verificar si el mensaje contiene una imagen o video
                if any(attachment.content_type.startswith('image/') or attachment.content_type.startswith('video/') for attachment in message.attachments):
                    submissions.append(message)
        
        if not submissions:
            await announcement_channel.send("😢 Nadie participó esta semana... ¡Anímense a participar la próxima!")
            data['last_announcement_id'] = None
            data['current_challenge'] = {
            'start': None,
            'end': None,
            'theme': None,
            'next_theme': next_ch,
            'active_challenge': False
            }
            self.save_data()
            return
        
        # Encontrar máximo de reacciones del emoji más usado
        max_reactions = 0
        candidates = []
        for message in submissions:
            reaction_counts = [reaction.count for reaction in message.reactions]
            if reaction_counts:
                max_reaction_count = max(reaction_counts)
                if max_reaction_count > max_reactions:
                    max_reactions = max_reaction_count
                    candidates = [message]
                elif max_reaction_count == max_reactions:
                    candidates.append(message)

        if not candidates:
            return
        
        
        winner = random.choice(candidates)
        
        # Obtener la URL de la imagen o video del mensaje ganador
        media_url = winner.attachments[0].url
        
        await announcement_channel.send(
            f"🏆 **Ganador de la semana!** 🎉\n"
            f"Obra de {winner.author.mention} con {max_reactions} reacciones!\n"
            f"{winner.jump_url}\n"
            f"![Ganador]({media_url})"
        )

        data['last_announcement_id'] = None
        data['current_challenge'] = {
            'start': None,
            'end': None,
            'theme': None,
            'next_theme': None,
            'active_challenge': False
        }
        self.save_data()
    
#    async def soft_reset(self, ctx, error):
#
#        
#        guild_id = str(ctx.guild.id)
#        await ctx.send("⏳ Resetting the current challenge...")
#        if guild_id in self.guild_data:
#            data = self.guild_data[guild_id]
#
#            data['last_announcement_id'] = None
#            data['current_challenge'] = {
#                'start': None,
#                'end': None,
#                'theme': None,
#                'next_theme': None,
#                'active_challenge': False
#            }
#            self.save_data()
#            await ctx.send("✅ Current challenge has been reset successfully.")
#
#        else:
#            await ctx.send("❌ No configuration found for this server.")
    

bot = ArtBot()

if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))