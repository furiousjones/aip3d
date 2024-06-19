import os

class AutoSlicer:
    def __init__(self, slicer_executable_path):
        self.slicer_executable_path = slicer_executable_path

    def slice(self, model, output_path):
        command = f"{self.slicer_executable_path} -i {model.file_path} -o {output_path}"
        os.system(command)
        return output_path
