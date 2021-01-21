import sqlite3


class Stats:
    def __init__(self):
        self.name_db = "hollister.db"
        self.original_talbe = "hollister_items"
        self.stats_table = "hollister_stats"

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
            c.execute(f'SELECT * FROM {self.stats_table} WHERE id= ?', t)
            result = c.fetchone()
            print(result)
        conn.commit()
        conn.close()
        return result

    def generate_stat(self):
        full_data = self.all_data_from_table(self.original_talbe)
        for item in full_data:
            self.db_item(item[0])



#"UPDATE Table SET Age = 18 WHERE Age = 17"




###########TEST ENV#############
tes_env = Stats()
tes_env.generate_stat()
# tes_env.db_item(42556823)