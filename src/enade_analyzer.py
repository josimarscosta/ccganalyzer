import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json

class ENADEAnalyzer:
    """
    Classe para análise dos microdados do ENADE da Universidade de Fortaleza
    """
    
    def __init__(self, excel_path: str):
        """
        Inicializa o analisador com os dados da planilha
        """
        self.df = pd.read_excel(excel_path)
        self.setup_dimensions()
        
    def setup_dimensions(self):
        """
        Define as dimensões conforme a Nota Técnica nº 4/2023
        """
        # Organização Didático-Pedagógica (NOC)
        self.noc_questions = ['Q27', 'Q29', 'Q30', 'Q31', 'Q33', 'Q34', 'Q35', 
                             'Q36', 'Q37', 'Q38', 'Q42', 'Q49', 'Q56']
        
        # Infraestrutura e Instalações Físicas (NFC)  
        self.nfc_questions = ['Q55', 'Q58', 'Q59', 'Q60', 'Q61', 'Q62', 'Q63', 
                             'Q64', 'Q65', 'Q66', 'Q68']
        
        # Oportunidades de Ampliação da Formação (NAC)
        self.nac_questions = ['Q43', 'Q44', 'Q45', 'Q46', 'Q47', 'Q52', 'Q53', 'Q67']
        
        # Todas as questões
        self.all_questions = self.noc_questions + self.nfc_questions + self.nac_questions
        
    def get_unifor_data(self) -> pd.DataFrame:
        """
        Filtra dados da Universidade de Fortaleza
        """
        return self.df[self.df['Nome da IES'].str.contains('UNIVERSIDADE DE FORTALEZA', case=False, na=False)]
    
    def get_state_data(self, state: str = 'CE') -> pd.DataFrame:
        """
        Filtra dados por estado
        """
        return self.df[self.df['Sigla da UF'] == state]
    
    def get_region_data(self, region_states: List[str]) -> pd.DataFrame:
        """
        Filtra dados por região
        """
        return self.df[self.df['Sigla da UF'].isin(region_states)]
    
    def get_national_data(self) -> pd.DataFrame:
        """
        Retorna todos os dados nacionais
        """
        return self.df
    
    def calculate_dimension_scores(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calcula as médias por dimensão
        """
        scores = {}
        
        # Organização Didático-Pedagógica
        noc_scores = data[self.noc_questions].mean(axis=1)
        scores['NOC'] = noc_scores.mean()
        
        # Infraestrutura e Instalações Físicas
        nfc_scores = data[self.nfc_questions].mean(axis=1)
        scores['NFC'] = nfc_scores.mean()
        
        # Oportunidades de Ampliação da Formação
        nac_scores = data[self.nac_questions].mean(axis=1)
        scores['NAC'] = nac_scores.mean()
        
        # Média geral
        scores['GERAL'] = data['Média'].mean()
        
        return scores
    
    def find_extremes(self, data: pd.DataFrame, n: int = 4) -> Dict[str, Dict[str, List[Tuple[str, float]]]]:
        """
        Encontra os n menores e maiores valores por questão
        """
        extremes = {
            'menores': {},
            'maiores': {}
        }
        
        for question in self.all_questions:
            if question in data.columns:
                # Ordenar por questão
                sorted_data = data.sort_values(by=question, na_position='last')
                
                # N menores valores
                menores = []
                for _, row in sorted_data.head(n).iterrows():
                    if pd.notna(row[question]):
                        menores.append((row['Nome da IES'], row[question]))
                
                # N maiores valores
                maiores = []
                for _, row in sorted_data.tail(n).iterrows():
                    if pd.notna(row[question]):
                        maiores.append((row['Nome da IES'], row[question]))
                
                extremes['menores'][question] = menores
                extremes['maiores'][question] = maiores[::-1]  # Reverter para ordem decrescente
        
        return extremes
    
    def compare_with_levels(self, course_area: str = None) -> Dict[str, Dict[str, float]]:
        """
        Compara Universidade de Fortaleza com diferentes níveis
        """
        # Dados da Universidade de Fortaleza
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        # Dados do estado (Ceará)
        state_data = self.get_state_data('CE')
        if course_area:
            state_data = state_data[state_data['Área de Avaliação'] == course_area]
        
        # Dados da região Nordeste
        nordeste_states = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
        region_data = self.get_region_data(nordeste_states)
        if course_area:
            region_data = region_data[region_data['Área de Avaliação'] == course_area]
        
        # Dados nacionais
        national_data = self.get_national_data()
        if course_area:
            national_data = national_data[national_data['Área de Avaliação'] == course_area]
        
        comparison = {
            'UNIFOR': self.calculate_dimension_scores(unifor_data),
            'CEARA': self.calculate_dimension_scores(state_data),
            'NORDESTE': self.calculate_dimension_scores(region_data),
            'BRASIL': self.calculate_dimension_scores(national_data)
        }
        
        return comparison
    
    def get_course_areas(self) -> List[str]:
        """
        Retorna lista de áreas de avaliação disponíveis
        """
        return sorted(self.df['Área de Avaliação'].unique())
    
    def get_unifor_courses(self) -> List[str]:
        """
        Retorna lista de cursos da Universidade de Fortaleza
        """
        unifor_data = self.get_unifor_data()
        return sorted(unifor_data['Área de Avaliação'].unique())
    
    def generate_detailed_report(self, course_area: str = None) -> Dict:
        """
        Gera relatório detalhado de análise
        """
        report = {
            'metadata': {
                'course_area': course_area,
                'total_courses': len(self.df),
                'unifor_courses': len(self.get_unifor_data()),
                'dimensions': {
                    'NOC': 'Organização Didático-Pedagógica',
                    'NFC': 'Infraestrutura e Instalações Físicas',
                    'NAC': 'Oportunidades de Ampliação da Formação'
                }
            },
            'comparison': self.compare_with_levels(course_area),
            'extremes': self.find_extremes(self.df if not course_area else 
                                         self.df[self.df['Área de Avaliação'] == course_area]),
            'unifor_details': self.get_unifor_data().to_dict('records') if not course_area else
                             self.get_unifor_data()[self.get_unifor_data()['Área de Avaliação'] == course_area].to_dict('records')
        }
        
        return report
    
    def analyze_unifor_questions(self, course_area: str = None) -> Dict:
        """
        Analisa especificamente as questões da UNIFOR para identificar pontos fortes e fracos
        """
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        if unifor_data.empty:
            return {}
        
        # Calcular médias por questão para a UNIFOR
        unifor_questions = {}
        for question in self.all_questions:
            if question in unifor_data.columns:
                avg_score = unifor_data[question].mean()
                if pd.notna(avg_score):
                    unifor_questions[question] = {
                        'score': avg_score,
                        'dimension': self.get_question_dimension(question),
                        'courses_count': unifor_data[question].notna().sum()
                    }
        
        # Ordenar questões por score
        sorted_questions = sorted(unifor_questions.items(), key=lambda x: x[1]['score'])
        
        # Identificar 5 piores e 5 melhores
        worst_questions = sorted_questions[:5]
        best_questions = sorted_questions[-5:]
        
        return {
            'worst_questions': [
                {
                    'question': q,
                    'score': data['score'],
                    'dimension': data['dimension'],
                    'courses_count': data['courses_count']
                }
                for q, data in worst_questions
            ],
            'best_questions': [
                {
                    'question': q,
                    'score': data['score'],
                    'dimension': data['dimension'],
                    'courses_count': data['courses_count']
                }
                for q, data in best_questions
            ],
            'all_questions': unifor_questions
        }
    
    def get_question_dimension(self, question: str) -> str:
        """
        Retorna a dimensão de uma questão específica
        """
        if question in self.noc_questions:
            return 'NOC'
        elif question in self.nfc_questions:
            return 'NFC'
        elif question in self.nac_questions:
            return 'NAC'
        else:
            return 'UNKNOWN'
    
    def get_similar_institutions(self, course_area: str = None, limit: int = 10) -> List[str]:
        """
        Retorna lista de instituições similares para comparação
        """
        data = self.df.copy()
        if course_area:
            data = data[data['Área de Avaliação'] == course_area]
        
        # Filtrar por categoria administrativa similar (Privada)
        private_institutions = data[data['Categoria Administrativa'].str.contains('Privada', na=False)]
        
        # Ordenar por média geral e pegar as top instituições
        top_institutions = private_institutions.nlargest(limit, 'Média')
        
        return top_institutions['Nome da IES'].unique().tolist()
    
    def compare_with_specific_institutions(self, institutions: List[str], course_area: str = None) -> Dict:
        """
        Compara UNIFOR com instituições específicas
        """
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        comparison = {
            'UNIFOR': self.calculate_dimension_scores(unifor_data)
        }
        
        for institution in institutions:
            inst_data = self.df[self.df['Nome da IES'] == institution]
            if course_area:
                inst_data = inst_data[inst_data['Área de Avaliação'] == course_area]
            
            if not inst_data.empty:
                comparison[institution] = self.calculate_dimension_scores(inst_data)
        
        return comparison
    
    def get_question_comparison(self, question: str, course_area: str = None) -> Dict:
        """
        Compara uma questão específica entre UNIFOR e outras instituições
        """
        data = self.df.copy()
        if course_area:
            data = data[data['Área de Avaliação'] == course_area]
        
        # Score da UNIFOR
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        unifor_score = unifor_data[question].mean() if question in unifor_data.columns else None
        
        # Estatísticas gerais da questão
        question_stats = {
            'unifor_score': unifor_score,
            'national_mean': data[question].mean(),
            'national_std': data[question].std(),
            'national_min': data[question].min(),
            'national_max': data[question].max(),
            'percentile_25': data[question].quantile(0.25),
            'percentile_50': data[question].quantile(0.50),
            'percentile_75': data[question].quantile(0.75),
            'dimension': self.get_question_dimension(question)
        }
        
        # Posição da UNIFOR no ranking
        if unifor_score:
            better_count = (data[question] < unifor_score).sum()
            total_count = data[question].notna().sum()
            percentile_rank = (better_count / total_count) * 100 if total_count > 0 else 0
            question_stats['unifor_percentile'] = percentile_rank
        
        return question_stats
    
    def get_top_institutions_by_question(self, question: str, course_area: str = None, limit: int = 10) -> List[Dict]:
        """
        Retorna as top instituições para uma questão específica
        """
        data = self.df.copy()
        if course_area:
            data = data[data['Área de Avaliação'] == course_area]
        
        # Filtrar dados válidos para a questão
        valid_data = data[data[question].notna()].copy()
        
        # Ordenar por score da questão
        top_institutions = valid_data.nlargest(limit, question)
        
        result = []
        for _, row in top_institutions.iterrows():
            result.append({
                'institution': row['Nome da IES'],
                'score': row[question],
                'state': row['Sigla da UF'],
                'category': row['Categoria Administrativa'],
                'participants': row['Nº  de Concluintes Participantes']
            })
        
        return result
    
    def identify_improvement_priorities(self, course_area: str = None) -> Dict:
        """
        Identifica prioridades de melhoria para a UNIFOR
        """
        unifor_analysis = self.analyze_unifor_questions(course_area)
        
        if not unifor_analysis:
            return {}
        
        priorities = []
        
        # Analisar cada questão pior da UNIFOR
        for q_data in unifor_analysis['worst_questions']:
            question = q_data['question']
            comparison = self.get_question_comparison(question, course_area)
            top_institutions = self.get_top_institutions_by_question(question, course_area, 5)
            
            # Calcular gap de melhoria
            if comparison['unifor_score'] and comparison['national_mean']:
                gap_to_mean = comparison['national_mean'] - comparison['unifor_score']
                gap_to_top = top_institutions[0]['score'] - comparison['unifor_score'] if top_institutions else 0
                
                priorities.append({
                    'question': question,
                    'dimension': q_data['dimension'],
                    'unifor_score': comparison['unifor_score'],
                    'national_mean': comparison['national_mean'],
                    'percentile_rank': comparison['unifor_percentile'],
                    'gap_to_mean': gap_to_mean,
                    'gap_to_top': gap_to_top,
                    'top_performer': top_institutions[0] if top_institutions else None,
                    'improvement_potential': gap_to_mean * 10  # Score de prioridade
                })
        
        # Ordenar por potencial de melhoria
        priorities.sort(key=lambda x: x['improvement_potential'], reverse=True)
        
        return {
            'priorities': priorities,
            'summary': {
                'total_questions_analyzed': len(priorities),
                'avg_gap_to_mean': sum(p['gap_to_mean'] for p in priorities) / len(priorities) if priorities else 0,
                'worst_dimension': max(priorities, key=lambda x: x['gap_to_mean'])['dimension'] if priorities else None
            }
        }

if __name__ == "__main__":
    # Teste das novas funcionalidades
    analyzer = ENADEAnalyzer('/home/ubuntu/upload/ResumoQuestionário.xlsx')
    
    print("=== ANÁLISE ESPECÍFICA DA UNIFOR ===")
    unifor_analysis = analyzer.analyze_unifor_questions('ADMINISTRAÇÃO')
    
    print("\n--- PIORES QUESTÕES DA UNIFOR ---")
    for q in unifor_analysis['worst_questions']:
        print(f"{q['question']} ({q['dimension']}): {q['score']:.3f}")
    
    print("\n--- MELHORES QUESTÕES DA UNIFOR ---")
    for q in unifor_analysis['best_questions']:
        print(f"{q['question']} ({q['dimension']}): {q['score']:.3f}")
    
    print("\n=== PRIORIDADES DE MELHORIA ===")
    priorities = analyzer.identify_improvement_priorities('ADMINISTRAÇÃO')
    
    for i, priority in enumerate(priorities['priorities'][:3], 1):
        print(f"\n{i}. {priority['question']} ({priority['dimension']})")
        print(f"   UNIFOR: {priority['unifor_score']:.3f}")
        print(f"   Média Nacional: {priority['national_mean']:.3f}")
        print(f"   Gap: {priority['gap_to_mean']:.3f}")
        if priority['top_performer']:
            print(f"   Melhor: {priority['top_performer']['institution']} ({priority['top_performer']['score']:.3f})")
    
    # Extremos para uma área específica
    print("\n=== ANÁLISE DE EXTREMOS (ADMINISTRAÇÃO) ===")
    extremes = analyzer.find_extremes(analyzer.df[analyzer.df['Área de Avaliação'] == 'ADMINISTRAÇÃO'])
    
    # Mostrar alguns exemplos
    for question in ['Q27', 'Q55', 'Q43']:
        if question in extremes['menores']:
            print(f"\n{question} - Menores valores:")
            for inst, score in extremes['menores'][question]:
                print(f"  {inst}: {score:.3f}")


    
    def analyze_unifor_questions(self, course_area: str = None) -> Dict:
        """
        Analisa especificamente as questões da UNIFOR para identificar pontos fortes e fracos
        """
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        if unifor_data.empty:
            return {}
        
        # Calcular médias por questão para a UNIFOR
        unifor_questions = {}
        for question in self.all_questions:
            if question in unifor_data.columns:
                avg_score = unifor_data[question].mean()
                if pd.notna(avg_score):
                    unifor_questions[question] = {
                        'score': avg_score,
                        'dimension': self.get_question_dimension(question),
                        'courses_count': unifor_data[question].notna().sum()
                    }
        
        # Ordenar questões por score
        sorted_questions = sorted(unifor_questions.items(), key=lambda x: x[1]['score'])
        
        # Identificar 5 piores e 5 melhores
        worst_questions = sorted_questions[:5]
        best_questions = sorted_questions[-5:]
        
        return {
            'worst_questions': [
                {
                    'question': q,
                    'score': data['score'],
                    'dimension': data['dimension'],
                    'courses_count': data['courses_count']
                }
                for q, data in worst_questions
            ],
            'best_questions': [
                {
                    'question': q,
                    'score': data['score'],
                    'dimension': data['dimension'],
                    'courses_count': data['courses_count']
                }
                for q, data in best_questions
            ],
            'all_questions': unifor_questions
        }
    
    def get_question_dimension(self, question: str) -> str:
        """
        Retorna a dimensão de uma questão específica
        """
        if question in self.noc_questions:
            return 'NOC'
        elif question in self.nfc_questions:
            return 'NFC'
        elif question in self.nac_questions:
            return 'NAC'
        else:
            return 'UNKNOWN'
    
    def get_similar_institutions(self, course_area: str = None, limit: int = 10) -> List[str]:
        """
        Retorna lista de instituições similares para comparação
        """
        data = self.df.copy()
        if course_area:
            data = data[data['Área de Avaliação'] == course_area]
        
        # Filtrar por categoria administrativa similar (Privada)
        private_institutions = data[data['Categoria Administrativa'].str.contains('Privada', na=False)]
        
        # Ordenar por média geral e pegar as top instituições
        top_institutions = private_institutions.nlargest(limit, 'Média')
        
        return top_institutions['Nome da IES'].unique().tolist()
    
    def compare_with_specific_institutions(self, institutions: List[str], course_area: str = None) -> Dict:
        """
        Compara UNIFOR com instituições específicas
        """
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        comparison = {
            'UNIFOR': self.calculate_dimension_scores(unifor_data)
        }
        
        for institution in institutions:
            inst_data = self.df[self.df['Nome da IES'] == institution]
            if course_area:
                inst_data = inst_data[inst_data['Área de Avaliação'] == course_area]
            
            if not inst_data.empty:
                comparison[institution] = self.calculate_dimension_scores(inst_data)
        
        return comparison
    
    def get_question_comparison(self, question: str, course_area: str = None) -> Dict:
        """
        Compara uma questão específica entre UNIFOR e outras instituições
        """
        data = self.df.copy()
        if course_area:
            data = data[data['Área de Avaliação'] == course_area]
        
        # Score da UNIFOR
        unifor_data = self.get_unifor_data()
        if course_area:
            unifor_data = unifor_data[unifor_data['Área de Avaliação'] == course_area]
        
        unifor_score = unifor_data[question].mean() if question in unifor_data.columns else None
        
        # Estatísticas gerais da questão
        question_stats = {
            'unifor_score': unifor_score,
            'national_mean': data[question].mean(),
            'national_std': data[question].std(),
            'national_min': data[question].min(),
            'national_max': data[question].max(),
            'percentile_25': data[question].quantile(0.25),
            'percentile_50': data[question].quantile(0.50),
            'percentile_75': data[question].quantile(0.75),
            'dimension': self.get_question_dimension(question)
        }
        
        # Posição da UNIFOR no ranking
        if unifor_score:
            better_count = (data[question] < unifor_score).sum()
            total_count = data[question].notna().sum()
            percentile_rank = (better_count / total_count) * 100 if total_count > 0 else 0
            question_stats['unifor_percentile'] = percentile_rank
        
        return question_stats
    
    def get_top_institutions_by_question(self, question: str, course_area: str = None, limit: int = 10) -> List[Dict]:
        """
        Retorna as top instituições para uma questão específica
        """
        data = self.df.copy()
        if course_area:
            data = data[data['Área de Avaliação'] == course_area]
        
        # Filtrar dados válidos para a questão
        valid_data = data[data[question].notna()].copy()
        
        # Ordenar por score da questão
        top_institutions = valid_data.nlargest(limit, question)
        
        result = []
        for _, row in top_institutions.iterrows():
            result.append({
                'institution': row['Nome da IES'],
                'score': row[question],
                'state': row['Sigla da UF'],
                'category': row['Categoria Administrativa'],
                'participants': row['Nº  de Concluintes Participantes']
            })
        
        return result
    
    def generate_comprehensive_analysis(self, course_area: str = None) -> Dict:
        """
        Gera análise abrangente incluindo todas as novas funcionalidades
        """
        # Análise das questões da UNIFOR
        unifor_analysis = self.analyze_unifor_questions(course_area)
        
        # Instituições similares
        similar_institutions = self.get_similar_institutions(course_area, 5)
        
        # Comparação com instituições específicas
        institutional_comparison = self.compare_with_specific_institutions(similar_institutions, course_area)
        
        # Análise detalhada das piores questões da UNIFOR
        worst_questions_analysis = {}
        if unifor_analysis.get('worst_questions'):
            for q_data in unifor_analysis['worst_questions']:
                question = q_data['question']
                worst_questions_analysis[question] = {
                    'unifor_data': q_data,
                    'comparison': self.get_question_comparison(question, course_area),
                    'top_institutions': self.get_top_institutions_by_question(question, course_area, 5)
                }
        
        return {
            'unifor_questions_analysis': unifor_analysis,
            'similar_institutions': similar_institutions,
            'institutional_comparison': institutional_comparison,
            'worst_questions_detailed': worst_questions_analysis,
            'metadata': {
                'course_area': course_area,
                'analysis_date': pd.Timestamp.now().isoformat(),
                'total_institutions_analyzed': len(similar_institutions) + 1
            }
        }

if __name__ == "__main__":
    # Teste das novas funcionalidades
    analyzer = ENADEAnalyzer('/home/ubuntu/upload/ResumoQuestionário.xlsx')
    
    print("=== ANÁLISE ESPECÍFICA DA UNIFOR ===")
    unifor_analysis = analyzer.analyze_unifor_questions('ADMINISTRAÇÃO')
    
    print("\n--- PIORES QUESTÕES DA UNIFOR ---")
    for q in unifor_analysis['worst_questions']:
        print(f"{q['question']} ({q['dimension']}): {q['score']:.3f}")
    
    print("\n--- MELHORES QUESTÕES DA UNIFOR ---")
    for q in unifor_analysis['best_questions']:
        print(f"{q['question']} ({q['dimension']}): {q['score']:.3f}")
    
    print("\n=== INSTITUIÇÕES SIMILARES ===")
    similar = analyzer.get_similar_institutions('ADMINISTRAÇÃO', 5)
    for inst in similar:
        print(f"- {inst}")
    
    print("\n=== COMPARAÇÃO COM INSTITUIÇÕES ESPECÍFICAS ===")
    comparison = analyzer.compare_with_specific_institutions(similar[:3], 'ADMINISTRAÇÃO')
    for inst, scores in comparison.items():
        print(f"\n{inst}:")
        for dim, score in scores.items():
            print(f"  {dim}: {score:.3f}")

