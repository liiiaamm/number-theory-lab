

"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP05A
Integrantes:
    - Sergio Fernández
    - Liam Esgueva

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict, Optional
import math
import random

class IncompatibleEquationError(Exception):
    pass
class UndefinedError(Exception):
    pass

def es_primo(n: int) -> bool:
    """
    Verifica si un número entero es primo.

    Args:
        n (int): El número entero a verificar.
    
    Returns:
        bool: True si el número es primo, False en caso contrario.
    
    Raises:
        None
    """
    if n <= 1:
        return False
    if n <= 3:
        return True  # 2 y 3 son primos
    if n % 2 == 0 or n % 3 == 0:
        return False  # Elimina múltiplos de 2 y 3
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6  # Solo considerar números de la forma 6k ± 1
    return True

def lista_primos(a: int, b: int) -> List[int]:
    """
    Genera una lista de números primos en el intervalo [a, b) usando la Criba de Eratóstenes.

    Args:
        a (int): Límite inferior del intervalo (incluido).
        b (int): Límite superior del intervalo (no incluido).
    
    Returns:
        List[int]: Lista ordenada de números primos mayores o iguales que a y menores que b.
    
    Raises:
        ValueError: Si los límites del intervalo no cumplen con 0 <= a < b.
    """
    if a < 0 or b <= a:
        raise ValueError("Los límites del intervalo deben ser: 0 <= a < b.")
    lista = [False, False] + [True for i in range(b-2)]  
    lim_sup_root = int(math.sqrt(b))
    for pos in range(2, lim_sup_root + 1):
        if lista[pos]:
            for multiplo in range(pos * pos, b, pos):
                lista[multiplo] = False
    primos = [numero for numero in range(b) if lista[numero] and numero >= a]
    return primos

