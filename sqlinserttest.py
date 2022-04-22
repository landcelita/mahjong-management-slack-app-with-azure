import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = os.environ.get('SQL_SERVER')
database = os.environ.get('SQL_DATABASE')
username = os.environ.get('SQL_USERNAME')
password = '{' + os.environ.get('SQL_PASSWORD') + '}'
driver= '{'+ os.environ.get('SQL_DRIVER') + '}'

conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
        ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

sql = """
INSERT INTO [dbo].[Participants]
    VALUES ('test1', 'test2', 'test3', 'test4') 
"""

cursor.execute(sql)
conn.commit()

cursor.close()
conn.close()

