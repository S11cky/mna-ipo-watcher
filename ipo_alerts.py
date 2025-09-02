def build_ipo_alert(ipo: dict) -> str:
    """Vytvorenie textu alertu pre Telegram na z�klade IPO d�t so strategick�m pohladom"""
    
    # Z�skanie d�t z IPO dictu
    company = ipo["company_name"]
    ticker = ipo["ticker"]
    price = ipo["price_usd"]
    market_cap = ipo["market_cap_usd"]
    free_float = ipo.get("free_float_pct", 0)
    insiders_total_pct = ipo.get("insiders_total_pct", 0)
    ipo_date = ipo.get("ipo_first_trade_date", "Nezn�my")
    days_to_lockup = ipo.get("days_to_lockup", "Nezn�my")
    
    # Zaokr�hlenie hodn�t na rozumn� pocet desatinn�ch miest
    price = round(price, 2)
    market_cap = round(market_cap / 1e9, 2)  # Trhov� kapitaliz�cia v miliard�ch USD
    free_float = round(free_float, 2)
    insiders_total_pct = round(insiders_total_pct, 2)
    
    # V�pocty pre optim�lny vstup a v�stup (Buy band a Exit band)
    buy_band_lower = round(price * 0.85, 2)  # 15% pod aktu�lnou cenou
    buy_band_upper = round(price * 0.90, 2)  # 10% pod aktu�lnou cenou
    exit_band_lower = round(price * 1.10, 2)  # 10% nad aktu�lnou cenou
    exit_band_upper = round(price * 1.20, 2)  # 20% nad aktu�lnou cenou
    
    # Definovanie strat�gie (strategick� pohlad)
    strategy = ""
    if free_float > 70:
        strategy += "?? **Siln� Free Float**: Tento IPO m� siln� free float, co m��e naznacovat vy��iu likviditu a v�c�� z�ujem o akcie. M��e to byt vhodn� pr�le�itost na n�kup. "
    if insiders_total_pct < 10:
        strategy += "?? **N�zk� Insider Ownership**: Ni��� podiel insiderov m��e znamenat ni��iu d�veru zo strany zakladatelov a zamestnancov. "

    # Odhat kr�tkodob�ho a dlhodob�ho zisku
    short_term_profit = f"**Kr�tkodob� ciel**: Cena m��e vzr�st o 10% a� 20% v kr�tkom horizonte po IPO. Odhadovan� v�stup medzi {exit_band_lower} a {exit_band_upper} USD."
    long_term_profit = f"**Dlhodob� ciel**: Ak spolocnost uspeje v raste, cena akcie m��e dosiahnut 25% a� 50% zisk v priebehu nasleduj�cich 12-18 mesiacov."

    # Vytvorenie form�tovan�ho textu pre alert bez rizikov�ch faktorov
    message = f"""
?? IPO Alert - {company} ({ticker})

?? **Cena akcie**: {price} USD
?? **Market Cap**: {market_cap} mili�rd USD
?? **Free Float**: {free_float}%
?? **Insider %**: {insiders_total_pct}%
?? **IPO D�tum**: {ipo_date}
?? **Lock-up**: {days_to_lockup} dn�

?? **Optim�lny vstup do poz�cie (Buy Band)**: {buy_band_lower} - {buy_band_upper} USD
?? **Optim�lny v�stup z poz�cie (Exit Band)**: {exit_band_lower} - {exit_band_upper} USD

?? **Strategick� pohlad**: 
{strategy}

?? **Kr�tkodob� strat�gia**: {short_term_profit}
?? **Dlhodob� strat�gia**: {long_term_profit}
"""
    return message
