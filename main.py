import discord
from discord import option, commands
from UI.TextModals import PatternModal
from UI.Views import TestView, PossitionView
from DataManager import EmbedByPattern, Start, GetLastPattern, GetDataChat, GetAdmin
from Database import PushListToDb, GetDataByOwner
import asyncio
BotonesPersonalizables = ["Ataque", "Defensa"]
Token = "MTEwMTM5MzU3MDI4MTMwODE5Mg.G6Qyeq.KJdPgTmUtAIsPIC9GJUVAPpeguoSxk6BiLH3cs"



def main(botToken:str):
    
    intents = discord.Intents.all()

    bot = discord.Bot(intents=intents)
    
    @bot.command(name="start", description="Inicia a Jane")
    @commands.default_permissions(administrator=True)
    async def test_command(interaction):
        await Start(interaction)
        
        while True:
            await testlectura(interaction, False)
            await asyncio.sleep(60)
    
    @bot.command(name="ping", description="Comprueba si el bot va")
    async def test_command(interaction):
        await interaction.respond("Pong!")     
    
    @bot.command(name="yo", description="Muestra tu ficha")
    @option("ficha", int, description="Ficha de personaje a elegir", required=False)
    async def test_embed(interaction, ficha = 1):
        if GetAdmin().Ownername == "":
            embed = await EmbedByPattern(GetLastPattern(), interaction)
            
        embed = await EmbedByPattern(GetLastPattern(), interaction, await GetDataByOwner(interaction.author.mention, interaction, ficha))
        await interaction.respond(embed=embed,view=TestView(GetAdmin().BotonesComandos, GetAdmin().SliderSetting))
    
    @bot.command(name="set_pattern", description="Introduce el pattern de datos")
    @commands.default_permissions(administrator=True)
    async def testmodal(interaction):
        myModal = PatternModal(title="TEST")
        await interaction.send_modal(myModal)
    
    @bot.command(name="read", description="Lee el canal de datos")
    @commands.default_permissions(administrator=True)
    async def testlectura(interaction, mensaje=True):
        Mensajes = []
        async for elem in GetDataChat().history(limit=None):
            Mensajes.append(elem)
        await PushListToDb(Mensajes, interaction)
        if mensaje:
            await interaction.respond("Lectura hecha")
            
    @bot.command(name="posición", description="Pone un sistema para cambiar tu ubicación a este chat")
    async def possition(interaction):
        await interaction.respond(view=PossitionView())
        
    bot.run(botToken)
    
    
main(Token)