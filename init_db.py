# -*- coding: utf-8 -*-
import sqlite3

def init_database():
    conn = sqlite3.connect('mna_watch.db')
    c = conn.cursor()
    
    # M&A events table (už máš)
    c.execute('''
    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      dt TEXT,
      source TEXT,
      acquirer TEXT,
      target TEXT,
      url TEXT UNIQUE,
      snippet TEXT,
      amount REAL,
      currency TEXT,
      confidence REAL
    )''')
    
    # IPO tracking table (NOVÉ - pre duplikáty)
    c.execute('''
    CREATE TABLE IF NOT EXISTS ipo_alerts_sent (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticker TEXT NOT NULL,
      company_name TEXT,
      price REAL,
      market_cap REAL,
      sent_date TEXT DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(ticker, sent_date)
    )''')
    
    # Indexy
    c.execute('CREATE INDEX IF NOT EXISTS ix_events_dt ON events(dt);')
    c.execute('CREATE INDEX IF NOT EXISTS ix_ipo_ticker ON ipo_alerts_sent(ticker);')
    c.execute('CREATE INDEX IF NOT EXISTS ix_ipo_date ON ipo_alerts_sent(sent_date);')
    
    conn.commit()
    conn.close()
    print("DB initialized: mna_watch.db")

if __name__ == "__main__":
    init_database()
