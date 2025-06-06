import unittest
from isogeny_curve import curve
import cypari
pari = cypari.pari


class TestCurveStruct(unittest.TestCase):
    def setUp(self):
        # Set up a test curve
        self.curve = curve.create_curve(2, 216, 3, 137, 1)

    def test_create_curve(self):
        # Check that curve initialization is correct
        self.assertEqual(self.curve.l_a, 2)
        self.assertEqual(self.curve.e_a, 216)
        self.assertEqual(self.curve.l_b, 3)
        self.assertEqual(self.curve.e_b, 137)
        assert pari.ellissupersingular(self.curve.elli_curve) == 1

    def test_get_random_point(self):
        # Test get_random_point function
        P = self.curve.P_a
        Q = self.curve.Q_a
        R = curve.get_random_point(self.curve.elli_curve, self.curve.l_a, self.curve.e_a, P, Q)
        self.assertIsNotNone(R)

    def test_random_bases(self):
        # Test random_bases function
        P = self.curve.P_a
        Q = self.curve.Q_a
        P_new, Q_new = curve.random_bases(self.curve.elli_curve, self.curve.l_a, self.curve.e_a, P, Q)
        self.assertIsNotNone(P_new)
        self.assertIsNotNone(Q_new)
        assert pari.ellmul(self.curve.elli_curve, P_new, self.curve.order) == 0
        assert pari.ellmul(self.curve.elli_curve, Q_new, self.curve.order) == 0

    def test_generate_base_points(self):
        # Test generate_base_points function
        P_a, Q_a, P_b, Q_b = curve.generate_base_points(self.curve.gen_fp2, self.curve.elli_curve, 2, 216, 3, 137)
        self.assertIsNotNone(P_a)
        self.assertIsNotNone(Q_a)
        self.assertIsNotNone(P_b)
        self.assertIsNotNone(Q_b)
        assert pari.ellmul(self.curve.elli_curve, P_a, self.curve.order) == 0
        assert pari.ellmul(self.curve.elli_curve, Q_a, self.curve.order) == 0
        assert pari.ellmul(self.curve.elli_curve, P_b, self.curve.order) == 0
        assert pari.ellmul(self.curve.elli_curve, Q_b, self.curve.order) == 0


if __name__ == '__main__':
    unittest.main()
