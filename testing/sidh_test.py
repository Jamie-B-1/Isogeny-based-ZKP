import unittest
import random
import cypari
from isogeny_curve import curve
from isogeny_curve import sidh

curve_1 = curve.create_curve(2, 4, 3, 3, 1)
params_1 = sidh.create_params(2, 4, 3, 3, curve_1.P_a, curve_1.Q_a, curve_1.P_b, curve_1.Q_b)
curve_2 = curve.create_curve(2, 4, 3, 3, 1)
params_2 = sidh.create_params(2, 4, 3, 3, curve_2.P_a, curve_2.Q_a, curve_2.P_b, curve_2.Q_b)


class TestSIDH(unittest.TestCase):

    def setUp(self):
        # Create Curve instances for testing
        self.curve_a = curve_1
        self.curve_b = curve_2
        # Initialize SIDH instances with Curve instances
        self.sidh_instance_a = sidh.SIDH("A", self.curve_a.elli_curve, params_1, self.curve_a)
        self.sidh_instance_b = sidh.SIDH("B", self.curve_b.elli_curve, params_2, self.curve_b)

    def test_init(self):
        # Test initialization of SIDH instances
        self.assertEqual(self.sidh_instance_a.agent, "A")
        self.assertEqual(self.sidh_instance_a.l, 2)
        self.assertEqual(self.sidh_instance_a.e, 4)

        self.assertIsInstance(self.sidh_instance_a.s_key, int)
        self.assertIsNotNone(self.sidh_instance_a.S)
        self.assertIsNotNone(self.sidh_instance_a.pub_key)

    def test_get_other_agent(self):
        # Test getting other agent parameters
        self.assertEqual(self.sidh_instance_a.get_other_agent(params_1), params_2["B"])
        self.assertEqual(self.sidh_instance_b.get_other_agent(params_2), params_2["A"])

    def test_public_key(self):
        # Test computing public key
        other_agent_a = self.sidh_instance_a.get_other_agent(params_1)
        other_agent_b = self.sidh_instance_b.get_other_agent(params_2)
        pub_key_a = self.sidh_instance_a.public_key(other_agent_a, self.curve_a.elli_curve, self.curve_a)
        pub_key_b = self.sidh_instance_b.public_key(other_agent_b, self.curve_b.elli_curve, self.curve_b)
        self.assertIsNotNone(pub_key_a)
        self.assertIsNotNone(pub_key_b)

    def test_shared_secret(self):
        # Test computing shared secret
        shared_secret_a, S_a = self.sidh_instance_a.shared_secret(self.sidh_instance_b, self.curve_a)
        shared_secret_b, S_b = self.sidh_instance_b.shared_secret(self.sidh_instance_a, self.curve_b)
        self.assertIsNotNone(shared_secret_a)
        self.assertIsNotNone(shared_secret_b)
        self.assertIsNotNone(S_a)
        self.assertIsNotNone(S_b)


if __name__ == '__main__':
    unittest.main()
