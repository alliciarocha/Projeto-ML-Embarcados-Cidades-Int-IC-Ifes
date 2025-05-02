import os
from preprocessing.datasetLoader import load_my_dataset
from models.lstmModel import create_model
from training.train import train_model
from training.metrics_callback import MetricsPerClassCallback
from visualization.confusionMatrixPlot import plot_confusion_matrix
os.makedirs('reports', exist_ok=True)


file_paths = {
    'drinking': 'dataset/drinking_2.csv',
    'driving': 'dataset/driving_2.csv',
    'throwing': 'dataset/throwing_2.csv'
}

label_map = {'drinking': 0, 'driving': 1, 'throwing': 2}

X_train, X_test, y_train, y_test = load_my_dataset(file_paths, label_map, window_size=50)

n_timesteps, n_features, n_outputs = 50, 3, 3
model = create_model(n_timesteps, n_features, n_outputs)

metrics_callback = MetricsPerClassCallback(
    X_val=X_test,
    y_val=y_test,
    class_names=['Drinking', 'Driving', 'Throwing'],
    save_path='reports/classification_report.txt' 
)

class_names = ['Drinking', 'Driving', 'Throwing']

train_model(model, X_train, y_train,  callbacks=[metrics_callback])