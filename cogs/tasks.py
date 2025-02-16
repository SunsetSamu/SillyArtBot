import discord
from discord.ext import tasks, commands
from datetime import datetime, timezone
from utils.data_manager import DataManager

class ChallengeTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_data = DataManager.load_data()

    @tasks.loop(hours=0.5)
    async def weekly_challenge(self):
        print("++++ Running task at ", datetime.now(timezone.utc), " ++++")
        for guild_id, data in self.guild_data.items():

            current_challenge_end_str = data.get('current_challenge', {}).get('end')
            current_challenge_end = datetime.fromisoformat(current_challenge_end_str) if current_challenge_end_str else None

            announcement_channel_id = data.get('announcement_channel')
            submission_channel_id = data.get('submission_channel')
            announcement_channel = self.bot.get_channel(announcement_channel_id)
            submission_channel = self.bot.get_channel(submission_channel_id)
            if not announcement_channel_id or not submission_channel_id:
                print(f"ERROR CODE 1")
                continue
            
            try:
                if current_challenge_end and datetime.now(timezone.utc) > current_challenge_end and data.get('last_announcement_id') is not None:
                    print(f"Current challenge for guild {guild_id} has ended.")
                    await self.bot.process_winner(guild_id, submission_channel, announcement_channel)
                elif current_challenge_end and datetime.now(timezone.utc) < current_challenge_end and data.get('last_announcement_id') is not None:
                    print(f"Last announcement for guild {guild_id} is within 7 days, skipping new announcement.\n= = = =\nCurrent challenge end date: {current_challenge_end}\nCurrent date: {datetime.now(timezone.utc)}\n= = = =")
                    continue
                else:
                    print(f"Not found an active challenge in guild {guild_id}.")

                    if datetime.now(tz=timezone.utc).weekday() == 6 and datetime.now(tz=timezone.utc).hour == 12:
                        print(f"Announcing new challenge for guild {guild_id}.")
                        await self.bot.announce_weekly_challenge(guild_id, data)
                    else:
                        print(f"Today is not Sunday, skipping announcement for guild {guild_id}.")
                    continue

            except discord.NotFound:
                print("\nxxxxxxxxx\n\ndiscord.NotFound\n\nxxxxxxxxx\n")
                continue
            
async def setup(bot):
    await bot.add_cog(ChallengeTasks(bot))