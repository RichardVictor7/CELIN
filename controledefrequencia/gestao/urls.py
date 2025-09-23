from django.urls import path
from . import views

urlpatterns = [
    path('excluir_aula/<int:aula_id>', views.excluir_aula, name='excluir_aula'),
    path('view_alunos/<int:turma_id>',views.alunos_view, name="view_alunos"),
    path('visualizar_aula/<int:aula_id>', views.visualizar_aula, name='visualizar_aula'),
    path('editar_aula/<int:aula_id>', views.editar_aula, name='editar_aula')
]