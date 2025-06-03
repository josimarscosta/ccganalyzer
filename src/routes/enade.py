from flask import Blueprint, jsonify, request
import json
import os
from src.enade_analyzer import ENADEAnalyzer

enade_bp = Blueprint('enade', __name__)

# Carregar dados pré-processados
def load_web_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'web_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Inicializar analisador
def get_analyzer():
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'ResumoQuestionário.xlsx')
    return ENADEAnalyzer(excel_path)

@enade_bp.route('/metadata')
def get_metadata():
    """Retorna metadados da análise"""
    try:
        data = load_web_data()
        return jsonify(data['metadata'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/comparisons')
def get_comparisons():
    """Retorna comparações por área"""
    try:
        data = load_web_data()
        area = request.args.get('area', 'geral')
        
        if area in data['comparisons']:
            return jsonify(data['comparisons'][area])
        else:
            return jsonify({'error': 'Área não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/unifor-courses')
def get_unifor_courses():
    """Retorna dados dos cursos da UNIFOR"""
    try:
        data = load_web_data()
        return jsonify(data['unifor_courses'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/extremes')
def get_extremes():
    """Retorna análise de extremos por área"""
    try:
        data = load_web_data()
        area = request.args.get('area')
        
        if not area:
            return jsonify({'error': 'Parâmetro area é obrigatório'}), 400
        
        if area in data['detailed_analysis']:
            return jsonify(data['detailed_analysis'][area]['extremes'])
        else:
            return jsonify({'error': 'Área não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/course-detail')
def get_course_detail():
    """Retorna detalhes de um curso específico"""
    try:
        data = load_web_data()
        area = request.args.get('area')
        
        if not area:
            return jsonify({'error': 'Parâmetro area é obrigatório'}), 400
        
        # Encontrar curso da UNIFOR na área especificada
        unifor_course = None
        for course in data['unifor_courses']:
            if course['area'] == area:
                unifor_course = course
                break
        
        if not unifor_course:
            return jsonify({'error': 'Curso da UNIFOR não encontrado nesta área'}), 404
        
        # Adicionar dados de extremos
        result = {
            'course': unifor_course,
            'extremes': data['detailed_analysis'][area]['extremes'] if area in data['detailed_analysis'] else {},
            'comparison': data['comparisons'][area] if area in data['comparisons'] else {}
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/areas')
def get_areas():
    """Retorna lista de áreas disponíveis"""
    try:
        data = load_web_data()
        return jsonify({
            'all_areas': data['metadata']['course_areas'],
            'unifor_areas': data['metadata']['unifor_areas']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/dashboard-data')
def get_dashboard_data():
    """Retorna dados consolidados para o dashboard"""
    try:
        data = load_web_data()
        
        # Preparar dados para gráficos
        dashboard_data = {
            'summary': {
                'total_courses': data['metadata']['total_courses'],
                'unifor_courses': data['metadata']['unifor_courses'],
                'unifor_areas': len(data['metadata']['unifor_areas'])
            },
            'comparison_chart': data['comparisons']['geral'],
            'unifor_performance': [],
            'dimension_analysis': {
                'NOC': {'name': 'Organização Didático-Pedagógica', 'courses': []},
                'NFC': {'name': 'Infraestrutura e Instalações Físicas', 'courses': []},
                'NAC': {'name': 'Oportunidades de Ampliação da Formação', 'courses': []}
            }
        }
        
        # Dados de performance da UNIFOR por curso
        for course in data['unifor_courses']:
            course_perf = {
                'area': course['area'],
                'media_geral': course['media_geral'],
                'noc': course['scores']['NOC'],
                'nfc': course['scores']['NFC'],
                'nac': course['scores']['NAC']
            }
            dashboard_data['unifor_performance'].append(course_perf)
            
            # Adicionar aos dados de dimensão
            dashboard_data['dimension_analysis']['NOC']['courses'].append({
                'area': course['area'],
                'score': course['scores']['NOC']
            })
            dashboard_data['dimension_analysis']['NFC']['courses'].append({
                'area': course['area'],
                'score': course['scores']['NFC']
            })
            dashboard_data['dimension_analysis']['NAC']['courses'].append({
                'area': course['area'],
                'score': course['scores']['NAC']
            })
        
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@enade_bp.route('/unifor-analysis')
def get_unifor_analysis():
    """Retorna análise específica das questões da UNIFOR"""
    try:
        analyzer = get_analyzer()
        area = request.args.get('area')
        
        analysis = analyzer.analyze_unifor_questions(area)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/improvement-priorities')
def get_improvement_priorities():
    """Retorna prioridades de melhoria para a UNIFOR"""
    try:
        analyzer = get_analyzer()
        area = request.args.get('area')
        
        priorities = analyzer.identify_improvement_priorities(area)
        return jsonify(priorities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/similar-institutions')
def get_similar_institutions():
    """Retorna instituições similares para comparação"""
    try:
        analyzer = get_analyzer()
        area = request.args.get('area')
        limit = int(request.args.get('limit', 10))
        
        institutions = analyzer.get_similar_institutions(area, limit)
        return jsonify({'institutions': institutions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/institutional-comparison')
def get_institutional_comparison():
    """Compara UNIFOR com instituições específicas"""
    try:
        analyzer = get_analyzer()
        area = request.args.get('area')
        institutions_param = request.args.get('institutions', '')
        
        if institutions_param:
            institutions = institutions_param.split(',')
        else:
            # Usar instituições similares por padrão
            institutions = analyzer.get_similar_institutions(area, 5)
        
        comparison = analyzer.compare_with_specific_institutions(institutions, area)
        return jsonify(comparison)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/question-analysis')
def get_question_analysis():
    """Análise detalhada de uma questão específica"""
    try:
        analyzer = get_analyzer()
        question = request.args.get('question')
        area = request.args.get('area')
        
        if not question:
            return jsonify({'error': 'Parâmetro question é obrigatório'}), 400
        
        analysis = analyzer.get_question_comparison(question, area)
        top_institutions = analyzer.get_top_institutions_by_question(question, area, 10)
        
        return jsonify({
            'question_stats': analysis,
            'top_institutions': top_institutions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enade_bp.route('/comprehensive-analysis')
def get_comprehensive_analysis():
    """Análise abrangente incluindo todas as funcionalidades"""
    try:
        analyzer = get_analyzer()
        area = request.args.get('area')
        
        # Análise das questões da UNIFOR
        unifor_analysis = analyzer.analyze_unifor_questions(area)
        
        # Prioridades de melhoria
        priorities = analyzer.identify_improvement_priorities(area)
        
        # Instituições similares
        similar_institutions = analyzer.get_similar_institutions(area, 5)
        
        # Comparação institucional
        institutional_comparison = analyzer.compare_with_specific_institutions(similar_institutions, area)
        
        return jsonify({
            'unifor_analysis': unifor_analysis,
            'improvement_priorities': priorities,
            'similar_institutions': similar_institutions,
            'institutional_comparison': institutional_comparison,
            'metadata': {
                'area': area,
                'analysis_type': 'comprehensive'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

