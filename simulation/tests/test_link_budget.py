"""Check physical scaling, an independent linear calculation and invalid inputs."""
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('link_budget', ROOT / 'models/link_budget.py')
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)
CONFIG = json.loads((ROOT / 'configs/link_budget.example.json').read_text(encoding='utf-8'))


class LinkBudgetTests(unittest.TestCase):
    def power(self, **changes):
        return MODEL.calculate(dict(CONFIG, **changes))['received_power_dbm']

    def test_reference_linear_watts(self):
        wavelength = 299792458 / 2.45e9
        watts = (0.001 * 10**1.5 * 10**1.885 * wavelength**2 * 10
                 / ((4*math.pi)**3 * 1000**4 * 10**0.6))
        self.assertAlmostEqual(self.power(), 10*math.log10(watts/0.001), places=10)
        self.assertAlmostEqual(self.power(), -133.39, delta=0.1)

    def test_range_fourth_power(self):
        self.assertAlmostEqual(self.power(range_m=2000)-self.power(), -40*math.log10(2))

    def test_rcs_linear(self):
        self.assertAlmostEqual(self.power(rcs_m2=100)-self.power(), 10)

    def test_losses(self):
        self.assertAlmostEqual(self.power(loss_db=9)-self.power(), -3)

    def test_noise_bandwidth(self):
        a = MODEL.calculate(CONFIG)
        b = MODEL.calculate(dict(CONFIG, noise_bandwidth_hz=1e8))
        self.assertAlmostEqual(b['noise_power_dbm']-a['noise_power_dbm'], 10)
        self.assertAlmostEqual(b['snr_before_processing_db']-a['snr_before_processing_db'], -10)

    def test_invalid_inputs(self):
        for key, value in [('range_m',0),('rcs_m2',-1),('frequency_hz',float('nan')),
                           ('temperature_k',0),('loss_db',-1),('tx_power_dbm',True)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                MODEL.calculate(dict(CONFIG, **{key:value}))


if __name__ == '__main__':
    unittest.main()
