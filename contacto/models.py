from django.db import models

class ContactMessage(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
