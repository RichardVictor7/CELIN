from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Aula, Turma, Presenca
from django.contrib import messages
from django.db.models import Sum


# Create your views here.
@login_required
def excluir_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    aula.delete()

    messages.success(request,'aula excluida com sucesso')

    return redirect('presenca', turma_id=aula.turma.id)



@login_required
def editar_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    turma = aula.turma
    alunos = turma.alunos.all()

    alunos_com_faltas = []
    for aluno in alunos:
        frequencia = Presenca.objects.filter(aula=aula, aluno=aluno).first()
        faltas = frequencia.faltas if frequencia and frequencia.faltas > 0 else ''
        alunos_com_faltas.append((aluno, faltas))

    if request.method == "POST":

        aula.nome = request.POST.get("nome_aula")
        aula.data = request.POST.get("data_aula")
        aula.save()


        for aluno in alunos:
            faltas_str = request.POST.get(f"faltas_{aluno.id}", "")
            faltas = int(faltas_str) if faltas_str else 0

            frequencia, created = Presenca.objects.get_or_create(aula=aula, aluno=aluno)
            frequencia.faltas = faltas
            frequencia.save()


        return redirect("presenca", turma_id=turma.id)

    contexto = {
        "aula": aula,
        "turma": turma,
        "alunos_com_faltas": alunos_com_faltas,
    }

    return render(request, "editar_aula.html", contexto)


@login_required
def visualizar_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    alunos = aula.turma.alunos.all()

    alunos_com_faltas = []
    for aluno in alunos:
        frequencia = Presenca.objects.filter(aula=aula, aluno=aluno).first()

        faltas = frequencia.faltas if frequencia and frequencia.faltas > 0 else ''
        alunos_com_faltas.append((aluno, faltas))

    contexto = {
        'aula': aula,
        'alunos_com_faltas': alunos_com_faltas,
    }

    return render(request, 'visualizar_aula.html', contexto)



@login_required
def alunos_view(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = turma.alunos.all()

    for aluno in alunos:
        total_faltas = aluno.presencas.aggregate(total=Sum('faltas'))['total']
        aluno.faltas = total_faltas if total_faltas else 0  

    return render(request, "alunos.html", {"alunos": alunos})


