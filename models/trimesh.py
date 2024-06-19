import trimesh

class Model3D:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.mesh = None

    def load_model(self, file_path):
        self.file_path = file_path
        self.mesh = trimesh.load(file_path)
        if self.mesh.is_empty:
            raise ValueError("Failed to load the 3D model.")

    def save_model(self, file_path):
        self.file_path = file_path
        self.mesh.export(file_path)

    def get_vertices(self):
        if self.mesh:
            return self.mesh.vertices
        return []

    def get_faces(self):
        if self.mesh:
            return self.mesh.faces
        return []
