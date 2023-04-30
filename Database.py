import sqlite3 as sqlite
import os,re
import exceptionHandler as eh
from DataManager import HasSpecialCommand, ClearPattern, GetAdmin

async def Start(mensaje):
    await NewDatabaseByPattern(mensaje)


async def NewDatabaseByPattern(pattern :str):
    if os.path.exists("players.db"):
        os.remove("players.db")
    con = sqlite.connect("players.db")
    cur = con.cursor()
    data = ""
    for linea in pattern.split("\n"):
        if linea.strip().__len__() > 0:
            if not HasSpecialCommand(linea.split(":")[1]):
                data += linea.split(":")[0] + " DEFAULT '',"
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
            Cabeceras = []
            for msg in mensaje.content.split("\n"):
                if not HasSpecialCommand(msg) and msg.__contains__(":"):
                    Cabeceras.append(msg.split(":")[0])
            
            for i in range(0, len(Cabeceras)-1):
                MsgList.append([Cabeceras[i], mensaje.content.split(Cabeceras[i]+":")[1].split(Cabeceras[i+1]+":")[0].strip()])

            MsgList.append([Cabeceras[len(Cabeceras)-1], mensaje.content.split(Cabeceras[len(Cabeceras)-1]+":")[1].strip()])                
            
            Datos = ""
            Valores = ""
            for name in names:
                Datos += "'"+name+"'" + ","
                asignado = False
                
                for item in MsgList:
                    if name.lower() == item[0].lower():
                        Valores += "'"+item[1].strip()+"'" + ","
                        asignado = True
                        break
                    
                if not asignado:
                    Valores += "'NA'," 
                        
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
    
    filtro = admin.Ownername + " LIKE '%" + owner + "%'"
    cur.execute(f"SELECT * FROM jugadores WHERE {filtro};")
    data = cur.fetchall()
    
    con.close()
    return data

async def replaceFromString(string:str, owner, ownername, pos, posname):
    con = sqlite.connect("players.db")
    cur = con.cursor()
    
    columnas = re.findall(r"\[[^\]]*\]", string)
    for columna in columnas:
        try:
            columna = columna.replace("[", "").replace("]", "")
            cur.execute(f"SELECT {columna} FROM jugadores WHERE {ownername} LIKE '%{owner}%' AND {posname} LIKE '%{pos}%'")
            valor = cur.fetchone()[0]
            string = string.replace(f"[{columna}]",str(valor).strip()).strip()
        except: pass
    con.close()
    return string.strip()

async def Update(newval, name, owner, ownername):
    con = sqlite.connect("players.db")
    cur = con.cursor()
    
    cur.execute(f"UPDATE jugadores SET {name} = '{newval}' WHERE {ownername} LIKE '%{owner}%' ")
    con.commit()
    
    con.close()