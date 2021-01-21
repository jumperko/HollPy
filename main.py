from hollister_data import HollisterData

hollister = HollisterData()
# hollister.save_data_to_json()
# hollister.export_data_to_db()
lookup = hollister.find_by_id("39915320")
for item in lookup:
    print(f"{item[0]}")
