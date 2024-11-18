import sqlite3

class BancoDados():

    def conecta_db(self):
        self.conn = sqlite3.connect("gov_app.db")
        print("Conexão estabelecida com o banco de dados")
        self.cursor = self.conn.cursor()

    def desconecta_db(self):
        print("Conexão encerrada com o banco de dados")
        self.conn.close()

    def monta_tabelas(self):
        self.conecta_db()

        self.comando_tabela_user = """CREATE TABLE IF NOT EXISTS 
            users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                fingerprint TEXT,
                role INTEGER
            )"""
        
        self.cursor.execute(self.comando_tabela_user)
        self.conn.commit()

        self.comando_tabela_propriedades = """CREATE TABLE IF NOT EXISTS 
            propriedades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                info TEXT,
                acl INTEGER
            )"""  
        self.cursor.execute(self.comando_tabela_propriedades)
        self.conn.commit()

        self.desconecta_db()
    
    def inserir_user(self, username, password, role, hash):
        self.conecta_db()
        self.cursor.execute("""SELECT username FROM users WHERE username = ?; """, [username])
        acesso = self.cursor.fetchone()
        if not acesso:
            self.cursor.execute("""INSERT INTO users (username, password, fingerprint, role) VALUES (?,?,?,?)""", (username, password, hash, role))
            print(f'INSERIDO USER {username}')
            self.conn.commit()
            self.desconecta_db()
        else:
            inserido = True
            return inserido
    
    def select_lista(self, acl):
        self.conecta_db()
        lista_dados = self.cursor.execute("""SELECT id, name, info FROM propriedades WHERE acl <= ? ORDER BY name ASC; """, [acl])
        return lista_dados
    
    def pesquisar_lista(self, name, acl):
        self.conecta_db()
        name = name + '%'
        lista_dados = self.cursor.execute("""SELECT id, name, info FROM propriedades WHERE name LIKE ? AND acl <= ?; """, [name, acl])
        return lista_dados
    
    def altenticar_user(self, username, password):
        self.conecta_db()
        self.cursor.execute("""SELECT username, role FROM users WHERE username = ? AND password = ?; """, [username, password])
        user = self.cursor.fetchone()

        if user:
            acesso = True
            name = user[0]
            role = user[1]
        else:
            acesso = False
            name = None
            role = None
        return acesso, name, role
    
    def altenticar_user_fingerprint(self, hash):
        self.conecta_db()
        self.cursor.execute("""SELECT username, role FROM users WHERE fingerprint = ?; """, [hash])
        user = self.cursor.fetchone()

        if user:
            acesso = True
            name = user[0]
            role = user[1]
        else:
            acesso = False
            name = None
            role = None
        
        print(acesso, name, role)
        return acesso, name, role
    
    def inserir_propriedade(self, name, info, acl):
        self.conecta_db()
        self.cursor.execute("""INSERT INTO propriedades (name, info, acl) VALUES (?,?,?)""", (name, info, acl))
        print(f'INSERIDO Propriedade {name}')
        self.conn.commit()
        self.desconecta_db()

    def deletar_propriedade(self, name):
        self.conecta_db()
        self.cursor.execute("""DELETE FROM propriedades WHERE name = ?""", [name])
        print(f'DELETADO a  Propriedade {name}')
        self.conn.commit()
        self.desconecta_db()
