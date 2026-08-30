import os
import requests
from pathlib import Path

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

LIMITE = 5.0


def dados_btc():
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
    )

    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()

    dados = resposta.json()["bitcoin"]

    return dados["usd"], dados["usd_24h_change"]


def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    resposta = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": texto
        },
        timeout=10
    )

    resposta.raise_for_status()

enviar_mensagem("🧪 TESTE: o alerta do BTC está funcionando!")
preco, variacao = dados_btc()

print(f"BTC: US$ {preco:,.2f}")
print(f"Variação nas últimas 24h: {variacao:.2f}%")

if variacao <= -LIMITE:
    enviar_mensagem(
        f"📉 BTC caiu {abs(variacao):.2f}% nas últimas 24 horas!\n"
        f"💰 Preço: US$ {preco:,.2f}"
    )

elif variacao >= LIMITE:
    enviar_mensagem(
        f"📈 BTC subiu {variacao:.2f}% nas últimas 24 horas!\n"
        f"💰 Preço: US$ {preco:,.2f}"
    )
