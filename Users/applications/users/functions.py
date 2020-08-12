# funciones extras de la aplicacion users

import random
import string

#genera un string es decir un codigo de 6 digitos en letras mayusculas que incluye numeros y letras
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) 

