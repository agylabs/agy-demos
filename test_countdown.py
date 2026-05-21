import unittest
import subprocess
import sys
import os

class TestCountdownCLI(unittest.TestCase):
    def setUp(self):
        # Path to countdown.py relative to this test file
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "countdown.py"))

    def run_cli(self, args):
        cmd = [sys.executable, self.script_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_standard_countdown_three(self):
        res = self.run_cli(["3"])
        self.assertEqual(res.returncode, 0)
        expected = "3\n2\n1\nLiftoff!\n"
        self.assertEqual(res.stdout, expected)
        self.assertEqual(res.stderr, "")

    def test_standard_countdown_one(self):
        res = self.run_cli(["1"])
        self.assertEqual(res.returncode, 0)
        expected = "1\nLiftoff!\n"
        self.assertEqual(res.stdout, expected)
        self.assertEqual(res.stderr, "")

    def test_reverse_countdown_three(self):
        res = self.run_cli(["3", "--reverse"])
        self.assertEqual(res.returncode, 0)
        expected = "1\n2\n3\nLiftoff!\n"
        self.assertEqual(res.stdout, expected)
        self.assertEqual(res.stderr, "")

    def test_reverse_countdown_shorthand(self):
        res = self.run_cli(["2", "-r"])
        self.assertEqual(res.returncode, 0)
        expected = "1\n2\nLiftoff!\n"
        self.assertEqual(res.stdout, expected)
        self.assertEqual(res.stderr, "")

    def test_validation_non_integer(self):
        res = self.run_cli(["abc"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error: 'abc' is not a valid integer.", res.stderr)
        self.assertEqual(res.stdout, "")

    def test_validation_float(self):
        res = self.run_cli(["4.5"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error: '4.5' is not a valid integer.", res.stderr)
        self.assertEqual(res.stdout, "")

    def test_validation_zero(self):
        res = self.run_cli(["0"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error: 0 is not positive. The count must be 1 or greater.", res.stderr)
        self.assertEqual(res.stdout, "")

    def test_validation_negative(self):
        res = self.run_cli(["-5"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error: -5 is not positive. The count must be 1 or greater.", res.stderr)
        self.assertEqual(res.stdout, "")

    def test_validation_missing_argument(self):
        res = self.run_cli([])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error: Missing required argument 'number'.", res.stderr)
        self.assertEqual(res.stdout, "")

if __name__ == "__main__":
    unittest.main()
