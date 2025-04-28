from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Topico, Comentario

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['titulo', 'descricao']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': 'Comentário',
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3}),
        }

@login_required
def listar_topicos(request):
    topicos = Topico.objects.all().order_by('-data_criacao')
    
    context = {
        'topicos': topicos,
    }
    return render(request, 'forum/listar_topicos.html', context)

@login_required
def novo_topico(request):
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.autor = request.user
            topico.save()
            
            messages.success(request, 'Tópico criado com sucesso!')
            return redirect('detalhe_topico', topico_id=topico.id)
    else:
        form = TopicoForm()
    
    context = {
        'form': form,
    }
    return render(request, 'forum/novo_topico.html', context)

@login_required
def detalhe_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    comentarios = Comentario.objects.filter(topico=topico).order_by('data_criacao')
    form = ComentarioForm()
    
    context = {
        'topico': topico,
        'comentarios': comentarios,
        'form': form,
    }
    return render(request, 'forum/detalhe_topico.html', context)

@login_required
def adicionar_comentario(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.topico = topico
            comentario.autor = request.user
            comentario.save()
            
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('detalhe_topico', topico_id=topico.id)
    
    return redirect('detalhe_topico', topico_id=topico.id)
