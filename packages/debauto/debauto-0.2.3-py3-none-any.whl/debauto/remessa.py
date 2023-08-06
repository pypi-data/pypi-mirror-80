# -*- encoding: utf-8 -*-


class Configuracao(object):
    """
        Configuração do débito automático
    """

    def __init__(self, agencia, conta, convenio, empresa, sequencial, vencimento):
        self.agencia = agencia
        self.conta = conta
        self.convenio = convenio
        self.empresa = empresa
        self.sequencial = sequencial
        self.vencimento = vencimento


class Debito(object):
    """
        Débito
    """
    def __init__(self, identificacao, agencia, conta, vencimento, valor, moeda, livre, tipo):
        self.identificacao = identificacao
        self.agencia = agencia
        self.conta = conta
        self.vencimento = vencimento
        self.valor = valor
        self.moeda = moeda
        self.livre = livre
        self.tipo = tipo


class Remessa(object):
    """
        Remessa Debito Automatico
    """

    def __init__(self, cfg):
        # assert
        assert isinstance(cfg, Configuracao), TypeError("cfg deve ser uma instância de Configuração.")

        # configuração
        self.configuracao = cfg

        # debitos
        self.__debitos = []

    @property
    def debitos(self):
        return self.__debitos

    @debitos.setter
    def debitos(self, value):
        # assert
        assert isinstance(value, Debito), TypeError("Você deve passar uma instância de débito.")
        self.__debitos.append(value)

    def quantidade(self):
        """ quantidade de débitos """
        return len(self.__debitos)

    def valor_total(self):
        """ valor total dos débitos """
        return sum(_.valor for _ in self.debitos)
