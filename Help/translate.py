import random

cadenas = ""
def first_letter(cadena: str) -> int:
        for n, c in enumerate(cadena):
            if c.isalnum() and not c.isdigit(): return n
        return -1

while True:
    print("Generador de cadenas validas KRAVNIKA".center(60,'-'))
    cadena = input("Cadena en latino (Numeros no disponibles, ingresa un número para salir): ")

    if cadena.isdigit(): 
        break 
    kravnika = ""
    for _ in cadena.split(" "):
        first = first_letter(_)
        character = '"' if random.randint(0, 1) == 0 else "'"
        word = _[:first+1] + character + _[first+1:]
        if word.find('.') != -1:
            kravnika += word
        else: kravnika += word +":"
        
    if kravnika[-1] == ':':
        kravnika = kravnika[0:len(kravnika)-1] +'.'
        
    kravnika = kravnika.replace('¿', '?').replace('¡', '!')
    
    cadenas += kravnika + '\n'
    print("\nCadena agregada!")

if cadenas != "":
    with open('VALID_STRING.txt', 'w') as file:
        file.write(cadenas)

    print("Revisa el archivo \"VALID_STRINGS.txt\"")
else:
    print("Saliste sin generar ninguna cadena")