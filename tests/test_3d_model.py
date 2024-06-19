import unittest
from models.3d_model import Model3D
import os

class TestModel3D(unittest.TestCase):
    def setUp(self):
        self.model = Model3D()

    def test_load_stl(self):
        self.model.load_model("path/to/sample.stl")
        self.assertGreater(len(self.model.vertices), 0)

    def test_save_stl(self):
        self.model.vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        self.model.faces = [[1, 2, 3]]
        self.model.save_model("path/to/sample_output.stl")
        self.assertTrue(os.path.exists("path/to/sample_output.stl"))

    def test_load_obj(self):
        self.model.load_model("path/to/sample.obj")
        self.assertGreater(len(self.model.vertices), 0)

    def test_save_obj(self):
        self.model.vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        self.model.faces = [[1, 2, 3]]
        self.model.save_model("path/to/sample_output.obj")
        self.assertTrue(os.path.exists("path/to/sample_output.obj"))

if __name__ == "__main__":
    unittest.main()
