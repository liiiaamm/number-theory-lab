import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import rsa  # noqa: E402

class PaddingRegressionTests(unittest.TestCase):
    def test_textbook_round_trip_without_padding(self):
        encrypted = rsa.cifrar_rsa(65, 3233, 17, 0)
        self.assertEqual(encrypted, 2790)
        self.assertEqual(rsa.descifrar_rsa(encrypted, 3233, 2753, 0), 65)

    def test_padding_round_trip(self):
        for digits in (0, 1, 2, 3):
            for message in (0, 1, 65):
                with self.subTest(digits=digits, message=message):
                    padded = rsa.aplicar_padding(message, digits)
                    self.assertEqual(rsa.eliminar_padding(padded, digits), message)

    def test_negative_padding_rejected(self):
        for function in (rsa.aplicar_padding, rsa.eliminar_padding):
            with self.assertRaises(ValueError):
                function(65, -1)

if __name__ == '__main__':
    unittest.main()
