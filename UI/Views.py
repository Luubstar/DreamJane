import discord
from discord.components import SelectOption
from discord.emoji import Emoji
from discord.enums import ButtonStyle, ChannelType, ComponentType
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, Select
from discord.ui.item import Item

from Database import replaceFromString, GetListOfData, GetDataByOwner, Update
from DataManager import diceParser, EmbedByPattern,GetAdmin,GetLastPattern
from discord import PartialEmoji

class CustomButton(Button):
    command = ""
    owner = None
    position = ""
    def __init__(self, *,command, owner, position, style = ButtonStyle.secondary, label = None, disabled: bool = False, custom_id = None, url = None, emoji= None, row = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.command = command
        self.owner = owner
        self.position = position
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        if interaction.user.mention == self.owner:
            admin = GetAdmin()
            rawval = await replaceFromString(self.command, self.owner, admin.Ownername, self.position, admin.Fichaname)
            
            if not rawval.__contains__("[nodice]"):
                cadena = await diceParser(rawval)
            else:
                cadena = rawval.replace("[nodice]", "")
                
            lista = await GetDataByOwner(self.owner, None, self.position)
            chatid = "NA"
            for item in lista:
                if (item[0] == admin.PosicionName):
                    chatid = item[1].replace("<#", "").replace(">","")
                    
            canal = None
            if chatid != "NA":
                for channel in interaction.guild.channels:
                    if int(channel.id) == int(chatid):
                        canal = channel
            
                await canal.send(interaction.user.mention +": \n" +cadena.replace("[nextline]", "\n").replace("[skip]", "")) 
            else:
                await interaction.followup.send(interaction.user.mention +": \n" +cadena.replace("[nextline]", "\n").replace("[skip]", "")) 
        

class CustomSelector(Select):
    owner = None
    def __init__(self,owner,select_type = ComponentType.string_select, *, custom_id = None, placeholder = None, min_values = 1, max_values = 1, options = None, channel_types = None, disabled: bool = False, row = None) -> None:
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
            view = TestView(GetAdmin().BotonesComandos, GetAdmin().SliderSetting, position=seleccion)
            await interaction.edit_original_response(embed=embed,view=view)
        

class TestView(discord.ui.View): 
    
    def __init__(self, buttons, selector, position = 1,*items: Item, timeout = 600, disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        for button in buttons:
            but = CustomButton(command=button[2], owner=button[4], label=button[0],emoji=PartialEmoji.from_str(str(button[1]).strip()), row=int(button[3]), style=discord.ButtonStyle.green, position=position)
            self.add_item(but)

        sel = CustomSelector(owner=selector[2], row=int(selector[1]), max_values=1, min_values=0)
        self.add_item(sel)
       
    
class PossitionView(discord.ui.View):
    
    def __init__(self, *items: Item, timeout = 600, disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
    
    @discord.ui.button(label="Cambiar posición", row=0, style=discord.ButtonStyle.blurple)
    async def botonSetter(self, button, interaction):
        await interaction.response.defer()
        await Update("<#"+str(interaction.channel_id) +">", GetAdmin().PosicionName, interaction.user.mention, GetAdmin().Ownername)
        await interaction.followup.send("Posición cambiada")
    
   