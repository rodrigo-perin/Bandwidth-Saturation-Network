from flask import Flask, request, jsonify, render_template
from scapy.all import Ether, IP, UDP, sendpfast
import threading

app = Flask(__name__)

running = False  # Variável global para controlar o envio de tráfego

@app.route("/")
def index():
    return render_template("index.html")

def send_traffic(target_ip, size_in_bytes):
    global running
    packet = Ether() / IP(dst=target_ip) / UDP(dport=12345) / (b'X' * 1024)  # Adiciona cabeçalho Ethernet
    packets_to_send = size_in_bytes // 1024  # Total de pacotes a enviar

    if running:
        print(f"Enviando {packets_to_send} pacotes para {target_ip}, tamanho total: {size_in_bytes} bytes.")
        try:
            sendpfast(packet, loop=packets_to_send, iface="ens18")
            print("Envio concluído.")
        except Exception as e:
            print(f"Erro ao enviar pacotes: {e}")

@app.route("/start", methods=["POST"])
def start_traffic():
    global running
    if running:
        print("Tentativa de iniciar tráfego enquanto já está em execução.")
        return jsonify({"status": "Já em execução"})

    running = True
    data = request.get_json()

    # Log para depuração
    print(f"Dados recebidos na requisição: {data}")

    try:
        target_ip = data["target_ip"]
        size_in_mb = int(data["size_in_mb"])
    except (KeyError, TypeError, ValueError) as e:
        print(f"Erro: Parâmetros inválidos recebidos. Detalhes: {e}")
        print(f"target_ip: {data.get('target_ip')}, size_in_mb: {data.get('size_in_mb')}")
        return jsonify({"error": "Parâmetros inválidos"}), 400

    size_in_bytes = size_in_mb * 1024 * 1024
    print(f"Iniciando tráfego: target_ip={target_ip}, size_in_bytes={size_in_bytes}")

    thread = threading.Thread(target=send_traffic, args=(target_ip, size_in_bytes))
    thread.start()

    return jsonify({"status": "Envio iniciado"})

@app.route("/stop", methods=["POST"])
def stop_traffic():
    global running
    running = False
    print("Tráfego interrompido pelo usuário.")
    return jsonify({"status": "Envio interrompido"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)