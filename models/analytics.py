import pandas as pd
import numpy as np
import os
import re

def clean_price(price):
    if pd.isna(price) or str(price).strip() in ['N/A', 'Valor sob consulta']:
        return np.nan
    
    numbers = re.sub(r'[^\d]', '', str(price))
    return float(numbers) if numbers else np.nan

def clean_range(value):
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
    df = df[df['endereco'] != 'N/A'].copy()
    
    df['preco'] = df['preco'].apply(clean_price)
    df['area'] = df['area'].apply(clean_range)
    df['quartos'] = df['quartos'].apply(clean_range)
    df['banheiros'] = df['banheiros'].apply(clean_range)
    df['vagas'] = df['vagas'].apply(clean_range)
    
    df['bairro'] = df['endereco'].str.split(',').str[0].str.strip()
    
    df = df[~df['preco'].isna()].copy()
    
    return df

def analyze_properties(file_path):
    df = pd.read_csv(file_path)
    
    df = clean_data(df)
    
    output_dir = '../data/analytics'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    avg_price = df.groupby('bairro')['preco'].mean().sort_values(ascending=False)
    avg_price.to_csv(f'{output_dir}/valor_medio_por_bairro.csv')
    
    df['preco_m2'] = df['preco'] / df['area']
    avg_price_m2 = df.groupby('bairro')['preco_m2'].mean().sort_values(ascending=False)
    avg_price_m2.to_csv(f'{output_dir}/valor_por_metro_quadrado.csv')
    
    for feature in ['quartos', 'banheiros', 'vagas']:
        dist = df[feature].value_counts().sort_index()
        dist.to_csv(f'{output_dir}/distribuicao_{feature}.csv')
    
    correlation = df[['area', 'preco']].corr().iloc[0,1]
    pd.DataFrame({'correlacao': [correlation]}).to_csv(f'{output_dir}/correlacao_area_preco.csv')
    
    top5_expensive = avg_price.head(5)
    top5_cheapest = avg_price.tail(5)
    top5_expensive.to_csv(f'{output_dir}/top5_bairros_mais_caros.csv')
    top5_cheapest.to_csv(f'{output_dir}/top5_bairros_mais_baratos.csv')
    
    stats = df.describe()
    stats.to_csv(f'{output_dir}/estatisticas_descritivas.csv')
    
    df.to_csv(f'{output_dir}/dados_limpos.csv', index=False)
    
    print("\n=== ANALYSIS RESULTS ===\n")
    print(f"Total valid properties: {len(df)}")
    print(f"\nAverage price by neighborhood:\n{avg_price}")
    print(f"\nAverage price per m²:\n{avg_price_m2}")
    print(f"\nArea-price correlation: {correlation:.2f}")
    print(f"\nTop 5 most expensive neighborhoods:\n{top5_expensive}")
    print(f"\nTop 5 cheapest neighborhoods:\n{top5_cheapest}")
    print(f"\nCleaned data and analysis saved in the '{output_dir}' folder")

