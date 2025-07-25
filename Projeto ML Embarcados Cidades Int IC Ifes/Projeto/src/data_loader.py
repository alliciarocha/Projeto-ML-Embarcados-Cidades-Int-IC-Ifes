import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler # Adicionado para escalamento

def create_windows(data, window_size):
    """
    Cria janelas deslizantes a partir de dados de séries temporais.
    Args:
        data (np.ndarray): Array NumPy 2D com as features (linhas, features).
        window_size (int): Tamanho da janela.
    Returns:
        np.ndarray: Array NumPy 3D com as janelas (num_windows, window_size, num_features).
                    Retorna um array vazio se não houver dados suficientes.
    """
    X = []
    if len(data) < window_size:
        return np.array([]) 

    for i in range(len(data) - window_size + 1):
        X.append(data[i:i + window_size])
    return np.array(X)

def load_data(train_obstacle_paths, full_course_path, label_map, window_size, features_columns):
    """
    Carrega e prepara os datasets para treino, validação e teste.

    Args:
        train_obstacle_paths (dict): Dicionário com nomes dos obstáculos e caminhos
                                     das pastas contendo os 30 arquivos de cada.
        full_course_path (str): Caminho para o arquivo de dados do "percurso completo".
        label_map (dict): Mapeamento de nomes de obstáculos para IDs numéricos.
        window_size (int): Tamanho da janela de tempo para o modelo LSTM.
        features_columns (list): Lista de strings com os nomes das colunas de features a serem usadas.

    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
               Arrays NumPy dos dados e rótulos para treino, validação e teste.
               Os conjuntos de validação e teste podem ser vazios se full_course_path for None ou falhar.
    """
    X_train_list = []
    y_train_list = []

    # --- 1. Carregar dados para TREINO (30 de cada obstáculo) ---
    print("Iniciando carregamento de dados para treino (30 arquivos de cada obstáculo)...")
    for obstacle_name, folder_path in train_obstacle_paths.items():
        label = label_map[obstacle_name]
        all_obstacle_raw_data = [] # Para armazenar todos os dados brutos de um tipo de obstáculo

        print(f"  Processando obstáculo: {obstacle_name} (Label: {label})")
        
        for i in range(1, 31): # Assume arquivos numerados de 1 a 30 (ex: quebramola1.txt a quebramola30.txt)
            file_name = f"{obstacle_name}{i}.txt" 
            file_full_path = os.path.join(folder_path, file_name)

            if os.path.exists(file_full_path):
                try:
                    df = pd.read_csv(file_full_path)
                    df.columns = df.columns.str.strip() # Limpa espaços nos nomes das colunas
                    
                    missing_cols = [col for col in features_columns if col not in df.columns]
                    if missing_cols:
                        print(f"    AVISO: Arquivo '{file_name}' não possui as colunas esperadas: {missing_cols}. Pulando este arquivo.")
                        continue # Pula para o próximo arquivo
                        
                    features_data = df[features_columns].values
                    all_obstacle_raw_data.append(features_data)
                except Exception as e:
                    print(f"    ERRO ao ler '{file_name}': {e}. Pulando este arquivo.")
            
        # Concatena todos os dados brutos de um tipo de obstáculo ANTES de janelar
        if all_obstacle_raw_data:
            concatenated_obstacle_data = np.vstack(all_obstacle_raw_data)
            
            windows_for_obstacle = create_windows(concatenated_obstacle_data, window_size)

            if windows_for_obstacle.size > 0:
                X_train_list.append(windows_for_obstacle)
                y_train_list.append(np.full(len(windows_for_obstacle), label))
                print(f"    Criadas {len(windows_for_obstacle)} janelas para '{obstacle_name}'.")
            else:
                print(f"    AVISO: Nenhuma janela criada para '{obstacle_name}'. Total de linhas de dados brutos: {len(concatenated_obstacle_data)}. Necessário pelo menos {window_size} linhas.")
        else:
            print(f"  AVISO: Nenhum dado válido encontrado para o obstáculo '{obstacle_name}'. Verifique os caminhos e o conteúdo dos arquivos.")


    X_train = np.vstack(X_train_list) if X_train_list else np.array([])
    y_train = np.hstack(y_train_list) if y_train_list else np.array([])
    
    # --- DEBUG para verificar X_train antes do escalamento ---
    print(f"\nDEBUG CARREGAMENTO: X_train.shape antes do escalamento: {X_train.shape}")
    # --- FIM DO DEBUG ---

    # --- Escalamento dos dados de treino ---
    scaler = StandardScaler()
    # Verifica se X_train não está vazio antes de tentar escalá-lo
    if X_train.size > 0:
        original_train_shape = X_train.shape
        X_train_reshaped = X_train.reshape(-1, original_train_shape[2])
        X_train_scaled_reshaped = scaler.fit_transform(X_train_reshaped)
        X_train_scaled = X_train_scaled_reshaped.reshape(original_train_shape)
        print(f"DEBUG SCALER: X_train escalado. Shape original: {original_train_shape}, Nova shape: {X_train_scaled.shape}")
    else:
        X_train_scaled = np.array([]) # Se X_train estiver vazio, X_train_scaled também fica vazio
        print("DEBUG SCALER: X_train está vazio, não será escalado.")
    # --- FIM DO BLOCO DE ESCALAMENTO ---

    print(f"\nResumo do Treino: Total de janelas (X_train): {X_train_scaled.shape if X_train_scaled.size > 0 else 'Vazio'}")
    print(f"Resumo do Treino: Total de rótulos (y_train): {y_train.shape if y_train.size > 0 else 'Vazio'}")


    # --- 2. Carregar e dividir dados do "percurso completo" (VAL/TEST) ---
    X_val, X_test, y_val, y_test = np.array([]), np.array([]), np.array([]), np.array([]) 

    if full_course_path and os.path.exists(full_course_path):
        print(f"\nDEBUG PERCURSO: Tentando carregar percurso completo de: '{full_course_path}'")
        try:
            full_course_df = pd.read_csv(full_course_path)
            full_course_df.columns = full_course_df.columns.str.strip() 
            
            label_column_name = 'label_id' # Nome da sua nova coluna de rótulos (confirmado por você)
            
            missing_cols_full = [col for col in features_columns + [label_column_name] if col not in full_course_df.columns]
            if missing_cols_full:
                print(f"  ERRO: O arquivo '{full_course_path}' não possui as colunas necessárias: {missing_cols_full}.")
                print("  Não será possível criar conjuntos de validação/teste.")
                return X_train_scaled, X_val, X_test, y_train, y_val, y_test 
                
            features_full_course = full_course_df[features_columns].values
            
            # Mapeamento de rótulos de texto para números, removendo espaços em branco
            raw_labels_full_course = full_course_df[label_column_name].astype(str).str.strip().values
            
            try:
                labels_full_course = np.array([label_map[label_text] for label_text in raw_labels_full_course])
            except KeyError as e:
                print(f"  ERRO: Rótulo '{e}' encontrado no CSV do percurso completo não está no label_map. Verifique a consistência dos nomes dos rótulos (maiúsculas/minúsculas).")
                print("  Não será possível criar conjuntos de validação/teste.")
                return X_train_scaled, X_val, X_test, y_train, y_val, y_test

            # Cria janelas do percurso completo e atribui o rótulo do último ponto da janela
            windows_full_course = create_windows(features_full_course, window_size)
            
            # --- Escalamento dos dados de validação/teste ---
            if windows_full_course.size > 0:
                original_valtest_shape = windows_full_course.shape
                windows_full_course_reshaped = windows_full_course.reshape(-1, original_valtest_shape[2])
                windows_full_course_scaled_reshaped = scaler.transform(windows_full_course_reshaped) # Usa o MESMO scaler
                windows_full_course_scaled = windows_full_course_scaled_reshaped.reshape(original_valtest_shape)
                print(f"DEBUG SCALER: Percurso completo escalado. Shape original: {original_valtest_shape}, Nova shape: {windows_full_course_scaled.shape}")
            else:
                windows_full_course_scaled = np.array([]) 
                print("DEBUG SCALER: Janelas do percurso completo estão vazias, não serão escaladas.")
            # --- FIM DO BLOCO DE ESCALAMENTO ---

            y_full_course_windows = []
            if len(features_full_course) >= window_size: # Usa features_full_course porque windows_full_course pode ser vazio
                for i in range(len(features_full_course) - window_size + 1):
                    y_full_course_windows.append(labels_full_course[i + window_size - 1])
                y_full_course_windows = np.array(y_full_course_windows)
            
            if windows_full_course_scaled.size > 0 and y_full_course_windows.size > 0: 
                if len(np.unique(y_full_course_windows)) > 1:
                    X_val, X_test, y_val, y_test = train_test_split(
                        windows_full_course_scaled, y_full_course_windows, test_size=0.5, random_state=42, stratify=y_full_course_windows
                    )
                else:
                    print("  AVISO: Apenas uma classe encontrada no percurso completo. Não será feita estratificação na divisão.")
                    X_val, X_test, y_val, y_test = train_test_split(
                        windows_full_course_scaled, y_full_course_windows, test_size=0.5, random_state=42
                    )

                print(f"  Janelas do percurso completo carregadas (escaladas): {len(windows_full_course_scaled)}")
                print(f"  Janelas de validação (X_val): {X_val.shape}")
                print(f"  Janelas de teste (X_test): {X_test.shape}")
            else:
                print("  AVISO: Nenhuma janela ou rótulo válido criado a partir do percurso completo. Verifique os dados e o window_size.")
                
        except Exception as e:
            print(f"  ERRO ao carregar ou processar '{full_course_path}': {e}.")
            print("  Não será possível criar conjuntos de validação/teste.")
    else:
        print(f"AVISO: Caminho do arquivo de percurso completo '{full_course_path}' não fornecido ou arquivo não encontrado.")
        print("Conjuntos de validação e teste não serão criados.")

    return X_train_scaled, X_val, X_test, y_train, y_val, y_test