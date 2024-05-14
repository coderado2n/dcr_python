import sqlite3
import json

def fetch_stats():
    connection = sqlite3.connect('../data/countries.db')
    cursor = connection.cursor()


    cursor.execute('''SELECT a.region_id, b.name, COUNT(a.name) AS num_countries, SUM(a.population) AS total_population
                      FROM country a
                      left outer join region b
                      on a.region_id = b.id
                      GROUP BY a.region_id''')
    stats = cursor.fetchall()
    connection.close()
    return stats


def main():
    stats = fetch_stats()
    '''
    Create a list of dictionaries for each region
    '''
    regions_list = [
        {"name": region, "number_countries": num_countries, "total_population": total_population}
        for _, region, num_countries, total_population in stats
    ]
    regions_dict = {"regions": regions_list}
    print(json.dumps(regions_dict, indent=4))


if __name__ == "__main__":
    main()
