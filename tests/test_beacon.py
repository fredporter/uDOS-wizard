from __future__ import annotations

import unittest

from wizard.beacon import BeaconNode


class BeaconTests(unittest.TestCase):
    def test_announce_returns_ok_status(self) -> None:
        result = BeaconNode().announce()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["beacon"], "announce")

    def test_connect_returns_target(self) -> None:
        result = BeaconNode().connect("control-plane")
        self.assertEqual(result["target"], "control-plane")


if __name__ == "__main__":
    unittest.main()
