import logging
from locust import HttpUser, task, between

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class WalletUser(HttpUser):
    wait_time = between(0.1, 0.2)  # Уменьшено время ожидания для увеличения RPS
    host = "http://web:8000"

    def on_start(self):
        response = self.client.post(
            "/api/v1/wallets/",
            headers={"Content-Type": "application/json"},
            json={}
        )
        if response.status_code == 201:
            self.wallet_id = response.json()['id']
        else:
            self.wallet_id = None
            logging.error(f"Ошибка при создании кошелька: {response.status_code}")

    @task(10)
    def deposit(self):
        if self.wallet_id:
            response = self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
                "operation_type": "DEPOSIT",
                "amount": 100.0
            })
            if response.status_code != 201:
                logging.error(f"Ошибка при пополнении: {response.status_code}")

    @task(1)
    def withdraw(self):
        if self.wallet_id:
            response = self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
                "operation_type": "WITHDRAW",
                "amount": 1.0
            })
            if response.status_code != 201:
                logging.error(f"Ошибка при снятии средств: {response.status_code}")

    @task(10)
    def get_balance(self):
        if self.wallet_id:
            response = self.client.get(f"/api/v1/wallets/{self.wallet_id}/balance/")
            if response.status_code != 200:
                logging.error(f"Ошибка при запросе баланса: {response.status_code}")