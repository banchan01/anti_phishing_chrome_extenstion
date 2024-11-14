# -*- coding: cp949 -*-
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib


# Load data
data = pd.read_csv("../ml/dataset/dataset_training.csv")
data = data[['url', 'status']]  # Only use URL and phishing status (status)

# Convert 'status' to 0 and 1 (0 = legitimate, 1 = phishing)
data['status'] = data['status'].apply(lambda x: 1 if x == 'phishing' else 0)

# Hyperparameter settings
max_length = 100  # Maximum URL length
vocab_size = 1000  # Size of character vocabulary
embedding_dim = 50  # Embedding dimension

# Character-level tokenizer setup
tokenizer = Tokenizer(char_level=True, oov_token='UNK')
tokenizer.fit_on_texts(data['url'])
sequences = tokenizer.texts_to_sequences(data['url'])
X = pad_sequences(sequences, maxlen=max_length, padding='post')

# Set target variable
y = data['status'].values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Early stopping callback settings
early_stopping = EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)

# ReduceLROnPlateau callback settings (reduce learning rate when validation loss plateaus)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6)

# Define model (LSTM removed)
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
    Conv1D(filters=128, kernel_size=3, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),
    Conv1D(filters=64, kernel_size=3, activation='relu', kernel_regularizer=l2(0.001)),
    GlobalMaxPooling1D(),
    Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test),
                    callbacks=[early_stopping, reduce_lr])

# Save the model
model.save("model/CNN_model.h5")
print("Model saved as CNN_model.h5")

# Save the tokenizer
joblib.dump(tokenizer, "model/CNN_tokenizer.joblib")
print("Tokenizer saved as tokenizer.joblib")

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

# Plot training curves
def plot_training_curves(history):
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    # Accuracy curve
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, history.history['accuracy'], label='Training Accuracy')
    plt.plot(epochs, history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    
    # Loss curve
    plt.subplot(1, 2, 2)
    plt.plot(epochs, history.history['loss'], label='Training Loss')
    plt.plot(epochs, history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.show()

plot_training_curves(history)
