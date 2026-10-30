# Number Theory Lab

Modular arithmetic from first principles, a small command language on top of it, and textbook RSA built and then broken with the same library. Pure Python, no dependencies.

```
$ python imatlab.py
>>> raiz(-1,5)
2, 3
>>> resolverSistema([1;1;3],[4;7;11])
10 (mod 33)
>>> inv(3,9)
NE (3 has no inverse mod 9)
```

## What's inside

**`modular.py`**: the library.

| Area | Functions |
|---|---|
| Primes | trial-division and Miller–Rabin primality, prime lists, factorisation by trial division and Pollard's rho |
| Divisibility | gcd, extended Euclid (Bézout) for two or $n$ numbers, coprimality |
| Modular arithmetic | fast exponentiation (negative exponents included), inverses, Euler's $\varphi$ |
| Equations | linear systems $a_i x \equiv b_i \pmod{p_i}$ via the generalised CRT (non-coprime moduli included), Legendre symbol, square roots mod $p$ (Tonelli–Shanks), quadratics $ax^2 + bx + c \equiv 0 \pmod p$ |

**`imatlab.py`**: an interpreter for the library, interactive or in batch mode. Every command returns a result, `NE` if the problem has no solution, or `NOP` if the call is invalid. It never crashes on bad input.

**`rsa.py`**: textbook RSA over the library: key generation, integer and string encryption, a simple padding scheme, and two attacks. One recovers the private key by factoring $n$ with Pollard's rho; the other decrypts unpadded messages with a chosen-plaintext attack, which is why real RSA needs randomised padding.

**`registrarusuario.py` / `criptochat.py`**: generate a key pair per user and exchange encrypted messages locally.

## Commands

| Command | Meaning | Example → output |
|---|---|---|
| `primo(n)` | is $n$ prime? | `primo(7)` → `Sí` |
| `primos(a,b)` | primes in $[a, b]$ | `primos(5,20)` → `5, 7, 11, 13, 17, 19` |
| `factorizar(n)` | prime factorisation | `factorizar(120)` → `2: 3, 3: 1, 5: 1` |
| `mcd(a,b)` / `coprimos(a,b)` | gcd / coprimality | `mcd(1,20)` → `1` |
| `pow(b,e,p)` | $b^e \bmod p$ | `pow(-3,-8,7)` → `4` |
| `inv(n,p)` | $n^{-1} \bmod p$ | `inv(3,7)` → `5` |
| `euler(n)` | $\varphi(n)$ | `euler(10)` → `4` |
| `legendre(n,p)` | $\left(\frac{n}{p}\right)$ | `legendre(10,3)` → `1` |
| `resolverSistema([a;b;p],...)` | system $a_i x \equiv b_i \pmod{p_i}$ | see above |
| `raiz(n,p)` | $x^2 \equiv n \pmod p$ | `raiz(-1,5)` → `2, 3` |
| `ecCuadratica(a,b,c,p)` | $ax^2+bx+c \equiv 0 \pmod p$ | `ecCuadratica(4,1,5,11)` → `3, 5` |

Command names and `Sí`/`No` answers are in Spanish because that was the specification of the original course assignment.

## Run it

```bash
python imatlab.py                                          # interactive
python imatlab.py examples/commands.txt out.txt            # batch
python -m unittest discover -s tests -v                    # tests
```

```python
import rsa

n, e, d = rsa.generar_claves(10**5, 10**6)
c = rsa.cifrar_cadena_rsa("hola mundo", n, e, 0)
rsa.descifrar_cadena_rsa(c, n, d, 0)    # 'hola mundo'
rsa.romper_clave(n, e) == d             # True: n is small enough to factor
```

## Testing

- `examples/` holds the 21 reference commands from the course statement with their expected output. All of them match.
- Property tests check Bézout's identity, that every square root really squares to $n$, CRT solutions against random systems, and negative exponents.
- During development the interpreter was also checked against SymPy on a few thousand large inputs (primality, factorisation, gcd, $\varphi$, powers, inverses), with no mismatches.

This is an educational implementation: Python's `random` is not a cryptographic RNG and the padding is not OAEP. Don't use it to protect anything.

## Authors

Liam Esgueva González and Sergio Fernández Cordero. Discrete Mathematics, BSc in Mathematical Engineering and AI, Comillas ICAI.
