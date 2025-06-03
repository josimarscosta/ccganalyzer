import json
import pandas as pd
from enade_analyzer import ENADEAnalyzer

def generate_web_data():
    """
    Gera dados estruturados para a aplicação web
    """
    analyzer = ENADEAnalyzer('/home/ubuntu/upload/ResumoQuestionário.xlsx')
    
    # Dados básicos
    web_data = {
        'metadata': {
            'total_courses': len(analyzer.df),
            'unifor_courses': len(analyzer.get_unifor_data()),
            'course_areas': analyzer.get_course_areas(),
            'unifor_areas': analyzer.get_unifor_courses(),
            'dimensions': {
                'NOC': {
                    'name': 'Organização Didático-Pedagógica',
                    'questions': analyzer.noc_questions
                },
                'NFC': {
                    'name': 'Infraestrutura e Instalações Físicas',
                    'questions': analyzer.nfc_questions
                },
                'NAC': {
                    'name': 'Oportunidades de Ampliação da Formação',
                    'questions': analyzer.nac_questions
                }
            }
        },
        'comparisons': {},
        'detailed_analysis': {}
    }
    
    # Comparação geral (todas as áreas)
    web_data['comparisons']['geral'] = analyzer.compare_with_levels()
    
    # Comparações por área da UNIFOR
    for area in analyzer.get_unifor_courses():
        web_data['comparisons'][area] = analyzer.compare_with_levels(area)
    
    # Análise detalhada por área
    for area in analyzer.get_unifor_courses():
        web_data['detailed_analysis'][area] = {
            'extremes': analyzer.find_extremes(
                analyzer.df[analyzer.df['Área de Avaliação'] == area]
            ),
            'unifor_data': analyzer.get_unifor_data()[
                analyzer.get_unifor_data()['Área de Avaliação'] == area
            ].to_dict('records')
        }
    
    # Dados da UNIFOR por curso
    unifor_data = analyzer.get_unifor_data()
    web_data['unifor_courses'] = []
    
    for _, course in unifor_data.iterrows():
        course_data = {
            'codigo': course['CO_CURSO'],
            'area': course['Área de Avaliação'],
            'participantes': course['Nº  de Concluintes Participantes'],
            'percentual_participacao': course['Percentual Participantes'],
            'media_geral': course['Média'],
            'scores': {
                'NOC': course[analyzer.noc_questions].mean(),
                'NFC': course[analyzer.nfc_questions].mean(),
                'NAC': course[analyzer.nac_questions].mean()
            },
            'questions': {}
        }
        
        # Adicionar todas as questões
        for question in analyzer.all_questions:
            if pd.notna(course[question]):
                course_data['questions'][question] = course[question]
        
        web_data['unifor_courses'].append(course_data)
    
    return web_data

def save_web_data():
    """
    Salva os dados para uso na aplicação web
    """
    data = generate_web_data()
    
    # Salvar como JSON
    with open('/home/ubuntu/web_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Dados salvos em web_data.json")
    print(f"Áreas da UNIFOR: {len(data['metadata']['unifor_areas'])}")
    print(f"Cursos da UNIFOR: {len(data['unifor_courses'])}")
    
    # Mostrar exemplo de comparação
    print("\n=== EXEMPLO DE COMPARAÇÃO (ADMINISTRAÇÃO) ===")
    if 'ADMINISTRAÇÃO' in data['comparisons']:
        admin_comp = data['comparisons']['ADMINISTRAÇÃO']
        for level, scores in admin_comp.items():
            print(f"{level}:")
            for dim, score in scores.items():
                print(f"  {dim}: {score:.3f}")
    
    return data

if __name__ == "__main__":
    save_web_data()

