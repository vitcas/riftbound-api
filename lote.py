import json
import os

INPUT_FILE = "riftbound_cards.json"
OUTPUT_FILE = "riftbound_cards_modificado.json"


def carregar_json():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Arquivo '{INPUT_FILE}' não encontrado.")
        exit()
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Alterações salvas em '{OUTPUT_FILE}'")


def detectar_chaves(data):
    keys = set()
    for item in data:
        keys.update(item.keys())
    return sorted(keys)


def menu_campos(keys):
    print("\n===== CAMPOS DETECTADOS =====")
    for i, k in enumerate(keys, 1):
        print(f"{i} - {k}")
    escolha = input("\nEscolha o número do campo: ")
    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(keys):
        print("❌ Opção inválida.")
        exit()
    return keys[int(escolha) - 1]


def menu_acao():
    print("\n===== AÇÃO =====")
    print("1 - Remover campo de todos os objetos")
    print("2 - Replace texto (ex: trocar 'Epic' por 'Lendário')")
    print("3 - Definir valor fixo para todos os registros")
    print("4 - Remover campo apenas se tiver valor específico")
    print("5 - Mostrar registros que contenham valor (modo inspeção)")

    escolha = input("\nEscolha a ação: ")
    if escolha not in ["1", "2", "3", "4", "5"]:
        print("❌ Opção inválida.")
        exit()
    return escolha


def aplicar_acao(data, campo, acao):
    alterados = 0

    if acao == "1":
        # Remover campo completamente
        for item in data:
            if campo in item:
                item.pop(campo)
                alterados += 1
        print(f"🗑 Campo '{campo}' removido de {alterados} registros.")

    elif acao == "2":
        # Replace texto
        antigo = input("Texto antigo: ")
        novo = input("Novo texto: ")
        for item in data:
            if campo in item and isinstance(item[campo], str) and antigo in item[campo]:
                item[campo] = item[campo].replace(antigo, novo)
                alterados += 1
        print(f"🔁 Replace aplicado em {alterados} registros.")

    elif acao == "3":
        # Definir valor fixo
        valor = input("Digite o valor que deseja aplicar em todos: ")
        for item in data:
            item[campo] = valor
            alterados += 1
        print(f"🎯 Campo '{campo}' definido como '{valor}' em {alterados} registros.")

    elif acao == "4":
        # Remover campo apenas se valor = X
        valor = input("Remover apenas se o valor for: ")
        for item in data:
            if campo in item and str(item[campo]) == valor:
                item.pop(campo)
                alterados += 1
        print(f"🚫 Campo '{campo}' removido de {alterados} registros com valor '{valor}'.")

    elif acao == "5":
        # Modo inspeção
        valor = input("Mostrar apenas registros que contenham (substring ou valor exato): ")
        print("\n===== REGISTROS QUE CONTÊM O VALOR =====")
        for item in data:
            if campo in item and valor.lower() in str(item[campo]).lower():
                print(f"- {item.get('name', 'Sem nome')} → {campo}: {item[campo]}")
        print("\n🔍 Inspeção concluída. Nenhuma modificação foi salva.")
        exit()

    return data


def main():
    data = carregar_json()
    chaves = detectar_chaves(data)
    campo = menu_campos(chaves)
    acao = menu_acao()
    data_modificada = aplicar_acao(data, campo, acao)
    salvar_json(data_modificada)


if __name__ == "__main__":
    main()
