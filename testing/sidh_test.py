import unittest
import cypari
pari = cypari.pari
from isogeny_curve import curve
from isogeny_curve import sidh

# instance 1
curve_1 = curve.create_curve(2, 4, 3, 3, 1)
params_1 = sidh.create_params(2, 4, 3, 3, curve_1.P_a, curve_1.Q_a, curve_1.P_b, curve_1.Q_b)

curve_2 = curve.create_curve(2, 216, 3, 137, 1)
params_2 = sidh.create_params(2, 216, 3, 137, curve_2.P_a, curve_2.Q_a, curve_2.P_b, curve_2.Q_b)


class TestSIDH(unittest.TestCase):

    def setUp(self):
        # Create Curve instances for testing
        self.curve_a = curve_1
        self.params_a = params_1
        self.curve_b = curve_2
        self.params_b = params_2
        # Initialize SIDH instances with Curve instances for curve 1
        self.pub_key_a_1 = sidh.SIDH("A", self.curve_a.elli_curve, self.params_a, self.curve_a)
        self.pub_key_b_1 = sidh.SIDH("B", self.curve_a.elli_curve, self.params_a, self.curve_a)
        # Initialize SIDH instances with Curve instances for curve 2
        self.pub_key_a_2 = sidh.SIDH("A", self.curve_b.elli_curve, self.params_b, self.curve_b)
        self.pub_key_b_2 = sidh.SIDH("B", self.curve_b.elli_curve, self.params_b, self.curve_b)


    def test_init(self):
        # Test initialization of SIDH instances
        # curve 1
        self.assertEqual(self.pub_key_a_1.agent, "A")
        self.assertEqual(self.pub_key_a_1.l, 2)
        self.assertEqual(self.pub_key_a_1.e, 4)
        self.assertIsInstance(self.pub_key_a_1.s_key, int)

        self.assertEqual(self.pub_key_b_1.agent, "B")
        self.assertEqual(self.pub_key_b_1.l, 3)
        self.assertEqual(self.pub_key_b_1.e, 3)
        self.assertIsInstance(self.pub_key_b_1.s_key, int)

        # curve 2
        self.assertEqual(self.pub_key_a_2.agent, "A")
        self.assertEqual(self.pub_key_a_2.l, 2)
        self.assertEqual(self.pub_key_a_2.e, 216)
        self.assertIsInstance(self.pub_key_a_2.s_key, int)

        self.assertEqual(self.pub_key_b_2.agent, "B")
        self.assertEqual(self.pub_key_b_2.l, 3)
        self.assertEqual(self.pub_key_b_2.e, 137)


    def test_get_other_agent(self):
        # Test getting other agent parameters
        # curve 1
        self.assertEqual(self.pub_key_a_1.get_other_agent(params_1), params_1["B"])
        self.assertEqual(self.pub_key_b_1.get_other_agent(params_1), params_1["A"])
        # curve 2
        self.assertEqual(self.pub_key_a_2.get_other_agent(params_2), params_2["B"])
        self.assertEqual(self.pub_key_b_2.get_other_agent(params_2), params_2["A"])

    def test_public_key(self):
        # Test computing public key
        # curve 1
        other_agent_a = self.pub_key_a_1.get_other_agent(params_1)
        other_agent_b = self.pub_key_b_1.get_other_agent(params_1)
        pub_key_a = self.pub_key_a_1.public_key(other_agent_b, self.curve_a.elli_curve, self.curve_a)
        pub_key_b = self.pub_key_b_1.public_key(other_agent_a, self.curve_a.elli_curve, self.curve_a)
        self.assertIsNotNone(pub_key_a)
        self.assertIsNotNone(pub_key_b)
        assert len(pub_key_a) == 6
        assert len(pub_key_b) == 6
        # curve 2
        other_agent_a = self.pub_key_a_2.get_other_agent(params_2)
        other_agent_b = self.pub_key_b_2.get_other_agent(params_2)
        pub_key_a = self.pub_key_a_2.public_key(other_agent_b, self.curve_b.elli_curve, self.curve_b)
        pub_key_b = self.pub_key_b_2.public_key(other_agent_a, self.curve_b.elli_curve, self.curve_b)
        self.assertIsNotNone(pub_key_a)
        self.assertIsNotNone(pub_key_b)
        assert len(pub_key_a) == 6
        assert len(pub_key_b) == 6


    def test_shared_secret(self):
        # Test computing shared secret
        # curve 1
        shared_secret_a = self.pub_key_a_1.shared_secret(self.pub_key_b_1, self.curve_a)
        shared_secret_b = self.pub_key_b_1.shared_secret(self.pub_key_a_1, self.curve_a)
        self.assertIsNotNone(shared_secret_a[0])
        self.assertIsNotNone(shared_secret_b[0])
        self.assertIsNotNone(shared_secret_a[1])
        self.assertIsNotNone(shared_secret_b[1])
        assert shared_secret_a[0][0].j() == shared_secret_b[0][0].j()
        # curve 2
        shared_secret_a = self.pub_key_a_2.shared_secret(self.pub_key_b_2, self.curve_b)
        shared_secret_b = self.pub_key_b_2.shared_secret(self.pub_key_a_2, self.curve_b)
        self.assertIsNotNone(shared_secret_a[0])
        self.assertIsNotNone(shared_secret_b[0])
        self.assertIsNotNone(shared_secret_a[1])
        self.assertIsNotNone(shared_secret_b[1])
        assert shared_secret_a[0][0].j() == shared_secret_b[0][0].j()


if __name__ == '__main__':
    unittest.main()
