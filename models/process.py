import pandas as pd
import glob

def process_csv(pasta, arquivo_saida):
    arquivos = glob.glob(f"{pasta}/*.csv")
    dfs = []
    
    for arquivo in arquivos:
        try:
            df = pd.read_csv(arquivo)
            dfs.append(df)
            print(f"Processado: {arquivo}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
    
    if dfs:
        pd.concat(dfs, ignore_index=True).to_csv(arquivo_saida, index=False)
        print(f"Arquivos combinados salvos em {arquivo_saida}")
        return True
    return False

