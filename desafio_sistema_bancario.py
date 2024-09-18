# Três operações: Depóstio, saque e extrato
# Depósito: valores positivos; um único usuário, armazenar em variáveis
# Saque: 3 saques diários, limite 500 por saque, msg saldo insuficiente
from datetime import datetime

menu = """
####### BEM VINDO AO BANCO GALILLEO ########

    [1] - Depositar
    [2] - Sacar
    [3] - Extrato
    [4] - Saldo

Digite [0] para sair

"""

saldo = 0
operacoes = ""
limite_valor = 500
data_saque = ""
qtd_saques = 0
LIMITE_SAQUE = 3

def adicionar_operacao(op):
    global operacoes
    operacoes += op +" \n"

print(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))[0:10])
while True:
    opcao = int(input(menu))
      
    if opcao == 1:
        print("Informe o valor a ser deposidato: ")
        valor = round(float(input()),2)
        if valor > 0:
            saldo = round(saldo + valor,2)
            data_hora_atual = datetime.now()
            data_hora_str = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
            msg = f"Depósito : R$ {valor} em {data_hora_str}"
            adicionar_operacao(msg)
            print(f"Novo Saldo : {saldo}")
        else:
            print("Somente pode ser depositado valor positivo !!!")
    elif opcao == 2:
        print("Informe o valor a ser sacado: ")
        valor = float(input())
        if valor > saldo:
            print("Saldo insuficiente!!!")
        elif valor <= 500:
            if data_saque == "" or data_saque != str(data_hora_atual.strftime('%d-%m-%Y %H:%M:%S'))[0:10]:
                data_saque = str(data_hora_atual.strftime('%d-%m-%Y %H:%M:%S'))[0:10]
                qtd_saques = 0
            if qtd_saques < 3:
                saldo -= round(valor,2)
                qtd_saques += 1
                data_hora_atual = datetime.now()
                data_hora_str = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
                msg = f"Saque : R$ {valor} em {data_hora_str}"
                adicionar_operacao(msg)
                print(f"Novo Saldo {saldo}")
            else:
                print("Atingiu a quantidade de saques diário !!!!")  
        else:
            print("Saque excede o limite de 500 reais por operação!!!")
        
        
    elif opcao == 3:
        print("\n########### EXTRATO #############")
        print(operacoes)
        print(f"Saldo: R$ {saldo}")
        print("\n########### FIM EXTRATO #############")
    elif opcao == 4:
        print(f"O saldo atual é {saldo}")
    else:
        print("Operação inválidade, verifique as opções do menu!!!")
    