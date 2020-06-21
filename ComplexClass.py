#!/usr/bin/env python3
"""A simple class for Complex Numbers
Obviously Python has built-in support for complex numbers. 
This class is created for educational purposes, 
to understand how OOP can be handled using Python.
This software is not error free, just like all the others. 

    Copyright (C) 2020 Exforge exforge@karasite.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Overload Methods:
__str__:        str() (string conversion) overload
__add__:        + (addition) overload
__radd__:       + (right addition) overload 
__mul__:        * (multiply) overload
__rmul__:       * (right multiply) overload
__neg__:        - (negative sign) overload
__pos__:        + (positive sign) overload
__sub__:        - (subtract) overload
__rsub__:       - (right subtract) overload
__truediv__:    / (division) overload
__rtruediv__:   / (right division) overload
__eq__:         == (equal) overload
__neq__:        != (not equal) overload
__abs__:        abs() (absolute) overload

Other Methods:
conjugate:      conjugate of the complex number
re:             real part of the complex number
real:           alias for re
im:             imaginery part of the complex number
imaginery:      alias for im
sqrt:           first squareroot of the complex number
sqrtother:      second squareroot of the complex number
sqrtall:        both squareroots of the complex number (as a tuple)
"""

class Complex:
    """Complex number a+bi

    attributes: a, b
    """
    def __init__(self, a=0, b=0):
        """Initialize complex number

        a: float or int
        b: float or int
        """
        self.a = a
        self.b = b

    def __str__(self):
        """Returns a string representation of the complex number.
        a + bi   a - bi  a  -a   bi   -bi   i   -i  0
        (-a)( )(+- )(-)(b)(i)  d1, d2, d3, d4, d5, d6
        
        d1 = "-a" or "a" or "0" or ""
        d2 = " " or ""
        d3 = "+ " or "- " or ""
        d4 = "" or "-"
        d5 = "b" or ""
        d6 = "i" or ""
        str() overload
        """
        
        # Handle -0.0, I don't know why but it happens
        if self.a == -0.0:
            d1 = "0.0"
        else:
            d1 = str(self.a)
        d2 = " "
        d3 = "+ "
        d4 = ""
        d5 = str(abs(self.b))
        d6 = "i"

        # if imaginery part is negative, write the number as a - bi 
        if self.b < 0:
            d3 = "- "
        # if there is no imaginery part, write as a
        if self.b == 0 or self.b == 0.0:
            d2 = d3 = d4 = d5 = d6 = ""
        
        # if there is no real part
        if self.a == 0 or self.a == 0.0:
            # also if there is no imaginery part write as 0
            if self.b == 0 or self.b == 0.0:
                d2 = d3 = d4 = d5 = d6 = ""
            # if there is imaginery part, we should omit the 0 as real number,
            # omit +/- and add a - sign without spaces to b if it is negative
            else:
                d1 = d2 = d3 = ""
                if self.b < 0:
                    d4 = "-"
        
        # if b=1 or b=-1, instead of 1i write i
        if self.b == 1 or self.b == -1:
            d5 = ""

        # Prepare the full string and return it
        disp = d1 + d2 + d3 + d4 + d5 + d6
        return disp


    def __add__(self, other):
        """Adds two Complex numbers or a Complex number and a number.
        other: Complex or real  number 
        + (addition) overload
        """
        temp = Complex()
        if isinstance(other, Complex):
            temp.a = self.a + other.a
            temp.b = self.b + other.b
        else:
            temp.a = self.a + other
            temp.b = self.b
        return temp

    def __radd__(self, other):
        """Adds two Complex numbers or a complex number and a real number.
        Complex number is on the right now
        + (addition) overload on the right
        """
        return self.__add__(other)

    def __mul__(self, other):
        """Multiply two Complex numbers or a Complex number and a number.
        other: Complex or real  number 
        * (multiplication) overload
        """
        temp = Complex()
        if isinstance(other, Complex):
            temp.a = (self.a * other.a) - (self.b * other.b)
            temp.b = (self.a * other.b) + (self.b * other.a)
        else:
            temp.a = self.a * other
            temp.b = self.b * other
        return temp
    
    def __rmul__(self, other):
        """Multiply two Complex numbers or a Complex number and a number.
        Complex number is on the right now
        * (multiplication) overload on the right
        """
        return self.__mul__(other)

    def __neg__(self):
        """Negate the complex number
        - (sign) overload
        """
        temp = Complex()
        temp.a = self.a * -1
        temp.b = self.b * -1
        return temp

    def __pos__(self):
        """+C, return as it is, simply do nothing
        + (sign) overload, 
        """
        return self

    def __sub__(self, other):
        """Subtracts from the Complex Number, 
        another Complex number or a real number.
        - (subtraction) overload
        """
        temp = Complex()
        if isinstance(other, Complex):
            temp.a = self.a - other.a
            temp.b = self.b - other.b
        else:
            temp.a = self.a - other
            temp.b = self.b
        return temp

    def __rsub__(self, other):
        """Subtracts the complex number from 
        another complex number or real number
        Comlex number is on the right
        - (subtraction) overload on the right
        """
        temp = -self
        return self + other

    def __truediv__(self, other):
        """Divides the Complex Number, 
        with another Complex number or a real number.
        (a+bi)/(c+di) = (a+bi)(c-di)/(c**2+d**2)
        / (division) overload
        """

        temp = Complex()
        if isinstance(other, Complex):
            if other.a == 0 and other.b == 0:
                print("Division by 0")
                return None
            temp = self * other.conjugate()
            temp = temp / (other.a**2 + other.b**2)
            
        else:
            if other == 0:
                print("Division by 0")
                return None
            temp.a = self.a / other
            temp.b = self.b / other
        return temp

    def __rtruediv__(self, other):
        """Divides a complex or a real number
        by the Complex number
        Comlex number is on the right
        / (division) overload on the right
        """
        if self.a == 0 and self.b == 0:
            print("Division by 0")
            return None
        temp = self.inverse()   #Get 1/Complex and multiply with the other
        return temp * other

    def __eq__(self, other):
        """Returns true if the complex number 
        is equal to the other complex number
        == overload
        """
        if self.a == other.a and self.b == other.b:
            return True
        else:
            return False

    def __neq__(self, other):
        """Returns true if the complex number 
        is not equal to the other complex number
        != overload
        """
        if self.a != other.a or self.b != other.b:
            return True
        else:
            return False

    def __abs__(self):
        """Returns absolute value of the complex number
        (a**2 + b**2)**1/2
        abs() overload
        """
        return (self.a**2 + self.b**2)**0.5

    def conjugate(self):
        """Returns the conjugate of the complex number
        for a+bi return a-bi
        """
        temp = Complex()
        temp.a = self.a
        temp.b = -self.b
        return temp

    def inverse(self):
        """Returns 1/(Complex Number)
        1/(a+bi) = (a-bi)/(a**2+b**2)
        """
        temp = Complex()
        squares = self.a ** 2 + self.b ** 2
        temp.a = self.a / squares
        temp.b = (-1 * self.b) / squares
        return temp

    def re(self):
        """Returns real part of the complex number
        a + bi --> a
        """
        return self.a

    def real(self):
        """Returns real part of the complex number
        a + bi --> a
        alias for re
        """
        return self.re()

    def im(self):
        """Returns Imaginary part of the complex number
        a + bi --> b
        """
        return self.b

    def imaginery(self):
        """Returns real part of the complex number
        a + bi --> b
        alias for im
        """
        return self.im()

    """ Square root formula is:
    First:
        temp.a = sqrt((sqrt(a**2+b**2)+a)/2)
        temp.b = sqrt((sqrt(a**2+b**2)-a)/2)
        sign of temp.b must be the same as complex.b
    Second:
        -1 * First
    """ 
    def sqrt(self):
        """Return one of the squareroots of the complex number"""
        temp = Complex()
        temp.a = ((abs(self) + self.a) / 2) ** 0.5
        sign = 1
        if self.b < 0:
            sign = -1
        temp.b = (((abs(self) - self.a) / 2) ** 0.5) * sign
        return temp

    def sqrtother(self):
        """Return the other squareroot of the complex number"""
        temp = self.sqrt()
        temp = -temp
        return temp

    def sqrtall(self):
        """Return both of the squareroots of the complex number as a tuple"""
        return self.sqrt(), self.sqrtother()


