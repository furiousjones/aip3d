import unittest
from models.3d_model import Model3D
from ai.auto_slicer import AutoSlicer
from ai.error_predictor import ErrorPredictor
import numpy as np

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.model = Model3D("path/to/sample.stl")
        self.slicer = AutoSlicer("/path/to/CuraEngine")
        self.predictor = ErrorPredictor()
        self.predictor.load_model("enhanced_error_predictor_model.pkl")

    def test_slicing(self):
        sliced_file = self.slicer.slice(self.model, "path/to/output.gcode")
        self.assertTrue(os.path.exists(sliced_file))

    def test_error_prediction(self):
        features = np.random.rand(1, 20)  # Replace with actual feature extraction logic
        prediction = self.predictor.predict(features)
        self.assertIn(prediction[0], [0, 1])

if __name__ == "__main__":
    unittest.main()
