import os
import requests
from datetime import datetime, timezone

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MOEDAS = {
    "bitcoin": "₿ Bitcoin",
    "ethereum": "Ξ Ethereum"
}

LIMITES = [3, 5, 10]


def buscar_dados():
    url = (
        "https://api.coingecko.com/api/v3/coins/markets"
        "?vs_currency=brl"
        "&ids=bitcoin,ethereum"
        "&price_change_percentage=1h,24h,7d"
    )

    resposta = requests.get(url, timeout=15)
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
        timeout=15
    )

    resposta.raise_for_status()


dados = buscar_dados()

# =========================
# RESUMO HORÁRIO
# =========================

agora = datetime.now(timezone.utc)

if True:

    mensagem = (
        f"🕐 RESUMO BTC & ETH\n"
        f"🗓️ {agora.strftime('%d/%m/%Y %H:%M')} UTC\n\n"
    )

    for moeda in dados:
        nome = MOEDAS[moeda["id"]]

        preco = moeda["current_price"]
        variacao_1h = moeda.get(
            "price_change_percentage_1h_in_currency"
        )
        variacao_24h = moeda.get(
            "price_change_percentage_24h_in_currency"
        )
        variacao_7d = moeda.get(
            "price_change_percentage_7d_in_currency"
        )

        mensagem += (
            f"{nome}\n"
            f"🇧🇷 R$ {preco:,.2f}\n"
            f"🕐 1h: {variacao_1h:+.2f}%\n"
            f"📅 24h: {variacao_24h:+.2f}%\n"
            f"📆 7d: {variacao_7d:+.2f}%\n\n"
        )

    enviar_mensagem(mensagem)

print("Verificação concluída.")
