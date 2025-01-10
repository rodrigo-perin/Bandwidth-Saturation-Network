from flask import Flask, request, jsonify, send_from_directory
from scapy.all import IP, UDP, send
import threading
import os

app = Flask(__name__)
threads = []
running = False

def send_traffic(target_ip, size_in_bytes):
    global running
    packet = IP(dst=target_ip) / UDP(dport=12345) / (b'X' * 1024)  # Pacote UDP com payload de 1KB
    packets_to_send = size_in_bytes // 1024  # Quantidade de pacotes a enviar

    for _ in range(packets_to_send):
        if not running:
            break
        send(packet, verbose=False)

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/start', methods=['POST'])
def start_traffic():
    global running, threads
    if running:
        return jsonify({'message': 'Teste já está em execução!'}), 400

    data = request.json
    target_ip = data.get('ip')
    size = data.get('size')  # Tamanho em bytes

    if not target_ip or not size:
        return jsonify({'message': 'Parâmetros inválidos!'}), 400

    running = True
    thread = threading.Thread(target=send_traffic, args=(target_ip, size))
    threads.append(thread)
    thread.start()

    return jsonify({'message': 'Tráfego iniciado!'})

@app.route('/stop', methods=['POST'])
def stop_traffic():
    global running, threads
    running = False
    for thread in threads:
        thread.join()
    threads.clear()
    return jsonify({'message': 'Teste encerrado!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)