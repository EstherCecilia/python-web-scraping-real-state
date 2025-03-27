import pandas as pd
import glob

def process_csv(path, output_file):
    files = glob.glob(f"{path}/*.csv")
    dfs = []
    
    for file in files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"Processed file: {file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    if dfs:
        pd.concat(dfs, ignore_index=True).to_csv(output_file, index=False)
        print(f"Combined files saved in {output_file}")
        return True
    return False

