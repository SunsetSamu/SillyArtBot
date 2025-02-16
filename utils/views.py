from discord.ui import View, Button
import discord

class ConfirmationView(View):
    def __init__(self, ctx, action):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.action = action

    @discord.ui.button(label="Continuar", style=discord.ButtonStyle.green)
    async def confirm(self, interaction, Button):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("...")
            await self.action(self.ctx)
            self.stop()
        else:
            await interaction.response.send_message("❌ No tienes permisos.")

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.red)
    async def cancel(self, interaction, Button):
        if interaction.user.guild_permissions.administrator:
            # await interaction.response.send_message("❌ Acción cancelada.")
            self.stop()
        else:
            await interaction.response.send_message("❌ No tienes permisos.")