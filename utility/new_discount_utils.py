from user.models import Perfil
from discount.models import Discount
from trophy.models import Trophy

import string
import random

def verificar_y_otorgar_descuento(user_id, trofeo_nombre, count_check):
    t_comments = Trophy.objects.get(nom=trofeo_nombre)
    new_points = 0
        
    if count_check == t_comments.punts_nivell1:
        nivell = 1
        new_points = 10
    elif count_check == t_comments.punts_nivell2:
        nivell = 2
        new_points = 50
    elif count_check == t_comments.punts_nivell3:
        nivell = 3
        new_points = 100
    else:
        nivell = None
        
    if nivell is not None:
        #se suman los puntos
        u = Perfil.objects.get(id=user_id) 
        u.puntuacio += new_points
        u.save()
        
        caracteres_validos_codigo = string.ascii_uppercase + string.digits
        codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
        while Discount.objects.filter(codi=codigo_descuento).exists():
            codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
          
        #trofeo dorado mirar si gana trofeo para el coleccionista  
        if nivell == 3:
            count_trophies_gold = Discount.objects.filter(nivellTrofeu=3, userDiscount=user_id).count()+1 #+1 pq todavía no se ha creado el descuento anterior
            t_trophies_gold = Trophy.objects.get(nom="Col·leccionista d'or")
            new_points2 = 0
            
            if count_trophies_gold == t_trophies_gold.punts_nivell1:
                nivell2 = 1
                new_points2 = 10
            elif count_trophies_gold == t_trophies_gold.punts_nivell2:
                nivell2 = 2
                new_points2 = 50
            elif count_trophies_gold == t_trophies_gold.punts_nivell3:
                nivell2 = 3
                new_points2 = 100
            else:
                nivell2 = None
                
            if nivell2 is not None:
                u.puntuacio += new_points2
                u.save()
                
                codigo_descuento2= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                while Discount.objects.filter(codi=codigo_descuento2).exists():
                    codigo_descuento2 = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                
                Discount.objects.create(codi=codigo_descuento2,userDiscount=Perfil.objects.get(id=user_id),nivellTrofeu=nivell2,nomTrofeu="Col·leccionista d'or",usat=False)
         
                
        Discount.objects.create(codi=codigo_descuento,userDiscount=Perfil.objects.get(id=user_id),nivellTrofeu=nivell,nomTrofeu=trofeo_nombre,usat=False)