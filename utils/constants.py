class Movimento:
    EMPRESTIMO = 'S'
    DEVOLUCAO  = 'E'

class Livro:
    ID        = 0
    NOME      = 1
    AUTOR     = 2
    QTD_ATUAL = 3
    QTD_TOTAL = 4

class Gerenciamento:
    OPERACAO   = 0
    ID_LIVRO   = 1
    ID_USUARIO = 2
    MOVIMENTO  = 3
    QUANTIDADE = 4
    DATA_VCTO  = 5
    DATA_DEVOL = 6

class Usuario:
    ID         = 0
    NOME       = 1
    NASCIMENTO = 2
    ENDERECO   = 3
    CIDADE     = 4
    EMAIL      = 5
    STATUS     = 6

DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DISPLAY_DATE_FORMAT = 'dd/MM/yyyy'
DATE_INPUT_WIDTH = 110
BUSINESS_DAYS_LOAN = 5

CATALOG_TABLE_HEADERS = [ 'ID', 'Título', 'Autor', 'Ano', 'Quantidade', 'Status' ]
USERS_TABLE_HEADERS = [ 'ID', 'Nome', 'Nascimento', 'Endereço', 'Cidade', 'Bairro', 'Estado', 'CEP', 'Email', 'Status', 'Telefone' ]
LOAN_BOOK_TABLE_HEADERS = [ 'ID', 'Livro', 'Autor', 'Ano', 'Disponível', 'Local' ]