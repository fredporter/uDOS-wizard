from __future__ import annotations

class BudgetPolicy:
    def __init__(self) -> None:
        self.policy = {
            "daily_limit": 100,
            "provider_limits": {
                "openai": 50,
                "local": 9999
            }
        }

    def get(self) -> dict:
        return self.policy
