import pyodbc
import param

class SQL:
    def __init__(self):
        odbc_string = '''DRIVER=''' + param.DRIVER+''';SERVER=''' + param.SERVER + \
                        ''';DATABASE=''' + param.DATABASE + ''';UID=''' + param.UID + ''';PWD=''' + param.PWD + \
                        ''';Trusted_Connection=yes;Encrypt=no;Integrated_Security=no'''
        self.conn = pyodbc.connect(odbc_string)
        self.cursor = self.conn.cursor()
        print("Connection established")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print("Connection closed")

if __name__ == '__main__':
    sql = SQL()
    sql.cursor.execute('insert into test values (1)')
    sql.cursor.commit()
    sql.cursor.execute('select tbl_id from test')
    records = sql.cursor.fetchall()
    for r in records:
        print(r.tbl_id)


