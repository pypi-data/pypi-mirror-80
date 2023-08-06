# variables
__pack = 'htam'



# INFO function
def __print_info(func, ops = ''):
    o = '(x' + ops + ')'
    a = 34
    b = (a - len(__pack + '.' +  func + o))/2
    b1 = 0
    b2 = 0
    

    if b != int(b):
        b1 = int((a - len(__pack + '.' + func + o))//2)
        b2 = int((a - len(__pack + '.' + func + o))/2) - 1
    else:
        b1 = b2 = int((a - len(__pack + '.' + func + o))/2) - 1
    
    print('\n' + '|============= INFO =============|')
    print('|' + ' '*(a-2) + '|')
    print('|' + ' '*b1 + __pack + '.' + func + o + ' '*b2 + '|' + '')
    print('|' + ' '*(a-2) + '|')
    print('|================================|')



# Floor
def floor(x):
    '''\nthis function returns the greatest integer less or equal to x\nit returns "None" if the argument is not valid'''

    try:
        if x >= 0:
            return int(x)
        else:
            if int(x) == x:
                return int(x)
            else:
                return int(x) - 1
    except:
        return None



# Ceil
def ceil(x):
    '''\nthis function returns the least integer greater or equal to x\nit returns "None" if the argument is not valid'''

    try:
        if int(x) == x:
            return int(x)
        else:
            if x >= 0:
                return int(x) + 1
            else:
                return int(x)
    except:
        return None



# Fractional part
def frac(x):
    '''\nthis function returns the fractional part of a number as an integer\nit returns "None" if the argument is not valid'''

    try:
        power = 10 ** int(len(str(float(x))))
        ix = int(x)
        x *= power
        while x % 10 == 0:
            x /= 10
            power /= 10
        else:
            return int(x) - ix * int(power)
    except:
        return None



# Root
def root(x, y = 2):
    '''\ny is a number automatically set to 2\nthis function returns the yth root of x\nit returns "None" if 1 or more arguments are not valid'''

    try:
        return x**(1/y)
    except:
        return None



# Mod
def mod(x, y = 10, z = 0):
    '''\ny is an integer automatically set to 10\nz is an integer automatically set to 0\n
        \nthis function returns the solution to the equation
        \n      zk ≡ x (mod y)
        \nthe result will be k = "solution" (mod y) with "solution" returned
        \nthis function will return "None" if the equation has no solution, or if 1 or more arguments are not valid
        \nif z is missing or set to 0 this fuction will return
        \n        x (mod y)'''
    
    try:
        while True:
            z0 = z
            y0 = y
            while y > 0:
                z, y = y, z % y
                gcd_xy = z
            
            z = int(z0)
            y = int(y0)

            if gcd_xy == 1:
                if z == 0:
                    return x % y
                else:
                    inverse = 0
                    z = z % y
                    x = x % y
                    for i in range(1, y):
                        if z*i % y == 1:
                            inverse = i
                            break
                        else:
                            continue
                    return int((x*inverse) % y)
            else:
                try:
                    assert int(x/gcd_xy) == x/gcd_xy
                    x /= gcd_xy
                    z /= gcd_xy
                    y /= gcd_xy
                    continue
                except:
                    return None
    except:
        return None
    



# GCD
def gcd(x, y):
    '''this function returns the greatest common divisor of two numbers\nit returns "None" if 1 or more arguments are not valid'''

    try:
        while y > 0:
            x, y = y, x % y
        return x
    except:
        return None
    


# LCM
def lcm(x, y):
    '''this function returns the least common multiple of two numbers\nit returns "None" if 1 or more arguments are not valid'''

    try:
        if x > y:
            greater = x
        else:
            greater = y

        while True:
            if((greater % x == 0) and (greater % y == 0)):
                lcm_xy = greater
                break
            greater += 1

        return lcm_xy
    except:
        return None



# Divisors
def div(x, y = 1):
    '''\ny is an integer automatically set to 1\nthis function returns the number of divisors of x if y is 1 or missing
        \nit returns the list of divisors of x if y is 2\nit returns "None" if 1 or more arguments are not valid'''

    try:
        count = 0
        divlist = []

        for i in range(1, x + 1):
            if x % i == 0:
                count += 1
                divlist.append(i)
        
        if y == 1:
            return count
        elif y ==2:
            return divlist
        else:
            return None
    except:
        return None



# Prime
def prime(x):
    '''\nthis function returns the xth prime number\nit returns "None" if the argument is not valid'''

    try:
        primelist = [2]
        num = 3
        while len(primelist) < x:
            for p in primelist:
                if num % p == 0:
                    break
            else:
                primelist.append(num)
            num += 2
        return primelist[-1]
    except:
        return None



# Primes less than a given number
def pi(x, y=1):
    '''\nthis function returns the number of primes less than x if y is 1 or missing\nthis function returns the number of primes between y argument and x otherwise\nit returns "None" if 1 or more arguments are not valid'''

    try:
        count = 0
        def isprime(x):
            primecheck = 0

            if x == 2:
                primecheck = 1
                return primecheck
            else:
                for i in range(2, x):
                    if x % i == 0:
                        primecheck = 0
                        return primecheck
                    else:
                        primecheck = 1
            
            return primecheck
        
        for i in range(y, x):
            if bool(isprime(i)) == True:
                count += 1
        return count
    except:
        return None



# Factors
def primefac(x):
    '''\nthis function returns a list of x's prime factors\nit returns "None" if the argument is not valid'''
    try:
        factors = []

        primelist = [2]
        num = 3
        while len(primelist) < x:
            for p in primelist:
                if num % p == 0:
                    break
            else:
                primelist.append(num)
            num += 2

        while x != 1:
            for i in primelist:
                if x % i == 0:
                    factors.append(i)
                    x /= i

        factors.sort()
        return factors
    except:
        return None



# Factorial
def fac(x):
    '''\nthis function returns argument factorial'''
    prod = 1

    for i in range(1, x + 1):
        prod *= i
    
    return prod



# Collatz
def col(x):
    '''\nthis function returns a list containing each step of the Collatz Conjecture check process\nit returns "None" if the argument is not valid'''

    try:
        collist = []
        while x > 1:
            collist.append(int(x))
            if x % 2 == 0:
                x /= 2
            else:
                x = (3*x + 1)/2
        else:
            collist.append(int(x))
        return collist
    except:
        return None


funcdict = {
    'floor': floor,
    'ceil': ceil,
    'frac': frac,
    'root': root,
    'mod': mod,
    'gcd': gcd,
    'lcm': lcm,
    'div': div,
    'prime': prime,
    'pi': pi,
    'primefac': primefac,
    'fac': fac,
    'col': col,
}

# Info
def info(x = 0):
    '''
    run htam.info() to see general informations about htam functions
    '''
    if x == 0:
        print(
            '\n' + __pack.upper() + '\n'
            '\nver. 1.0.2\n '
            '\nHere\'s a list of functions ' + __pack + ' can perform. \n'
            )
        for i in funcdict.keys():
            print('>    ' + i)
        print(
            '\nrun ' + __pack + '.info(*function_name*) to see more detailed informations for that function.'
            )
    elif x in funcdict.keys():
        if x == 'root' or x == 'div' or x == 'gcd' or x == 'lcm' or x == 'pi':
            __print_info(x, ',y')
        elif x == 'mod':
            __print_info(x, ', y, z')
        else:
            __print_info(x)
        print(funcdict[x].__doc__)