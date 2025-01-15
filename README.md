<h1>Bandwidth-Saturation-Network</h1>
<br />
<b>Autor: Rodrigo Perin</b>
<br /><br />
<h3>Resumo:</h3>
Essa aplicação em Python é uma interface web criada com Flask que permite gerar tráfego de rede para um <b>endereço IP de destino</b>, utilizando pacotes UDP enviados pela função sendpfast da biblioteca Scapy. O tráfego é configurado para ser enviado em tamanhos pré-definidos (100 MB, 500 MB, ou 1 GB). A aplicação também permite interromper o envio de tráfego por meio de uma chamada à rota /stop.
<br /><br />
<h3>Objetivo:</h3>
Testar capacidade e performace dos equipamentos da rede para identificar gargalos sem depender de um servidor de recebimento no destino.
<br /><br />
<h3>Os principais componentes da aplicação são:</h3>

<b>Flask:</b> Serve como o framework web para gerenciar as rotas e a interação com o frontend.
<br />
<b>Scapy:</b> Biblioteca responsável por construir e enviar os pacotes Ethernet/IP/UDP.
<br />
<b>Threading:</b> Utilizado para executar a função de envio de tráfego em um thread separado, permitindo que a aplicação responda a outras solicitações simultaneamente.

<h3>Observação:</h3> 
É necessário especificar a interface física no parâmetro iface da função sendpfast. Isso é importante porque o sendpfast precisa saber qual interface de rede será usada para enviar os pacotes. 
<br />
Exemplo:
<br /><br />
<i>sendpfast(packet, loop=packets_to_send, iface="eth0")</i>
<br /><br />
No exemplo acima, "eth0" deve ser substituído pelo nome correto da interface de rede física disponível no sistema (como "ens18" ou outro nome configurado). A escolha correta da interface garante que o tráfego será roteado para a rede desejada.
