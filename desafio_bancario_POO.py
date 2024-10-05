from abc import ABC, abstractclassmethod, abstractproperty

from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []
   
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco) -> None:
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
   
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Saldo insuficiente!")
        elif valor > 0:
            self._saldo -=valor
            print("\n ++++++ Saque realizado com sucesso !!!")
            return True
        else:
            print("\n@@@ Operação falhou - valor informado inválido")
        
        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n ##### valor depositado com sucesso")
        else:
            print ("Valor inválido para depósito !!!!")
            return False



class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(transacao for transacao in self.historico.transacoes 
                            if transacao["tipo"] == Saque.__name__)
        
        excedeu_limite = valor >self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite!!!")
        elif excedeu_saques:
            print("\n@@@ Operacao falhou! Numero máximo de Saques excedido!!!")
        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            C/C:\t\t{self.numero}
            Titular:\t\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def trasacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

    
    def transacoes_do_dia(self):
        data_atual = datetime.now(datetime.timezone.utc)
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self,conta):
        pass

class Saque(Transacao):
    def __init__(self,valor) -> None:
       self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        

class Deposito(Transacao):
    def __init__(self,valor) -> None:
       self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def localizar_cliente(cpf, clientes):
    for cli in clientes:
        if cli.cpf == cpf:
            return cli
    return False


def localizar_conta_cliente(cliente):
    
    if cliente.contas:
        return cliente.contas[0]
    else: 
        return False



def depositar(cliente):
   
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = localizar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = localizar_conta_cliente(clientes)
    if not conta:
        return
    conta.realizar_transacao(conta, transacao)


def extrato(cliente):
    conta = localizar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


#@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = localizar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
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


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

def listar_contas(contas):
    if len(contas) != 0:
        for conta in ContasIterador(contas):
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
    else:
        print("=" * 10 + " Sem contas a Exibir" +"=" * 10)
        print("=" * 100)

#@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente, numero=numero_conta, limite=500, limite_saques=50
    )
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

menu = """
####### BEM VINDO AO BANCO SG2 ########

    [1] - Depositar
    [2] - Sacar
    [3] - Extrato
    [4] - Criar Usuário
    [5] - Criar Conta
    [6] - Listar Contas

Digite [0] para sair

"""

def main():
    clientes = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == "1":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if cliente == False: print("Cliente Não cadastrado!!!")
            else: depositar(cliente)

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if cliente != False: sacar(clientes)
            else: print("CLiente não cadastrado !!!")

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            extrato(cliente)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print(
                "\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@"
            )


main()
