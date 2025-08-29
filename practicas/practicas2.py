def invertir_cadena(cadena:str)-> str:
    invertida = ""
    for i in range(len(cadena)-1 ,-1,-1):
        invertida += cadena[i]

    return invertida
def es_palindromo(numero:int)-> bool:
    return str(numero) == str(numero)[::-1]

def elemento_unico(nums: list)-> int:
    diccionario: dict[int, int] = {}
    for i in nums:
        if i not in diccionario:
            diccionario[i] = 1
        elif i in diccionario:
            diccionario[i] += 1
        else:
            return 0
    
    for i , j  in diccionario.items(): # me tuvieron que ayudar aqui xd
        if j == 1:
            return i
    
def numero_faltante(nums : list[int])-> int:
    nums2 = sorted(nums)
    x : int = nums2[0] - 1
    for i in range(len(nums2)):
        x += 1
        if nums2[i] != x:
            return x

def pares(nums: list[int], n : int):
    lista_pares = set()
    numeros_vistos = set()
    for i in nums:
        if n - i > 0:
            complemento = n-i
            if complemento in numeros_vistos:
                par = tuple(sorted([i,complemento]))
                lista_pares.add(par)

        numeros_vistos.add(i)
    return lista_pares

def parentesis_balanceados(cadena : str)-> bool:
    contador = 0
    for i in cadena:
        match i:
            case "(":
                contador +=1
            case ")":
                contador -=1
            case _:
                return False #seria mejor poner que no es un parentesis pero ps el ejercicio pide booleanos
        if contador < 0 :
            return False
        
    return True

def parentesis_balanceados2(cadena : str)-> bool: # me tuvieron que ayudar :c
    parentesis = []
    diccionario = {")":"(","]":"[","}":"{"}
    for i in cadena:
        if i in "([{":
            parentesis.append(i)
        elif i in ")]}":
            if not parentesis or parentesis[-1] != diccionario[i]:
                return False
            parentesis.pop()
    return len(parentesis) == 0

def fizzbuzz(n : int)->None:
    for i in range(1,n+1,1):
        if (i % 3) == 0 and (i % 5) == 0:
            print("FizzBuzz")
        elif (i % 3) == 0:
            print("Fizz")
        elif (i % 5) == 0:
            print("Buzz")
        else:
            print(i)

def son_anagramas(str1 : str, str2 :str)->bool:
    return sorted(str1) == sorted(str2)

def fibonacci(n: int)->list: # me tuvieron que ayudar para imprimir la lista ;-;
    lista:list[int]
    if n==0:
        return [0]
    elif n == 1:
        return [0,1]
    a= 0
    b= 1
    lista = [0, 1]
    for i in range(2, n+1):
        temp = a + b
        lista.append(temp)
        a, b = b, temp
    return lista
                            

print(invertir_cadena("algoritmo"))

print(es_palindromo(121))
print(es_palindromo(122))

print(elemento_unico([4,1,2,1,2]))

# Prueba
print(numero_faltante([1, 2, 4, 6, 3, 7, 8]))  # Debería imprimir 5
print(numero_faltante([1, 2, 3, 5]))  # Debería imprimir 4

# Prueba
print(pares([1, 5, 7, 1, 8, 3, 5, 2], 10))  # Debería contar los pares (2,8), (5,5), (7,3)

# Pruebas
print(parentesis_balanceados("()"), parentesis_balanceados2("()"))        # Debería imprimir True
print(parentesis_balanceados("()[]{}"), parentesis_balanceados2("()[]{}"))    # Debería imprimir True
print(parentesis_balanceados("(]"), parentesis_balanceados2("(]"))        # Debería imprimir False
print(parentesis_balanceados("([)]"), parentesis_balanceados2("([)]"))      # Debería imprimir False
print(parentesis_balanceados("{[]}"), parentesis_balanceados2("{[]}"))      # Debería imprimir True

# Prueba
fizzbuzz(15)
# Salida esperada:
# 1
# 2
# Fizz
# 4
# Buzz
# Fizz
# 7
# 8
# Fizz
# Buzz
# 11
# Fizz
# 13
# 14
# FizzBuzz

#prueba
print(son_anagramas("anagrama", "naaagram"))  # Debería imprimir True
print(son_anagramas("hola", "adios"))         # Debería imprimir False
print(son_anagramas("roma", "amor"))          # Debería imprimir True

# Prueba
print(fibonacci(8))  # Debería imprimir [0, 1, 1, 2, 3, 5, 8, 13]