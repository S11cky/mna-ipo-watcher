# -*- coding: utf-8 -*-
def build_ipo_alert(ipo: dict) -> str:
    """Vytvorenie textu alertu pre Telegram na zaklade IPO dat so strategickym pohladom"""
    
    # Získanie dát z IPO dictu
    company = ipo["company_name"]
    ticker = ipo["ticker"]
    price = ipo["price_usd"]
    market_cap = ipo["market_cap_usd"]
    free_float = ipo.get("free_float_pct", 0)
    insiders_total_pct = ipo.get("insiders_total_pct", 0)
    ipo_date = ipo.get("ipo_first_trade_date", "Neznamy")
    days_to_lockup = ipo.get("days_to_lockup", "Neznamy")
    
    # Zaokruhlenie hodnôt na rozumny pocet desatinných miest
    price = round(price, 2)
    market_cap = round(market_cap / 1e9, 2)  # Trhova kapitalizacia v miliardach USD
    free_float = round(free_float, 2)
    insiders_total_pct = round(insiders_total_pct, 2)
    
    # Výpocty pre optimalny vstup a vystup (Buy band a Exit band)
    buy_band_lower = round(price * 0.85, 2)  # 15% pod aktualnou cenou
    buy_band_upper = round(price * 0.90, 2)  # 10% pod aktualnou cenou
    exit_band_lower = round(price * 1.10, 2)  # 10% nad aktualnou cenou
    exit_band_upper = round(price * 1.20, 2)  # 20% nad aktualnou cenou
    
    # Definovanie strategie (strategicky pohlad)
    strategy = ""
    if free_float > 70:
        strategy += "Silny Free Float: Tento IPO ma silny free float, co moze naznacovat vyssiu likviditu a vacsi zaujem o akcie. Môze to byt vhodna prilezitost na nakup. "
    if insiders_total_pct < 10:
        strategy += "Nizky Insider Ownership: Nizsi podiel insiderov moze znamenat nizsiu doveru zo strany zakladatelov a zamestnancov. "

    # Odhad kratkodobeho a dlhodobeho zisku
    short_term_profit = f"Kratkodoby ciel: Cena moze vzrast o 10% az 20% v kratkom horizonte po IPO. Odhadovany vystup medzi {exit_band_lower} a {exit_band_upper} USD."
    long_term_profit = f"Dlhodoby ciel: Ak spolocnost uspeje v raste, cena akcie moze dosiahnut 25% az 50% zisk v priebehu nasledujucich 12-18 mesiacov."

    # Vytvorenie formatovaneho textu pre alert bez rizikových faktorov
    message = f"""
IPO Alert - {company} ({ticker})

Cena akcie: {price} USD
Market Cap: {market_cap} miliard USD
Free Float: {free_float}%
Insider %: {insiders_total_pct}%
IPO Datum: {ipo_date}
Lock-up: {days_to_lockup} dni

Optimalny vstup do pozicie (Buy Band): {buy_band_lower} - {buy_band_upper} USD
Optimalny vystup z pozicie (Exit Band): {exit_band_lower} - {exit_band_upper} USD

Strategicky pohlad: 
{strategy}

Kratkodoba strategia: {short_term_profit}
Dlhodoba strategia: {long_term_profit}
"""
    return message
