import sqlite3
import json
import requests
import logging


class LoadData:
    DATA_URL = "https://storage.googleapis.com/dcr-django-test/countries.json"
    DB_PATH = "../data/countries.db" 
    LOG_FILE = "schema_update.log"  

    def __init__(self):
        logging.basicConfig(filename=self.LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')
        self.connection = sqlite3.connect(self.DB_PATH)
        self.update_schema()
        self.regions = {}

    def update_schema(self):
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA table_info(country)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "topLevelDomain" not in columns:
            sql_command = "ALTER TABLE country ADD COLUMN topLevelDomain TEXT"
            cursor.execute(sql_command)
            logging.info(f"Executed SQL: {sql_command}") 

        if "capital" not in columns:
            sql_command = "ALTER TABLE country ADD COLUMN capital TEXT"
            cursor.execute(sql_command)
            logging.info(f"Executed SQL: {sql_command}") 

        self.connection.commit()

    def get_raw_data(self):
        response = requests.get(self.DATA_URL)
        response.raise_for_status()
        return response.json()

    def get_region_id(self, region_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM region WHERE name = ?", (region_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        cursor.execute("INSERT INTO region (name) VALUES (?)", (region_name,))
        return cursor.lastrowid

    def add_country(self, data):
        region_name = data.get("region", "Unknown")
        region_id = self.get_region_id(region_name)
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM country WHERE name = ?", (data["name"],))
        if cursor.fetchone():
            return
        cursor.execute("""INSERT INTO country (name, alpha2Code, alpha3Code, population, region_id, topLevelDomain, capital)
                          VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (data["name"], data["alpha2Code"], data["alpha3Code"],
                        data["population"], region_id, data.get("topLevelDomain", [""])[0], data.get("capital", "")))
        self.connection.commit()

    def run(self):
        data = self.get_raw_data()
        for row in data:
            self.add_country(row)

    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    LoadData().run()
