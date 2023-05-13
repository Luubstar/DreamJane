from discord import Embed
import exceptionHandler as eh
import rolldice,os,sqlite3
import re
from ast import literal_eval

class Manager():
    Pattern = None
    Datachat = None
    Ownername = ""
    Fichaname = ""
    PosicionName = ""
    AvatarName = ""
    BotonesComandos = []
    SliderSetting = None
    def __init__(self) -> None:
        pass
    

admin = Manager()
Commands = ["[nextline]", "[title]", "[description]","[datachat]", "[replychat]", "[number]", "[ownertag]", "[button", "[numberselector", "[avatar]", "[noshow]"]
SpecialCommands = ["[title]", "[description]","[datachat]", "[button", "[numberselector"]

async def EmbedByPattern(pattern :str,interaction , values = []):
    try:
        if pattern != None:
            parent = Embed(title="Example title", description="Example description")
            lineas = pattern.split("\n")
            
            global admin
            admin.BotonesComandos.clear()
            for linea in lineas:
                value = "No Asignado"
                if linea.__contains__(":"):
                    
                    nextline = True
                    if linea.lower().__contains__("[nextline]"):
                        nextline = False
                        
                    if linea.lower().__contains__("[ownertag]"):
                        admin.Ownername = linea.split(":")[0]
                        
                    if linea.lower().__contains__("[number]"):
                        admin.Fichaname = linea.split(":")[0]
                        
                    if linea.lower().__contains__("[replychat]"):
                        admin.PosicionName = linea.split(":")[0]
                        
                    if linea.lower().__contains__("[avatar]"):
                        admin.AvatarName = linea.split(":")[0]
                        
                    if linea.lower().__contains__("[button"):
                        cadena = linea.split("[button")[1]
                        cadena = cadena.strip()[:-1]
                        cadena = cadena.split(",")
                        newcadena = []
                        for car in cadena:
                            newcar = car.strip().replace("id=", "").replace("emote=","").replace("command=","").replace("row=","")
                            newcadena.append(newcar.strip())
                        try:
                            newcadena.append(interaction.author.mention)
                        except:
                            newcadena.append(interaction.user.mention)
                        admin.BotonesComandos.append(newcadena)
                        
                    if linea.lower().__contains__("[numberselector"):    
                        cadena = linea.split("[numberselector")[1]
                        cadena = cadena.strip()[:-1]
                        cadena = cadena.split(",")
                        newcadena = []
                        for car in cadena:
                            newcar = car.strip().replace("max=", "").replace("row=","")
                            newcadena.append(newcar.strip())
                            
                        try:
                            newcadena.append(interaction.author.mention)
                        except:
                            newcadena.append(interaction.user.mention) 
                        
                        admin.SliderSetting = newcadena
                    
                    if linea.lower().__contains__("[title]"): 
                        parent.title = linea.split(":")[1].replace("[title]", "")
                    elif linea.lower().__contains__("[description]"):
                        parent.description = linea.split(":")[1].replace("[description]", "")
                    elif linea.lower().__contains__("[datachat]"):
                        admin.Datachat = GetChannelByID(int(linea.split(":")[1].replace("[datachat]", "").strip()), interaction)
                    else: 
                        for val in values:
                            if val[0].lower() == linea.lower().split(":")[0]:
                                value = val[1]
                        if  linea.lower().__contains__("[avatar]"):
                            try:
                                if str(value) != "NA":
                                    parent.set_image(url=value)
                            except:pass
                            
                        if not HasSpecialCommand(linea.lower()) and not linea.lower().__contains__("[avatar]") and not linea.lower().__contains__("[noshow]") and not linea.strip() == "":
                            parent.add_field(name= linea.split(":")[0], value=value, inline=nextline)
                            
                        
            admin.Pattern = pattern
            await SavePattern(pattern)
            return parent
    except Exception as e: await eh.InteractionException(e, interaction)
    
