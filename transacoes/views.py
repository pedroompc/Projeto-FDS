from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from decimal import Decimal
from user.models import Perfil
from .models import Transferencia, Cartao, Fatura, Transacao, Investimento, HistoricoInvestimento

class TransferenciaForm(forms.Form):
    destinatario = forms.CharField(label='Destinatário (username)', max_length=150)
    valor = forms.DecimalField(label='Valor', max_digits=10, decimal_places=2, min_value=0.01)
    tipo = forms.ChoiceField(label='Tipo', choices=[('PIX', 'Pix'), ('TED', 'TED'), ('DOC', 'DOC')])
    descricao = forms.CharField(label='Descrição', max_length=200, required=False)

class InvestimentoForm(forms.Form):
    TIPOS_INVESTIMENTO = [
        ('POUPANCA', 'Poupança'),
        ('CDB', 'CDB'),
        ('TESOURO', 'Tesouro Direto'),
        ('ACOES', 'Ações'),
        ('FUNDOS', 'Fundos de Investimento')
    ]
    
    tipo = forms.ChoiceField(label='Tipo de Investimento', choices=TIPOS_INVESTIMENTO)
    valor = forms.DecimalField(label='Valor', max_digits=10, decimal_places=2, min_value=100.00)

@login_required
def transferencias(request):
    transferencias_enviadas = Transferencia.objects.filter(remetente=request.user).order_by('-data')
    transferencias_recebidas = Transferencia.objects.filter(destinatario=request.user).order_by('-data')
    
    context = {
        'transferencias_enviadas': transferencias_enviadas,
        'transferencias_recebidas': transferencias_recebidas,
    }
    return render(request, 'transacoes/transferencias.html', context)


@login_required

    
@login_required
def nova_transferencia(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            destinatario_username = form.cleaned_data['destinatario']
            valor = form.cleaned_data['valor']
            
            try:
                destinatario = User.objects.get(username=destinatario_username)
                destinatario_perfil = Perfil.objects.get(usuario=destinatario)
            except (User.DoesNotExist, Perfil.DoesNotExist):
                messages.error(request, 'Destinatário não encontrado.')
                return render(request, 'transacoes/nova_transferencia.html', {'form': form, 'perfil': perfil})
            
            # Criar transferência
            transferencia = Transferencia.objects.create(
                remetente=request.user,
                destinatario=destinatario,
                valor=valor,
                tipo=form.cleaned_data['tipo'],
                descricao=form.cleaned_data['descricao']
            )
            
            # Atualizar saldos
            perfil.saldo -= valor
            perfil.save()
            
            destinatario_perfil.saldo += valor
            destinatario_perfil.save()
            
            messages.success(request, f'Transferência de R${valor} realizada com sucesso!')
            return redirect('detalhe_transferencia', transferencia_id=transferencia.id)
    else:
        form = TransferenciaForm()
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'transacoes/nova_transferencia.html', context)

@login_required
def detalhe_transferencia(request, transferencia_id):
    transferencia = get_object_or_404(Transferencia, id=transferencia_id)
    
    # Verificar se o usuário é o remetente ou destinatário
    if request.user != transferencia.remetente and request.user != transferencia.destinatario:
        messages.error(request, 'Você não tem permissão para visualizar esta transferência.')
        return redirect('transferencias')
    
    context = {
        'transferencia': transferencia,
    }
    return render(request, 'transacoes/detalhe_transferencia.html', context)

@login_required
def cartoes(request):
    cartoes = Cartao.objects.filter(usuario=request.user)
    
    context = {
        'cartoes': cartoes,
    }
    return render(request, 'transacoes/cartoes.html', context)

@login_required
def detalhe_cartao(request, cartao_id):
    cartao = get_object_or_404(Cartao, id=cartao_id, usuario=request.user)
    faturas = Fatura.objects.filter(cartao=cartao).order_by('-data_vencimento')
    transacoes = Transacao.objects.filter(cartao=cartao).order_by('-data')[:10]
    
    context = {
        'cartao': cartao,
        'faturas': faturas,
        'transacoes': transacoes,
    }
    return render(request, 'transacoes/detalhe_cartao.html', context)

@login_required
def faturas(request):
    cartoes = Cartao.objects.filter(usuario=request.user)
    faturas = Fatura.objects.filter(cartao__in=cartoes).order_by('-data_vencimento')
    
    context = {
        'faturas': faturas,
    }
    return render(request, 'transacoes/faturas.html', context)

@login_required
def detalhe_fatura(request, fatura_id):
    fatura = get_object_or_404(Fatura, id=fatura_id, cartao__usuario=request.user)
    transacoes = Transacao.objects.filter(fatura=fatura).order_by('-data')
    
    context = {
        'fatura': fatura,
        'transacoes': transacoes,
    }
    return render(request, 'transacoes/detalhe_fatura.html', context)

@login_required
def investimentos(request):
    investimentos = Investimento.objects.filter(usuario=request.user, ativo=True)
    
    # Atualizar valores dos investimentos
    for investimento in investimentos:
        investimento.atualizar_valor()
    
    context = {
        'investimentos': investimentos,
    }
    return render(request, 'transacoes/investimentos.html', context)

@login_required
def novo_investimento(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    
    if request.method == 'POST':
        form = InvestimentoForm(request.POST)
        if form.is_valid():
            valor = form.cleaned_data['valor']
            tipo = form.cleaned_data['tipo']
            
            # Verificar valor mínimo
            if valor < Decimal('100.00'):
                messages.error(request, 'O investimento mínimo é 100 reais.')
                return render(request, 'transacoes/novo_investimento.html', {'form': form, 'perfil': perfil})
            
            # Verificar saldo
            if perfil.saldo < valor:
                messages.error(request, 'Saldo insuficiente para realizar o investimento.')
                return render(request, 'transacoes/novo_investimento.html', {'form': form, 'perfil': perfil})
            
            # Definir rendimento com base no tipo
            rendimentos = {
                'POUPANCA': Decimal('6.17'),  # 6.17% ao ano
                'CDB': Decimal('10.65'),      # 10.65% ao ano
                'TESOURO': Decimal('11.75'),  # 11.75% ao ano
                'ACOES': Decimal('15.00'),    # 15% ao ano (estimativa)
                'FUNDOS': Decimal('12.50'),   # 12.5% ao ano (estimativa)
            }
            
            # Criar investimento
            investimento = Investimento.objects.create(
                usuario=request.user,
                tipo=tipo,
                valor_investido=valor,
                rendimento=rendimentos[tipo],
                valor_atual=valor,
                valor_resgate=valor * Decimal('0.9') if tipo != 'POUPANCA' else valor
            )
            
            # Criar histórico inicial
            HistoricoInvestimento.objects.create(
                investimento=investimento,
                valor=valor
            )
            
            # Atualizar saldo
            perfil.saldo -= valor
            perfil.save()
            
            messages.success(request, f'Investimento de R${valor} realizado com sucesso!')
            return redirect('detalhe_investimento', investimento_id=investimento.id)
    else:
        form = InvestimentoForm()
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    return render(request, 'transacoes/novo_investimento.html', context)

@login_required
def detalhe_investimento(request, investimento_id):
    investimento = get_object_or_404(Investimento, id=investimento_id, usuario=request.user)
    historico = HistoricoInvestimento.objects.filter(investimento=investimento).order_by('data')
    
    # Atualizar valor do investimento
    investimento.atualizar_valor()
    
    context = {
        'investimento': investimento,
        'historico': historico,
    }
    return render(request, 'transacoes/detalhe_investimento.html', context)
