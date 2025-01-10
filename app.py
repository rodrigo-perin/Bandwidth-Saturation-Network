from flask import Flask, request, jsonify, render_template
from threading import Thread
from scapy.all import IP, UDP, send

app = Flask(__name__)

running = False  # Flag para controlar o envio de tráfego

def send_traffic(target_ip, size_in_bytes):
    global running
    packet = IP(dst=target_ip) / UDP(dport=5001) / (b'X' * 1460)  # Payload com 1460 bytes
    packets_to_send = size_in_bytes // 1460  # Quantidade de pacotes a enviar

    print(f"Enviando {packets_to_send} pacotes para {target_ip}, tamanho total: {size_in_bytes} bytes.")

    sent_packets = 0
    for _ in range(packets_to_send):
        if not running:
            break
        send(packet, verbose=False)
        sent_packets += 1

    print(f"Total de pacotes enviados: {sent_packets}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_traffic():
    global running
    data = request.get_json()
    target_ip = data.get('target_ip')
    size_in_bytes = data.get('size')
    
    if not target_ip or not size_in_bytes:
        return jsonify({"error": "Parâmetros inválidos"}), 400

    running = True
    Thread(target=send_traffic, args=(target_ip, size_in_bytes)).start()
    return jsonify({"message": f"Iniciando tráfego para {target_ip} de {size_in_bytes} bytes"})

@app.route('/stop', methods=['POST'])
def stop_traffic():
    global running
    running = False
    return jsonify({"message": "Tráfego encerrado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)