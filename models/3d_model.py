from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QAction, QLineEdit, QListWidget, QMessageBox, QInputDialog
from models.3d_model import Model3D
from print_queue.queue_manager import QueueManager, PrintJob
from ai.auto_slicer import AutoSlicer
from print_queue.printer_interface import PrinterInterface
from notifications.email_notifications import EmailNotifier
from notifications.sms_notifications import SMSNotifier
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIP3D - AI-Powered 3D Printer Assistant")
        self.setGeometry(100, 100, 800, 600)

        self.model = Model3D()
        self.queue_manager = QueueManager()
        self.slicer = AutoSlicer("/path/to/CuraEngine")
        self.printer_interface = PrinterInterface()
        self.email_notifier = EmailNotifier("smtp.example.com", 587, "your_email@example.com", "your_password")
        self.sms_notifier = SMSNotifier("your_account_sid", "your_auth_token")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.load_button = QPushButton("Load 3D Model")
        self.load_button.clicked.connect(self.load_model)
        layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save 3D Model")
        self.save_button.clicked.connect(self.save_model)
        layout.addWidget(self.save_button)

        self.slice_button = QPushButton("Slice 3D Model")
        self.slice_button.clicked.connect(self.slice_model)
        layout.addWidget(self.slice_button)

        self.print_button = QPushButton("Start Print Job")
        self.print_button.clicked.connect(self.start_print_job)
        layout.addWidget(self.print_button)

        self.monitor_button = QPushButton("Start Monitoring")
        self.monitor_button.clicked.connect(self.start_monitoring)
        layout.addWidget(self.monitor_button)

        self.status_label = QLabel("No model loaded")
        layout.addWidget(self.status_label)

        self.monitoring_label = QLabel("Monitoring: Not started")
        layout.addWidget(self.monitoring_label)

        self.print_queue_list = QListWidget()
        layout.addWidget(self.print_queue_list)

        self.error_predict_button = QPushButton("Predict Errors")
        self.error_predict_button.clicked.connect(self.predict_errors)
        layout.addWidget(self.error_predict_button)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter email for notifications")
        layout.addWidget(self.email_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter phone number for notifications")
        layout.addWidget(self.phone_input)

        self.feedback_button = QPushButton("Submit Feedback")
        self.feedback_button.clicked.connect(self.collect_feedback)
        layout.addWidget(self.feedback_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.createMenuBar()

    def createMenuBar(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('File')
        
        loadAction = QAction('Load', self)
        loadAction.triggered.connect(self.load_model)
        fileMenu.addAction(loadAction)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.save_model)
        fileMenu.addAction(saveAction)

    def load_model(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open 3D Model File", "", "3D Files (*.stl *.obj);;All Files (*)", options=options)
        if file_name:
            self.model.load_model(file_name)
            self.status_label.setText(f"Loaded model: {file_name}")

    def save_model(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save 3D Model File", "", "3D Files (*.stl *.obj);;All Files (*)", options=options)
        if file_name:
            self.model.save_model(file_name)
            self.status_label.setText(f"Saved model: {file_name}")

    def slice_model(self):
        if not self.model.file_path:
            self.status_label.setText("No model loaded")
            return
        
        options = QFileDialog.Options()
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Sliced File", "", "G-Code Files (*.gcode);;All Files (*)", options=options)
        if output_file:
            sliced_file = self.slicer.slice(self.model, output_file)
            self.status_label.setText(f"Sliced model saved to: {sliced_file}")

    def start_print_job(self):
        if not self.model.file_path:
            self.status_label.setText("No model loaded")
            return

        print_job = PrintJob(self.model, self.queue_manager)
        self.queue_manager.add_job(print_job)
        self.update_print_queue()
        self.status_label.setText("Print job started")
        self.send_notifications("Print job started", f"Your print job for {self.model.file_path} has started.")

    def start_monitoring(self):
        self.printer_interface.start_monitoring(self.update_monitoring_status)
        self.monitoring_label.setText("Monitoring: Started")

    def update_monitoring_status(self, status):
        progress = status['progress']
        temperature = status['temperature']
        error = status['error']
        self.monitoring_label.setText(f"Monitoring: Progress={progress}%, Temp={temperature}°C, Error={error}")
        if error:
            self.send_notifications("Print job error", f"An error occurred during your print job: {error}")

    def send_notifications(self, subject, message):
        email = self.email_input.text()
        phone = self.phone_input.text()
        if email:
            self.email_notifier.send_email(email, subject, message)
        if phone:
            self.sms_notifier.send_sms(phone, "+1234567890", message)

    def predict_errors(self):
        predictor = ErrorPredictor()
        predictor.load_model('enhanced_error_predictor_model.pkl')
        features = self.extract_features(self.model)
        prediction = predictor.predict([features])
        if prediction[0] == 1:
            QMessageBox.warning(self, "Error Prediction", "Potential errors detected in the model.")
        else:
            QMessageBox.information(self, "Error Prediction", "No errors detected in the model.")

    def extract_features(self, model):
        return np.random.rand(1, 20)

    def update_print_queue(self):
        self.print_queue_list.clear()
        for job in self.queue_manager.list_jobs():
            self.print_queue_list.addItem(f"Model: {job.model.file_path}, Settings: {job.settings}")

    def collect_feedback(self):
        feedback, ok = QInputDialog.getText(self, "User Feedback", "Enter your feedback:")
        if ok and feedback:
            with open("user_feedback.txt", "a") as f:
                f.write(feedback + "\n")
            QMessageBox.information(self, "Thank you!", "Your feedback has been submitted.")
