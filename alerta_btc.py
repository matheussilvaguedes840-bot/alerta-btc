import os
import json
import requests
from datetime import datetime, timezone

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MOEDAS = {
    "bitcoin": "₿ Bitcoin",
    "ethereum": "Ξ Ethereum"
}

LIMITES = [3, 5, 10]

ARQUIVO_ESTADO = "estado_alertas.json"


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


def carregar_estado():
    if not os.path.exists(ARQUIVO_ESTADO):
        return {}

    with open(ARQUIVO_ESTADO, "r") as arquivo:
        return json.load(arquivo)


def salvar_estado(estado):
    with open(ARQUIVO_ESTADO, "w") as arquivo:
        json.dump(estado, arquivo, indent=2)


dados = buscar_dados()
estado = carregar_estado()

agora = datetime.now(timezone.utc)

# =========================
# RESUMO HORÁRIO
# =========================

if agora.minute < 5:

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


# =========================
# ALERTAS
# =========================

for moeda in dados:

    nome = MOEDAS[moeda["id"]]

    variacoes = {
        "1h": moeda.get(
            "price_change_percentage_1h_in_currency"
        ),
        "24h": moeda.get(
            "price_change_percentage_24h_in_currency"
        ),
        "7d": moeda.get(
            "price_change_percentage_7d_in_currency"
        )
    }

    for periodo, variacao in variacoes.items():

        if variacao is None:
            continue

        for limite in LIMITES:

            chave = f"{moeda['id']}_{periodo}_{limite}"

            acima = abs(variacao) >= limite
            estava_acima = estado.get(chave, False)

            # Só envia quando CRUZAR o limite
            if acima and not estava_acima:

                direcao = "📈 SUBIU" if variacao > 0 else "📉 CAIU"

                mensagem_alerta = (
                    f"🚨 ALERTA {nome}\n\n"
                    f"{direcao} {abs(variacao):.2f}% em {periodo}\n"
                    f"🇧🇷 Preço: R$ {moeda['current_price']:,.2f}\n"
                    f"🎯 Limite: {limite}%"
                )

                enviar_mensagem(mensagem_alerta)

            estado[chave] = acima


salvar_estado(estado)

print("Verificação concluída.")
