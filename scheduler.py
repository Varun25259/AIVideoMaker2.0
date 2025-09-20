import sqlite3, pathlib, datetime
DB = pathlib.Path(__file__).parent.parent / 'aivm_upgraded.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS scheduled(
                    id INTEGER PRIMARY KEY,
                    topic TEXT,
                    lang TEXT,
                    times_per_day INTEGER,
                    last_run TIMESTAMP,
                    status TEXT
                )""")
    conn.commit(); conn.close()

init_db()

def schedule_topic_for_all_channels(topic, lang, times_per_day):
    conn = sqlite3.connect(DB); c=conn.cursor()
    c.execute('INSERT INTO scheduled(topic,lang,times_per_day,status) VALUES (?,?,?,?)', (topic,lang,times_per_day,'queued'))
    conn.commit(); conn.close()
    return True
