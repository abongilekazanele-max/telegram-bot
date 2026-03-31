movement = abs(price2 - price1)

if movement < 0.00005:
    # too small → force direction instead of WAIT
    direction = random.choice(["BUY ⬆️", "SELL ⬇️"])
else:
    if price2 > price1:
        direction = "BUY ⬆️"
    else:
        direction = "SELL ⬇️"
