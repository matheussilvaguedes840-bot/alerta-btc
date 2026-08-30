import os
import requests
from pathlib import Path

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LIMITE = 0.05
ARQUIVO = Path("preco_anterior.txt")


def preco_btc():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    return float(resposta.json()["price"])


def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    resposta = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": texto},
        timeout=10
    )
    resposta.raise_for_status()


preco_atual = preco_btc()

if ARQUIVO.exists():
    preco_anterior = float(ARQUIVO.read_text())
else:
    preco_anterior = preco_atual

variacao = (preco_atual - preco_anterior) / preco_anterior

print(f"BTC: US$ {preco_atual:,.2f}")
print(f"Variação: {variacao * 100:.2f}%")

if variacao <= -LIMITE:
    enviar_mensagem(
        f"📉 BTC caiu 5%!\n"
        f"Preço atual: US$ {preco_atual:,.2f}\n"
        f"Variação: {variacao * 100:.2f}%"
    )

elif variacao >= LIMITE:
    enviar_mensagem(
        f"📈 BTC subiu 5%!\n"
        f"Preço atual: US$ {preco_atual:,.2f}\n"
        f"Variação: {variacao * 100:.2f}%"
    )

ARQUIVO.write_text(str(preco_atual))
