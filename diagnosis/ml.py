import os
import joblib
import numpy as np
import librosa
from django.conf import settings

# 🔸 Load the trained model using absolute path
model_path = os.path.join(settings.BASE_DIR, 'lung_disease_model.pkl')
model = joblib.load(model_path)

# 🔸 Preprocess audio: extract MFCC features
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc_processed = np.mean(mfcc.T, axis=0)
    return mfcc_processed.reshape(1, -1)

# 🔸 Predict disease from audio file
# def predict_disease(audio_path):
#     features = extract_features(audio_path)
#     prediction = model.predict(features)[0]
#     return prediction


def predict_disease(audio_path):
    try:
        features = extract_features(audio_path)
        prediction = model.predict(features)[0]
        return prediction
    except Exception as e:
        print(f"❌ Error in prediction: {e}")
        return "Prediction Failed"
