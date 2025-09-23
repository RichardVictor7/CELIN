from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from gestao.models import Turma, Aula
from .models import Aluno
from gestao.models import Presenca

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    professor = request.user
    turmas = Turma.objects.filter(professor=professor)

    return render(request,'home.html', {'turmas':turmas})

@login_required
def presenca(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    # CORREÇÃO: usar 'turmas' (ManyToMany) e não 'turma'
    alunos = Aluno.objects.filter(turmas=turma).order_by("nome")
    aulas = Aula.objects.filter(turma=turma).order_by("-data")

    if request.method == "POST":
        nome_aula = request.POST.get("nome_aula")
        data_aula = request.POST.get("data_aula")

        # cria a aula
        aula = Aula.objects.create(
            turma=turma,
            nome=nome_aula,
            data=data_aula
        )

        # salva as faltas
        for aluno in alunos:
            faltas = request.POST.get(f"faltas_{aluno.id}", 0)
            if faltas == "":
                faltas = 0
            Presenca.objects.create(
                aula=aula,
                aluno=aluno,
                faltas=int(faltas)
            )

        return redirect("presenca", turma_id=turma.id)

    context = {
        "turma": turma,
        "alunos": alunos,
        "aulas": aulas,
    }
    return render(request, "presenca.html", context)
