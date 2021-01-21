import sqlite3


class Stats:
    def __init__(self):
        self.name_db = "hollister.db"
        self.original_talbe = "hollister_items"
        self.stats_table = "hollister_stats"

    def table_exist(self):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        t = ("hollister_items",)
        c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ", t)
        if c.fetchone()[0] == 1:
            print("Table exists")
            conn.close()
            return True
        else:
            print("Table does not exist.")
            conn.close()
            return False




tes_env = Stats()
tes_env.table_exist()