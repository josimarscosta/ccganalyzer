// Variáveis globais
let currentData = null;
let currentArea = '';
let charts = {};

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadAreas();
    loadInitialData();
});

// Carregar áreas disponíveis
async function loadAreas() {
    try {
        const response = await fetch('/api/enade/metadata');
        const data = await response.json();
        
        const select = document.getElementById('areaSelect');
        select.innerHTML = '<option value="">Visão Geral</option>';
        
        data.areas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao carregar áreas:', error);
    }
}

// Carregar dados iniciais
async function loadInitialData() {
    await updateAnalysis();
}

// Atualizar análise
async function updateAnalysis() {
    const area = document.getElementById('areaSelect').value;
    currentArea = area;
    
    // Mostrar loading
    showLoading();
    
    try {
        // Carregar análise abrangente
        await loadComprehensiveAnalysis(area);
        
        // Carregar prioridades de melhoria
        await loadImprovementPriorities(area);
        
        // Carregar comparação institucional
        await loadInstitutionalComparison(area);
        
    } catch (error) {
        console.error('Erro ao atualizar análise:', error);
        showError('Erro ao carregar dados. Tente novamente.');
    }
}

// Carregar análise abrangente
async function loadComprehensiveAnalysis(area) {
    const url = area ? `/api/enade/comprehensive-analysis?area=${encodeURIComponent(area)}` : '/api/enade/comprehensive-analysis';
    const response = await fetch(url);
    const data = await response.json();
    
    currentData = data;
    
    // Atualizar gráficos
    updateUniforQuestionsChart(data.unifor_analysis);
    updateDimensionChart(data.institutional_comparison);
    updateQuestionDetailsTable(data.improvement_priorities);
}

// Carregar prioridades de melhoria
async function loadImprovementPriorities(area) {
    const url = area ? `/api/enade/improvement-priorities?area=${encodeURIComponent(area)}` : '/api/enade/improvement-priorities';
    const response = await fetch(url);
    const data = await response.json();
    
    updatePrioritiesDisplay(data);
}

// Carregar comparação institucional
async function loadInstitutionalComparison(area) {
    const url = area ? `/api/enade/institutional-comparison?area=${encodeURIComponent(area)}` : '/api/enade/institutional-comparison';
    const response = await fetch(url);
    const data = await response.json();
    
    updateInstitutionalComparison(data);
}

