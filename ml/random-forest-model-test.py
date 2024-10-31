import joblib
import pandas as pd

# 1. Load the saved model
try:
    model = joblib.load('../ml/model/random_forest_model.joblib')
    print("Model loaded successfully!")

    # 2. Load some test data (using the same dataset)
    data = pd.read_csv('../ml/dataset/dataset_training.csv')

    # 3. Select same features as training
    selected_features = [
        'length_url',
        'length_hostname',
        'ip',
        'nb_dots',
        'nb_hyphens',
        'nb_qm',
        'nb_and',
        'nb_eq',
        'nb_underscore',
        'nb_percent',
        'nb_slash',
        'nb_semicolumn',
        'nb_www',
        'page_rank',
        'google_index'
    ]

    # 4. Prepare test data
    X_test = data[selected_features].head(10)  # Adjust head to test the number of rows
    print(X_test)
    
    # 5. Make predictions
    predictions = model.predict(X_test)
    print("\nTest Predictions for first 5 entries:")
    print(predictions)
    
    print("\nModel works correctly!")

except Exception as e:
    print(f"Error: {e}")