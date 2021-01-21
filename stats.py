import sqlite3


class Stats:
    def __init__(self):
        self.name_db = "hollister.db"
        self.original_table = "hollister_items"
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
            conn.close()
            return True
        else:
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

    def db_stat_item(self, item_id):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        t = (f"{item_id}",)
        result = ""
        if self.check_if_table_exist(self.stats_table):
            c.execute(f'SELECT * FROM {self.stats_table} WHERE id=?', t)
            result = c.fetchone()
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

    def update_item_in_stats(self, id, what="actual_price", new_value=0.0):
        conn = sqlite3.connect(self.name_db)
        c = conn.cursor()
        c.execute(f"UPDATE {self.stats_table} SET {what} = {new_value} WHERE id = {id} ")
        print(f"update complete {id}")
        conn.commit()
        conn.close()

    def generate_stat(self):
        full_data = self.all_data_from_table(self.original_table)
        for item in full_data:
            item_id = item[0]
            item_in_stat_db = self.db_stat_item(item[0])
            if item_in_stat_db:
                item_price = float(item[3])
                stat_actual_price = float(item_in_stat_db[2])
                stat_min_price = float(item_in_stat_db[3])
                stat_max_price = float(item_in_stat_db[4])
                if item_price < stat_actual_price:
                    self.update_item_in_stats(id=item_id, what="actual_price", new_value=item_price)
                    if item_price < stat_min_price:
                        self.update_item_in_stats(id=item_id, what="min_price", new_value=item_price)
                elif item_price > stat_actual_price:
                    self.update_item_in_stats(id=item_id, what="actual_price", new_value=item_price)
                    if item_price > stat_max_price:
                        self.update_item_in_stats(id=item_id, what="max_price", new_value=item_price)
                else:
                    print("Cena bez zmeny.")
                    pass

                pass
            else:
                #Item neexistuje vytaram novy zaznam
                self.insert_stats_item(id=item[0], name=item[2], actual=item[3], min=item[3], max=item[3], url=item[4])
                print(f"vytváram zaznam pre {item[0]}")