"""Following lines are for testing only, you can safely delete them"""

a = Complex(0.0, 0.0)
b = Complex(0, 3)
c = Complex(0, -4)
d = Complex(2, 0)
e = Complex(-5, 0)
f = Complex(1, 2)
g = Complex(-1, 2)
h = Complex(1, -2)
i = Complex(-1, -2)
j = Complex(0, 1)
k = Complex(0, -1)
l = Complex(3, 1)
m = Complex(3, -1)
n = Complex(3, 4)

print("a:", a, end=" ")
print("b:", b, end=" ")
print("c:", c, end=" ")
print("d:", d, end=" ")
print("e:", e)
print("f:", f, end=" ")
print("g:", g, end=" ")
print("h:", h, end=" ")
print("i:", i, end=" ")
print("j:", j)
print("k:", k, end=" ")
print("l:", l, end=" ")
print("m:", m, end=" ")
print("n:", n)


ab = a + b
ax = a + 5
hi = h + i
ix = i + 5

print("a+b: ", ab, end=" ")
print("a+5: ", ax, end=" ")
print("h+i: ", hi, end=" ")
print("i+5: ", ix)

xf = 5 + f
xi = 1 + i

print("5+f:", xf, end=" ")
print("1+i:", xi, end=" ")
print("Conj b:", b.conjugate(), end=" ")
print("Conj l:", l.conjugate())

