from io import BytesIO
from django.db import models
from events.models import Event
from user.models import Perfil
import random
from datetime import datetime
from django.template import Context, Template
from storages.backends.gcloud import GoogleCloudStorage
from django.core.files.storage import default_storage
storage = GoogleCloudStorage()
import datetime
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def make_pdf(user, event, image):
    buffer = BytesIO()
    my_canvas = canvas.Canvas(buffer, pagesize=letter)

    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica-Bold', 12)
    my_canvas.drawString(30, 750,'TICKET')
    my_canvas.drawString(30, 735,'CULTUCAT')
    my_canvas.setFont('Helvetica', 12)
    #my_canvas.drawImage('images/CultuCat.png', 120, 735, width=30, height=30)
    my_canvas.drawString(437, 750,'DATE:')
    my_canvas.drawString(500, 750, event.dataIni.strftime('%d-%m-%Y'))
    my_canvas.line(490, 747, 580, 747)
    my_canvas.drawString(370, 725,'ORIGINAL PRICE:') #(275, 725,'ORIGINAL PRICE:')
    my_canvas.drawString(500, 725, str(event.preu))
    my_canvas.line(490,723, 580, 723)
    my_canvas.drawString(30, 703,'OWNER:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, user.first_name)
    my_canvas.drawString(30, 681,'EVENT:')
    my_canvas.line(120, 678, 580, 678)
    my_canvas.drawString(120, 681, event.nom)
    my_canvas.drawString(30, 659,'ADDRESS:')
    my_canvas.line(120, 656, 580, 656)
    my_canvas.drawString(120, 659, event.adreca)


    my_canvas.drawImage(image.url, 110, 210, width=400, height=400)

    my_canvas.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    name = user.username+"_"+str(event.id)+".pdf"

    reviewer(pdf_bytes, name)
    return "docs/"+name

def reviewer(file, filename):
    try:
        target_path = '/docs/' + filename
        file_object = BytesIO(file)
        path = storage.save(target_path, file_object)
        return storage.url(path)
    except Exception as e:
        print(str(e))
        return str(e)

IMAGE_CHOICES = [
        'images/EncontradoQR.png',
        'images/NanoQR.png',
        'images/GolasoQR.png',
        'images/PatacasQR.png',
    ]

def get_random_image():
    return random.choice(IMAGE_CHOICES)

class Ticket(models.Model):
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(default=get_random_image)
    pdf_url = models.FileField(upload_to='docs/', null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el Ticket primero
        if not self.pdf_url:  # Si no hay pdf_url, genera el PDF
            self.pdf_url = make_pdf(self.user, self.event, self.image)
            super().save(update_fields=['pdf_url']) # Guarda el Ticket de nuevo con el nuevo pdf_url

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['event__dataIni']
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"