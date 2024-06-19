import os
import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog, simpledialog
from ai.auto_slicer import AutoSlicer
from ai.error_predictor import ErrorPredictor
from print_queue.queue_manager import QueueManager, PrintJob
from print_queue.printer_interface import PrinterInterface
from notifications.email_notifications import EmailNotifier
from notifications.sms_notifications import SMSNotifier
import numpy as np
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

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("AIP3D - AI-Powered 3D Printer Assistant")
        self.root.geometry("800x600")

        icon_path = os.path.abspath('icons/app_icon.png')
        if not os.path.exists(icon_path):
            messagebox.showerror("Error", f"Icon file not found: {icon_path}")
            return

        self.root.iconphoto(False, PhotoImage(file=icon_path))

        self.model = Model3D()
        self.queue_manager = QueueManager()
        self.slicer = AutoSlicer("/path/to/CuraEngine")
        self.printer_interface = PrinterInterface()
        self.email_notifier = EmailNotifier("smtp.example.com", 587, "your_email@example.com", "your_password")
        self.sms_notifier = SMSNotifier("your_account_sid", "your_auth_token")
        self.error_predictor = ErrorPredictor()
        self.error_predictor.load_model('enhanced_error_predictor_model.pkl')
        self.initUI()

    def initUI(self):
        main_layout = tk.Frame(self.root)
        main_layout.pack(fill=tk.BOTH, expand=True)

        # Load and Save Buttons
        load_save_layout = tk.Frame(main_layout)
        load_save_layout.pack(pady=10)

        self.load_button = tk.Button(load_save_layout, text="Load 3D Model", command=self.load_model)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(load_save_layout, text="Save 3D Model", command=self.save_model)
        self.save_button.pack(side=tk.RIGHT, padx=10)

        # Slice and Print Buttons
        slice_print_layout = tk.Frame(main_layout)
        slice_print_layout.pack(pady=10)

        self.slice_button = tk.Button(slice_print_layout, text="Slice 3D Model", command=self.slice_model)
        self.slice_button.pack(side=tk.LEFT, padx=10)

        self.print_button = tk.Button(slice_print_layout, text="Start Print Job", command=self.start_print_job)
        self.print_button.pack(side=tk.RIGHT, padx=10)

        # Monitoring and Status Labels
        self.monitor_button = tk.Button(main_layout, text="Start Monitoring", command=self.start_monitoring)
        self.monitor_button.pack(pady=10)

        self.status_label = tk.Label(main_layout, text="No model loaded", anchor="center")
        self.status_label.pack(pady=10)

        self.monitoring_label = tk.Label(main_layout, text="Monitoring: Not started", anchor="center")
        self.monitoring_label.pack(pady=10)

        # Progress Bars
        self.slicing_progress = tk.Label(main_layout, text="Slicing Progress: 0%")
        self.slicing_progress.pack(pady=10)

        self.printing_progress = tk.Label(main_layout, text="Printing Progress: 0%")
        self.printing_progress.pack(pady=10)

        # Print Queue List
        self.print_queue_list = tk.Listbox(main_layout)
        self.print_queue_list.pack(pady=10)

        # Error Prediction Button
        self.error_predict_button = tk.Button(main_layout, text="Predict Errors", command=self.predict_errors)
        self.error_predict_button.pack(pady=10)

        # Email and Phone Inputs
        self.email_input = tk.Entry(main_layout)
        self.email_input.insert(0, "Enter email for notifications")
        self.email_input.pack(pady=5)

        self.phone_input = tk.Entry(main_layout)
        self.phone_input.insert(0, "Enter phone number for notifications")
        self.phone_input.pack(pady=5)

        # Feedback Button
        self.feedback_button = tk.Button(main_layout, text="Submit Feedback", command=self.collect_feedback)
        self.feedback_button.pack(pady=10)

    def load_model(self):
        file_name = filedialog.askopenfilename(
            title="Open 3D Model File",
            filetypes=[("3D Files", "*.stl *.obj"), ("All Files", "*.*")]
        )
        if file_name:
            try:
                self.model.load_model(file_name)
                self.status_label.config(text=f"Loaded model: {file_name}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_model(self):
        file_name = filedialog.asksaveasfilename(
            title="Save 3D Model File",
            filetypes=[("3D Files", "*.stl *.obj"), ("All Files", "*.*")]
        )
        if file_name:
            try:
                self.model.save_model(file_name)
                self.status_label.config(text=f"Saved model: {file_name}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def slice_model(self):
        if not self.model.file_path:
            self.status_label.config(text="No model loaded")
            return

        output_file = filedialog.asksaveasfilename(
            title="Save Sliced File",
            filetypes=[("G-Code Files", "*.gcode"), ("All Files", "*.*")]
        )
        if output_file:
            self.slicing_progress.config(text="Slicing Progress: 0%")
            try:
                sliced_file = self.slicer.slice(self.model, output_file)
                self.slicing_progress.config(text="Slicing Progress: 100%")
                self.status_label.config(text=f"Sliced model saved to: {sliced_file}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def start_print_job(self):
        if not self.model.file_path:
            self.status_label.config(text="No model loaded")
            return

    
        ' print'python
            job = PrintJob(self.model, self.queue_manager)
            self.queue_manager.add_job(print_job)
            self.update_print_queue()
            self.status_label.config(text="Print job started")
            self.send_notifications("Print job started", f"Your print job for {self.model.file_path} has started.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_monitoring(self):
        try:
            self.printer_interface.start_monitoring(self.update_monitoring_status)
            self.monitoring_label.config(text="Monitoring: Started")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_monitoring_status(self, status):
        progress = status['progress']
        temperature = status['temperature']
        error = status['error']
        self.monitoring_label.config(text=f"Monitoring: Progress={progress}%, Temp={temperature}°C, Error={error}")
        self.printing_progress.config(text=f"Printing Progress: {progress}%")
        if error:
            self.send_notifications("Print job error", f"An error occurred during your print job: {error}")

    def predict_errors(self):
        features = self.extract_features(self.model)
        prediction = self.error_predictor.predict([features])
        if prediction[0] == 1:
            messagebox.showwarning("Error Prediction", "Potential errors detected in the model.")
        else:
            messagebox.showinfo("Error Prediction", "No errors detected in the model.")

    def extract_features(self, model):
        vertices = len(model.get_vertices())
        faces = len(model.get_faces())
        return np.array([vertices, faces]).reshape(1, -1)

    def update_print_queue(self):
        self.print_queue_list.delete(0, tk.END)
        for job in self.queue_manager.list_jobs():
            self.print_queue_list.insert(tk.END, f"Model: {job.model.file_path}, Settings: {job.settings}")

    def collect_feedback(self):
        feedback = simpledialog.askstring("User Feedback", "Enter your feedback:")
        if feedback:
            with open("user_feedback.txt", "a") as f:
                f.write(feedback + "\n")
            messagebox.showinfo("Thank you!", "Your feedback has been submitted.")

    def send_notifications(self, subject, message):
        email = self.email_input.get()
        phone = self.phone_input.get()
        if email:
            self.email_notifier.send_email(email, subject, message)
        if phone:
            self.sms_notifier.send_sms(phone, "+1234567890", message)
