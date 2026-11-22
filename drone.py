import unittest
from drone_sentinelle import *


class Tests(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(classify(30), "AUCUN")
        self.assertEqual(classify(100), "FAIBLE")
        self.assertEqual(classify(300), "MOYENNE")
        self.assertEqual(classify(800), "FORTE")

    def test_median_ignores_outliers(self):
        ms = [Measurement("a", t, 0.9) for t in (200, 205, 198, 5000, 202)]
        self.assertAlmostEqual(robust_temperature(ms), 201.0, delta=5)

    def test_low_battery_aborts(self):
        home = Position(0, 0)
        m = Mission(SimulatedDrone(home, battery_pct=26), SimulatedWaveSensor({}),
                    ConsoleUnitLink(), home, Position(50000, 0), ["A"])
        self.assertIsNone(m.run())
        self.assertEqual(m.state, State.ABANDON)

    def test_full_mission(self):
        home = Position(0, 0)
        m = Mission(SimulatedDrone(home), SimulatedWaveSensor({"A": 600.0}),
                    ConsoleUnitLink(), home, Position(2000, 0), ["A"])
        r = m.run()
        self.assertEqual(r.level, "FORTE")
        self.assertEqual(r.vehicles, 4)


if __name__ == "__main__":
    unittest.main()