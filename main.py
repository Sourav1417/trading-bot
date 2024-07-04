from database import Database
from trading_bot import TradingBot
import time

def main():
    with Database() as db:
        bot = TradingBot(db)

        for _ in range(5):  # Run 5 cycles for demonstration
            bot.simulate_and_trade()
            time.sleep(2)  # Wait for 2 seconds between cycles for demonstration

if __name__ == "__main__":
    main()