import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import imatlab  # noqa: E402
import modular  # noqa: E402


class ReferenceExamples(unittest.TestCase):
    """The 21 reference commands from the course statement, with their expected output."""

    def test_examples(self):
        commands = (ROOT / "examples" / "commands.txt").read_text(encoding="utf-8").splitlines()
        expected = (ROOT / "examples" / "expected_output.txt").read_text(encoding="utf-8").splitlines()
        for line, want in zip(commands, expected):
            with self.subTest(command=line):
                self.assertEqual(imatlab.evaluate(line), want.strip())


class NeverCrashes(unittest.TestCase):
    def test_garbage_input(self):
        for line in ["", "primo", "primo()", "primo(a)", "pow(1,2)", "inv(3,0)", "raiz(2,8)",
                     "resolverSistema([1;2],[3;4;5])", "ecCuadratica(0,1,1,7)", "mcd(1,2,3)", "euler(-4)"]:
            with self.subTest(command=line):
                self.assertEqual(imatlab.evaluate(line), "NOP")


class Properties(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        self.primes = modular.lista_primos(3, 20000)

    def test_bezout_identity(self):
        for _ in range(500):
            a, b = random.randint(-10**9, 10**9), random.randint(1, 10**9)
            g, x, y = modular.bezout(a, b)
            self.assertEqual(a * x + b * y, g)
            self.assertEqual(g, modular.mcd(a, b))

    def test_square_roots(self):
        for _ in range(500):
            p = random.choice(self.primes)
            n = random.randrange(p)
            roots = modular.raiz_mod_p(n, p)
            for r in roots:
                self.assertEqual(r * r % p, n)
            self.assertEqual(bool(roots), modular.legendre(n, p) >= 0)

    def test_crt(self):
        for _ in range(300):
            ps = random.sample(self.primes, 3)
            xs = [random.randrange(p) for p in ps]
            r, m = modular.resolver_sistema_congruencias([1, 1, 1], xs, ps)
            self.assertEqual(m, ps[0] * ps[1] * ps[2])
            self.assertTrue(all(r % p == x for p, x in zip(ps, xs)))

    def test_negative_exponent(self):
        for _ in range(300):
            p = random.choice(self.primes)
            b = random.randrange(1, p)
            e = random.randint(1, 50)
            self.assertEqual(modular.potencia_mod_p(b, -e, p) * modular.potencia_mod_p(b, e, p) % p, 1)


if __name__ == "__main__":
    unittest.main()
