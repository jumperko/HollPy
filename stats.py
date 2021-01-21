import sqlite3


class Stats:
    def __init__(self):
        self.name_db = "hollister.db"
        self.original_talbe = "hollister_items"
        self.stats_table = "hollister_stats"

    def create_table_for_stats(self):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        c.execute(f"""CREATE TABLE {self.stats_table} (
                    id integer,
                    name text,
                    actual_price real,
                    min_price real,
                    max_price real,
                    url text)""")
        conn.commit()
        conn.close()

    def check_if_table_exist(self, table_name):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        t = table_name
        c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ", (t,))
        if c.fetchone()[0] == 1:
            print("Table exists")
            conn.close()
            return True
        else:
            print("Table does not exist.")
            conn.close()
            return False

    def all_data_from_table(self, table_name):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        t = table_name
        c.execute(f" SELECT * FROM {t} ")
        result = c.fetchall()
        conn.close()
        return result

    def db_item(self, item_id):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        t = (f"{item_id}",)
        result = ""
        if self.check_if_table_exist(self.stats_table):
            c.execute(f'SELECT * FROM {self.stats_table} WHERE id=?', t)
            result = c.fetchone()
            print(result)
        else:
            self.create_table_for_stats()
        conn.commit()
        conn.close()
        return result

    def insert_stats_item(self, id, name, actual, min, max, url):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        d = (id, name, actual, min, max, url)
        c.execute(f"INSERT INTO {self.stats_table} (id,name,actual_price,min_price,max_price,url) VALUES (?,?,?,?,?,?)", d)
        conn.commit()
        conn.close()

    def generate_stat(self):
        full_data = self.all_data_from_table(self.original_talbe)
        for item in full_data:
            if self.db_item(item[0]):
                #Item existuje v stats tabulke upravujem
                pass
            else:
                #Item neexistuje vytaram novy zaznam
                self.insert_stats_item(id=item[0],name=item[0],actual=item[0],min=item[0],max=item[0])
                pass



#"UPDATE table SET Age = 18 WHERE Age = 17"


# f"""CREATE TABLE {self.stats_table} (
#                     id integer,
#                     name text,
#                     actual_price real,
#                     min_price real,
#                     max_price real,
#                     url text)""")

###########TEST ENV#############
tes_env = Stats()
# tes_env.create_table_for_stats()
# tes_env.generate_stat()
tes_env.insert_stats_item()
# tes_env.db_item(42556823)