import discord
import DataManager
import Database

class PatternModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Patrón", style=discord.InputTextStyle.paragraph))

    async def callback(self, interaction: discord.Interaction):
        Embed = await DataManager.EmbedByPattern(self.children[0].value, interaction)
        await Database.NewDatabaseByPattern(self.children[0].value)
        await interaction.response.send_message(embeds=[Embed])

