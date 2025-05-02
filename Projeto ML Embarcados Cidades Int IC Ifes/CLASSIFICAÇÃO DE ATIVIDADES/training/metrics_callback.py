from sklearn.metrics import classification_report
from keras._tf_keras.keras.callbacks import Callback
from visualization.confusionMatrixPlot import plot_confusion_matrix
import numpy as np

class MetricsPerClassCallback(Callback):
    """
    Callback para exibir e/ou salvar métricas por classe (precision, recall, f1-score)
    ao final de cada época durante o treinamento.

    Parameters
    ----------
    X_val : np.ndarray
        Dados de validação (features).
    y_val : np.ndarray
        Rótulos de validação.
    class_names : list of str, optional
        Nomes das classes para exibição.
    save_path : str, optional
        Caminho do arquivo .txt para salvar os relatórios por época. Se None, apenas imprime.
    """
    def __init__(self, X_val, y_val, class_names=None, save_path=None):
        super().__init__()
        self.X_val = X_val
        self.y_val = y_val
        self.class_names = class_names
        self.save_path = save_path

    def on_epoch_end(self, epoch, logs=None):
        y_pred = np.argmax(self.model.predict(self.X_val), axis=1)
        y_true = self.y_val if len(self.y_val.shape) == 1 else np.argmax(self.y_val, axis=1)
        
        report = classification_report(y_true, y_pred, target_names=self.class_names, digits=4)

        print(f"\n[Epoca {epoch + 1}] Relatório de Classificação:\n{report}")

        if self.save_path:
            with open(self.save_path, "a") as f:
                f.write(f"\n[Epoca {epoch + 1}]\n{report}\n")
                
        if epoch == self.params['epochs'] - 1:
            y_pred = np.argmax(self.model.predict(self.X_val), axis=1)
            
            y_true = np.argmax(self.y_val, axis=1) if self.y_val.ndim > 1 else self.y_val

            plot_confusion_matrix(y_true, y_pred, class_names=self.class_names, save_path='reports/confusion_matrix.png')