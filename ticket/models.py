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
    my_canvas.drawImage("https://storage.googleapis.com/cultucat_bucket/images/CultuCat.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=cultucatserviceaccount%40cultucat-405114.iam.gserviceaccount.com%2F20240108%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240108T170810Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=5b9c2580d700f7b898e7b609e145e72bdc7897ef5d069599b1d236562e7f465d269c30f73605fd3e340ecf56e361d7ac9d331ca1fae03127e64825860350853835569b3248e9dec6943e11e58995a96daed9e91c5c8715ee7ed33b606ab3fe9c3507883e82fb7ccb7783a010b7bd6a726c2a6bb7c16c07818fbf67d25c04cbd2d159acea9c18e0adeb512ea401d1006c3d12c3230a885477d7eda74dec88132046e7796bdaa2dbf0930bf8aac253968518319ba99b0ebc048e01cee299ed106b57d190ddf5d9cb33fe1930c47e65d69d9cab04d5f3762fc9a9778b2531b6e04c56a1b31ee16ec304f41c917f7cbcd81da688189b56863408a2e36f98d6d56d5b", 120, 735, width=30, height=30)
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