import json
import csv

from flask import Flask, request, jsonify

app = Flask(__name__)

filename = "csv_files/csv_data.csv"

try:
    with open(filename, 'x', newline='') as f:
        write = csv.writer(f)
        write.writerow(['Temperature', 'Brightness'])
except FileExistsError:
    pass

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    if data:
        print("Datos recibidos:", data)
        with open(filename, 'a', newline='') as f:
            write = csv.writer(f)
            write.writerow([data['temp'], data['brightness']])
        return jsonify({'setpoint': 50}), 200
    print("No se enviaron datos o el formato no es JSON")
    return jsonify({'error': 'No se enviaron datos'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)