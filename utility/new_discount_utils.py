from user.models import Perfil
from discount.models import Discount
from trophy.models import Trophy

import string
import random

def random_discount():
    caracteres_validos_codigo = string.ascii_uppercase + string.digits
    codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
    while Discount.objects.filter(codi=codigo_descuento).exists():
        codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
        
    return codigo_descuento
    

def verificar_y_otorgar_descuento(user_id, trofeo_nombre, count_check):
    t_comments = Trophy.objects.get(nom=trofeo_nombre)
    new_points = 0
        
    switch = {
        t_comments.punts_nivell1: (1, 10),
        t_comments.punts_nivell2: (2, 50),
        t_comments.punts_nivell3: (3, 100)
    }

    nivell, new_points = switch.get(count_check, (None, None))
        
    if nivell is not None:
        #se suman los puntos
        u = Perfil.objects.get(id=user_id) 
        u.puntuacio += new_points
        u.save()
        
        codigo_descuento= random_discount()
          
        #trofeo dorado mirar si gana trofeo para el coleccionista  
        if nivell == 3:
            count_trophies_gold = Discount.objects.filter(nivellTrofeu=3, userDiscount=user_id).count()+1 #+1 pq todavía no se ha creado el descuento anterior
            t_trophies_gold = Trophy.objects.get(nom="Col·leccionista d'or")
            new_points2 = 0
            
            switch2 = {
                t_trophies_gold.punts_nivell1: (1, 10),
                t_trophies_gold.punts_nivell2: (2, 50),
                t_trophies_gold.punts_nivell3: (3, 100)
            }

            nivell2, new_points2 = switch2.get(count_trophies_gold, (None, None))
                
            if nivell2 is not None:
                u.puntuacio += new_points2
                u.save()
                
                codigo_descuento2= random_discount()                
                Discount.objects.create(codi=codigo_descuento2,userDiscount=Perfil.objects.get(id=user_id),nivellTrofeu=nivell2,nomTrofeu="Col·leccionista d'or",usat=False)
         
                
        Discount.objects.create(codi=codigo_descuento,userDiscount=Perfil.objects.get(id=user_id),nivellTrofeu=nivell,nomTrofeu=trofeo_nombre,usat=False)