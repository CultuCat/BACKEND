from user.models import User
from discount.models import Discount
from trophy.models import Trophy

import string
import random

def verificar_y_otorgar_descuento(user_id, trofeo_nombre, count_check):
    t_comments = Trophy.objects.get(nom=trofeo_nombre)
        
    if count_check == t_comments.punts_nivell1:
        nivell = 1
    elif count_check == t_comments.punts_nivell2:
        nivell = 2
    elif count_check == t_comments.punts_nivell3:
        nivell = 3
    else:
        nivell = None
        
    if nivell is not None:
        caracteres_validos_codigo = string.ascii_uppercase + string.digits
        codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
        while Discount.objects.filter(codi=codigo_descuento).exists():
            codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                
        Discount.objects.create(codi=codigo_descuento,userDiscount=User.objects.get(id=user_id),nivellTrofeu=nivell,nomTrofeu=trofeo_nombre,usat=False)