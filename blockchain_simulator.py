import random
import time
from database import Database

class SimulatedBlockchain:
    def __init__(self):
        self.db = Database()

    def create_wallet(self, address):
        self.db.add_wallet(address, 0, 0)

    def simulate_transaction(self, from_address, to_address, token, amount):
        timestamp = time.time()
        self.db.add_transaction(from_address, to_address, token, amount, timestamp)

    def get_hero_only_wallets(self):
        return self.db.get_hero_only_wallets()