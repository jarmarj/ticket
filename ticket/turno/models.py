from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return '%s' % (self.username)

class Qr(models.Model):
    image = models.ImageField(upload_to='curps')
    

class Estatus(models.Model):
    estatus = models.CharField(max_length=50)
    
    def __str__(self):
        return self.estatus
    
class Municipio(models.Model):
    municipio = models.CharField(max_length=50)
    
    def __str__(self):
        return self.municipio

class Nivel(models.Model):
    nivel = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nivel

class Asunto(models.Model):
    asunto = models.CharField(max_length=100)
    
    def __str__(self):
        return self.asunto

class Turno(models.Model):
    curp = models.CharField(max_length=25)
    nombres = models.CharField(max_length=50)
    paterno = models.CharField(max_length=50)
    materno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    correo = models.EmailField(max_length=254)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name='niveles')
    asunto = models.ForeignKey(Asunto, on_delete=models.CASCADE, related_name='asuntos')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='municipios', null=True)
    status = models.ForeignKey(Estatus,  on_delete=models.CASCADE, related_name='status', null=True)
    turno = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"turno {str(self.turno)}"