# main.py

import os
import sys
import numpy as np

# Adiciona o diretório 'src', 'models' e 'training' ao sys.path
# Isso permite a importação de módulos de outras pastas no projeto.
script_dir = os.path.dirname(__file__)
project_root = script_dir # main.py já está na raiz do projeto
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Adiciona pastas de módulos específicas (src, models, training)
# É uma boa prática adicionar o diretório base de cada módulo se for um pacote
# (Ou sys.path.insert(0, os.path.join(project_root, 'src')) etc. funciona também)
# Neste caso, como project_root já foi adicionado, e as imports são absolutas desde a raiz,
# podemos importar diretamente.
# Se der erro de importação (ModuleNotFoundError), verifique este bloco.

# Importa a função de carregamento de dados
from src.data_loader import load_data # Note a mudança para 'src.data_loader'

# Importa a função de criação do modelo
from models.lstm_model import create_lstm_model

# Importa a função de treinamento do modelo
from training.model_trainer import train_lstm_model

# === IMPORTAÇÕES FUTURAS (para métricas e visualização, se você recriá-los) ===
# from training.metrics_callback import MetricsPerClassCallback
# from visualization.confusionMatrixPlot import plot_confusion_matrix
# ===============================================================

# Cria a pasta 'reports' se ela não existir
os.makedirs('reports', exist_ok=True)
os.makedirs('saved_models', exist_ok=True) # Pasta para salvar o modelo treinado

# --- CONFIGURAÇÕES DE DADOS E CAMINHOS ---
# ATENÇÃO: AJUSTE ESTES CAMINHOS PARA CORRESPONDER À SUA ESTRUTURA REAL!
# Estes caminhos são relativos à raiz do seu projeto (onde main.py está).

train_obstacle_paths = {
    'quebramola': os.path.join('OBSTÁCULOS', 'Data', 'quebraMola'),
    'buraco': os.path.join('OBSTÁCULOS', 'Data', 'buraco'),
    'buracoMaior': os.path.join('OBSTÁCULOS', 'Data', 'buracoMaior'),
    'lombofaixa': os.path.join('OBSTÁCULOS', 'Data', 'lobofaixa'),
    'tartaruga': os.path.join('OBSTÁCULOS', 'Data', 'tartaruga')
}

# Caminho para o arquivo de dados do "percurso completo" (para VALIDAÇÃO e TESTE)
full_course_data_path = os.path.join('dataset', 'percurso_completo.csv') # Deixamos como None por enquanto, conforme solicitado

# Mapeamento de rótulos
label_map = {
    'quebramola': 0,
    'buraco': 1,
    'buracoMaior': 2,
    'lombofaixa': 3,
    'tartaruga': 4,
    'normal': 5
}

# Nomes das colunas de features no seu arquivo de dados (confirmadas anteriormente)
features_cols = ['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ'] 

window_size = 50 

# --- CARREGAMENTO DE DADOS ---
print("Iniciando o processo de carregamento de dados...")
X_train, X_val, X_test, y_train, y_val, y_test = load_data(
    train_obstacle_paths=train_obstacle_paths,
    full_course_path=full_course_data_path, 
    label_map=label_map,
    window_size=window_size,
    features_columns=features_cols
)

# --- VERIFICAÇÃO DE DADOS CARREGADOS ---
if X_train.size == 0:
    print("\nERRO: Nenhum dado de treino foi carregado com sucesso. Verifique os caminhos, nomes de arquivos e conteúdo.")
    sys.exit("Encerrando o script devido à falha no carregamento de dados de treino.")
else:
    print(f"\nDados de treino carregados com sucesso: X_train.shape={X_train.shape}, y_train.shape={y_train.shape}")
    print(f"Número de features usado: {X_train.shape[2]}")
    print(f"Número de classes únicas nos dados de treino: {np.unique(y_train).size}")

# --- CRIAÇÃO DO MODELO ---
n_timesteps = X_train.shape[1] 
n_features = X_train.shape[2] 
n_outputs = len(label_map) 

print(f"\nConfiguração do Modelo: timesteps={n_timesteps}, features={n_features}, outputs={n_outputs}")

model = create_lstm_model(n_timesteps, n_features, n_outputs)

# --- TREINAMENTO DO MODELO ---
model_save_path = os.path.join('saved_models', 'best_obstacle_detector_model.h5')

# Define os dados de validação para o treinamento
validation_data_tuple = None
if X_val.size > 0 and y_val.size > 0:
    validation_data_tuple = (X_val, y_val)

train_lstm_model(
    model, 
    X_train, 
    y_train, 
    X_val=X_val, # Passa X_val e y_val explicitamente para train_lstm_model
    y_val=y_val, 
    epochs=50, # Número de épocas para treinamento
    batch_size=32, # Tamanho do batch
    model_save_path=model_save_path
)

print(f"\nMelhor modelo salvo em: {model_save_path}")

# --- AVALIAÇÃO FINAL NO CONJUNTO DE TESTE (se disponível) ---
if X_test.size > 0 and y_test.size > 0:
    print("\nAvaliação final do modelo no conjunto de teste:")
    # Carrega o melhor modelo salvo para avaliação final
    from keras._tf_keras.keras.models import load_model
    best_model = load_model(model_save_path)
    
    loss, accuracy = best_model.evaluate(X_test, y_test, verbose=1)
    print(f"Acurácia no conjunto de teste: {accuracy:.4f}")
    print(f"Loss no conjunto de teste: {loss:.4f}")

    # === VISUALIZAÇÃO DA MATRIZ DE CONFUSÃO (precisaria do confusionMatrixPlot.py) ===
    # Você pode recriar este módulo mais tarde, se desejar.
    # from visualization.confusionMatrixPlot import plot_confusion_matrix
    # y_pred_probs = best_model.predict(X_test)
    # y_pred = np.argmax(y_pred_probs, axis=1)
    # class_names = list(label_map.keys())
    # plot_confusion_matrix(y_test, y_pred, class_names=class_names, title='Confusion Matrix (Test Set)')
else:
    print("\nDados de teste não disponíveis. Não é possível realizar a avaliação final.")

print("\nScript main.py concluído.")