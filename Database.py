import sqlite3 as sqlite
import os,re
import exceptionHandler as eh
from DataManager import HasSpecialCommand, ClearPattern, GetAdmin

async def NewDatabaseByPattern(pattern :str):
    if os.path.exists("players.db"):
        os.remove("players.db")
    con = sqlite.connect("players.db")
    cur = con.cursor()
    data = ""
    for linea in pattern.split("\n"):
        if linea.strip().__len__() > 0:
            if not HasSpecialCommand(linea.split(":")[1]):
                data += linea.split(":")[0] + ","
    data = data[:-1]
    cur.execute(f"CREATE TABLE jugadores ({data})")
    con.close()
    
async def PushListToDb(messages: list, interaction):
    try:
        con = sqlite.connect("players.db")
        cur = con.cursor()
        cur.execute("DELETE FROM jugadores")
        
        cursor = con.execute('select * from jugadores')
        names = list(map(lambda x: x[0], cursor.description))
        
        MsgList = []
        
        for mensaje in messages:
            MsgList.clear()
            try:
                for msg in mensaje.content.split("\n"):
                    if not HasSpecialCommand(msg):
                        MsgList.append([msg.split(":")[0], ClearPattern(msg.split(":")[1])])
            except Exception as e: print(e)
            
            Datos = ""
            Valores = ""
            for name in names:
                Datos += "'"+name+"'" + ","
                for item in MsgList:
                    if name.lower() == item[0].lower():
                        Valores += "'"+item[1]+"'" + ","
                        
            Datos = Datos[:-1]
            Valores = Valores[:-1]
            cur.execute(f"INSERT INTO jugadores ({Datos}) VALUES ({Valores})")
            con.commit()
        con.close()
    except Exception as e: await eh.InteractionException(e, interaction)
        
async def GetDataByOwner(owner,interaction, position = 1):
    try:
        con = sqlite.connect("players.db")
        cur = con.cursor()
        admin = GetAdmin()
    
        cursor = con.execute('select * from jugadores')
        names = list(map(lambda x: x[0], cursor.description))
        
        filtro = admin.Ownername + " LIKE '%" + owner + "%' AND " + admin.Fichaname + " LIKE '%" + str(position) +"%'"
        cur.execute(f"SELECT * FROM jugadores WHERE {filtro};")
        data = cur.fetchall()[0]
        enddata = []
        i = 0
        for name in names:
            enddata.append([name, data[i]])
            i += 1
        con.close()
        return enddata
    except Exception as e: await eh.InteractionException(e, interaction)
    
def GetListOfData(owner):
    con = sqlite.connect("players.db")
    cur = con.cursor()
    admin = GetAdmin()

    cursor = con.execute('select * from jugadores')
    
    filtro = admin.Ownername + " LIKE '%" + owner + "%'"
    cur.execute(f"SELECT * FROM jugadores WHERE {filtro};")
    data = cur.fetchall()
    
    con.close()
    return data

async def replaceFromString(string:str):
    con = sqlite.connect("players.db")
    cur = con.cursor()
    
    columnas = re.findall(r'\[([A-Z]+)\]', string)

    for columna in columnas:
        cur.execute(f"SELECT {columna} FROM jugadores")
        valor = cur.fetchone()[0]
        string = string.replace(f"[{columna}]",str(valor).strip()).strip()
    con.close()
    return string.strip()

async def ChangePosition(id):
    con = sqlite.connect("players.db")
    cur = con.cursor()
    
    cur.execute("UPDATE")
    
    con.close()