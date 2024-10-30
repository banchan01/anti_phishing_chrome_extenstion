import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input

# 1. Load the data
data = pd.read_csv('ml-scripts/dataset/dataset_small.csv')

# 2. Separate features and target
X = data.drop('phishing', axis=1)
y = data['phishing']

# 3. Handle missing values with -1 if there are
X = X.fillna(-1)  # Replace NaNs with -1

# 4. Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 6. Define the model
def create_model(input_shape):
    model = Sequential([
        Input(shape=(input_shape,)),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 7. Create and train the model
model = create_model(X_train.shape[1])
model.summary()
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 8. Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")