// Atualizar display de prioridades
function updatePrioritiesDisplay(data) {
    const container = document.getElementById('prioritiesContainer');
    
    if (!data.priorities || data.priorities.length === 0) {
        container.innerHTML = '<div class="loading">Nenhuma prioridade identificada para esta área.</div>';
        return;
    }
    
    let html = '';
    
    data.priorities.slice(0, 8).forEach((priority, index) => {
        const priorityClass = index < 3 ? 'high' : index < 6 ? 'medium' : 'low';
        const gap = priority.gap_to_mean;
        const gapText = gap > 0 ? `+${gap.toFixed(3)}` : gap.toFixed(3);
        const gapClass = gap > 0 ? 'score-positive' : 'score-negative';
        
        html += `
            <div class="priority-item ${priorityClass}">
                <div class="priority-header">
                    <span class="priority-question">${priority.question} (${priority.dimension})</span>
                    <span class="priority-score">${priority.unifor_score.toFixed(3)}</span>
                </div>
                <div class="priority-details">
                    <strong>Gap vs Média Nacional:</strong> <span class="${gapClass}">${gapText}</span> | 
                    <strong>Percentil:</strong> ${priority.percentile_rank.toFixed(1)}% | 
                    <strong>Melhor IES:</strong> ${priority.top_performer ? priority.top_performer.institution : 'N/A'} 
                    (${priority.top_performer ? priority.top_performer.score.toFixed(3) : 'N/A'})
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Atualizar gráfico de questões UNIFOR
function updateUniforQuestionsChart(uniforAnalysis) {
    const ctx = document.getElementById('uniforQuestionsChart').getContext('2d');
    
    if (charts.uniforQuestions) {
        charts.uniforQuestions.destroy();
    }
    
    if (!uniforAnalysis || !uniforAnalysis.worst_questions) {
        return;
    }
    
    // Combinar piores e melhores questões
    const allQuestions = [
        ...uniforAnalysis.worst_questions.map(q => ({...q, type: 'Pior'})),
        ...uniforAnalysis.best_questions.map(q => ({...q, type: 'Melhor'}))
    ];
    
    const labels = allQuestions.map(q => q.question);
    const scores = allQuestions.map(q => q.score);
    const colors = allQuestions.map(q => q.type === 'Pior' ? '#e74c3c' : '#27ae60');
    
    charts.uniforQuestions = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Score UNIFOR',
                data: scores,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const item = allQuestions[context.dataIndex];
                            return [
                                `Score: ${item.score.toFixed(3)}`,
                                `Dimensão: ${item.dimension}`,
                                `Tipo: ${item.type}`
                            ];
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
                    ticks: {
                        maxRotation: 45
                    }
                }
            }
        }
    });
}

// Atualizar comparação institucional
function updateInstitutionalComparison(data) {
    const container = document.getElementById('institutionalComparison');
    
    if (!data || Object.keys(data).length === 0) {
        container.innerHTML = '<div class="loading">Dados de comparação não disponíveis.</div>';
        return;
    }
    
    let html = '<div class="institution-comparison">';
    
    Object.entries(data).forEach(([institution, scores]) => {
        const isUnifor = institution === 'UNIFOR';
        const cardClass = isUnifor ? 'style="border: 2px solid #667eea;"' : '';
        
        html += `
            <div class="institution-card" ${cardClass}>
                <div class="institution-name">${institution}</div>
                <div class="institution-score">${scores.GERAL ? scores.GERAL.toFixed(3) : 'N/A'}</div>
                <div style="font-size: 0.8em; color: #7f8c8d; margin-top: 5px;">
                    NOC: ${scores.NOC ? scores.NOC.toFixed(2) : 'N/A'} | 
                    NFC: ${scores.NFC ? scores.NFC.toFixed(2) : 'N/A'} | 
                    NAC: ${scores.NAC ? scores.NAC.toFixed(2) : 'N/A'}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Atualizar gráfico de dimensões
function updateDimensionChart(institutionalData) {
    const ctx = document.getElementById('dimensionChart').getContext('2d');
    
    if (charts.dimension) {
        charts.dimension.destroy();
    }
    
    if (!institutionalData || !institutionalData.UNIFOR) {
        return;
    }
    
    const dimensions = ['NOC', 'NFC', 'NAC'];
    const uniforScores = dimensions.map(dim => institutionalData.UNIFOR[dim] || 0);
    
    // Calcular média dos concorrentes
    const competitors = Object.entries(institutionalData).filter(([name]) => name !== 'UNIFOR');
    const competitorAvg = dimensions.map(dim => {
        const scores = competitors.map(([, data]) => data[dim] || 0).filter(score => score > 0);
        return scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    });
    
    charts.dimension = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'Organização Didático-Pedagógica',
                'Infraestrutura e Instalações',
                'Oportunidades de Ampliação'
            ],
            datasets: [
                {
                    label: 'UNIFOR',
                    data: uniforScores,
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: '#667eea',
                    borderWidth: 3,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                },
                {
                    label: 'Média Concorrentes',
                    data: competitorAvg,
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    borderColor: '#e74c3c',
                    borderWidth: 2,
                    pointBackgroundColor: '#e74c3c',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 6,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    },
                    pointLabels: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Atualizar tabela de detalhes das questões
function updateQuestionDetailsTable(prioritiesData) {
    const tbody = document.querySelector('#questionDetailsTable tbody');
    
    if (!prioritiesData || !prioritiesData.priorities) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading">Dados não disponíveis.</td></tr>';
        return;
    }
    
    let html = '';
    
    prioritiesData.priorities.slice(0, 10).forEach(priority => {
        const gap = priority.gap_to_mean;
        const gapText = gap > 0 ? `+${gap.toFixed(3)}` : gap.toFixed(3);
        const gapClass = gap > 0 ? 'score-positive' : 'score-negative';
        
        html += `
            <tr>
                <td><strong>${priority.question}</strong></td>
                <td><span style="background: #f8f9fa; padding: 4px 8px; border-radius: 4px;">${priority.dimension}</span></td>
                <td><strong>${priority.unifor_score.toFixed(3)}</strong></td>
                <td>${priority.national_mean.toFixed(3)}</td>
                <td class="${gapClass}">${gapText}</td>
                <td>${priority.percentile_rank.toFixed(1)}%</td>
                <td>${priority.top_performer ? priority.top_performer.institution : 'N/A'}<br>
                    <small>(${priority.top_performer ? priority.top_performer.score.toFixed(3) : 'N/A'})</small>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

// Carregar top instituições
async function loadTopInstitutions() {
    try {
        const response = await fetch('/api/enade/similar-institutions' + (currentArea ? `?area=${encodeURIComponent(currentArea)}` : ''));
        const data = await response.json();
        
        const container = document.getElementById('topInstitutions');
        
        if (!data.institutions || data.institutions.length === 0) {
            container.innerHTML = '<div class="loading">Nenhuma instituição similar encontrada.</div>';
            return;
        }
        
        let html = '<div style="display: grid; gap: 10px;">';
        
        data.institutions.slice(0, 5).forEach((institution, index) => {
            html += `
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600;">${index + 1}. ${institution}</span>
                    <span style="background: #27ae60; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.9em;">Benchmark</span>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Erro ao carregar top instituições:', error);
        document.getElementById('topInstitutions').innerHTML = '<div class="loading">Erro ao carregar dados.</div>';
    }
}

// Mostrar loading
function showLoading() {
    document.getElementById('prioritiesContainer').innerHTML = '<div class="loading">Carregando prioridades...</div>';
    document.getElementById('institutionalComparison').innerHTML = '<div class="loading">Carregando comparação...</div>';
    document.getElementById('topInstitutions').innerHTML = '<div class="loading">Carregando benchmarks...</div>';
    document.querySelector('#questionDetailsTable tbody').innerHTML = '<tr><td colspan="7" class="loading">Carregando detalhes...</td></tr>';
}

// Mostrar erro
function showError(message) {
    const errorHtml = `<div style="color: #e74c3c; text-align: center; padding: 20px;">${message}</div>`;
    document.getElementById('prioritiesContainer').innerHTML = errorHtml;
}

// Carregar top instituições após carregar dados principais
setTimeout(() => {
    loadTopInstitutions();
}, 2000);

