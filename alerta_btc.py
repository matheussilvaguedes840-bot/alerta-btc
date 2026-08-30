import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MOEDAS = {
    "bitcoin": "₿ Bitcoin",
    "ethereum": "Ξ Ethereum"
}


def buscar_precos():
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum"
        "&vs_currencies=brl,usd"
        "&include_24hr_change=true"
    )

    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()

    return resposta.json()


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


dados = buscar_precos()

mensagem = "🚀 BTC & ETH ALERT PRO\n\n"

for moeda, nome in MOEDAS.items():
    preco_brl = dados[moeda]["brl"]
    preco_usd = dados[moeda]["usd"]
    variacao = dados[moeda]["usd_24h_change"]

    mensagem += (
        f"{nome}\n"
        f"🇧🇷 R$ {preco_brl:,.2f}\n"
        f"💵 US$ {preco_usd:,.2f}\n"
        f"📊 24h: {variacao:+.2f}%\n\n"
    )

enviar_mensagem(mensagem)

print(mensagem)
