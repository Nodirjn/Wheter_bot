import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    def connect(self):
        return pymysql.Connection(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False) :
        database = self.connect()
        cursor = database.cursor()

        cursor.execute(sql, params)
        data = None

        if fetchone:
            data = cursor.fetchone()

        elif fetchall:
            data = cursor.fetchall()

        if commit:
            database.commit()

        return data

    def create_users_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
           id INT AUTO_INCREMENT PRIMARY KEY,
           telegram_id INT NOT NULL UNIQUE, 
           full_name VARCHAR(100) NOT NULL
        
        
        )
    """
        self.execute(sql)

    def create_cities_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            owner INT NOT NULL ,
            name VARCHAR(100) NOT NULL,
            CONSTRAINT owner_and_name_unique UNIQUE(owner, name)
        )
    """
        self.execute(sql)

    def get_user(self, telegram_id):
        sql = """
        SELECT * FROM users WHERE telegram_id = %s
        """
        params = (telegram_id,)
        return self.execute(sql, params)







    def register_user(self, telegram_id, full_name,username):
        sql = """
        INSERT INTO users (telegram_id, full_name, username)
        VALUES (%s, %s, %s)
    """
        params = (telegram_id, full_name, username)
        self.execute(sql, params, commit=True)


    def register_city(self, telegram_id, city_name):
        user = self.get_user(telegram_id)
        user_id = user.get("id")

        sql = """
        INSERT INTO cities (owner, name)
        VALUES (%s, %s)
        
        """
        params = (user_id, city_name)
        self.execute(sql, params, commit=True)