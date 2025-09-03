# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta

def already_sent_recently(ticker: str, hours: int = 24) -> bool:
    """
    Skontroluje, či už bolo IPO pre daný ticker odoslané v posledných X hodinách
    """
    conn = sqlite3.connect('mna_watch.db')
    c = conn.cursor()
    
    cutoff_time = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute('''
    SELECT COUNT(*) FROM ipo_alerts_sent 
    WHERE ticker = ? AND sent_date > ?
    ''', (ticker, cutoff_time))
    
    count = c.fetchone()[0]
    conn.close()
    
    return count > 0

def mark_as_sent(ipo_data: dict):
    """
    Označí IPO ako odoslané v databáze
    """
    conn = sqlite3.connect('mna_watch.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT INTO ipo_alerts_sent (ticker, company_name, price, market_cap)
    VALUES (?, ?, ?, ?)
    ''', (
        ipo_data['ticker'],
        ipo_data['company_name'],
        ipo_data['price_usd'],
        ipo_data['market_cap_usd']
    ))
    
    conn.commit()
    conn.close()
