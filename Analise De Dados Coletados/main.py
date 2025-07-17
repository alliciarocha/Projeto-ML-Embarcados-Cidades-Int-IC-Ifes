import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILES_PATH = 'Analise De Dados Coletados/TESTES/teste'
FILE_NAME = 'datalog (13).txt' 

file_path = os.path.join(DATA_FILES_PATH, FILE_NAME)

if not os.path.exists(file_path):
    print(f"Arquivo não encontrado: {file_path}")
    exit()

try:
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.replace(r'\s+', '', regex=True)
    print(f"Arquivo carregado com sucesso: {FILE_NAME}")
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    exit()


plt.figure(figsize=(18, 12))

plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['accX'], label='AccX', alpha=0.8)
plt.plot(df['timestamp'], df['accY'], label='AccY', alpha=0.8)
plt.plot(df['timestamp'], df['accZ'], label='AccZ', alpha=0.8)
plt.title('Acelerômetro')
plt.xlabel('Timestamp')
plt.ylabel('Aceleração')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['gyroX'], label='GyroX', alpha=0.8)
plt.plot(df['timestamp'], df['gyroY'], label='GyroY', alpha=0.8)
plt.plot(df['timestamp'], df['gyroZ'], label='GyroZ', alpha=0.8)
plt.title('Giroscópio')
plt.xlabel('Timestamp')
plt.ylabel('Velocidade Angular')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
