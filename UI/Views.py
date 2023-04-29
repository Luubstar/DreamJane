import discord
from discord.components import SelectOption
from discord.emoji import Emoji
from discord.enums import ButtonStyle, ChannelType, ComponentType
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, Select
from discord.ui.item import Item

from Database import replaceFromString, GetListOfData, GetDataByOwner
from DataManager import diceParser, EmbedByPattern,GetAdmin,GetLastPattern

class CustomButton(Button):
    command = ""
    owner = None
    def __init__(self, *,command, owner, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.command = command
        self.owner = owner
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        if interaction.user.mention == self.owner:
            cadena = await diceParser(await replaceFromString(self.command))
            await interaction.followup.send(cadena.replace("[nextline]", "\n"))   
        

class CustomSelector(Select):
    owner = None
    def __init__(self,owner, select_type: ComponentType = ComponentType.string_select, *, custom_id: str | None = None, placeholder: str | None = None, min_values: int = 1, max_values: int = 1, options: list[SelectOption] = None, channel_types: list[ChannelType] = None, disabled: bool = False, row: int | None = None) -> None:
        super().__init__(select_type, custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, channel_types=channel_types, disabled=disabled, row=row)
        self.owner = owner
        lista = GetListOfData(owner)
        lista.reverse()
        i = 0
        for item in lista:
            self.add_option(label=item[0], value=str(i))
            i += 1
            
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        if interaction.user.mention == self.owner:
            seleccion = int(self.values[0]) + 1
            embed = await EmbedByPattern(GetLastPattern(), interaction, await GetDataByOwner(interaction.user.mention, interaction, seleccion))
            view = TestView(GetAdmin().BotonesComandos, GetAdmin().SliderSetting)
            await interaction.edit_original_response(embed=embed,view=view)
        

class TestView(discord.ui.View): 
    
    def __init__(self, buttons, selector, *items: Item, timeout: float | None = 270, disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        for button in buttons:
            but = CustomButton(command=button[2], owner=button[4], label=button[0],emoji=button[1], row=int(button[3]), style=discord.ButtonStyle.green)
            self.add_item(but)

        sel = CustomSelector(owner=selector[2], row=int(selector[1]), max_values=1, min_values=0)
        self.add_item(sel)
       
       
 
    
class PossitionView(discord.ui.View):
    
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
    
    @discord.ui.button(label="Cambiar posición", row=0, style=discord.ButtonStyle.blurple)
    async def botonSetter(self, button, interaction):
        pass
    
    
   