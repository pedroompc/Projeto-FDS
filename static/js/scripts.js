// Scripts personalizados para o OurBank

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers do Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Formatação de campos de moeda
    const currencyInputs = document.querySelectorAll('.currency-input');
    currencyInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (parseInt(value) / 100).toFixed(2);
            e.target.value = value;
        });
    });

    // Formatação de CPF
    const cpfInput = document.getElementById('id_cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) {
                value = value.substring(0, 11);
            }
            if (value.length > 9) {
                value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*/, '$1.$2.$3-$4');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{3})(\d{3})(\d{0,3}).*/, '$1.$2.$3');
            } else if (value.length > 3) {
                value = value.replace(/^(\d{3})(\d{0,3}).*/, '$1.$2');
            }
            e.target.value = value;
        });
    }

    // Animações para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });

    // Confirmação para operações importantes
    const confirmForms = document.querySelectorAll('.needs-confirmation');
    confirmForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = form.getAttribute('data-confirm-message') || 'Tem certeza que deseja continuar?';
            if (confirm(message)) {
                form.submit();
            }
        });
    });

    // Atualização de saldo em tempo real (simulação)
    const saldoElement = document.getElementById('saldo-atual');
    if (saldoElement) {
        // Apenas para demonstração - em um ambiente real, isso seria feito com WebSockets
        setInterval(() => {
            const currentValue = parseFloat(saldoElement.getAttribute('data-value'));
            const variation = (Math.random() * 0.2) - 0.1; // Variação entre -0.1 e 0.1
            const newValue = (currentValue + variation).toFixed(2);
            saldoElement.setAttribute('data-value', newValue);
            saldoElement.textContent = 'R$ ' + newValue;
        }, 30000); // Atualiza a cada 30 segundos
    }

    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Função para alternar entre modo claro e escuro (não implementada completamente)
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            // Aqui seria implementada a lógica para salvar a preferência do usuário
        });
    }
});

// Funções utilitárias para cálculos financeiros
const financialUtils = {
    // Calcula juros compostos
    compoundInterest: function(principal, rate, time) {
        return principal * Math.pow(1 + rate/100, time);
    },
    
    // Calcula prestações de empréstimo
    loanPayment: function(principal, rate, time) {
        const monthlyRate = rate / 100 / 12;
        return principal * monthlyRate * Math.pow(1 + monthlyRate, time) / (Math.pow(1 + monthlyRate, time) - 1);
    },
    
    // Formata valor como moeda
    formatCurrency: function(value) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    }
};

// Funções para gráficos (complementando o Chart.js)
const chartUtils = {
    // Gera cores aleatórias para gráficos
    generateColors: function(count) {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const hue = (i * 137) % 360; // Distribuição de cores pelo círculo cromático
            colors.push(`hsla(${hue}, 70%, 60%, 0.7)`);
        }
        return colors;
    },
    
    // Cria um gráfico de linha para histórico de saldo
    createBalanceChart: function(canvasId, dates, values) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Saldo',
                    data: values,
                    backgroundColor: 'rgba(13, 110, 253, 0.2)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value;
                            }
                        }
                    }
                }
            }
        });
    }
};
