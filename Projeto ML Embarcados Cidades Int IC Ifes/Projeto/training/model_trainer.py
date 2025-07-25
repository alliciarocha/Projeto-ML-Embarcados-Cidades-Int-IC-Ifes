# training/model_trainer.py

from keras._tf_keras.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np

def train_lstm_model(model, X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32, model_save_path='best_model.h5'):
    callbacks = []
    validation_data = None

    if X_val is not None and y_val is not None and X_val.size > 0 and y_val.size > 0:
        validation_data = (X_val, y_val)
        print(f"\nTreinando modelo com validação em {len(X_val)} amostras de validação.")

        # Aumente a paciência para dar mais chances ao modelo
        early_stopping = EarlyStopping(monitor='val_accuracy', patience=20, mode='max', verbose=1) # <--- PATIENCE AUMENTADA
        callbacks.append(early_stopping)

        model_checkpoint = ModelCheckpoint(
            filepath=model_save_path,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True,
            verbose=1
        )
        callbacks.append(model_checkpoint)
    else:
        print("\nTreinando modelo SEM conjunto de validação. EarlyStopping e ModelCheckpoint baseados em validação não serão usados.")

    print(f"Iniciando treinamento por até {epochs} épocas com batch_size={batch_size}...")

    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=validation_data,
        callbacks=callbacks,
        verbose=1 
    )

    print("\nTreinamento concluído.")
    return history