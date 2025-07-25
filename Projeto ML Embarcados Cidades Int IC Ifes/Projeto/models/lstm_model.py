# models/lstm_model.py

from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense, Dropout

def create_lstm_model(n_timesteps, n_features, n_outputs):
    model = Sequential()

    # Primeira camada LSTM: Aumente units, mantenha return_sequences=True
    model.add(LSTM(units=150, activation='relu', input_shape=(n_timesteps, n_features), return_sequences=True))
    model.add(Dropout(0.2)) 

    # Segunda camada LSTM: Mantenha return_sequences=True para adicionar uma terceira
    model.add(LSTM(units=150, activation='relu', return_sequences=True)) # <--- Adicionado return_sequences=True aqui
    model.add(Dropout(0.2))

    # Terceira camada LSTM (nova): return_sequences=False na última antes de Dense
    model.add(LSTM(units=100, activation='relu')) # <--- NOVA CAMADA
    model.add(Dropout(0.2))


    # Camada densa de saída
    model.add(Dense(units=n_outputs, activation='softmax'))

    # Compila o modelo
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print("\nModelo LSTM criado com sucesso:")
    model.summary() 

    return model