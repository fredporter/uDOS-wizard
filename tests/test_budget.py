from __future__ import annotations

import unittest

from wizard.budget import BudgetPolicy


class BudgetTests(unittest.TestCase):
    def test_budget_policy_exposes_limits(self) -> None:
        policy = BudgetPolicy().get()
        self.assertIn("daily_limit", policy)
        self.assertIn("provider_limits", policy)
        self.assertIn("openai", policy["provider_limits"])


if __name__ == "__main__":
    unittest.main()
