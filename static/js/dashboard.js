// Funções específicas para o dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na página de dashboard
    if (document.querySelector('.dashboard-container')) {
        // Animação para os cards do dashboard
        const dashboardCards = document.querySelectorAll('.dashboard-card');
        dashboardCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });

        // Atualizar saldo com animação
        const saldoElement = document.getElementById('saldo-atual');
        if (saldoElement) {
            const originalValue = parseFloat(saldoElement.getAttribute('data-value') || saldoElement.textContent.replace(/[^\d.-]/g, ''));
            saldoElement.setAttribute('data-value', originalValue);
            
            // Animação de contagem para o saldo
            const countUp = (target, start, end, duration) => {
                let startTimestamp = null;
                const step = (timestamp) => {
                    if (!startTimestamp) startTimestamp = timestamp;
                    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                    const currentValue = progress * (end - start) + start;
                    target.textContent = 'R$ ' + currentValue.toFixed(2);
                    if (progress < 1) {
                        window.requestAnimationFrame(step);
                    }
                };
                window.requestAnimationFrame(step);
            };
            
            countUp(saldoElement, 0, originalValue, 1000);
        }
    }

    // Verificar se estamos na página de transferências
    if (document.querySelector('.transferencias-container')) {
        // Destacar transações recentes
        const recentTransactions = document.querySelectorAll('.transaction-recent');
        recentTransactions.forEach(transaction => {
            transaction.classList.add('bg-light');
            setTimeout(() => {
                transaction.classList.remove('bg-light');
            }, 3000);
        });
    }

    // Verificar se estamos na página de cartões
    if (document.querySelector('.cartoes-container')) {
        // Efeito de flip para cartões
        const cartoes = document.querySelectorAll('.credit-card');
        cartoes.forEach(cartao => {
            cartao.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
        });
    }

    // Verificar se estamos na página de investimentos
    if (document.querySelector('.investimentos-container')) {
        // Atualizar valores de investimentos periodicamente (simulação)
        const investimentoValores = document.querySelectorAll('.investimento-valor');
        investimentoValores.forEach(valor => {
            const originalValue = parseFloat(valor.getAttribute('data-value'));
            setInterval(() => {
                const variation = (Math.random() * 0.5) - 0.25; // Variação entre -0.25% e 0.25%
                const newValue = originalValue * (1 + variation/100);
                valor.textContent = 'R$ ' + newValue.toFixed(2);
                
                // Adicionar classe para indicar aumento ou diminuição
                valor.classList.remove('text-success', 'text-danger');
                if (variation > 0) {
                    valor.classList.add('text-success');
                } else if (variation < 0) {
                    valor.classList.add('text-danger');
                }
            }, 5000); // Atualiza a cada 5 segundos
        });
    }
});
