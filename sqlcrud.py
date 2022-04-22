import os
from typing import List
import pyodbc
from dotenv import load_dotenv

# そのうちサニタイズとかエスケープとかする

load_dotenv()
server = os.environ.get('SQL_SERVER')
database = os.environ.get('SQL_DATABASE')
username = os.environ.get('SQL_USERNAME')
password = '{' + os.environ.get('SQL_PASSWORD') + '}'
driver= '{'+ os.environ.get('SQL_DRIVER') + '}'

def exec_insert_sql(table, vals, cols=None):
    # table: テーブル名, vals: 挿入する値(List), cols: 列の名前(List)
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()
    sql = "INSERT INTO [dbo].[" + table + "]"
    if cols is not None:
        sql += "(" + ", ".join(cols) + ")"

    sql += "\n"

    for i in range(len(vals)):
        if isinstance(vals[i], str):
            vals[i] = "'" + vals[i] + "'"
        else:
            vals[i] = str(vals[i])
    sql += " VALUES (" + ", ".join(vals) + ")"

    cur.execute(sql)
    conn.commit()
    
    cur.close()
    conn.close()

def exec_sql(sql):
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

    