async def SavePattern(data :str):
    f = open("LastPattern.txt", "w")
    f.write(data)
    f.close()
    
async def Start(interaction):
    try:
        f = open("LastPattern.txt", "r")
        global admin
        admin.Pattern = f.read()
        lineas = admin.Pattern.split("\n")
        
        if os.path.exists("players.db"):
            os.remove("players.db")
        con = sqlite3.connect("players.db")
        cur = con.cursor()
        data = ""
        for linea in admin.Pattern.split("\n"):
            if linea.strip().__len__() > 0 and linea.__contains__(":"):
                if not HasSpecialCommand(linea.split(":")[1]):
                    data += "'"+linea.split(":")[0] + "' DEFAULT '',"
        data = data[:-1]
        cur.execute(f"CREATE TABLE jugadores ({data})")
        con.close()
        
        for linea in lineas:
            if linea.__contains__(":"):
                if linea.lower().__contains__("[datachat]"):
                        admin.Datachat = GetChannelByID(int(linea.split(":")[1].replace("[datachat]", "").strip()), interaction)
        await interaction.respond("Iniciado")
        
    except Exception as e: await eh.InteractionException(e, interaction)
    
        
def GetLastPattern():
    global admin
    return admin.Pattern

def GetDataChat():
    global admin
    return admin.Datachat

def GetChannelByID(id, interaction):
    for channel in interaction.guild.channels:
        if channel.id == id:
            return channel
                
def GetAdmin():
    global admin
    return admin    
        
def ClearPattern(msg):
    for item in Commands:
        msg = msg.replace(item, "")
    return msg

def HasSpecialCommand(msg):
    for item in SpecialCommands:
        if msg.lower().__contains__(item.lower()): return True
    return False

async def diceParser(entrada: str):
    print(entrada)
    dados = await find_critdice(entrada)
    print(dados)
    valores =[]
    for dado in dados:
        result, explanation = rolldice.rolldice.roll_dice(dado,floats=False)
        valores.append(f" {result}")
    
    return await reemplazar_dados(entrada,valores)

async def find_critdice(text):
    pattern = r"\b\d+d\d+(?:\*\d+)?\b"
    
    critdice_matches = re.findall(pattern, text)

    return critdice_matches


async def reemplazar_dados(cadena, valores):
    dados = re.findall(r"\b\d+d\d+(?:\*\d+)?\b", cadena)

    for i, dado in enumerate(dados):
        cadena = re.sub(dado, str(valores[i]), cadena, count=1)

    cadena = procesar_entrada(cadena)
   
    return cadena

def procesar_entrada(cadena):
    array = list(cadena)
    elementos = []
    elem = ""
    operaciones = ["+","-","/","*", "(", ")"]
    comparadores = ["<", ">", ">=", "<=", "==", "!="]
    
    detecting = False
    for item in array:
        if (item.isdigit() or item in operaciones):
            if detecting == False:
                detecting = True
                elementos.append(elem)
                elem = ""
            elem += item
            
        elif (item.isalpha() or item == "[" or item == "]") and not item in operaciones and detecting==True:
            elementos.append(elem)
            elem = item
            detecting = False
            
        elif item == "[":
            elementos.append(elem)
            elem = item
            
        else:
            elem += item
        
    if elem != "":
        elementos.append(elem)
    
    res = []
    next = True
    for item in elementos:
        try:
            if next:
                compara = False
                comparador = ""
                for comp in comparadores:
                    if item.__contains__(comp):
                        compara = True
                        comparador = comp
                
                if not compara:
                    resultado = str(eval(item))
                    res.append(resultado + f" [{item}] ")
                else:
                    resultado = str(eval(item))
                    bolres = eval(item)
                    next = bolres
                    if bolres:
                        res.append(item.split(comparador)[0] + f" [{item}]  ")
                    else:
                        res.append(item.split(comparador)[0])
            else: next = True
        except:res.append(item)
    
    cadena = ""
    for result in res: cadena+= result
    return cadena.replace("*","\*")
    