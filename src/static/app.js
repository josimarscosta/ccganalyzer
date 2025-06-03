// Variáveis globais
let currentData = null;
let charts = {};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    loadAreas();
    loadDashboardData();
});

// Carregar áreas disponíveis
async function loadAreas() {
    try {
        const response = await fetch('/api/enade/areas');
        const data = await response.json();
        
        const areaSelect = document.getElementById('areaSelect');
        areaSelect.innerHTML = '<option value="geral">Visão Geral</option>';
        
        data.unifor_areas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            areaSelect.appendChild(option);
        });
        
        areaSelect.addEventListener('change', function() {
            loadAnalysis();
        });
        
    } catch (error) {
        console.error('Erro ao carregar áreas:', error);
    }
}

// Carregar dados do dashboard
async function loadDashboardData() {
    try {
        const response = await fetch('/api/enade/dashboard-data');
        const data = await response.json();
        currentData = data;
        
        updateSummaryStats(data.summary);
        createComparisonChart(data.comparison_chart);
        createDimensionChart(data.unifor_performance);
        createCoursesChart(data.unifor_performance);
        updateDetailTable(data.comparison_chart);
        
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        showError('Erro ao carregar dados do dashboard');
    }
}

// Atualizar estatísticas resumo
function updateSummaryStats(summary) {
    const summaryStats = document.getElementById('summaryStats');
    summaryStats.innerHTML = `
        <div class="stat-item">
            <div class="stat-value">${summary.total_courses.toLocaleString()}</div>
            <div class="stat-label">Total de Cursos</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${summary.unifor_courses}</div>
            <div class="stat-label">Cursos UNIFOR</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${summary.unifor_areas}</div>
            <div class="stat-label">Áreas UNIFOR</div>
        </div>
    `;
}

// Criar gráfico de comparação
function createComparisonChart(data) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    
    if (charts.comparison) {
        charts.comparison.destroy();
    }
    
    const dimensions = ['NOC', 'NFC', 'NAC', 'GERAL'];
    const levels = ['UNIFOR', 'CEARA', 'NORDESTE', 'BRASIL'];
    const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c'];
    
    const datasets = levels.map((level, index) => ({
        label: level,
        data: dimensions.map(dim => data[level][dim] || 0),
        backgroundColor: colors[index],
        borderColor: colors[index],
        borderWidth: 2,
        borderRadius: 5
    }));
    
    charts.comparison = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dimensions.map(dim => getDimensionName(dim)),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(3)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 6,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Criar gráfico de dimensões
function createDimensionChart(data) {
    const ctx = document.getElementById('dimensionChart').getContext('2d');
    
    if (charts.dimension) {
        charts.dimension.destroy();
    }
    
    const areas = data.map(course => course.area);
    const nocData = data.map(course => course.noc);
    const nfcData = data.map(course => course.nfc);
    const nacData = data.map(course => course.nac);
    
    charts.dimension = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: areas,
            datasets: [
                {
                    label: 'Organização Didático-Pedagógica',
                    data: nocData,
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: '#667eea',
                    borderWidth: 2
                },
                {
                    label: 'Infraestrutura e Instalações',
                    data: nfcData,
                    backgroundColor: 'rgba(118, 75, 162, 0.2)',
                    borderColor: '#764ba2',
                    borderWidth: 2
                },
                {
                    label: 'Oportunidades de Ampliação',
                    data: nacData,
                    backgroundColor: 'rgba(56, 142, 60, 0.2)',
                    borderColor: '#388e3c',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 6,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                }
            }
        }
    });
}

