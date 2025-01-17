from locust import HttpUser, task, between

class WalletUser(HttpUser):
    wait_time = between(1, 2)  # Задержка между запросами

    def on_start(self):
        # Создаём новый кошелёк для тестирования
        response = self.client.post("/api/v1/wallets/", json={"balance": 1000.0})
        self.wallet_id = response.json()['id']

    @task(2)
    def deposit(self):
        self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
            "operation_type": "DEPOSIT",
            "amount": 100.0
        })

    @task(1)
    def withdraw(self):
        self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
            "operation_type": "WITHDRAW",
            "amount": 50.0
        })

    @task(1)
    def get_balance(self):
        self.client.get(f"/api/v1/wallets/{self.wallet_id}/balance/")