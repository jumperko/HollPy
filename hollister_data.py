from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import sqlite3
from hollister_item import HollisterItem


agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329"
language = "sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6"


class HollisterData:
    def __init__(self):
        self.url = 'https://www.hollisterco.com/shop/eu/guys-multipacks?filtered=true&rows=240&start=0&facet=ads_f43002_ntk_cs:("L"%20"XL")'
        self.headers = {
            "User-agent": agent,
            "Accept-Language": language,
        }
        self.loaded_items = []
        self.db_name = "hollister.db"
        self.get_data()

    def get_data(self):
        web_data = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(web_data.text, "html.parser")
        soup_second = soup.find("div", id="primary-content")

        soup_final = soup_second.find_all("div", class_="product-content")

        for item in soup_final:
            item: BeautifulSoup
            try:
                price = item.find("span", class_="product-price-text").text.strip()
                name = item.find("a", class_="product-card__name").text.strip()
                link = item.find("a", class_="product-card__name")["href"]
                id = link.split("?")[0]
                product_id = id.split("-")[-1]

                new_item = HollisterItem()
                new_item.id = int(product_id)
                new_item.name = name
                new_item.url = f'https://www.hollisterco.com{link}'
                new_item.price = float(price.lstrip("€").strip())
                self.loaded_items.append(new_item)
            except:
                print("Unknown error")

    def save_data_to_json(self, file_name="hollister_data.json"):
        data = {
            "last_update": datetime.now().strftime("%d/%m/%y - %H:%M:%S"),
            "hollister": {},
        }
        if self.loaded_items:
            for item in self.loaded_items:
                item: HollisterItem
                if item.id not in data["hollister"]:
                    data["hollister"][item.id] = {
                        'name': item.name,
                        'price': item.price,
                        'url': item.url
                    }
            with open(file_name, 'w') as outfile:
                json.dump(data, outfile, indent=2)
        else:
            print("items not found")

    def export_data_to_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='hollister_items' ''')
        date = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
        if c.fetchone()[0] == 1:
            print('Table exists.')
            if self.loaded_items:
                for item in self.loaded_items:
                    c.execute("INSERT INTO hollister_items (id,date,name,price,url) VALUES (?,?,?,?,?)",
                              (item.id, date, item.name, item.price, item.url))
        else:
            print('Table does not exist.')
            c.execute("""CREATE TABLE hollister_items (
                        id integer,
                        date text,
                        name text,
                        price real,
                        url text)""")
        conn.commit()
        conn.close()

    def find_in_db(self, string):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        t = (f"%{string}%",)
        c.execute('SELECT * FROM hollister_items WHERE name LIKE ?', t)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result

    def find_by_id(self, item_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        t = (f"{item_id}",)
        c.execute('SELECT * FROM hollister_items WHERE id= ?', t)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result
