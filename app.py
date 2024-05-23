from flask import Flask, render_template, request, jsonify
import paramiko
import time

app = Flask(__name__)

def get_temperature(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command('cat /sys/class/thermal/thermal_zone0/temp')
        temperature = float(stdout.read().decode()) / 1000
        client.close()
        return temperature
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_cpu(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(
            "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")
        cpu_usage = float(stdout.read().decode().strip())
        client.close()
        return cpu_usage
    except Exception as e:
        print(f"Error: {e}")
        return None
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/temperature', methods=['POST'])
def temperature():
    ip = request.form.get('ip')
    username = request.form.get('username')
    password = request.form.get('password')
    temp_data = {'time': int(time.time() * 1000), 'temperature': get_temperature(ip, username, password)}
    return jsonify(temp_data)

@app.route('/cpu', methods=['POST'])
def cpu():
    ip = request.form.get('ip')
    username = request.form.get('username')
    password = request.form.get('password')
    cpu_data = {'time': int(time.time() * 1000), 'cpu': get_cpu(ip, username, password)}
    return jsonify(cpu_data)

if __name__ == '__main__':
    app.run(debug=True)
