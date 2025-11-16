from monitor.window_tracker import registrar_janela, salvar_linha

info = {"titulo": "Teste", "programa": "teste.exe"}
linha = registrar_janela(info)
salvar_linha(linha)

print("Linha salva com sucesso:", linha)
