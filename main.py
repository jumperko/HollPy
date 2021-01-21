from hollister_data import HollisterData
from stats import Stats

hollister = HollisterData()
# hollister.save_data_to_json()
# hollister.export_data_to_db()

stat_table = Stats()
# stat_table.generate_stat()
print(stat_table.items_stats)

#
# lookup = hollister.find_by_id("43902319")
# for item in lookup:
#     print(f"iD:{item[0]}, Price: {item[3]}, date: {item[1]}, url: {item[4]}")
#
# price_compare = [price[3] for price in lookup]
# print(price_compare)
# av_price = sum(price_compare) / len(price_compare)
# print(av_price)