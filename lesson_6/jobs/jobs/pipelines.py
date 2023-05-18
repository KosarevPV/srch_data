import sqlite3


class JobsPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('jobs.db')
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
               id INTEGER PRIMARY KEY,
               name TEXT,
               employer TEXT,
               location TEXT,
               min_salary TEXT,
               max_salary TEXT,
               href TEXT);
               """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM jobs WHERE name = (?) AND employer = (?);",
                    (item['name'], item['employer']))
        if not self.cur.fetchone():
            values = (
            None, item['name'], item['employer'], item['location'],
            item['min_salary'], item['max_salary'], item['href'])
            self.cur.execute("INSERT INTO jobs VALUES(?, ?, ?, ?, ?, ?, ?);", values)
            self.conn.commit()
