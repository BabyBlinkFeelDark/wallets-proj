import logging
from locust import HttpUser, task, between

logging.basicConfig(
        level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class WalletUser(HttpUser):
    wait_time = between(3, 5)
    host = "http://web:8000"

    def on_start(self):
        response = self.client.post(
            "/api/v1/wallets/",
            headers={"Content-Type": "application/json"},
            json={}
        )
        logging.info(f"Статус ответа: {response.status_code}")
        if response.status_code == 201:
            logging.info(f"Кошелёк создан успешно: {response.status_code}, ID: {response.json()['id']}")
            self.wallet_id = response.json()['id']
        else:
            logging.error(f"Ошибка при создании кошелька: {response.text}")

    @task(4)
    def deposit(self):
        if hasattr(self, 'wallet_id'):
            response = self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
                "operation_type": "DEPOSIT",
                "amount": 100.0
            })
            if response.status_code == 201:
                logging.info(f"Пополнение кошелька успешно: {response.status_code}")
            else:
                logging.error(f"Ошибка при пополнении: {response.text}")

    @task(1)
    def withdraw(self):
        if hasattr(self, 'wallet_id'):
            response = self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
                "operation_type": "WITHDRAW",
                "amount": 1.0
            })
            if response.status_code == 201:
                logging.info(f"Снятие средств успешно: {response.status_code}")
            else:
                logging.error(f"Ошибка при снятии средств: {response.text}")

    @task(1)
    def get_balance(self):
        if hasattr(self, 'wallet_id'):
            response = self.client.get(f"/api/v1/wallets/{self.wallet_id}/balance/")
            if response.status_code == 200:
                logging.info(f"Запрос баланса успешен: {response.status_code}, Баланс: {response.json()['balance']}")
            else:
                logging.error(f"Ошибка при запросе баланса: {response.text}")
