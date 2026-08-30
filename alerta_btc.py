import os
import requests
import time

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LIMITE = 0.05

def preco_btc():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    return float(resposta.json()["price"])

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": texto},
        timeout=10
    )

preco_inicial = preco_btc()

print(f"BTC inicial: US$ {preco_inicial:,.2f}")
print("Monitorando BTC...")

while True:
    try:
        preco_atual = preco_btc()
        variacao = (preco_atual - preco_inicial) / preco_inicial

        print(
            f"BTC: US$ {preco_atual:,.2f} | "
            f"Variação: {variacao * 100:.2f}%"
        )

        if variacao <= -LIMITE:
            enviar_mensagem(
                f"📉 BTC caiu 5%!\nPreço: US$ {preco_atual:,.2f}"
            )
            preco_inicial = preco_atual

        elif variacao >= LIMITE:
            enviar_mensagem(
                f"📈 BTC subiu 5%!\nPreço: US$ {preco_atual:,.2f}"
            )
            preco_inicial = preco_atual

        time.sleep(60)

    except Exception as erro:
        print("Erro:", erro)
        time.sleep(60)
