# models/lstm_model.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_lstm_model(n_timesteps, n_features, n_outputs):
    """
    Cria e retorna um modelo LSTM sequencial.

    Args:
        n_timesteps (int): Número de passos de tempo em cada janela de entrada (window_size).
        n_features (int): Número de features por passo de tempo (ex: 3 para accX, accY, accZ; 6 para acc+gyro).
        n_outputs (int): Número de classes de saída (número de tipos de obstáculos + 'normal', se aplicável).

    Returns:
        tensorflow.keras.Model: O modelo LSTM compilado.
    """
    model = Sequential()
    
    # Primeira camada LSTM
    # return_sequences=True para que a saída seja uma sequência para a próxima camada LSTM
    model.add(LSTM(units=100, activation='relu', input_shape=(n_timesteps, n_features), return_sequences=True))
    model.add(Dropout(0.2)) # Camada de Dropout para regularização

    # Segunda camada LSTM (opcional, adicione mais se o modelo precisar de mais complexidade)
    # return_sequences=False na última camada LSTM se você estiver passando para Dense
    model.add(LSTM(units=100, activation='relu'))
    model.add(Dropout(0.2))

    # Camada densa de saída
    # activation='softmax' para problemas de classificação multi-classe
    model.add(Dense(units=n_outputs, activation='softmax'))

    # Compila o modelo
    # optimizer='adam' é um bom ponto de partida
    # loss='sparse_categorical_crossentropy' é usado quando os rótulos de saída são inteiros (0, 1, 2, ...)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    print("\nModelo LSTM criado com sucesso:")
    model.summary() # Exibe um resumo da arquitetura do modelo

    return model