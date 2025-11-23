import time
from datetime import datetime
from monitor.window_tracker import obter_janela_ativa, salvar_linha


def analisar_multitarefa(historico):
    """
    Recebe uma lista com histórico recente de programas.
    Retorna um nível de multitarefa ou evento específico.
    """

    # só começa a analisar quando tiver pelo menos 3 registros
    if len(historico) < 3:
        return None

    ultimas3 = historico[-3:]
    ultimas4 = historico[-4:]
    ultimas5 = historico[-5:]

    # ============================================================
    # 🔥 1) MULTITAREFA INTENSA
    # ============================================================

    # 1A — Muitos programas diferentes nos últimos 5
    if len(ultimas5) >= 5 and len(set(ultimas5)) >= 4:
        return "NIVEL_MULTITAREFA_INTENSA"

    # 1B — Oscilação ABAB (sempre intensa)
    if len(ultimas4) == 4 and len(set(ultimas4)) == 2:
        a, b, c, d = ultimas4
        if a != b and a == c and b == d:
            return "NIVEL_MULTITAREFA_INTENSA"

    # 1C — Troca muito diversa (3 trocas e 3 programas diferentes)
    if len(ultimas5) >= 5 and len(set(ultimas5)) == 3:
        # se última sequência tiver 3 apps diferentes rapidamente
        if len(set(ultimas3)) == 3:
            return "NIVEL_MULTITAREFA_INTENSA"

    # ============================================================
    # 🟡 2) MULTITAREFA MODERADA
    # ============================================================

    # Critério: 3 programas diferentes nos últimos 5, sem ser intensa
    if len(ultimas5) >= 5 and len(set(ultimas5)) == 3:
        return "NIVEL_MULTITAREFA_MODERADA"

    # ============================================================
    # 🟢 3) MULTITAREFA LEVE
    # ============================================================

    # Critério: 2 programas diferentes, sem forte oscilação
    if len(ultimas5) >= 3 and len(set(ultimas5)) == 2:
        return "NIVEL_MULTITAREFA_LEVE"

    # ============================================================
    # EVENTOS BÁSICOS (mantidos como complemento)


    # TROCA_RÁPIDA
    if len(set(ultimas3)) == 3:
        return "TROCA_RAPIDA"

    return None



def monitorar_multitarefa(stop_event, interval):
    """
    Loop contínuo que analisa o histórico de programas usados.
    """
    historico = []     # últimos programas usados
    max_itens = 10     # manter apenas os últimos 10

    try:
        while not stop_event.is_set():

            janela = obter_janela_ativa()

            if janela:
                programa = janela.get("programa")

                if programa:
                    historico.append(programa)

                    # limitar histórico
                    if len(historico) > max_itens:
                        historico.pop(0)

                    # aplicar análise
                    evento = analisar_multitarefa(historico)
                    if evento:
                        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data, hora = agora.split(" ")
                        linha = f"{data},{hora},EVENTO_MULTITAREFA,{evento}\n"
                        salvar_linha(linha)

            # respeitar intervalo configurado
            time.sleep(interval)

    except Exception as e:
        print(f"[monitorar_multitarefa] erro: {e}")

    finally:
        print("monitorar_multitarefa finalizado")
