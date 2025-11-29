import requests, time

def kava_repay():
    print("Kava — Massive Loan Repay Detector (> $2M repaid in one tx)")
    seen = set()
    while True:
        r = requests.get("https://kava.api.explorers.guru/api/v2/transactions?limit=40")
        for tx in r.json().get("items", []):
            h = tx["hash"]
            if h in seen: continue
            seen.add(h)

            # Kava Lend repay events usually go to hard module
            if "hard" not in tx.get("messages", [{}])[0].get("type", ""): continue
            if "repay" not in str(tx.get("messages")).lower(): continue

            # Approximate USD value from logs
            value_usd = 0
            for log in tx.get("logs", []):
                for ev in log.get("events", []):
                    if "repay" in ev.get("type", ""):
                        for attr in ev["attributes"]:
                            if attr["key"] == "amount":
                                # rough parse
                                try:
                                    amt = int(attr["value"].split(",")[0].strip("0123456789").strip())
                                    value_usd += amt / 1e6  # most are USDT/USDC
                                except:
                                    continue
            if value_usd >= 2_000_000:
                print(f"WHALE REPAID $2M+ LOAN\n"
                      f"~${value_usd:,.0f} repaid on Kava Lend\n"
                      f"Wallet: {tx['from_address'][:16]}...\n"
                      f"Tx: https://explorer.kava.io/tx/{h}\n"
                      f"→ DeFi whale just closed a massive position\n"
                      f"{'-'*60}")
        time.sleep(4.2)

if __name__ == "__main__":
    kava_repay()
