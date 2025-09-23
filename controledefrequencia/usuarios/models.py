from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.TextField()

    def __str__(self):
        return self.nome