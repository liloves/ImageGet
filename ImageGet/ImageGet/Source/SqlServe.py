#-*- coding: UTF-8 -*-
import mysql.connector

class SqlServe:
    
    def __init__ (self):
        config={'host':'127.0.0.1',
                'user':'root',
                'password':'woaini123',
                'port':3306,
                'database':'sakila',
                'charset':'utf8'
                }

        connectState = 0    # 0 for off, 1 for open
    
    def connect(self):
        try:
            self.cnn = mysql.connector.connect(**config)
            connectState = 1
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))

    def execute(self,sql_query):
        cursor=cnn.cursor()
        try:
            cursor.execute(sql_query)
        except mysql.connector.Error as e:
            print('query error!{}'.format(e))
        finally:
            cursor.close()



