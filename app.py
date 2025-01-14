from flask import Flask, request, jsonify, render_template
from scapy.all import IP, UDP, sendpfast
import threading

app = Flask(__name__)

running = False  # Variável global para controlar o envio de tráfego

@app.route("/")
def index():
    return render_template("index.html")

def send_traffic(target_ip, size_in_bytes):
    global running
    packet = IP(dst=target_ip) / UDP(dport=12345) / (b'X' * 1024)  # Pacote UDP com 1KB
    packets_to_send = size_in_bytes // 1024  # Total de pacotes a serem enviados

    if running:
        print(f"Enviando {packets_to_send} pacotes para {target_ip}, tamanho total: {size_in_bytes} bytes.")
        try:
            sendpfast(packet, loop=packets_to_send, iface="enp0s18", verbose=False)  # Substitua pela interface correta
            print("Envio concluído.")
        except Exception as e:
            print(f"Erro ao enviar pacotes: {e}")

@app.route("/start", methods=["POST"])
def start_traffic():
    global running
    if running:
        return jsonify({"status": "Já em execução"})

    running = True
    data = request.get_json()
    target_ip = data.get("target_ip")
    size_in_mb = data.get("size_in_mb")

    if not target_ip or not size_in_mb:
        return jsonify({"error": "Parâmetros inválidos"}), 400

    size_in_bytes = size_in_mb * 1024 * 1024

    thread = threading.Thread(target=send_traffic, args=(target_ip, size_in_bytes))
    thread.start()

    return jsonify({"status": "Envio iniciado"})

@app.route("/stop", methods=["POST"])
def stop_traffic():
    global running
    running = False
    return jsonify({"status": "Envio interrompido"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)