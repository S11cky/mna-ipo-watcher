# -*- coding: utf-8 -*-
import logging
import os
import requests
import time
from data_sources import fetch_company_snapshot
from ipo_alerts import build_ipo_alert
from db_utils import already_sent_recently, mark_as_sent
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Parametre pre Small Cap a cena akcie ≤ 50 USD
MAX_PRICE = 50
MIN_MARKET_CAP = 5e8

# Vybrané sektory pre filtrovanie IPO spoločností
SECTORS = ["Technológie", "Biotechnológia", "AI", "Zelené technológie", "FinTech", "E-commerce", "HealthTech", "SpaceTech", "Autonómne vozidlá", "Cybersecurity", "Agritech", "EdTech", "RetailTech"]

# Nastavenie logovania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Zoznam investorov
VC_FUNDS = ['Vanguard Group Inc.', 'Sequoia Capital', 'Andreessen Horowitz', 'Benchmark', 'Greylock Partners', 'Insight Partners']
TOP_COMPANIES = ['Apple', 'Microsoft', 'Google', 'Amazon', 'Facebook', 'Berkshire Hathaway']
TOP_BILLIONAIRES = ['Elon Musk', 'Jeff Bezos', 'Bill Gates', 'Warren Buffett', 'Mark Zuckerberg']
ALL_INVESTORS = VC_FUNDS + TOP_COMPANIES + TOP_BILLIONAIRES

def send_telegram(message: str) -> bool:
    """Send message to Telegram"""
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    if not token or not chat_id:
        logging.error("Chybajuce Telegram credentials!")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)  # Zvýšený timeout na 10s
        if response.status_code == 200:
            logging.info(f"Sprava uspesne odoslana: {message[:50]}...")
            return True
        else:
            logging.error(f"Chyba pri odosielani spravy: {response.status_code}")
            logging.error(f"Odpoved: {response.json()}")
            return False
    except Exception as e:
        logging.error(f"Chyba pri odosielani Telegram spravy: {e}")
        return False

def fetch_ipo_data(ticker: str) -> Dict[str, Any]:
    """Fetch IPO data for a single ticker"""
    try:
        logging.info(f"Získavam údaje pre {ticker}...")
        snap = fetch_company_snapshot(ticker)
        if snap:
            price = snap.get("price_usd")
            market_cap = snap.get("market_cap_usd")
            sector = snap.get("sector", "")
            if price is not None and market_cap is not None:
                if price <= MAX_PRICE and market_cap >= MIN_MARKET_CAP:
                    if any(sector in sector_name for sector_name in SECTORS):
                        return snap
                    else:
                        logging.warning(f"Ignorovane IPO {ticker} – sektor mimo poziadaviek.")
                else:
                    logging.warning(f"Ignorovane IPO {ticker} – cena alebo market cap je mimo kriterii.")
            else:
                logging.warning(f"Neuplne data pre {ticker}, ignorovane.")
        else:
            logging.warning(f"Neboli ziskane data pre {ticker}")
    except Exception as e:
        logging.error(f"Chyba pri spracovani {ticker}: {e}")
    return None

def fetch_and_filter_ipo_data(tickers: List[str]) -> List[Dict[str, Any]]:
    """Fetch IPO data for multiple tickers using multithreading"""
    ipo_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Znížený počet workerov na 10
        futures = {executor.submit(fetch_ipo_data, ticker): ticker for ticker in tickers}
        for future in as_completed(futures):
            ipo = future.result()
            if ipo:
                ipo_data.append(ipo)

    logging.info(f"Celkovy pocet filtrovanych IPO: {len(ipo_data)}")
    return ipo_data

def send_alerts():
    tickers = ["GTLB", "ABNB", "PLTR", "SNOW", "DDOG", "U", "NET", "ASAN", "PATH"]
    
    logging.info(f"Zacinam monitorovat {len(tickers)} IPO spolocnosti...")
    
    # Načítanie údajov o spoločnostiach a filtrovanie
    ipo_data = fetch_and_filter_ipo_data(tickers)
    
    # Poslanie alertov len pre filtrované IPO
    alert_count = 0
    for ipo in ipo_data:
        try:
            # KONTROLA DUPLIKÁTOV - či už nebolo odoslané v posledných 24h
            if already_sent_recently(ipo['ticker']):
                logging.info(f"Preskakujem {ipo['ticker']} - uz bolo odoslane v poslednych 24h")
                continue
            
            ipo_msg = build_ipo_alert(ipo)
            success = send_telegram(ipo_msg)
            
            if success:
                logging.info(f"Alert pre {ipo['ticker']} uspesne odoslany.")
                mark_as_sent(ipo)
                alert_count += 1
            else:
                logging.error(f"Chyba pri odosielani alertu pre {ipo['ticker']}")
                
        except Exception as e:
            logging.error(f"Chyba pri vytvarani alertu pre {ipo['ticker']}: {e}")
    
    logging.info(f"Proces dokonceny. Odoslanych alertov: {alert_count}")

# ZMENENÉ: Jednorazové spustenie namiesto nekonečnej slučky
if __name__ == "__main__":
    logging.info("Skript sa spustil.")
    
    start_time = time.time()
    send_alerts()
    end_time = time.time()
    
    duration = end_time - start_time
    logging.info(f"Skript ukonceny. Celkovy cas: {duration:.2f} sekund")
