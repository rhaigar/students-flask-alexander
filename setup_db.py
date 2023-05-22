import sqlite3
def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur=conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


