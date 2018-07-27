
import pandas
import sqlite3
import calendar


###################################################################################################
## Task
###################################################################################################

class Task:

    def __init__(self, args):
        self.args = args

    def run(self, args):
        pass

    def execute(self):

        args = ""

        if isinstance(self.args, Task):
            args = self.args.execute()
        else:
            args = self.args

        return self.run(args)


###################################################################################################
## Tasks
###################################################################################################

class Extract(Task):
    def run(self, name):
        with open(name) as file:
            df = pandas.read_csv(file)
            return (df.values[-1][1], df[:-1])

class Transform(Task):
    def run(self, data):

        id, df = data

        df["date min"] = df["date"]
        df["date max"] = df["date"]

        df["rate"] = df.apply(lambda f: 20 if f["job group"] == "A" else 30 , axis=1)
        df["amount"] = df["hours worked"] * df["rate"]

        df = df.groupby(["employee id"]).agg({"amount": "sum", "date min": "min", "date max": "max"}).reset_index()

        return (id, df)

class Load(Task):
    def run(self, data):

        id, df = data

        payments = [ (id, r["employee id"], r["date min"], r["date max"], r["amount"]) for i, r in df.iterrows() ]

        try:

            conn = sqlite3.connect("db.db")

            c = conn.cursor()

            c.execute("CREATE TABLE IF NOT EXISTS report (report_id INTEGER, employee_id INTEGER, min_date TEXT, max_date TEXT, amount REAL, UNIQUE(report_id, employee_id))")

            c.executemany("INSERT INTO report VALUES (?, ?, ?, ?, ?)", payments)

            conn.commit()

            conn.close()

        except sqlite3.IntegrityError:
            return (False, 'Integrity Error')

        except:
            return (False, 'Unknown Error')

        return (True, '')

