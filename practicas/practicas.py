def suma_pares(nums):
    x=0
    for i in range(len(nums)):
        if(nums[i] % 2 == 0):
            x += nums[i]
    return x

def suma_pares2(nums):
    return sum(i for i in nums if i % 2 == 0)

def invertir_cadenas(cadena):
    invertida = ""
    for i in range(len(cadena) -1, -1,-1):
        invertida += cadena[i]
    return invertida

def palindromo(numero):
    return numero == numero[::-1]

def fibonnacci(n):
    if n==0:
        return 0
    elif n == 1:
        return 1
    a= 0
    b= 1
    for i in range(2, n+1):
        temp = a + b
        a = b
        b= temp
    return b

def anagrama(palabra1, palabra2):
    return sorted(palabra1) == sorted(palabra2)

def parentesisBalanceado(cadena_parentesis):
    contador = 0
    for char in cadena_parentesis:
        if char == "(":
            contador +=1
        elif char == ")":
            contador -=1

        if contador < 0:
            return False
    
    return contador == 0

def contar_letras(palabra):
    diccionario = {}

    for char in palabra:
        if char not in diccionario:
            diccionario[char]= 1
        else:
            diccionario[char] +=1
    print(f"la palabra {palabra}")
    for letra in sorted(diccionario.keys()):
        print(f"la {letra} se repite {diccionario[letra]}")
    
    return 0

def cambio_minimo(n, monedas):
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # 0 monedas para formar 0

    for i in range(1, n + 1):
        for moneda in monedas:
            if i - moneda >= 0:
                dp[i] = min(dp[i], dp[i - moneda] + 1)
    print(dp)

    return dp[n] if dp[n] != float('inf') else -1  # -1 si no se puede formar





lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(f"la suma de los pares de la lista {lista} es : {suma_pares(lista)}")
print(f"la suma de los pares de la lista {lista} es : {suma_pares2(lista)}")

print(f"la palabra invertida hola es : {invertir_cadenas("hola")}")

print(f"el numero '2' (dos) es palindromo? : {palindromo("dos")}")

n = 7

print(f"la secuencia de fibonnacci del {n} es : {fibonnacci(n)}")

palabra1 = "hola"

palabra2 = "holo"

print(f"la palbra {palabra1} es anagrama de la palabra {palabra2}? : {anagrama(palabra1,palabra2)}")

cadena_parentesis = "((())"

print(f"la {cadena_parentesis} esta balanceada? : {parentesisBalanceado(cadena_parentesis)}")

palabra = "paraplejico"

contar_letras(palabra)

lista_monedas: list[int] = [1,2,5]

print(f"la lista de monedas minima para devolver {n} con la lista {lista_monedas} es : {cambio_minimo(n,lista_monedas)}")

