import joblib

class ErrorPredictor:
    def __init__(self):
        self.model = None

    def load_model(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, features):
        if self.model:
            return self.model.predict(features)
        else:
            raise ValueError("Model not loaded")
