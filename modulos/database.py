import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def connect_to_database():
    cnx = mysql.connector.connect(
        host= os.environ['MYSQL_HOST'],
        user= os.environ['MYSQL_USER'],
        password= os.environ['MYSQL_PASSWORD'],
        database= os.environ['MYSQL_DATABASE']
    )

    cursor = cnx.cursor()
    return cnx, cursor