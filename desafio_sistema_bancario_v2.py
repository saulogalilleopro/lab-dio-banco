# Três operações: Depóstio, saque e extrato

# Depósito: valores positivos; um único usuário, armazenar em variáveis
# Saque: 3 saques diários, limite 500 por saque, msg saldo insuficiente
from datetime import datetime

menu = """
####### BEM VINDO AO BANCO SG2 ########

    [1] - Depositar
    [2] - Sacar
    [3] - Extrato
    [4] - Saldo
    [5] - Criar Usuário
    [6] - Criar Conta

Digite [0] para sair

"""

saldo = 0
operacoes = ""
limite_valor = 500
data_saque = ""
qtd_saques = 0
qtd_transacoes = 0
dia_atual = datetime.now().strftime('%d-%m-%Y')
LIMITE_SAQUE = 3
LIMITE_TRANSACOES = 10

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


print(dia_atual)

def adicionar_operacao(op):
    global operacoes
    operacoes += op +" \n"

def depositar(valor_deposito, /):
    global saldo, qtd_transacoes
    saldo = round(saldo + valor_deposito,2)
    data_hora_str = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
    msg = f"Depósito : R$ {valor} em {data_hora_str}"
    adicionar_operacao(msg)
    qtd_transacoes += 1
    print(f"Novo Saldo : {saldo}")

def saque(*, valor_saque):
    global data_saque, qtd_saques, data_hora_atual, qtd_transacoes, saldo
    if data_saque == "" or data_saque != str(data_hora_atual.strftime('%d-%m-%Y %H:%M:%S'))[0:10]:
        data_saque = str(data_hora_atual.strftime('%d-%m-%Y %H:%M:%S'))[0:10]
        qtd_saques = 0
    if qtd_saques < 3:
        saldo -= round(valor,2)
        qtd_saques += 1
        qtd_transacoes +=1
        data_hora_atual = datetime.now()
        data_hora_str = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
        msg = f"Saque : R$ {valor_saque} em {data_hora_str}"
        adicionar_operacao(msg)
        print(f"Novo Saldo {saldo}")
    else:
        print("Atingiu a quantidade de saques diário !!!!") 

def extrato(valor_saldo, /, *, lista_trasacoes):
    global qtd_transacoes
    print("\n########### EXTRATO #############")
    print(lista_trasacoes)
    print(f"Saldo: R$ {valor_saldo}")
    print("\n########### FIM EXTRATO #############")
    qtd_transacoes +=1

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None
 
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("####### Já existe cliente com esse CPF! #######")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )
    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente, numero=numero_conta, limite=500, limite_saques=50
    )
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")



#print(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))[0:10])
data_hora_atual = datetime.now()
clientes = []
contas = []
while True:
    
    opcao = int(input(menu))
    #print(f"Quantidade de transações {qtd_transacoes}")
    if qtd_transacoes < 10:     
        if opcao == 1:
            print("Informe o valor a ser deposidato: ")
            valor = round(float(input()),2)
            if valor > 0:
                depositar(valor)
            else:
                print("Somente pode ser depositado valor positivo !!!")
        elif opcao == 2:
            print("Informe o valor a ser sacado: ")
            valor = float(input())
            if valor > saldo:
                print("Saldo insuficiente!!!")
            elif valor <= 500:
                saque(valor_saque=valor)
            else:
                print("Saque excede o limite de 500 reais por operação!!!")
        elif opcao == 3:
            extrato(saldo, lista_trasacoes=operacoes)
        elif opcao == 4:
            print(f"O saldo atual é {saldo}")
            qtd_transacoes +=1
        elif opcao == 5:
            criar_cliente(clientes)
        elif opcao == 6:
            criar_conta(contas)
        else:
            print("Operação inválidade, verifique as opções do menu!!!")
    else: 
        print("Excedeu o limite de transações diária (10 transsações)!!!")