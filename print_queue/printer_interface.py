import time

class PrinterInterface:
    def start_monitoring(self, update_status_callback):
        while True:
            # Simulate printer status updates
            status = {
                'progress': 50,  # example progress
                'temperature': 200,  # example temperature
                'error': None  # example error
            }
            update_status_callback(status)
            time.sleep(5)
