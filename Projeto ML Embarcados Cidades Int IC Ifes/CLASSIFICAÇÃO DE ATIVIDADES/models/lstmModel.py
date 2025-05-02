from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense

def create_model(n_timesteps, n_features, n_outputs, lstm_units=64, 
                 dense_units=32, activation_dense='relu', activation_output='softmax'):

    """
        Cria um modelo LSTM sequencial configurável para classificação de séries temporais.

        Parameters
        ----------
        n_timesteps : int
            Número de passos temporais em cada sequência de entrada (ex: 50).

        n_features : int
            Número de características por passo temporal (ex: 3 para X, Y, Z).

        n_outputs : int
            Número de classes de saída (ex: 3 para drinking, driving, throwing).

        lstm_units : int, optional
            Número de unidades na camada LSTM (padrão: 64).

        dense_units : int, optional
            Número de neurônios na camada densa intermediária (padrão: 32).

        activation_dense : str, optional
            Função de ativação da camada densa (padrão: 'relu').

        activation_output : str, optional
            Função de ativação da camada de saída (padrão: 'softmax').

        Returns
        -------
        keras.Sequential
            Um modelo LSTM compilado, pronto para treinamento.
    """
    
    model = Sequential([
        LSTM(lstm_units, input_shape=(n_timesteps, n_features)),
        Dense(dense_units, activation=activation_dense),
        Dense(n_outputs, activation=activation_output)
    ])
    return model