gh = g * h
ij = i * j
lm = l * m
g2 = g * 2
m3 = -3 * m


print("g*h:", gh, end=" ")
print("i*j:", ij, end=" ")
print("l*m:", lm, end=" ")
print("g*2:", g2, end=" ")
print("3*m:", m3,)

fg = f - g
gf = g - f
gh = g - h
f5 = f - 5
f6 = 1 - f

print("f-g:", fg, end=" ")
print("g-f:", gf, end=" ")
print("g-h:", gh, end=" ")
print("f-5:", f5, end=" ")
print("6-f:", f6)

fg = f / g
ce = c / e
h2 = h / 2
h3 = 3 / h
ba = b / a

print("f/g:", fg, end=" ")
print("c/e:", ce, end=" ")
print("h/2:", h2, end=" ")
print("3/h:", h3, end=" ")
print("b/a:", ba)

ff = f
gg = g
hh = h
ii = i

print("a:", a, end=" ")
print("b:", b, end=" ")
print("c:", c, end=" ")
print("d:", d, end=" ")
print("e:", e)
print("f:", f, end=" ")
print("g:", g, end=" ")
print("h:", h, end=" ")
print("i:", i, end=" ")
print("j:", j)
print("k:", k, end=" ")
print("l:", l, end=" ")
print("m:", m)

ff+= g
gg-= h
hh*= i
ii/= j

print("f+g:", ff, f+g, end=" ")
print("g-h:", gg, g-h, end=" ")
print("h*i:", hh, h*i, end=" ")
print("i/j:", ii, i/j)

print("abs(b):", abs(b), end=" ")
print("abs(g):", abs(g), end=" ")
print("abs(h):", abs(h), end=" ")
print("abs(n):", abs(n))

print("a.re():", a.re(), end=" ")
print("m.real():", m.real(), end=" ")
print("b.im():", b.im(), end=" ")
print("m.imaginery():", m.imaginery())

if f == f:
    print("f == f")
else:
    print("f != f")
if f == g:
    print("f == g")
else:
    print("f != g")

sq1a = a.sqrt()
sq2a = a.sqrtother()
sq1b = b.sqrt()
sq2b = b.sqrtother()
sq1d = d.sqrt()
sq2d = d.sqrtother()
sq1m = m.sqrt()
sq2m = m.sqrtother()

print("a:", a, "sqrta1:", sq1a, "sqrta1", sq2a)
print("b:", b, "sqrtb1:", sq1b, "sqrtb1", sq2b)
print("d:", d, "sqrtd1:", sq1d, "sqrtd1", sq2d)
print("m:", m, "sqrtm1:", sq1m, "sqrtm1", sq2m)

at = a.sqrtall()
bt = b.sqrtall()
dt = d.sqrtall()
mt = m.sqrtall()

print("tuple sqrt(a)", at[0], at[1])
print("tuple sqrt(b)", bt[0], bt[1])
print("tuple sqrt(d)", dt[0], bt[1])
print("tuple sqrt(m)", mt[0], mt[1])


a21 = sq1a * sq1a
a22 = sq2a * sq2a
b21 = sq1b * sq1b
b22 = sq2b * sq2b
d21 = sq1d * sq1d
d22 = sq2d * sq2d
m21 = sq1m * sq1m
m22 = sq2m * sq2m

print("a:", a, "a**0.5**2:", a21, a22)
print("b:", a, "b**0.5**2:", b21, b22)
print("d:", a, "d**0.5**2:", d21, d22)
print("m:", a, "m**0.5**2:", m21, m22)

