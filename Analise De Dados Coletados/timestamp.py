import pandas as pd
import os

# --- Configurações do Caminho do Arquivo ---
# Use barras normais ou barras duplas para o caminho em Windows.
# Exemplo para Windows: DATA_FILES_PATH = 'Analise De Dados Coletados\\TESTES\\teste'
# Exemplo para Linux/macOS: DATA_FILES_PATH = 'Analise De Dados Coletados/TESTES/teste'
DATA_FILES_PATH = 'Analise De Dados Coletados\TESTES\Individualmente\lombofaixa'
FILE_NAME = 'datalog5.txt' # Substitua pelo nome real do seu arquivo, se for diferente
DATA = 'Analise De Dados Coletados\DataLombofaixa'
# Constrói o caminho completo para o arquivo de entrada
file_path = os.path.join(DATA_FILES_PATH, FILE_NAME)

# --- Função para zerar os timestamps ---
def reset_timestamp(df):
    """
    Recebe um DataFrame e adiciona uma nova coluna 'timestamp_reset'
    com os timestamps zerados em relação ao primeiro timestamp do DataFrame.
    """
    if 'timestamp' not in df.columns:
        raise ValueError("O DataFrame deve conter uma coluna 'timestamp'.")
    min_timestamp = df['timestamp'].min()
    df['timestamp_reset'] = df['timestamp'] - min_timestamp
    return df

# --- Processamento do Arquivo ---
try:
    # 1. Ler o arquivo de entrada
    print(f"Tentando ler o arquivo: {file_path}")
    df_original = pd.read_csv(file_path)
    print("Arquivo lido com sucesso!")

    # 2. Processar o DataFrame (zerar os timestamps)
    df_reset = reset_timestamp(df_original.copy())
    print("Timestamps zerados com sucesso.")

    # 3. Definir o nome e caminho para o novo arquivo de saída
    # Cria um nome para o novo arquivo (ex: 'datalog (1)_resetado.csv')
    base_name, ext = os.path.splitext(FILE_NAME)
    new_file_name = f"{base_name}_resetado.csv" # Mude para .txt se preferir a mesma extensão
    output_file_path = os.path.join(DATA, new_file_name)

    # 4. Salvar o novo DataFrame em um arquivo CSV
    df_reset.to_csv(output_file_path, index=False)
    print(f"Novo arquivo salvo em: {output_file_path}")
    print("\nConteúdo das primeiras linhas do novo arquivo:")
    print(df_reset.head().to_string()) # Imprime as primeiras linhas para verificação

except FileNotFoundError:
    print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    print("Por favor, verifique se o caminho e o nome do arquivo estão corretos.")
except pd.errors.EmptyDataError:
    print(f"Erro: O arquivo '{file_path}' está vazio ou não contém dados válidos.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")