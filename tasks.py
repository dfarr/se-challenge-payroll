
import pandas
import sqlite3
import calendar
import datetime


###################################################################################################
## Task
##
## This is a generic task framework that allows a instances of the Task class to be composed
## together into workflows. Each workflow contains an execution context that will be executed
## recursively when the execute method is called. The output of each task is used as the input for
## the subsequent task. Very loosely based on the Luigi framework.
###################################################################################################

class Task:

    def __init__(self, args):
        self.args = args

    def run(self, args):
        pass

    def execute(self):

        args = ''

        if isinstance(self.args, Task):
            args = self.args.execute()
        else:
            args = self.args

        return self.run(args)


###################################################################################################
## Tasks
##
## The following tasks are specific to our payroll problem domain. Follows the extract, transform,
## load pattern common in data warehousing.
###################################################################################################

class Extract(Task):
    def run(self, name):
        with open(name) as file:
            df = pandas.read_csv(file)
            return (df.values[-1][1], df[:-1])

class Transform(Task):
    def run(self, data):

        id, df = data

        df['date'] = pandas.to_datetime(df['date'], format='%d/%m/%Y')

        df['date min'] = df['date'].map(lambda d: datetime.datetime(d.year, d.month, 1, 0, 0) if d.day < 15 else datetime.datetime(d.year, d.month, 15, 0, 0))
        df['date max'] = df['date'].map(lambda d: datetime.datetime(d.year, d.month, 15, 0, 0) if d.day < 15 else datetime.datetime(d.year, d.month, calendar.monthrange(d.year, d.month)[1], 0, 0))

        df['rate'] = df.apply(lambda f: 20 if f['job group'] == 'A' else 30 , axis=1)
        df['amount'] = df['hours worked'] * df['rate']

        df = df.groupby(['employee id', 'date min', 'date max']).agg({'amount': 'sum'}).reset_index()

        return (id, df)

class Load(Task):
    def run(self, data):

        id, df = data

        payments = [ (id, r['employee id'], r['date min'].strftime('%d/%m/%Y') + ' - ' + r['date max'].strftime('%d/%m/%Y'), r['amount']) for i, r in df.iterrows() ]

        try:

            conn = sqlite3.connect('db.db')

            c = conn.cursor()

            c.execute('CREATE TABLE IF NOT EXISTS report (report_id INTEGER, employee_id INTEGER, period TEXT, amount REAL, UNIQUE(report_id, employee_id, period))')

            c.executemany('INSERT INTO report VALUES (?, ?, ?, ?)', payments)

            conn.commit()

            conn.close()

        except sqlite3.IntegrityError:
            return ('Integrity Error', False)

        except:
            return ('Unknown Error', False)

        return ('Ok', True)

