import unittest
from unittest.mock import patch
from isogeny_curve import curve, sidh
from zk_protocol import utility, sigma_protocol as sig
import cypari
pari = cypari.pari


class TestSigmaProtocol(unittest.TestCase):

    def setUp(self):
        # Set up the curves and parameters for testing
        self.curves = [
            curve.create_curve(2, 4, 3, 3, 1),  # Curve 1
            curve.create_curve(2, 18, 3, 13, 1),  # Curve 2
            curve.create_curve(2, 216, 3, 137, 1)  # Curve 3
        ]
        self.params = [
            sidh.create_params(curve.l_a, curve.e_a, curve.l_b, curve.e_b,
                               curve.P_a, curve.Q_a, curve.P_b, curve.Q_b)
            for curve in self.curves
        ]

    def test_prover(self):
        for curve, params in zip(self.curves, self.params):
            # Test prover function for each curve
            with patch('secrets.choice', return_value=1):
                chal = 1
                p = sig.prover(curve, params, chal)
                # Add your assertions here
                self.assertIsNotNone(p[0])
                self.assertIsNotNone(p[1])
                self.assertEqual(chal, 1)
                self.assertEqual(len(p[0][0]), 64)
                self.assertEqual(len(p[0][1]), 64)
                self.assertEqual(len(p[0][2]), 64)
                assert p[0][0] != p[0][1] != p[0][2]
                assert pari.ellissupersingular(p[1][0][0]) == 1
                assert pari.ellissupersingular(p[1][3][0]) == 1

    def test_verify(self):
        for curve, params in zip(self.curves, self.params):
            # Test verify function for each curve
            # Add test cases for different challenge values (1, 0, -1) and valid/invalid responses
            chal = 1
            p = sig.prover(curve, params, chal)
            v = sig.verify(curve, p, chal)
            self.assertTrue(v)

    def test_sigma_protocol(self):
        for curve, params in zip(self.curves, self.params):
            # Test sigma_protocol function for each curve
            # Add test cases to verify the protocol behavior under different scenarios
            k = 128
            res = sig.sigma_protocol(curve, params, k)
            self.assertEqual(res, "response accepted")


if __name__ == '__main__':
    unittest.main()

