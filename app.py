from flask import Flask, request, jsonify
from scapy.all import IP, UDP, send
import threading

app = Flask(__name__)
running = False
thread = None

# Função para enviar tráfego de rede
def send_traffic(target_ip, size_in_bytes):
    global running

    # Tamanho do payload ajustado para 1472 bytes (MTU menos cabeçalhos IP/UDP)
    payload_size = 1472
    packet = IP(dst=target_ip) / UDP(dport=12345) / (b'X' * payload_size)

    # Calcula o número de pacotes a enviar
    packets_to_send = size_in_bytes // payload_size

    print(f"Enviando {packets_to_send} pacotes para {target_ip}...")

    # Envio de pacotes
    for _ in range(packets_to_send):
        if not running:
            break
        send(packet, verbose=False)

@app.route("/start", methods=["POST"])
def start_traffic():
    global running, thread

    if running:
        return jsonify({"status": "error", "message": "Tráfego já está em execução."}), 400

    data = request.get_json()
    target_ip = data.get("target_ip")
    size = data.get("size")

    if not target_ip or not size:
        return jsonify({"status": "error", "message": "Parâmetros inválidos."}), 400

    running = True
    thread = threading.Thread(target=send_traffic, args=(target_ip, size))
    thread.start()

    return jsonify({"status": "success", "message": "Tráfego iniciado."})

@app.route("/stop", methods=["POST"])
def stop_traffic():
    global running, thread

    if not running:
        return jsonify({"status": "error", "message": "Nenhum tráfego em execução."}), 400

    running = False
    if thread:
        thread.join()

    return jsonify({"status": "success", "message": "Tráfego interrompido."})

@app.route("/", methods=["GET"])
def index():
    return "Servidor de Teste de Vazão Ativo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)