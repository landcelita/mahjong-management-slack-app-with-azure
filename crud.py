import os
from pprint import pprint
from typing import Any, List, Tuple, Union
import pyodbc
from dotenv import load_dotenv

# そのうちサニタイズとかエスケープとかする

load_dotenv()
server = os.environ.get('SQL_SERVER')
database = os.environ.get('SQL_DATABASE')
username = os.environ.get('SQL_USERNAME')
password = '{' + os.environ.get('SQL_PASSWORD') + '}'
driver= '{'+ os.environ.get('SQL_DRIVER') + '}'

def enclose_quot(val):
    if isinstance(val, str):
        return "'" + val + "'"
    elif val is None:
        return "Null"
    else:
        return str(val)

# C
def exec_insert_sql(table: str, vals: List[Any], cols: List[str] = None) -> int :
    # table: テーブル名, vals: 挿入する値, cols: 列の名前, 返り値はinsertした列のID
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()
    vals = vals.copy()

    # 前処理
    for i in range(len(vals)):
        if type(vals[i]) == bool:
            vals[i] = int(vals[i])
        vals[i] = enclose_quot(vals[i])
    
    sql = "INSERT INTO [dbo].[" + table + "]"
    if cols is not None:
        sql += "(" + ", ".join(cols) + ")"
    sql += "\n"
    sql += " VALUES (" + ", ".join(vals) + ")"

    cur.execute(sql)
    conn.commit()

    cur.execute("SELECT @@IDENTITY")
    ret = cur.fetchone()
    cur.close()
    conn.close()
    return ret[0]

# R
def exec_select_sql(table: str, cols: Union[List[str], None] = None, where: Union[str, None] = None) -> List[Tuple]:
    # table: テーブル名, cols: 取得したい行, where: 指定する条件
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()

    sql = "SELECT "
    if cols is None:
        sql += "* "
    else:
        sql += ", ".join(cols)
    sql += " FROM [dbo].[" + table + "]"
    if where is not None:
        sql += " WHERE " + where

    cur.execute(sql)
    ret = cur.fetchall()
    cur.close()
    conn.close()
    return ret

# U
def exec_update_sql(table: str, cols: Union[List[str], str], vals: Union[List[Any], Any], where: Union[str, None]) -> None:
    # table: テーブル名, cols: 更新したい列名, vals: 更新する値, where: 条件節
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()
    vals = vals.copy()

    # 前処理
    if isinstance(vals, List):
        for i in range(len(vals)):
            if type(vals[i]) == bool: vals[i] = int(vals[i])
            vals[i] = enclose_quot(vals[i])
    else:
        if type(vals) == bool: vals = int(vals)
        vals = enclose_quot(vals)
    
    sql = "UPDATE [dbo].[" + table + "]\nSET "
    if isinstance(cols, List):
        sets = []
        for i in range(len(cols)):
            sets.append(cols[i] + ' = ' + vals[i])
        sql += ", ".join(sets)
    else:
        sql += cols + ' = ' + vals
    sql += "\n"
    if where is not None:
        sql += "WHERE " + where

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

# D
def exec_delete_sql(table: str, where: Union[str, None]) -> None:
    # table: テーブル名, where: 条件節
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()

    sql = "DELETE FROM [dbo].[" + table + "]\n"
    if where is not None:
        sql += "WHERE " + where

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def exec_sql(sql: str) -> None:
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

    