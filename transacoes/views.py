from django.shortcuts import render

def home(request):
    return render(request, 'transacoes/home.html')

def transferencia_pix(request):
    if request.method == 'POST':
        chave_pix = request.POST.get('chave_pix')
        valor = request.POST.get('valor')
        descricao = request.POST.get('descricao')
        return render(request, 'transacoes/transferencia_pix.html', {
            'sucesso': True,
            'chave_pix': chave_pix,
            'valor': valor,
            'descricao': descricao,
        })
    return render(request, 'transacoes/transferencia_pix.html')
