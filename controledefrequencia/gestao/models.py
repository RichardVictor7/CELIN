from django.db import models
from usuarios.models import Aluno
from django.contrib.auth.models import User

# Create your models here.
class Turma(models.Model):
    nome = models.TextField()
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turmas')
    alunos = models.ManyToManyField(Aluno, related_name='turmas')

    def __str__(self):
        return self.nome
    
class Aula(models.Model):
    nome = models.TextField()
    data = models.DateField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='aulas')

    def __str__(self):
        return self.nome

class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='presencas')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='presencas')
    faltas = models.IntegerField(default=0)

    