from flask import Flask, request, jsonify, render_template
from scapy.all import Ether, IP, UDP, sendpfast
import threading

app = Flask(__name__)

# Variável global para controlar o envio de tráfego
running = False

@app.route("/")
def index():
    # Retorna a página principal renderizada
    return render_template("index.html")

def send_traffic(target_ip, size_in_bytes):
    """Função que gera pacotes de tráfego e os envia para o IP de destino."""
    global running
    packet = Ether() / IP(dst=target_ip) / UDP(dport=12345) / (b'X' * 1024)  # Monta o pacote Ethernet com dados fictícios
    packets_to_send = size_in_bytes // 1024  # Calcula o número total de pacotes

    if running:
        try:
            # Envia os pacotes utilizando a interface especificada
            sendpfast(packet, loop=packets_to_send, iface="ens18")
        except Exception as e:
            # Trata erros durante o envio
            pass

@app.route("/start", methods=["POST"])
def start_traffic():
    """Rota para iniciar o tráfego."""
    global running
    if running:
        # Retorna um status se já estiver em execução
        return jsonify({"status": "Já em execução"})

    running = True
    data = request.get_json()  # Obtém dados do corpo da requisição

    try:
        # Extrai os parâmetros necessários da requisição
        target_ip = data["target_ip"]
        size_in_mb = int(data["size_in_mb"])
    except (KeyError, TypeError, ValueError):
        # Retorna erro se os parâmetros forem inválidos
        return jsonify({"error": "Parâmetros inválidos"}), 400

    size_in_bytes = size_in_mb * 1024 * 1024  # Converte tamanho para bytes

    # Inicia a thread para envio de pacotes
    thread = threading.Thread(target=send_traffic, args=(target_ip, size_in_bytes))
    thread.start()

    return jsonify({"status": "Envio iniciado"})

@app.route("/stop", methods=["POST"])
def stop_traffic():
    """Rota para interromper o tráfego."""
    global running
    running = False  # Define a variável para interromper o envio
    return jsonify({"status": "Envio interrompido"})

if __name__ == "__main__":
    # Inicia o servidor Flask
    app.run(host="0.0.0.0", port=5000, debug=True)