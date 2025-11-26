import json
from datetime import datetime
from monitor.window_tracker import salvar_linha


def carregar_classificacao():
    """
    Lê o arquivo JSON com a classificação dos aplicativos.
    Retorna um dicionário com categorias e listas de apps.
    """
    try:
        with open("config/classificacao_apps.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[carregar_classificacao] Erro ao carregar JSON: {e}")
        return {}


def classificar_programa(programa):
    """
    Recebe um programa (ex.: 'Discord.exe') e retorna a categoria correspondente.
    Caso o programa não esteja nas listas, retorna None.
    """
    classificacao = carregar_classificacao()

    for categoria, apps in classificacao.items():
        if programa in apps:
            return categoria

    return None  # não classificado


def registrar_classificacao(programa):
    """
    Registra no logs.csv um evento indicando a categoria do programa.
    Formato: data,hora,EVENTO_CLASSIFICACAO,categoria
    """
    categoria = classificar_programa(programa)

    # Só registra se o app tiver categoria definida
    if categoria is None:
        return None

    # Gera data e hora no padrão do WorkWatch
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data, hora = agora.split(" ")

    # Linha que será salva no logs.csv
    linha = f"{data},{hora},EVENTO_CLASSIFICACAO,{categoria}\n"

    # Salvar usando o sistema padrão do WorkWatch
    salvar_linha(linha)

    return categoria
