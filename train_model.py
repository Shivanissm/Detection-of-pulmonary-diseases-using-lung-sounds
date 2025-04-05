import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Dataset path with class folders like 'Tc', 'Pr', etc.
dataset_path = r"C:\Users\Shivani\Downloads\archive (4)\output_loc"

# Function to extract MFCC features from an audio file
def extract_features(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    return np.mean(mfccs.T, axis=0)

# Arrays to store features and labels
X = []
y = []

# Loop through each folder (label)
for label in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, label)
    if not os.path.isdir(folder_path):
        continue

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            try:
                features = extract_features(file_path)
                X.append(features)
                y.append(label)  # Folder name as label (like 'Tc')
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

# Check if data is available
if len(X) == 0:
    print("❌ No data found! Please check your folder path and audio files.")
else:
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Prediction and accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Model training complete. Accuracy: {accuracy * 100:.2f}%")

    # Save model
    joblib.dump(model, "lung_disease_model.pkl")
    print("💾 Model saved as 'lung_disease_model.pkl'")
