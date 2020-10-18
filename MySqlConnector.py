import mysql.connector
import os
from mysql.connector import (connection)
from mysql.connector import errorcode

#Returns a connection object, which is used to connect and interact with Database
def mysqlConnection():
    #Connecting to the mysql server hosted in localhost (current server)
    cnx = mysql.connector.connect(user='root',
                                 database='warehouse',
                                 host='localhost',
                                 port='3306')
    return cnx;

#Executes a SQL query in Database,
def mysqlExecutor(sqlQuery, vals=None):
    mySqlConnector = mysqlConnection()
    cursor = mySqlConnector.cursor()

    if vals is None:
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
    else:
        cursor.execute(sqlQuery, vals)
        mySqlConnector.commit()
        records = cursor.rowcount

    mySqlConnector.close()
    return records;
