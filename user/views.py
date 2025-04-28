from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil
from django.utils import timezone
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class RegistroForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)
    cpf = forms.CharField(label='CPF', max_length=14)
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.DateInput(attrs={'type': 'date'}))
    tipo_conta = forms.ChoiceField(label='Tipo de Conta', choices=[('PESSOAL', 'Pessoal'), ('EMPRESA', 'Empresa')])

class PerfilForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = Perfil
        fields = ['cpf', 'data_nascimento']
        labels = {
            'cpf': 'CPF',
            'data_nascimento': 'Data de Nascimento',
        }
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

def index(request):
    return render(request, 'user/index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                messages.error(request, 'As senhas não coincidem.')
                return render(request, 'user/registro.html', {'form': form})
            
            # Criar usuário
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            
            # Criar perfil
            perfil = Perfil.objects.create(
                usuario=user,
                cpf=form.cleaned_data['cpf'],
                data_nascimento=form.cleaned_data['data_nascimento'],
                tipo_conta=form.cleaned_data['tipo_conta'],
                saldo=1000.00  # Saldo inicial para teste
            )
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    
    return render(request, 'user/registro.html', {'form': form})

@login_required
def dashboard(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    context = {
        'perfil': perfil,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def perfil(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    context = {
        'perfil': perfil,
    }
    return render(request, 'user/perfil.html', context)

@login_required
def editar_perfil(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            # Atualizar email do usuário
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            # Salvar perfil
            form.save()
            
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil, initial={'email': request.user.email})
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'user/editar_perfil.html', context)

@login_required
def trocar_conta(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        tipo_conta = request.POST.get('tipo_conta')
        
        # Verificar senha
        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            perfil = get_object_or_404(Perfil, usuario=request.user)
            perfil.tipo_conta = tipo_conta
            perfil.save()
            messages.success(request, f'Conta alterada para {perfil.get_tipo_conta_display()}.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Senha incorreta.')
    
    perfil = get_object_or_404(Perfil, usuario=request.user)
    context = {
        'perfil': perfil,
    }
    return render(request, 'user/trocar_conta.html', context)
