def train_model(model, X_train, y_train, epochs=20, batch_size=32, validation_split=0.2, callbacks=None):
    """
    Treina o modelo LSTM com os dados de treinamento fornecidos.

    Parameters
    ----------
    model : keras.Sequential
        O modelo LSTM a ser treinado.
    X_train : np.ndarray
        Dados de entrada para o treinamento (shape: n_samples x n_timesteps x n_features).
    y_train : np.ndarray
        Rótulos de treinamento (shape: n_samples,).
    epochs : int, optional, default=20
        Número de épocas para treinamento.
    batch_size : int, optional, default=32
        Tamanho do lote para treinamento.
    validation_split : float, optional, default=0.2
        Proporção de dados para validação durante o treinamento (0 a 1).

    Returns
    -------
    model : keras.Sequential
        O modelo treinado.

    Notes
    -----
    - Utiliza o otimizador 'adam' para otimização.
    - A função de perda é 'sparse_categorical_crossentropy', adequada para problemas de classificação multiclasse.
    """
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split, callbacks=callbacks or [])
    return model