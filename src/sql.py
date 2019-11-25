# Prithu Pareek - Created 11/19/19
# SQL Connect Class

import pymysql
import pymysql.cursors

class SQLConnection(object):
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host, user, password, db,
                                          charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    def login(self, username, password):

        with self.connection.cursor() as cursor:

            # get the record based on username and password
            sql = f"SELECT * FROM `user_info` WHERE `user_name`='{username}' AND `user_password`='{password}'"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def createAccount(self, username, password, name, acctType):
        with self.connection.cursor() as cursor:

            # Create a new record
            sql = f"INSERT INTO `user_info`(`user_name`, `user_password`, `user_firstName`, `user_typ`) VALUES ('{username}','{password}','{name}','{acctType}')"
            cursor.execute(sql)

            sql = "SELECT * FROM `user_info` ORDER BY `user_id` DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            # print(result)

        self.connection.commit()

        return result

    def findUserByUsername(self, username):
        with self.connection.cursor() as cursor:

            sql = f"SELECT * FROM `user_info` WHERE `user_name`='{username}'"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def updateAccountBalance(self, userid):
        with self.connection.cursor() as cursor:

            sql = f'SELECT `user_balance` FROM `user_info` WHERE `user_id` = {userid}'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def modifyAccountBalance(self, userid, amount):
        with self.connection.cursor() as cursor:

            sql = f"UPDATE `user_info` SET `user_balance` = '{amount}' WHERE `user_info`.`user_id` = {userid};"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def modifyAccount(self, userid, username, password, firstName):
        with self.connection.cursor() as cursor:

            sql = f"UPDATE `user_info` SET `user_name` = '{username}', `user_password` = '{password}', `user_firstName` = '{firstName}' WHERE `user_info`.`user_id` = {userid}"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def getImage(self, userid):
        with self.connection.cursor() as cursor:

            sql = f'SELECT `user_face` FROM `user_info` WHERE `user_id` = {userid};'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def updateFaceImage(self, userid, image):
        with self.connection.cursor() as cursor:

            sql = f'UPDATE `user_info` SET `user_face` = "{image}" WHERE `user_info`.`user_id` = {userid}'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def updateFaceEncoding(self, userid, encoding):
        with self.connection.cursor() as cursor:

            sql = f"""UPDATE `user_info` SET `user_face_encoding` = '{encoding}' WHERE `user_info`.`user_id` = {userid};"""
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def createMerchantInventoryTable(self, userid):
        with self.connection.cursor() as cursor:

            sql = f"""
                    CREATE TABLE M_{userid}_Inventory(
                        item_id INT(100) AUTO_INCREMENT PRIMARY KEY,
                        item_name VARCHAR(100),
                        item_price DECIMAL(10, 2)
                    );
                   """
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def setInventoryReference(self, userid):
        with self.connection.cursor() as cursor:

            sql = f'UPDATE `user_info` SET `user_inventory` = "M_{userid}_Inventory" WHERE `user_info`.`user_id` = {userid}'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def getInventoryData(self, tableName):
        with self.connection.cursor() as cursor:

            sql = f'SELECT * FROM `{tableName}`;'
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def getFaceEncodings(self):
        with self.connection.cursor() as cursor:

            sql = f"SELECT `user_id`, `user_face_encoding` FROM `user_info` WHERE `user_typ`='C'"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def transferMoney(self, senderId, recpId, amount):
        with self.connection.cursor() as cursor:

            sub = f"UPDATE `user_info` SET `user_balance` = (SELECT `user_balance` WHERE `user_id`={senderId}) - {amount} WHERE `user_id` = {senderId};"
            cursor.execute(sub)
            add = f"UPDATE `user_info` SET `user_balance` = (SELECT `user_balance` WHERE `user_id`={recpId}) + {amount} WHERE `user_id` = {recpId};"
            cursor.execute(add)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def closeConn(self):
        self.connection.close()