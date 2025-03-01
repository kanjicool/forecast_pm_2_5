import os
import numpy
from tensorflow.keras.models import load_model

def load_forecast_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(
        base_dir, "../utils/forecast_model/model.h5"
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    model = load_model(model_path)  # ใช้ load_model ของ TensorFlow
    print(f"\n... Complete loaded model ...")
    print(f"Model loaded from: {model_path}")
    return model


