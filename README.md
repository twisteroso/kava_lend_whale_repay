# Kava — Whale Loan Repay Tracker

Detects when someone repays **$2M+** in a single transaction on Kava Lend (HARD Protocol).

These are not regular users.  
This is:
- A whale closing leveraged position
- Liquidation avoidance at the last second
- Institutional borrower cleaning the books

## Run

```bash
python kava_lend_whale_repay.py
