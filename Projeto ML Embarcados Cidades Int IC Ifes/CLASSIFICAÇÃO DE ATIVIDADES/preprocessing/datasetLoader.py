import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def create_sequences(data, label, window_size):
    
    """
    Cria janelas deslizantes de sequência com rótulo fixo.

    Parameters
    ----------
    data : np.ndarray
        Dados do sensor no formato (N, 3).
    label : int
        Rótulo da classe correspondente.
    window_size : int
        Número de amostras por sequência.

    Returns
    -------
    sequences : list
        Lista de sequências (shape: n_seq x window_size x 3).
    labels : list
        Lista de rótulos correspondentes.
    """
    
    sequences = []
    labels = []
    for i in range(len(data) - window_size):
        seq = data[i:i + window_size]
        sequences.append(seq)
        labels.append(label)
    return sequences, labels


def load_my_dataset(file_paths, label_map, window_size=50, test_size=0.2):
    
    """
    Carrega, organiza e pré-processa o dataset a partir de arquivos CSV.

    Parameters
    ----------
    file_paths : dict
        Dicionário com nome da classe como chave e caminho do CSV como valor.
    label_map : dict
        Dicionário mapeando os nomes das classes para inteiros.
    window_size : int
        Tamanho da janela temporal.
    test_size : float
        Proporção do conjunto de teste.

    Returns
    -------
    X_train, X_test, y_train, y_test : tuple
        Dados para treino e teste.
    """
    
    all_sequences = []
    all_labels = []

    for label_name, file_path in file_paths.items():
        df = pd.read_csv(file_path)
        data = df[['X', 'Y', 'Z']].values
        seqs, lbls = create_sequences(data, label_map[label_name], window_size)
        all_sequences.extend(seqs)
        all_labels.extend(lbls)

    X = np.array(all_sequences)
    y = np.array(all_labels)

    scaler = StandardScaler()
    X_reshaped = X.reshape(-1, 3)
    X_scaled = scaler.fit_transform(X_reshaped).reshape(-1, window_size, 3)

    return train_test_split(X_scaled, y, test_size=test_size, random_state=42)
