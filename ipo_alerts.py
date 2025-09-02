# -*- coding: utf-8 -*-
def build_ipo_alert(ipo: dict) -> str:
    """Vytvorenie textu alertu pre Telegram na základe IPO dát so strategickým pohladom"""
    
    # Získanie dát z IPO dictu
    company = ipo["company_name"]
    ticker = ipo["ticker"]
    price = ipo["price_usd"]
    market_cap = ipo["market_cap_usd"]
    free_float = ipo.get("free_float_pct", 0)
    insiders_total_pct = ipo.get("insiders_total_pct", 0)
    ipo_date = ipo.get("ipo_first_trade_date", "Neznámy")
    days_to_lockup = ipo.get("days_to_lockup", "Neznámy")
    
    # Zaokrúhlenie hodnôt na rozumný pocet desatinných miest
    price = round(price, 2)
    market_cap = round(market_cap / 1e9, 2)  # Trhová kapitalizácia v miliardách USD
    free_float = round(free_float, 2)
    insiders_total_pct = round(insiders_total_pct, 2)
    
    # Výpocty pre optimálny vstup a výstup (Buy band a Exit band)
    buy_band_lower = round(price * 0.85, 2)  # 15% pod aktuálnou cenou
    buy_band_upper = round(price * 0.90, 2)  # 10% pod aktuálnou cenou
    exit_band_lower = round(price * 1.10, 2)  # 10% nad aktuálnou cenou
    exit_band_upper = round(price * 1.20, 2)  # 20% nad aktuálnou cenou
    
    # Definovanie stratégie (strategický pohlad)
    strategy = ""
    if free_float > 70:
        strategy += "?? **Silný Free Float**: Tento IPO má silný free float, co môže naznacovat vyššiu likviditu a väcší záujem o akcie. Môže to byt vhodná príležitost na nákup. "
    if insiders_total_pct < 10:
        strategy += "?? **Nízký Insider Ownership**: Nižší podiel insiderov môže znamenat nižšiu dôveru zo strany zakladatelov a zamestnancov. "

    # Odhat krátkodobého a dlhodobého zisku
    short_term_profit = f"**Krátkodobý ciel**: Cena môže vzrást o 10% až 20% v krátkom horizonte po IPO. Odhadovaný výstup medzi {exit_band_lower} a {exit_band_upper} USD."
    long_term_profit = f"**Dlhodobý ciel**: Ak spolocnost uspeje v raste, cena akcie môže dosiahnut 25% až 50% zisk v priebehu nasledujúcich 12-18 mesiacov."

    # Vytvorenie formátovaného textu pre alert bez rizikových faktorov
    message = f"""
?? IPO Alert - {company} ({ticker})

?? **Cena akcie**: {price} USD
?? **Market Cap**: {market_cap} miliárd USD
?? **Free Float**: {free_float}%
?? **Insider %**: {insiders_total_pct}%
?? **IPO Dátum**: {ipo_date}
?? **Lock-up**: {days_to_lockup} dní

?? **Optimálny vstup do pozície (Buy Band)**: {buy_band_lower} - {buy_band_upper} USD
?? **Optimálny výstup z pozície (Exit Band)**: {exit_band_lower} - {exit_band_upper} USD

?? **Strategický pohlad**: 
{strategy}

?? **Krátkodobá stratégia**: {short_term_profit}
?? **Dlhodobá stratégia**: {long_term_profit}
"""
    return message

