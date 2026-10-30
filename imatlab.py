"""
imatlab.py

Command interpreter for the modular arithmetic library in ``modular.py``.

    python imatlab.py                      # interactive mode
    python imatlab.py input.txt output.txt # batch mode, one command per line

Each command prints its result, ``NE`` when the problem has no solution, or
``NOP`` when the call itself is invalid (unknown command, wrong arguments,
bad input). The interpreter never crashes on user input.
"""

import re
import sys
from typing import Callable, Dict, List, TextIO

import modular

COMMAND_RE = re.compile(r"^\s*(\w+)\s*\((.*)\)\s*$")
INT_RE = re.compile(r"^[+-]?\d+$")
LIST_RE = re.compile(r"^\[(.*)\]$")


class NoSolution(Exception):
    """The command is well formed but the problem has no solution."""


class BadCall(Exception):
    """The command is malformed, unknown or called with invalid arguments."""


def _ints(items: List[str]) -> List[int]:
    if not all(INT_RE.match(x) for x in items):
        raise BadCall("all arguments must be integers")
    return [int(x) for x in items]


def _split_args(raw: str) -> List[str]:
    """Split on top-level commas, keeping ``[a;b;c]`` lists intact."""
    parts, depth, current = [], 0, ""
    for ch in raw:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    return parts


def _yes_no(value: bool) -> str:
    return "Sí" if value else "No"


def _join(values) -> str:
    return ", ".join(str(v) for v in values)


def _arity(args: List[str], n: int) -> List[int]:
    if len(args) != n:
        raise BadCall(f"expected {n} arguments, got {len(args)}")
    return _ints(args)


def cmd_primo(args):
    (n,) = _arity(args, 1)
    return _yes_no(modular.es_primo(n))


def cmd_primos(args):
    a, b = _arity(args, 2)
    return _join(modular.lista_primos(a, b))


def cmd_factorizar(args):
    (n,) = _arity(args, 1)
    if n < 2:
        raise BadCall("n must be at least 2")
    return _join(f"{p}: {e}" for p, e in sorted(modular.factorizar(n).items()))


def cmd_mcd(args):
    a, b = _arity(args, 2)
    return str(modular.mcd(a, b))


def cmd_coprimos(args):
    a, b = _arity(args, 2)
    return _yes_no(modular.coprimos(a, b))


def cmd_pow(args):
    base, exp, p = _arity(args, 3)
    if p <= 0:
        raise BadCall("modulus must be positive")
    try:
        return str(modular.potencia_mod_p(base, exp, p))
    except ZeroDivisionError:
        raise NoSolution("base is not invertible")


def cmd_inv(args):
    n, p = _arity(args, 2)
    if p <= 0:
        raise BadCall("modulus must be positive")
    try:
        return str(modular.inversa_mod_p(n, p))
    except (ZeroDivisionError, ValueError):
        raise NoSolution(f"{n} has no inverse mod {p}")


def cmd_euler(args):
    (n,) = _arity(args, 1)
    if n <= 0:
        raise BadCall("n must be positive")
    return str(modular.euler(n))


def _require_prime(p: int):
    if not modular.es_primo(p):
        raise BadCall(f"{p} is not prime")


def cmd_legendre(args):
    n, p = _arity(args, 2)
    _require_prime(p)
    return str(modular.legendre(n, p))


def cmd_resolver_sistema(args):
    """Each argument is one congruence ``[a;b;p]`` meaning a·x ≡ b (mod p)."""
    if not args:
        raise BadCall("no congruences given")
    alist, blist, plist = [], [], []
    for arg in args:
        match = LIST_RE.match(arg)
        if not match:
            raise BadCall("each congruence must be written as [a;b;p]")
        fields = [x.strip() for x in match.group(1).split(";")]
        if len(fields) != 3:
            raise BadCall("each congruence needs exactly a, b and p")
        a, b, p = _ints(fields)
        if p <= 0:
            raise BadCall("moduli must be positive")
        alist.append(a)
        blist.append(b)
        plist.append(p)
    try:
        r, m = modular.resolver_sistema_congruencias(alist, blist, plist)
    except (modular.IncompatibleEquationError, ZeroDivisionError):
        raise NoSolution("incompatible system")
    return f"{r} (mod {m})"


def cmd_raiz(args):
    n, p = _arity(args, 2)
    _require_prime(p)
    roots = modular.raiz_mod_p(n, p)
    if not roots:
        raise NoSolution(f"{n} is not a square mod {p}")
    return _join(roots)


def cmd_ec_cuadratica(args):
    a, b, c, p = _arity(args, 4)
    _require_prime(p)
    if a % p == 0:
        raise BadCall("a must be non-zero mod p")
    solutions = modular.ecuacion_cuadratica(a, b, c, p)
    if solutions == "NE":
        raise NoSolution("no solutions")
    return _join(solutions)


COMMANDS: Dict[str, Callable[[List[str]], str]] = {
    "primo": cmd_primo,
    "primos": cmd_primos,
    "factorizar": cmd_factorizar,
    "mcd": cmd_mcd,
    "coprimos": cmd_coprimos,
    "pow": cmd_pow,
    "inv": cmd_inv,
    "euler": cmd_euler,
    "legendre": cmd_legendre,
    "resolverSistema": cmd_resolver_sistema,
    "raiz": cmd_raiz,
    "ecCuadratica": cmd_ec_cuadratica,
}


def evaluate(line: str, verbose: bool = False) -> str:
    """Run one command and return its output line. Never raises."""
    match = COMMAND_RE.match(line)
    try:
        if not match or match.group(1) not in COMMANDS:
            raise BadCall("unknown command")
        return COMMANDS[match.group(1)](_split_args(match.group(2)))
    except NoSolution as e:
        return f"NE ({e})" if verbose else "NE"
    except BadCall as e:
        return f"NOP ({e})" if verbose else "NOP"
    except Exception as e:  # anything unexpected is still a bad call, never a crash
        return f"NOP ({type(e).__name__}: {e})" if verbose else "NOP"


def run_commands(fin: TextIO, fout: TextIO, verbose: bool = False) -> None:
    for line in fin:
        if line.strip():
            fout.write(evaluate(line.strip(), verbose) + "\n")


def interactive() -> None:
    print("IMAT-LAB · modular arithmetic. Commands: " + ", ".join(COMMANDS) + ". Ctrl+D to exit.")
    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip():
            print(evaluate(line.strip(), verbose=True))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        with open(sys.argv[1], encoding="utf-8") as fin, open(sys.argv[2], "w", encoding="utf-8") as fout:
            run_commands(fin, fout)
    elif len(sys.argv) == 1:
        interactive()
    else:
        print("usage: python imatlab.py [input.txt output.txt]", file=sys.stderr)
        sys.exit(2)
