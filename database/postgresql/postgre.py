from psycopg2 import pool

HOST = ""
DATABASE = ""
USER = ""
PASSWORD = ""

class Postgre:
    db_pool = pool.SimpleConnectionPool(1,10,HOST,DATABASE,USER,PASSWORD)
    def __init__(self, table, schema = "public", params = None):
        self.schema = schema
        self.table = table
        self.params = params
    
    def query(self, sql, params=None):
        conn = self.db_pool.getconn()
        cur = conn.cursor()
        cur.execute(sql, params or ())
        result = cur.fetchall()
        cur.close()
        self.db_pool.putconn(conn)
        return result
    
    def find(self,params,values):
        params_str = ', '.join(params)
        sql = f"SELECT * FROM {self.table} WHERE {params_str} = %s"
        return self.query(sql, values)
    
    def find_by_id(self,id):
        sql = f"SELECT * FROM {self.table} WHERE id = %s"
        return self.query(sql, (id,))

    def insert(self, values, params = None):
        if params is None:
            if self.params is None:
                raise ValueError("Os parâmetros devem ser especificados.")
            else:
                params = self.params
        placeholders = ', '.join(['%s'] * len(values))
        params_str = ', '.join(params)
        sql = f"INSERT INTO {self.table} ({params_str}) VALUES ({placeholders})"
        conn = self.db_pool.getconn()
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        self.db_pool.putconn(conn)

    def insert_multiple(self, values_list, params = None):
        if params is None:
            if self.params is None:
                raise ValueError("Os parâmetros devem ser especificados.")
            else:
                params = self.params
        placeholders = ', '.join(['%s'] * len(params))
        params_str = ', '.join(params)
        sql = f"INSERT INTO {self.table} ({params_str}) VALUES ({placeholders})"
        conn = self.db_pool.getconn()
        cur = conn.cursor()
        for values in values_list:
            cur.execute(sql, values)
        conn.commit()
        cur.close()
        self.db_pool.putconn(conn)

    def list(self, column, filter = None):
        if filter is None:
            sql = f"SELECT id, {column} FROM {self.table}"
        else:
            sql = f"SELECT id, {column} FROM {self.table} WHERE {filter}"
        rows = self.query(sql)
        list_str = "\n".join([f"{i+1} - {row[1]}" for i, row in enumerate(rows)])
        id_dict = {i+1: row[0] for i, row in enumerate(rows)}
        return list_str, id_dict

users = Postgre(table='users', params=('nome'))
projeto = Postgre(table='projetos',params=('nome','numero','ativo'))
followup = Postgre(table='followups',params=('colaborador_id','projeto_id','nome'))