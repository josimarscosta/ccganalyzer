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

if __name__ == "__main__":
    # Teste da classe
    analyzer = ENADEAnalyzer('/home/ubuntu/upload/ResumoQuestionário.xlsx')
    
    print("=== ANÁLISE DOS MICRODADOS DO ENADE ===")
    print(f"Total de cursos: {len(analyzer.df)}")
    print(f"Cursos da UNIFOR: {len(analyzer.get_unifor_data())}")
    print(f"Áreas da UNIFOR: {analyzer.get_unifor_courses()}")
    
    # Comparação geral
    comparison = analyzer.compare_with_levels()
    print("\n=== COMPARAÇÃO POR DIMENSÕES ===")
    for level, scores in comparison.items():
        print(f"\n{level}:")
        for dimension, score in scores.items():
            print(f"  {dimension}: {score:.3f}")
    
    # Extremos para uma área específica
    print("\n=== ANÁLISE DE EXTREMOS (ADMINISTRAÇÃO) ===")
    extremes = analyzer.find_extremes(analyzer.df[analyzer.df['Área de Avaliação'] == 'ADMINISTRAÇÃO'])
    
    # Mostrar alguns exemplos
    for question in ['Q27', 'Q55', 'Q43']:
        if question in extremes['menores']:
            print(f"\n{question} - Menores valores:")
            for inst, score in extremes['menores'][question]:
                print(f"  {inst}: {score:.3f}")

