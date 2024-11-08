# train_dnn_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Define your feature names in the same order as in your app
FEATURE_NAMES = [
    'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens', 'nb_qm', 'nb_and',
    'nb_eq', 'nb_underscore', 'nb_percent', 'nb_slash', 'nb_semicolumn', 'nb_www',
    'page_rank', 'google_index'
]

# Load your data (replace with actual data loading)
# X should be your feature matrix and y should be your labels
X = np.random.rand(1000, len(FEATURE_NAMES))  # Replace with actual features
y = np.random.randint(0, 2, 1000)             # Replace with actual labels

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define DNN model architecture
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')  # Output layer for binary classification
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Save the trained model and scaler
model.save('dnn_model.h5')
joblib.dump(scaler, 'scaler.joblib')

print("Model and scaler saved successfully.")
