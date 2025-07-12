import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # Para adicionar legendas de cores se você quiser marcar manualmente no gráfico

# --- Re-execute a parte de carregamento e concatenação para ter o combined_df ---
# (Certifique-se de que o caminho DATA_FILES_PATH e a correção do nome do arquivo estejam corretos)

DATA_FILES_PATH = 'Analise De Dados Coletados/TESTES/dados 10_07' # Ajuste este caminho se necessário

all_dfs = []
file_found = True
file_index = 1

print("Carregando e concatenando arquivos datalog para plotagem...")

base_datalog_path = os.path.join(DATA_FILES_PATH, 'datalog.txt')
if os.path.exists(base_datalog_path):
    try:
        df_temp = pd.read_csv(base_datalog_path)
        df_temp.columns = df_temp.columns.str.strip().str.replace(r'\s+', '', regex=True)
        all_dfs.append(df_temp)
        print(f"Carregado: datalog.txt")
    except Exception as e:
        print(f"Erro ao ler {base_datalog_path}: {e}")

while file_found:
    file_name = f'datalog ({file_index}).txt' # Corrigido o espaço
    file_path = os.path.join(DATA_FILES_PATH, file_name)

    if os.path.exists(file_path):
        try:
            df_temp = pd.read_csv(file_path)
            df_temp.columns = df_temp.columns.str.strip().str.replace(r'\s+', '', regex=True)
            all_dfs.append(df_temp)
            print(f"Carregado: {file_name}")
            file_index += 1
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")
            file_found = False
    else:
        file_found = False

if not all_dfs:
    print("Nenhum arquivo de dados encontrado para concatenação.")
    exit()

combined_df = pd.concat(all_dfs, ignore_index=True)
print(f"Todos os {len(all_dfs)} arquivos foram concatenados. Tamanho total: {combined_df.shape[0]} amostras.")

# --- Parte de Plotagem ---

plt.figure(figsize=(18, 10)) # Aumenta o tamanho da figura para melhor visualização

# Plotar os dados do Acelerômetro
plt.subplot(2, 1, 1) # Cria um subplot (2 linhas, 1 coluna, primeiro gráfico)
plt.plot(combined_df['timestamp'], combined_df['accX'], label='AccX (Acel. X)', alpha=0.8)
plt.plot(combined_df['timestamp'], combined_df['accY'], label='AccY (Acel. Y)', alpha=0.8)
plt.plot(combined_df['timestamp'], combined_df['accZ'], label='AccZ (Acel. Z)', alpha=0.8) # AccZ é frequentemente útil para identificar impacto/movimento vertical
plt.title('Dados do Acelerômetro MPU6050 ao Longo do Percurso')
plt.xlabel('Timestamp')
plt.ylabel('Aceleração (unidade, e.g., g)')
plt.legend()
plt.grid(True)

# Plotar os dados do Giroscópio
plt.subplot(2, 1, 2) # Segundo gráfico (2 linhas, 1 coluna, segundo gráfico)
plt.plot(combined_df['timestamp'], combined_df['gyroX'], label='GyroX (Vel. Ang. X)', alpha=0.8)
plt.plot(combined_df['timestamp'], combined_df['gyroY'], label='GyroY (Vel. Ang. Y)', alpha=0.8)
plt.plot(combined_df['timestamp'], combined_df['gyroZ'], label='GyroZ (Vel. Ang. Z)', alpha=0.8)
plt.title('Dados do Giroscópio MPU6050 ao Longo do Percurso')
plt.xlabel('Timestamp')
plt.ylabel('Velocidade Angular (unidade, e.g., °/s)')
plt.legend()
plt.grid(True)

plt.tight_layout() # Ajusta o layout para evitar sobreposição de títulos/rótulos
plt.show()

print("\n--- INSTRUÇÕES PARA ROTULAGEM MANUAL ---")
print("1. Observe os gráficos para identificar padrões que correspondem à passagem pelos 5 obstáculos.")
print("2. Procure por picos, vales ou mudanças bruscas e sustentadas nas leituras.")
print("3. Anote cuidadosamente os 'timestamps' de início e fim de cada trecho onde o robô passou por um obstáculo específico.")
print("   Você pode usar as ferramentas de zoom do gráfico para ser mais preciso.")
print("4. Crie um arquivo CSV (ex: 'mapeamento_obstaculos.csv') com as seguintes colunas:")
print("   start_timestamp,end_timestamp,obstacle_type")
print("   Exemplo:")
print("   0,1000,plano")
print("   1001,2500,rampa")
print("   2501,3500,plano")
print("   3501,5000,degrau")
print("   ...")
print("   Lembre-se de cobrir todo o seu percurso e de incluir os trechos de 'plano' ou 'transição' se eles forem relevantes.")
print("5. Salve esse arquivo na mesma pasta do seu script Python.")
print("\nApós criar o 'mapeamento_obstaculos.csv', estaremos prontos para a próxima etapa!")