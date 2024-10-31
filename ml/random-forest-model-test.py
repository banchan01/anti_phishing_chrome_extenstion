import joblib
import pandas as pd

# Load the saved model
model = joblib.load("../ml/model/random_forest_model.joblib")

# Get feature names
feature_names = model.feature_names_in_

# Print feature names in order
print("Feature names in order:")
for i, name in enumerate(feature_names):
    print(f"{i}: {name}")

# Optional: Create a DataFrame of feature importances
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)