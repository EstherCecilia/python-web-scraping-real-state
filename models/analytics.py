import pandas as pd
import numpy as np
import os
import re

def clean_price(price):
    """Converte valores de preço para numérico, tratando casos especiais"""
    if pd.isna(price) or str(price).strip() in ['N/A', 'Valor sob consulta']:
        return np.nan
    
    # Extrai apenas números
    numbers = re.sub(r'[^\d]', '', str(price))
    return float(numbers) if numbers else np.nan

def clean_range(value):
    """Converte valores em intervalo para a média (ex: '47-67' vira 57)"""
    if pd.isna(value) or str(value).strip() == 'N/A':
        return np.nan
    
    parts = str(value).split('-')
    if len(parts) == 1:
        try:
            return float(parts[0])
        except:
            return np.nan
    try:
        return (float(parts[0]) + float(parts[1])) / 2
    except:
        return np.nan

def clean_data(df):
    """Limpa e prepara os dados para análise"""
    # Remover linhas completamente vazias
    df = df[df['endereco'] != 'N/A'].copy()
    
    # Converter colunas numéricas
    df['preco'] = df['preco'].apply(clean_price)
    df['area'] = df['area'].apply(clean_range)
    df['quartos'] = df['quartos'].apply(clean_range)
    df['banheiros'] = df['banheiros'].apply(clean_range)
    df['vagas'] = df['vagas'].apply(clean_range)
    
    # Extrair bairro do endereço
    df['bairro'] = df['endereco'].str.split(',').str[0].str.strip()
    
    # Remover linhas sem preço válido
    df = df[~df['preco'].isna()].copy()
    
    return df

def analyze_properties(file_path):
    """Realiza análises nos dados de imóveis"""
    # Carregar dados
    df = pd.read_csv(file_path)
    
    # Limpar dados
    df = clean_data(df)
    
    # Criar diretório para análises
    output_dir = '../analytics'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 1. Valor médio por bairro
    avg_price = df.groupby('bairro')['preco'].mean().sort_values(ascending=False)
    avg_price.to_csv(f'{output_dir}/valor_medio_por_bairro.csv')
    
    # 2. Valor por metro quadrado
    df['preco_m2'] = df['preco'] / df['area']
    avg_price_m2 = df.groupby('bairro')['preco_m2'].mean().sort_values(ascending=False)
    avg_price_m2.to_csv(f'{output_dir}/valor_por_metro_quadrado.csv')
    
    # 3. Distribuição de características
    for feature in ['quartos', 'banheiros', 'vagas']:
        dist = df[feature].value_counts().sort_index()
        dist.to_csv(f'{output_dir}/distribuicao_{feature}.csv')
    
    # 4. Relação entre área e preço
    correlation = df[['area', 'preco']].corr().iloc[0,1]
    pd.DataFrame({'correlacao': [correlation]}).to_csv(f'{output_dir}/correlacao_area_preco.csv')
    
    # 5. Top bairros
    top5_expensive = avg_price.head(5)
    top5_cheapest = avg_price.tail(5)
    top5_expensive.to_csv(f'{output_dir}/top5_bairros_mais_caros.csv')
    top5_cheapest.to_csv(f'{output_dir}/top5_bairros_mais_baratos.csv')
    
    # 6. Estatísticas descritivas
    stats = df.describe()
    stats.to_csv(f'{output_dir}/estatisticas_descritivas.csv')
    
    # 7. Salvar dados limpos
    df.to_csv(f'{output_dir}/dados_limpos.csv', index=False)
    
    # Resultados
    print("\n=== RESULTADOS DA ANÁLISE ===\n")
    print(f"Total de imóveis válidos: {len(df)}")
    print(f"\nValor médio por bairro:\n{avg_price}")
    print(f"\nValor médio por m²:\n{avg_price_m2}")
    print(f"\nCorrelação área-preço: {correlation:.2f}")
    print(f"\nTop 5 bairros mais caros:\n{top5_expensive}")
    print(f"\nTop 5 bairros mais baratos:\n{top5_cheapest}")
    print(f"\nDados limpos e análises salvos na pasta '{output_dir}'")

