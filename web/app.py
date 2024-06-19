from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from print_queue.queue_manager import QueueManager, PrintJob
from print_queue.printer_interface import PrinterInterface

app = Flask(__name__)
socketio = SocketIO(app)

queue_manager = QueueManager()
printer_interface = PrinterInterface()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_print', methods=['POST'])
def start_print():
    data = request.json
    model_file = data['model_file']
    print_job = PrintJob(model_file, queue_manager)
    queue_manager.add_job(print_job)
    printer_interface.start_print_job(print_job)
    return jsonify({"status": "Print job started"})

@app.route('/pause_print', methods=['POST'])
def pause_print():
    success = printer_interface.pause_print_job()
    status = "Print job paused" if success else "No active print job to pause"
    return jsonify({"status": status})

@app.route('/resume_print', methods=['POST'])
def resume_print():
    success = printer_interface.resume_print_job()
    status = "Print job resumed" if success else "No paused print job to resume"
    return jsonify({"status": status})

@app.route('/cancel_print', methods=['POST'])
def cancel_print():
    success = printer_interface.cancel_print_job()
    status = "Print job canceled" if success else "No active print job to cancel"
    return jsonify({"status": status})

@socketio.on('connect')
def handle_connect():
    emit('status_update', {'status': 'Connected to server'})

@socketio.on('request_status')
def handle_request_status():
    status = printer_interface.get_status()
    emit('status_update', status)

def monitor_printer():
    while True:
        status = printer_interface.get_status()
        socketio.emit('status_update', status)
        socketio.sleep(5)

if __name__ == '__main__':
    socketio.start_background_task(monitor_printer)
    socketio.run(app, host='0.0.0.0', port=5000)
