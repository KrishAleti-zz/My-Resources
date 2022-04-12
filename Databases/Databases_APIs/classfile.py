import mysql.connector as connection
class sql():
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.mydb = connection.connect(host=self.host, user=self.user, passwd=self.password, use_pure=True)
        self.cur = self.mydb.cursor()

    def db_connection(self, dbname):
        self.dbname = dbname
        query = f"Create database {self.dbname}"
        self.cur.execute(query)
        print(f"Database '{self.dbname}' is created")