def es_primo_miller_rabin(n: int, k: int = 6) -> bool:
    """
    Realiza el test de primalidad de Miller-Rabin para determinar si un número es primo.
    Args:
        n (int): Número a verificar si es primo.
        k (int): Número de iteraciones para asegurar la precisión del test.
                 Un número mayor de iteraciones reduce la probabilidad de error.
    Returns:
        bool: True si n es probablemente primo, False si es compuesto.
    """
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # Descomponemos n - 1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    # Realizamos k iteraciones del test
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = potencia_mod_p(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = potencia_mod_p(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def estimar_primos(x):
    """
    Estima la cantidad de números primos menores o iguales que x utilizando la fórmula aproximada x / log(x).

    Args:
        x (int): Número entero para el cual estimar el número de primos.

    Returns:
        int: Estimación de la cantidad de primos menores o iguales a x. Si x < 2, retorna 0.

    Raises:
        None
    """
    if x<2:
        return 0
    return int(x/math.log(x))

def factorizar(n:int)->Dict[int,int]:
    """
    Factoriza un número entero n en sus factores primos, devolviendo un diccionario donde las claves son los factores primos
    y los valores son sus exponentes correspondientes en la descomposición de n.

    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int, int]: Diccionario con los primos como claves y sus exponentes como valores.
            Si n = 0, retorna un diccionario vacío. Si n es negativo, incluye -1 como factor con exponente 1.
    
    Raises:
        None
    """
    if n == 0:  
        return {}
    factores = {}
    divisor = 2
    if n<0:
        n= abs(n)
        factores[-1] = 1
    limite_primos = estimar_primos(n)
    num_divisores_probados = 0
 
    while divisor*divisor <= n and  num_divisores_probados < limite_primos: 
        exponente = 0
        if divisor == 2:
            while n%2==0:
                n//=2
                exponente+=1
            if exponente > 0:
                factores[2] = exponente
                num_divisores_probados+=1
            divisor+=1
        exponente = 0
        if divisor == 3:
            while n % 3 == 0:
                n //=3
                exponente+=1
            if exponente > 0:
                factores[3] = exponente
                num_divisores_probados+=1
            divisor +=2
        #probamos 6n-1
        exponente = 0
        while n % divisor==0:
            n//= divisor
            exponente += 1
        if exponente > 0:
            factores[divisor] = exponente  
        exponente = 0
        while n % (divisor+2)==0:
            n//=(divisor+2)
            exponente+=1
        if exponente > 0:
            factores[divisor+2] = exponente
        divisor+=6
        num_divisores_probados += 2
    if n > 1:
        factores[n] = 1
    return factores

def factorizar_pollar_rho(n: int) -> Optional[List[int]]:
    """Factoriza un número n utilizando el algoritmo de Pollard's Rho.
    
    Args:
        n (int): Número a factorizar.
    
    Returns:
        Optional[List[int]]: Lista con dos factores primos de n si se encuentra, None si n es primo o no se encuentra factor.
    
    Raises:
        ValueError: Si n es menor o igual a 1.
    """
    if n <= 1:
        raise ValueError("n debe ser mayor que 1.")

    if n % 2 == 0:
        return [2]

    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    factores = []

    while d == 1:
        x = (potencia_mod_p(x, 2, n) + c) % n
        y = (potencia_mod_p(y, 2, n) + c) % n
        y = (potencia_mod_p(y, 2, n) + c) % n
        d = mcd(abs(x - y), n)

    if d != n:
        factores.append(d)
        p = d
        q = n // p
        if p != q:
            factores.append(q)
            return factores
    return None

def mcd(a: int, b: int) -> int:
    """
    Calcula el máximo común divisor (MCD) de dos enteros a y b utilizando el algoritmo de Euclides.

    El algoritmo de Euclides se basa en la idea de que el MCD de dos números no cambia si 
    el número más grande se reemplaza por su diferencia con el más pequeño. Esto es equivalente 
    a usar el resto de la división. El proceso se repite hasta que uno de los números se reduce a 0,
    y el otro número será el MCD.

    Args:
        a (int): Primer número entero.
        b (int): Segundo número entero.
    
    Returns:
        int: El máximo común divisor de a y b. Si uno de los números es 0, retorna el valor absoluto del otro.
    
    Raises:
        UndefinedError: Si ambos a y b son 0, ya que el MCD no está definido para este caso.
    """
    if a == 0 and b == 0:
        raise UndefinedError("El MCD no está definido para ambos números cero.")
    if a == b:
        return a
    while b != 0:
        a, b = b, a % b
    return abs(a)

def bezout(a, b):
    """
    Calcula el máximo común divisor (MCD) de dos enteros a y b, junto con los coeficientes de Bézout.

    Args:
        a (int): Primer número entero.
        b (int): Segundo número entero.
    
    Returns:
        Tuple[int, int, int]: Una tupla (d, x, y) donde:
            - d (int): El MCD de a y b.
            - x (int): El coeficiente correspondiente a a en la identidad de Bézout.
            - y (int): El coeficiente correspondiente a b en la identidad de Bézout.
    
    Raises:
        UndefinedError: Si ambos a y b son 0, ya que el MCD no está definido para este caso.
    """
    if a == 0 and b == 0:
        raise UndefinedError("El MCD no está definido para ambos números cero.")
    old_r, r = a, b  
    old_s, s = 1, 0
    old_t, t = 0, 1
 
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def mcd_n(nlist:List[int])->int:
    """
    Dada una lista de enteros, devuelve el máximo común divisor (MCD) de todos ellos.

    Args:
        nlist (List[int]): Lista de enteros.
    
    Returns:
        int: El máximo entero que divide a todos los enteros de la lista.

    Raises:
        ValueError: Si la lista está vacía.
    """
    if not nlist:
        raise ValueError("La lista no puede estar vacía.")
    a = nlist[0]
    for pos in range(1,len(nlist)):
       a = mcd(a,nlist[pos])
    return a

def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    """
    Dada una lista de enteros [a_1, ..., a_n], devuelve el máximo divisor común (d)
    a todos ellos y una lista de coeficientes [x_1, ..., x_n] tales que
    d = a_1*x_1 + ... + a_n*x_n.

    Args:
        nlist (List[int]): Lista de enteros.
    
    Returns:
        Tuple[int, List[int]]:
            d (int): El máximo entero que divide a todos los enteros de la lista.
            X (List[int]): Lista de coeficientes [x_1, ..., x_n].

    Raises:
        ValueError: Si la lista está vacía.
    """
    if not nlist:
        raise ValueError("La lista no puede estar vacía.")
    if len(nlist) == 1:
        return nlist[0], [1]
    gcd, x1, x2 = bezout(nlist[0], nlist[1])
    coefficients = [x1, x2]
 
    for i in range(2, len(nlist)):
        gcd, xgcd, xi = bezout(gcd, nlist[i])
        coefficients = [coef * xgcd for coef in coefficients]
        coefficients.append(xi)
    return gcd, coefficients

def coprimos(n:int,m:int)->bool:
    """
    Determina si dos enteros son coprimos.

    Args:
        n (int): Primer entero.
        m (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None
    """
    if mcd(n,m) == 1:
        return True
    return False

def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """
    Calcula base^exp % p de forma eficiente usando exponenciación modular.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0.
        ValueError: Si el exponente es negativo y la base no es invertible módulo p.
    """
    if p == 0:
        raise ZeroDivisionError("El módulo no puede ser cero.")
    if exp < 0:
        base = inversa_mod_p(base % p, p)
        exp = -exp
    result = 1 % p
    base = base % p
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % p
        exp //= 2
        base = (base * base) % p
    return result

def inversa_mod_p(n:int,p:int)->int:
    """
    Calcula la inversa de n módulo p utilizando el algoritmo extendido de Euclides.

    Args:
        n (int): Número que se desea invertir.
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
        ValueError: Si n es 0, ya que no tiene inversa modular.
    """
    if p <= 0:
        raise ZeroDivisionError("El módulo debe ser positivo.")
    if n == 0:
        raise ValueError("0 no tiene inversa modular.")
    gcd, x, _ = bezout(n, p)
    if gcd != 1:
        raise ZeroDivisionError(f"{n} no tiene inversa módulo {p}.")
    return x % p


def euler(n:int)->int:
    """
    Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cuántos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises:
        ValueError: Si el número n no es positivo.
    """
    if n <= 0:
        raise ValueError("El número debe ser positivo.")
    if n==1:
        return 1
    factores = factorizar(n)
    for p in factores:
        n = n // p * (p - 1)  # aritmética entera: sin errores de redondeo para n grande
    return n

def legendre(n:int,p:int)->int:
    """
    Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de n módulo p:
            0 si es múltiplo de p,
            1 si es un cuadrado perfecto (distinto de 0) módulo p,
            -1 en caso contrario.

    Raises:
        ValueError: Si el número p no es primo.
        ZeroDivisionError: Si el módulo p es 0.
    """
    if not es_primo(p):
        raise ValueError("El número p debe ser un número primo.")
    if p == 0:
        raise ZeroDivisionError("El numero primo no puede ser cero.")
    n = n % p
    if n == 0:
        return 0
    exp = (p - 1) // 2
    result = potencia_mod_p(n, exp, p)
    if result == p - 1:
        return -1
    return result

def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    """
    Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    a_i * x = b_i (mod p_i)   i=1,...,n devolviendo un entero r y un módulo m tales que las soluciones del sistema 
    corresponden a todos los enteros x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r, m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        ValueError: Si alguna de las listas está vacía o si tienen diferente tamaño.
        IncompatibleEquationError: Si no es posible resolver el sistema.
        ZeroDivisionError: si el módulo es 0
    """
    if len(alist) != len(blist) or len(alist) != len(plist) or len(plist) != len(blist):
        raise ValueError("Las listas deben tener la misma longitud.")
    if not alist:
        raise ValueError("La lista no puede estar vacía.")
    n = len(alist)
    r, m = None, None  
    for i in range(n):
        a_i, b_i, p_i = alist[i], blist[i], plist[i]
        if p_i == 0:
            raise ZeroDivisionError("El módulo no puede ser cero.")
        d = mcd(a_i, p_i)
        if b_i % d != 0:
            raise IncompatibleEquationError("El sistema no tiene solución")
        a_i_prime = a_i // d
        b_i_prime = b_i // d
        p_i_prime = p_i // d
        inv = inversa_mod_p(a_i_prime, p_i_prime)
        x_i = (inv * b_i_prime) % p_i_prime
        if m is None:
            r, m = x_i, p_i_prime
        else:
            g = mcd(m, p_i_prime)
            if (x_i - r) % g != 0:
                raise IncompatibleEquationError("El sistema no tiene solución")
            lcm = m * p_i_prime // g
            _, s, _ = bezout(m // g, p_i_prime // g)
            k = ((x_i - r) // g * s) % (p_i_prime // g)
            r = (r + m * k) % lcm
            m = lcm
    return r % m, m

def raiz_mod_p(n: int, p: int) -> List[int]:
    """
    Calcula todas las raíces cuadradas de n módulo un primo p con el algoritmo de Tonelli-Shanks,
    válido para cualquier primo (no solo p ≡ 3 mod 4).

    Args:
        n (int): Número del que se quiere la raíz cuadrada.
        p (int): Número primo.

    Returns:
        List[int]: Raíces x con 0 <= x < p y x^2 ≡ n (mod p), ordenadas. Lista vacía si no existen.

    Raises:
        ValueError: Si p no es primo.
    """
    if not es_primo(p):
        raise ValueError("El módulo debe ser un número primo.")
    n %= p
    if n == 0 or p == 2:
        return [n]
    if legendre(n, p) != 1:
        return []
    # p - 1 = q * 2^s con q impar
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m, c, t, r = s, potencia_mod_p(z, q, p), potencia_mod_p(n, q, p), potencia_mod_p(n, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = potencia_mod_p(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return sorted({r, p - r})

def ecuacion_cuadratica(a: int, b: int, c: int, p: int):
    """
    Resuelve la ecuación cuadrática ax^2 + bx + c ≡ 0 (mod p), 
    donde p es un número primo.
    Devuelve las soluciones en módulo p.

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1, x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        ValueError: Si p no es primo.
        ZeroDivisionError: Si a es 0.
    """
    if not es_primo(p):
        raise ValueError("El valor de p debe ser un número primo")
    if a == 0:
        raise ZeroDivisionError("a no puede ser 0 en una ecuación cuadrática")
    discriminante = (b**2 - 4*a*c) % p
    raices = raiz_mod_p(discriminante, p)
    if not raices:
        return "NE"
    inverso_2a = inversa_mod_p(2 * a % p, p) if p != 2 else 1
    soluciones = sorted({(-b + r) * inverso_2a % p for r in raices})
    if p == 2:  # 2a ≡ 0 (mod 2): se comprueban directamente los dos candidatos
        soluciones = [x for x in (0, 1) if (a * x * x + b * x + c) % 2 == 0] or "NE"
    return tuple(soluciones)



