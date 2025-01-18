from locust import HttpUser, task, between

class WalletUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"

    def on_start(self):
        response = self.client.post("api/v1/wallets/", json={"balance": 1000.0})
        if response.status_code == 201:
            self.wallet_id = response.json()['id']
        else:
            print("Ошибка при создании кошелька:", response.text)

    @task(2)
    def deposit(self):
        if hasattr(self, 'wallet_id'):
            self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
                "operation_type": "DEPOSIT",
                "amount": 100.0
            })

    @task(1)
    def withdraw(self):
        if hasattr(self, 'wallet_id'):
            self.client.post(f"/api/v1/wallets/{self.wallet_id}/operation/", json={
                "operation_type": "WITHDRAW",
                "amount": 50.0
            })

    @task(1)
    def get_balance(self):
        if hasattr(self, 'wallet_id'):
            self.client.get(f"/api/v1/wallets/{self.wallet_id}/balance/")