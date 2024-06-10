from django.shortcuts import render, redirect, get_object_or_404
from .forms import CriarUsuario, LogarUsuario, EmpresaForm, AvaliacaoForm
from .models import Empresa, Avaliacao
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def inicio(request):
    return render(request, 'crm/index.html')

def registro(request):
    form = CriarUsuario()
    if request.method == "POST":
        form = CriarUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crm:login")
    context = {'registroform': form}
    return render(request, 'crm/registro.html', context=context)

def login(request):
    form = LogarUsuario()
    if request.method == "POST":
        form = LogarUsuario(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("crm:dashboard")
    context = {'loginform': form}
    return render(request, 'crm/login.html', context=context)

def logout(request):
    auth_logout(request)
    return redirect("crm:inicio")

@login_required(login_url="crm:login")
def dashboard(request):
    empresas = Empresa.objects.all()
    if request.user.is_superuser:
        if request.method == "POST":
            form = EmpresaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("crm:dashboard")
        else:
            form = EmpresaForm()
        context = {'empresas': empresas, 'empresaform': form}
    else:
        context = {'empresas': empresas}
    return render(request, 'crm/dashboard.html', context=context)

@login_required(login_url="crm:login")
def empresa_detail(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    avaliacoes = Avaliacao.objects.filter(empresa=empresa)
    if request.method == "POST":
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.empresa = empresa
            avaliacao.usuario = request.user
            avaliacao.save()
            return redirect('crm:empresa_detail', empresa_id=empresa.id)
    else:
        form = AvaliacaoForm()
    context = {'empresa': empresa, 'avaliacoes': avaliacoes, 'avaliacaoform': form}
    return render(request, 'crm/empresa_detail.html', context=context)