// Criar gráfico de cursos
function createCoursesChart(data) {
    const ctx = document.getElementById('coursesChart').getContext('2d');
    
    if (charts.courses) {
        charts.courses.destroy();
    }
    
    const areas = data.map(course => course.area);
    const scores = data.map(course => course.media_geral);
    
    charts.courses = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: areas,
            datasets: [{
                data: scores,
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#f5576c',
                    '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
                    '#ffecd2', '#fcb69f'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        generateLabels: function(chart) {
                            const data = chart.data;
                            return data.labels.map((label, index) => ({
                                text: `${label}: ${data.datasets[0].data[index].toFixed(2)}`,
                                fillStyle: data.datasets[0].backgroundColor[index],
                                strokeStyle: data.datasets[0].borderColor,
                                lineWidth: data.datasets[0].borderWidth,
                                index: index
                            }));
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed.toFixed(3)}`;
                        }
                    }
                }
            }
        }
    });
}

// Atualizar tabela de detalhes
function updateDetailTable(data) {
    const tbody = document.getElementById('detailTableBody');
    const dimensions = ['NOC', 'NFC', 'NAC', 'GERAL'];
    
    tbody.innerHTML = '';
    
    dimensions.forEach(dim => {
        const row = document.createElement('tr');
        const unifor = data.UNIFOR[dim] || 0;
        const ceara = data.CEARA[dim] || 0;
        const nordeste = data.NORDESTE[dim] || 0;
        const brasil = data.BRASIL[dim] || 0;
        const diff = unifor - brasil;
        
        row.innerHTML = `
            <td><span class="dimension-badge ${dim.toLowerCase()}">${getDimensionName(dim)}</span></td>
            <td><strong>${unifor.toFixed(3)}</strong></td>
            <td>${ceara.toFixed(3)}</td>
            <td>${nordeste.toFixed(3)}</td>
            <td>${brasil.toFixed(3)}</td>
            <td style="color: ${diff >= 0 ? '#27ae60' : '#e74c3c'}">
                ${diff >= 0 ? '+' : ''}${diff.toFixed(3)}
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// Carregar análise específica
async function loadAnalysis() {
    const selectedArea = document.getElementById('areaSelect').value;
    
    if (selectedArea === 'geral') {
        loadDashboardData();
        hideExtremes();
        return;
    }
    
    try {
        // Carregar comparação específica
        const compResponse = await fetch(`/api/enade/comparisons?area=${encodeURIComponent(selectedArea)}`);
        const compData = await compResponse.json();
        
        // Carregar extremos
        const extResponse = await fetch(`/api/enade/extremes?area=${encodeURIComponent(selectedArea)}`);
        const extData = await extResponse.json();
        
        // Atualizar gráficos
        createComparisonChart(compData);
        updateDetailTable(compData);
        showExtremes(selectedArea, extData);
        
    } catch (error) {
        console.error('Erro ao carregar análise:', error);
        showError('Erro ao carregar análise específica');
    }
}

// Mostrar análise de extremos
function showExtremes(area, data) {
    const extremesSection = document.getElementById('extremesSection');
    const selectedAreaSpan = document.getElementById('selectedArea');
    const extremesContent = document.getElementById('extremesContent');
    
    selectedAreaSpan.textContent = area;
    extremesSection.style.display = 'block';
    
    // Selecionar algumas questões importantes para mostrar
    const importantQuestions = ['Q27', 'Q55', 'Q43', 'Q30', 'Q60', 'Q45'];
    
    extremesContent.innerHTML = '';
    
    importantQuestions.forEach(question => {
        if (data.menores[question] && data.maiores[question]) {
            const questionDiv = document.createElement('div');
            questionDiv.style.gridColumn = 'span 2';
            questionDiv.style.marginBottom = '20px';
            
            questionDiv.innerHTML = `
                <h4 style="margin-bottom: 15px; color: #2c3e50;">
                    ${question} - ${getQuestionDimension(question)}
                </h4>
                <div class="extremes-grid">
                    <div class="extreme-card lowest">
                        <h5 style="color: #e74c3c; margin-bottom: 10px;">
                            <i class="fas fa-arrow-down"></i> Menores Valores
                        </h5>
                        <ul class="extreme-list">
                            ${data.menores[question].map(([inst, score]) => 
                                `<li><span>${inst}</span><span class="score">${score.toFixed(2)}</span></li>`
                            ).join('')}
                        </ul>
                    </div>
                    <div class="extreme-card highest">
                        <h5 style="color: #27ae60; margin-bottom: 10px;">
                            <i class="fas fa-arrow-up"></i> Maiores Valores
                        </h5>
                        <ul class="extreme-list">
                            ${data.maiores[question].map(([inst, score]) => 
                                `<li><span>${inst}</span><span class="score">${score.toFixed(2)}</span></li>`
                            ).join('')}
                        </ul>
                    </div>
                </div>
            `;
            
            extremesContent.appendChild(questionDiv);
        }
    });
}

// Esconder análise de extremos
function hideExtremes() {
    document.getElementById('extremesSection').style.display = 'none';
}

// Funções auxiliares
function getDimensionName(dim) {
    const names = {
        'NOC': 'Organização Didático-Pedagógica',
        'NFC': 'Infraestrutura e Instalações',
        'NAC': 'Oportunidades de Ampliação',
        'GERAL': 'Média Geral'
    };
    return names[dim] || dim;
}

function getQuestionDimension(question) {
    const nocQuestions = ['Q27', 'Q29', 'Q30', 'Q31', 'Q33', 'Q34', 'Q35', 'Q36', 'Q37', 'Q38', 'Q42', 'Q49', 'Q56'];
    const nfcQuestions = ['Q55', 'Q58', 'Q59', 'Q60', 'Q61', 'Q62', 'Q63', 'Q64', 'Q65', 'Q66', 'Q68'];
    const nacQuestions = ['Q43', 'Q44', 'Q45', 'Q46', 'Q47', 'Q52', 'Q53', 'Q67'];
    
    if (nocQuestions.includes(question)) return 'Organização Didático-Pedagógica';
    if (nfcQuestions.includes(question)) return 'Infraestrutura e Instalações Físicas';
    if (nacQuestions.includes(question)) return 'Oportunidades de Ampliação da Formação';
    return 'Questão';
}

function showError(message) {
    console.error(message);
    // Aqui você pode implementar uma notificação de erro mais elaborada
}

