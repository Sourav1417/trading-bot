import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def initialize_tokens(self):
        self.cur.execute("""
            INSERT INTO tokens (token_symbol, token_name)
            VALUES ('HERO', 'Hero Token'), ('SOL', 'Solana')
            ON CONFLICT (token_symbol) DO NOTHING
        """)
        self.conn.commit()

    def add_wallet(self, wallet_address, is_hero_only):
        self.cur.execute(
            "INSERT INTO wallets (wallet_address, is_hero_only) VALUES (%s, %s) ON CONFLICT (wallet_address) DO UPDATE SET is_hero_only = EXCLUDED.is_hero_only",
            (wallet_address, is_hero_only)
        )
        self.conn.commit()

    def update_wallet_balance(self, wallet_address, token_symbol, balance):
        self.cur.execute(
            """
            INSERT INTO wallet_balances (wallet_address, token_symbol, balance) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (wallet_address, token_symbol) 
            DO UPDATE SET balance = EXCLUDED.balance, last_updated = CURRENT_TIMESTAMP
            """,
            (wallet_address, token_symbol, balance)
        )
        self.conn.commit()

    def add_transaction(self, wallet_address, token_symbol, transaction_type, amount):
        self.cur.execute(
            """
            INSERT INTO transactions (wallet_address, token_symbol, transaction_type, amount) 
            VALUES (%s, %s, %s, %s)
            """,
            (wallet_address, token_symbol, transaction_type, amount)
        )
        self.conn.commit()

    def get_hero_only_wallets(self):
        self.cur.execute("SELECT wallet_address FROM wallets WHERE is_hero_only = TRUE")
        return [row[0] for row in self.cur.fetchall()]

    def log_bot_action(self, action_type, token_symbol, amount, related_wallet, related_transaction):
        self.cur.execute(
            """
            INSERT INTO bot_actions (action_type, token_symbol, amount, related_wallet, related_transaction) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (action_type, token_symbol, amount, related_wallet, related_transaction)
        )
        self.conn.commit()
    
    def get_recent_transactions(self, wallet_address, limit=5):
        self.cur.execute(
            "SELECT * FROM transactions WHERE wallet_address = %s ORDER BY timestamp DESC LIMIT %s",
            (wallet_address, limit)
        )
        return self.cur.fetchall()

    def get_timed_out_actions(self, timeout_minutes=60):
        self.cur.execute(
            """
            SELECT * FROM bot_actions 
            WHERE action_type = 'BUY' AND timestamp < NOW() - INTERVAL '%s minutes'
            AND action_id NOT IN (SELECT related_transaction FROM bot_actions WHERE action_type IN ('SELL', 'TIMEOUT_SELL'))
            """,
            (timeout_minutes,)
        )
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()