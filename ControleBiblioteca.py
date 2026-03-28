import email
import os
from queue import Empty
import re
import sqlite3
from datetime import datetime, timedelta

from prompt_toolkit import print_formatted_text

# CONSTANTES
EMPRESTIMO = 'S'
DEVOLUCAO  = 'E'

LIVROS_ID        = 0
LIVROS_NOME      = 1
LIVROS_AUTOR     = 2
LIVROS_QTD_ATUAL = 3
LIVROS_QTD_TOTAL = 4

GERENCIAMENTO_OPERACAO   = 0
GERENCIAMENTO_ID_LIVRO   = 1
GERENCIAMENTO_ID_USUARIO = 2
GERENCIAMENTO_MOVIMENTO  = 3
GERENCIAMENTO_QUANTIDADE = 4
GERENCIAMENTO_DATA_VCTO  = 5
GERENCIAMENTO_DATA_DEVOL = 6

USUARIO_ID         = 0
USUARIO_NOME       = 1
USUARIO_NASCIMENTO = 2
USUARIO_ENDERECO   = 3
USUARIO_CIDADE     = 4
USUARIO_EMAIL      = 5
USUARIO_STATUS     = 6


def LimparTela():
    os.system( 'cls' if os.name == 'nt' else 'clear' )

def InputInt( descricao ):
    while True:
        try:
            valor = input( descricao ) 
            if not valor.isnumeric():
                print("Digite somente números")
                input()
                continue

            return int( valor )
        
        except:
            print( 'Digite somente números inteiros' )

def InputStr( descricao, nTamanho ):
    while True:
        try:
            usuario = input( descricao )
            if not usuario:
                print( 'Digite um valor' )
                continue

            elif len(usuario) <= nTamanho:
                return usuario
            
            else:
                print( f'Digite até {nTamanho} de caracteres')
                input()
                continue

        except:
            print( 'O campo está limitado até ' + str( nTamanho ) + ' caracterer(s)')

def InputStrUpper( descricao, nTamanho ):
    while True:
        try:
            usuario = input( descricao )
            if not usuario:
                print( 'Digite um valor' )
                input()
                continue

            elif len(usuario) <= nTamanho:
                return usuario.upper()
            
            else:
                print( f'Digite até {nTamanho} de caracteres')
                input()
                continue

        except:
            print( 'O campo está limitado até ' + str( nTamanho ) + 'de caracteres')

def InputData( descricao ):
    while True:
        captura_data = input( descricao )
        try:
            data = datetime.strptime( captura_data, "%d%m%Y" ).date()

        except ValueError:
            print( 'Data inválida. Use o formato DDMMAAAA' )
            continue

        return data

def InputEmail( descricao ):
    while True:
        capturaEmail = input( descricao )

        if '@' not in capturaEmail or '.com' not in capturaEmail:
            print( 'Email inválido tente novamente\nO email deve posuir "@" e ".com"' )
            continue
        
        return capturaEmail


def Main():

    conexaoBiblioteca = sqlite3.connect( 'biblioteca.db' )
    cursor            = conexaoBiblioteca.cursor()

    VerificaBiblioteca( cursor )

    while True:

        InicializaBiblioteca( cursor, conexaoBiblioteca )
        AtualizaStatusUsuarios( cursor, conexaoBiblioteca )
        movimentoBiblioteca = SelecionaOpcao()

        if movimentoBiblioteca == 'R':
            RegistrarLivro( cursor, conexaoBiblioteca )

        elif movimentoBiblioteca == 'U':
            RegistraUsuario( cursor, conexaoBiblioteca )

        elif movimentoBiblioteca == 'A':
            AdicionarLivro( cursor, conexaoBiblioteca )
            
        elif movimentoBiblioteca == 'E':
            EmprestaLivro( cursor, conexaoBiblioteca )

        elif movimentoBiblioteca == 'D':
            DevolveLivro( cursor, conexaoBiblioteca )

        elif movimentoBiblioteca == 'C':
            CatalogoLivros( cursor )

        elif movimentoBiblioteca == 'M':
            RegistroMovimentacao( cursor )

        elif movimentoBiblioteca == 'P':
            RegistroPerca( cursor, conexaoBiblioteca )

        elif movimentoBiblioteca == 'S':
            break 

    conexaoBiblioteca.commit()
    conexaoBiblioteca.close()


def VerificaBiblioteca( cursor ):
    cursor.execute( 
        """
        CREATE TABLE IF NOT EXISTS Livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro TEXT NOT NULL,
            autor TEXT,
            qtd_atual INTEGER NOT NULL,
            qtd_total INTEGER NOT NULL 
            )
        """
    )

    cursor.execute( 
        """
        CREATE TABLE IF NOT EXISTS Gerenciamento (
            operacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            movimento TEXT NOT NULL,
            quantidade INTEGER NOT NULL, 
            data_vencimento TEXT,
            data_devolucao TEXT
            ) 
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            data_nascimento INTEGER NOT NULL,
            endereco TEXT NOT NULL,
            cidade TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT NOT NULL
            )
        """
    )


def SelecionaOpcao():
    
    LimparTela()
    print( 'Sistema de controle de livros' )
    print()

    print( 'R - Registrar Livro' )
    print( 'U - Registrar Usuário' )
    print( 'A - Adicionar livro' )
    print( 'E - Emprestar' )
    print( 'D - Devolver' )
    print( 'C - Catálogo de livros' )
    print( 'M - Registro Movimentação dos Livros' )
    print( 'P - Registro de Perda dos Livros' )
    print( 'S - Sair' )

    movimentoBiblioteca = InputStrUpper( 'Movimento: ', 1 )

    return movimentoBiblioteca


def RegistrarLivro( cursor, conexaoBiblioteca ):
    LimparTela()

    print( 'Registrar livro' )
    nomeLivro  = InputStr( 'Livro: ', 40 )
    autorLivro = InputStr( 'Autor: ', 40 )

    cursor.execute(
        "SELECT * FROM livros WHERE livro = ? AND autor = ?",
        ( nomeLivro, autorLivro )
    )
    existe = cursor.fetchone()

    if existe:
        print( 'Livro ja cadastrado' )
        input()
        return
    
    cursor.execute(
        "INSERT INTO livros ( livro, autor, qtd_atual, qtd_total ) VALUES ( ?, ?, ?, ? )",
        ( nomeLivro, autorLivro, 0, 0 )
    )
    conexaoBiblioteca.commit()

    print( 'Livro Registrado' )
    input()


def AdicionarLivro( cursor, conexaoBiblioteca ):
    LimparTela()

    print( 'Adicionar livro na biblioteca' )
    nomeLivro  = InputStr( 'Livro.....: ', 40 )

    existeLivro = VerificaLivro( cursor, nomeLivro )
    if not existeLivro:
        return
    
    qtd_atual = existeLivro[ LIVROS_QTD_ATUAL ]
    qtd_total = existeLivro[ LIVROS_QTD_TOTAL ]

    quantidade = InputInt( 'Quantidade: ' )
    if quantidade == None:
        return

    qtd_atual += quantidade
    qtd_total += quantidade

    cursor.execute(
        "UPDATE Livros SET qtd_atual = ?, qtd_total = ? WHERE livro = ?",
        ( qtd_atual, qtd_total, nomeLivro )
    )

    cursor.execute(
        "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao ) VALUES ( ?, ?, ?, ?, ?, ? )",
        ( existeLivro[ LIVROS_ID ], 0, 'S', 1, None, None )
    )

    conexaoBiblioteca.commit()

    print( f'Livro { nomeLivro } adicionado com sucesso!' )
    input()


def EmprestaLivro( cursor, conexaoBiblioteca ):
    LimparTela()

    print( 'Emprestar livro' )

    id_usuario = InputStr( 'Id Usuário: ', 4 )
    
    cursor.execute(
        "SELECT * FROM Usuarios WHERE id = ?",
        ( id_usuario, )
    )
    movimentoUsuarioEncontrado = cursor.fetchall()

    if not movimentoUsuarioEncontrado:
        print( 'ID do usuário não cadastrado' )
        input()
        return

    for verificaPendenciaUsuario in movimentoUsuarioEncontrado:
        if verificaPendenciaUsuario[ USUARIO_STATUS ] == 'SIM':
            print( 'O usuário está com pendencia, resolva a pendencia para poder pegar emprestado outro livro!' )
            input()
            return

    nomeLivro = InputStr( 'Livro: ', 40 )
    cursor.execute(
        "SELECT * FROM Livros WHERE livro = ?",
        ( nomeLivro, )
    )
    existeLivro = cursor.fetchone()
    
    if not existeLivro:
        print( 'Livro não cadastrado' )
        input()
        return

    if existeLivro[ LIVROS_QTD_ATUAL ] < 1:
        print( 'Todos os exemplares desse livro estão emprestadas' )
        input()
        return
    
    cursor.execute(
        "SELECT * FROM Gerenciamento WHERE id_livro = ? AND id_usuario = ?",
        ( existeLivro[ LIVROS_ID ], id_usuario )
    )
    consultaMovimento = cursor.fetchall()

    if consultaMovimento:
        for consulta in consultaMovimento:
            if consulta[ GERENCIAMENTO_DATA_DEVOL ] == None:
                print( 'O usuário já possui o livro emprestado' )
                input()
                return
    
    vencimento = datetime.now() + timedelta(days=7)

    cursor.execute(
        "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao ) VALUES ( ?, ?, ?, ?, ?, ? )",
        ( existeLivro[ LIVROS_ID ], id_usuario, 'S', 1, vencimento.isoformat(), None )
    )

    cursor.execute(
        "UPDATE Livros SET qtd_atual = ? WHERE livro = ?",
        ( existeLivro[ LIVROS_QTD_ATUAL ] - 1, nomeLivro )
    )

    conexaoBiblioteca.commit()

    print( f'Livro {nomeLivro} emprestado com sucesso' )
    input()


def RegistraUsuario( cursor, conexaoBiblioteca ):
    LimparTela()

    print( 'Selecione uma das Opções' )
    print( 'C - Consulta usuário' )
    print( 'R - Registrar novo usuário' )
    opcaoUsuario = InputStrUpper( 'Opção: ', 1 )

    LimparTela()
    if opcaoUsuario == 'C':
        print( 'Usuários Cadastrados' )

        cursor.execute(
            "SELECT * FROM Usuarios"
        )
        registros = cursor.fetchall()

        if not len(registros):
            print( 'Nenhum usuário cadastrado!' )
            
        else:
            print( '{:<7.7}'.format( 'ID' ) + '{:<43.43}'.format( 'USUARIO' ) + '{:<13.13}'.format( 'DATA NASC' ) + '{:<33.33}'.format( 'ENDERECO' ) + '{:23.23}'.format( 'CIDADE' ) + '{:23.23}'.format( 'EMAIL' ) + '{:10.10}'.format( 'PENDENTE' ) )
            for id, usuario, data_nascimento, endereco, cidade, email, status in registros:
                print( f'{str( id ):>4.4} | {usuario:<40.40} | {data_nascimento:<10.10} | {str(endereco):<30.30} | {str(cidade):<20.20} | {str(email):<20.20} | {str(status):<6.6}' )

    if opcaoUsuario == 'R':
        print( 'Cadastre-se para poder emprestar livros' )
        nomeUsuario     = InputStr( 'Usuario.....: ', 40 )
        dataNascimento  = InputData( 'Nascimento (DDMMAAAA): ' )
        endereco        = InputStr( 'Endereco....: ', 40 )
        cidade          = InputStr( 'Cidade......: ', 40 )
        eMail           = InputEmail( 'Email.......: ' )

        cursor.execute(
            "SELECT * FROM Usuarios WHERE usuario = ? AND data_nascimento = ? AND endereco = ? AND cidade = ? AND email = ?",
            ( nomeUsuario, dataNascimento, endereco, cidade, eMail )
        )
        existe = cursor.fetchone()

        if not existe:
            cursor.execute(
                "INSERT INTO Usuarios ( usuario, data_nascimento, endereco, cidade, email, status ) VALUES ( ?, ?, ?, ?, ?, ? )",
                ( nomeUsuario, dataNascimento, endereco, cidade, eMail, 'NAO' )
            )
            conexaoBiblioteca.commit()

            print( 'Usuário cadastrado com sucesso' )

        else:
            print( 'Usuário já cadastrado' )

    input()


def DevolveLivro( cursor, conexaoBiblioteca ):
    LimparTela()

    print( 'Devolver livro' )

    usuario   = InputStr( 'Nome: ', 40 )
    cursor.execute(
        "SELECT * FROM Usuarios WHERE usuario = ?",
        ( usuario, )
    )
    existeUsuario = cursor.fetchone()

    if not existeUsuario:
        print( 'Usuário não cadastrado' )
        input()
        return
    
    cursor.execute(
        "SELECT * FROM Gerenciamento WHERE id_usuario = ?",
        ( existeUsuario[ USUARIO_ID ], )
    )
    existeMovimentoUsuario = cursor.fetchall()

    if existeMovimentoUsuario:

        movimentoSemDevolucao = 0

        for movimento in existeMovimentoUsuario:
            if movimento[ GERENCIAMENTO_MOVIMENTO ] == 'S' and movimento[ GERENCIAMENTO_DATA_DEVOL ] == None:
                movimentoSemDevolucao += 1

        if not movimentoSemDevolucao:
            print( 'O usuário não possui nenhum livro para ser devolvido!' )
            input()
            return
    
    else:
        print( 'O usuário ainda não pegou livro emprestado!' )
        input()
        return

    nomeLivro = InputStr( 'Livro: ', 40 )
    cursor.execute(
        "SELECT * FROM Livros WHERE livro = ?",
        ( nomeLivro, )
    )
    existeLivro = cursor.fetchone()
    
    if not existeLivro:
        print( 'Livro não cadastrado' )
        input()
        return

    if existeLivro[ LIVROS_QTD_ATUAL ] == existeLivro[ LIVROS_QTD_TOTAL ]:
        print( 'O livro que está sendo devolvido não é da biblioteca' )
        input()
        return
    
    registroMovimento = 0
    quantidadeLivro = 0
    datavencimento = None
    for movimento in existeMovimentoUsuario:
        if movimento[ GERENCIAMENTO_ID_LIVRO ] == existeLivro[ LIVROS_ID ] and movimento[ GERENCIAMENTO_ID_USUARIO ] == existeUsuario[ USUARIO_ID ] and movimento[ GERENCIAMENTO_MOVIMENTO ] == 'S' and movimento[ GERENCIAMENTO_DATA_DEVOL ] == None:
            registroMovimento = movimento[ GERENCIAMENTO_OPERACAO ]
            quantidadeLivro   = movimento[ GERENCIAMENTO_QUANTIDADE ]
            datavencimento    = movimento[ GERENCIAMENTO_DATA_VCTO ]

    if not registroMovimento:
        print( 'Emprestimo do livro pelo usuário não encontrado!' )
        input()
        return

    cursor.execute(
        "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao ) VALUES ( ?, ?, ?, ?, ?, ? )",
        ( existeLivro[ LIVROS_ID ], existeUsuario[ USUARIO_ID ], 'E', 1, datavencimento, datetime.now().date().isoformat() )
    )

    cursor.execute(
        "UPDATE Livros SET qtd_atual = ? WHERE livro = ?",
        ( existeLivro[ LIVROS_QTD_ATUAL ] + quantidadeLivro, nomeLivro )
    )

    cursor.execute(
        "UPDATE Gerenciamento SET data_devolucao = ? WHERE operacao = ?",
        ( datetime.now().date().isoformat(), registroMovimento )
    )

    conexaoBiblioteca.commit()

    print( f'Livro {nomeLivro} devolvido com sucesso' )
    input()


def CatalogoLivros( cursor ):
    LimparTela()

    cursor.execute(
        "SELECT id, livro, autor, qtd_atual, qtd_total FROM livros"
    )
    registros = cursor.fetchall()

    if not registros:
        print( 'NÃO HÁ NENHUM REGISTRO DE NENHUM LIVRO!' )
    else:
        while True:
            print( 'D - Filtrar os livros disponíveis' )
            print( 'I - Filtrar os livros indisponíveis' )
            print( 'T - Totods' )
            filtro = InputStrUpper( 'Filtrar por: ', 1 )
            
            LimparTela()
            print( ' ID    ' + '{:<42.42}'.format( 'LIVRO' ) + ' ' + '{:<20.20}'.format( 'AUTOR' ) + 'ATUAL' + ' ' + 'TOTAL  ' + '{:<12.12}'.format( 'STATUS' ) )
            
            if filtro == 'T':
                for id, livro, autor, qtd_atual, qtd_total in registros:

                    status = 'DISPONIVEL' if qtd_atual > 0 else 'INDISPONIVEL'
                    print( f'{str( id ):>4.4} | {livro:<40.40} | {autor:<18.18} |  {qtd_atual}  |  {qtd_total}  | {status}' )

            elif filtro == 'D':
                contador = sum( 1 for livro in registros if livro[ 3 ] > 0 )
                if not contador:
                    print( 'Não há nenhum livro disponível!' )
                else:
                    for id, livro, autor, qtd_atual, qtd_total in registros:

                        if not qtd_atual:
                            continue

                        status = 'DISPONIVEL'
                        print( f'{str( id ):>4.4} | {livro:<40.40} | {autor:<18.18} |  {qtd_atual}  |  {qtd_total}  | {status}' )

                print()

            elif filtro == 'I':
                contador = sum( 1 for livro in registros if livro[ 3 ] == 0 )
                if contador == 0:
                    print( 'Todos os livros estão disponíveis!' )
                else:
                    for id, livro, autor, qtd_atual, qtd_total in registros:

                        if qtd_atual > 0:
                            continue

                        status = 'INDISPONIVEL'
                        print( f'{str( id ):>4.4} | {livro:<40.40} | {autor:<18.18} |  {qtd_atual}  |  {qtd_total}  | {status}' )
    
            break

    input()


def RegistroMovimentacao( cursor ):
    LimparTela()
    print( 'Registro Movimentação dos Livros' )

    cursor.execute(
        "SELECT * FROM Gerenciamento" 
    )
    registros = cursor.fetchall()

    if not registros:
        print( 'Não há nenhum registro de movimento dos livros da biblioteca' )

    else:
        print( ' OPE  ' + '{:<42.42}'.format( 'LIVRO' ) + ' ' + '{:<25.25}'.format( 'USUARIO' ) + ' MOV QTD  PREVISAO     DEVOLUCAO' )
        for operacao, id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao in registros:

            registroLivro = VerificaLivro( cursor, id_livro )

            if not registroLivro:
                continue

            registroUsuario = VerificaUsuario( cursor, id_usuario )
            if not registroUsuario:
                continue

            print( f'{str(operacao):>4.4} | {registroLivro[ LIVROS_NOME ]:<40.40} | {str(id_usuario):>4.4}-{registroUsuario[ USUARIO_NOME ]:<18.18} | {movimento} | {quantidade} | {'' if data_vencimento is None else datetime.strptime( data_vencimento, "%Y-%m-%dT%H:%M:%S.%f" ).date()} | {'' if data_devolucao is None else datetime.strptime( data_devolucao, "%Y-%m-%dT%H:%M:%S.%f" ).date()}' )
    
    input()


def AtualizaStatusUsuarios( cursor, conexaoBiblioteca ):

    cursor.execute(
        "SELECT * FROM Gerenciamento WHERE movimento = ?",
        ( 'S', )
    )
    registros = cursor.fetchall()

    if not registros:
        return
    
    for registro in registros:
        if registro[ GERENCIAMENTO_DATA_VCTO ] == None:
            continue

        if datetime.strptime( registro[ GERENCIAMENTO_DATA_VCTO ], "%Y-%m-%dT%H:%M:%S.%f" ).date() < datetime.now().date():
            cursor.execute(
                "UPDATE Usuarios SET status = ? WHERE id = ?",
                ( 'SIM', registro[ GERENCIAMENTO_ID_USUARIO ] )
            )

    conexaoBiblioteca.commit()


def RegistroPerca( cursor, conexaoBiblioteca ):
    LimparTela()
    print( 'Registro de perca dos Livros' )
    print( 'C - Consultar livros perdidos' )
    print( 'B - Registro da baixa dos livros' )
    print( 'R - Reposição do livro' )

    opcaoPerca = InputStrUpper( 'Opcao: ', 1 )

    if opcaoPerca == 'C':
        LimparTela()
        print( 'Registro Movimentação dos Livros' )

        cursor.execute(
            "SELECT operacao, id_livro, id_usuario, movimento, quantidade FROM Gerenciamento WHERE movimento = ?",
            ( 'P', )
        )
        registroPerca = cursor.fetchall()

        if not registroPerca:
            print( 'Não há nenhum registro de perca dos livros da biblioteca' )

        else:
            print( ' OPE  ' + '{:<42.42}'.format( 'LIVRO' ) + ' ' + '{:<25.25}'.format( 'USUARIO' ) + ' MOV QTD' )
            for operacao, id_livro, id_usuario, movimento, quantidade in registroPerca:

                registroLivro = VerificaLivro( cursor, id_livro )
                if not registroLivro:
                    continue

                registroUsuario = VerificaUsuario( cursor, id_usuario )
                if not registroUsuario:
                    continue

                print( f'{str(operacao):>4.4} | {registroLivro[ LIVROS_NOME ]:<40.40} | {str(id_usuario):>4.4}-{registroUsuario[ USUARIO_NOME ]:<18.18} | {movimento} | {quantidade}' )

    elif opcaoPerca == 'B':
        LimparTela()
        print( 'Baixa do Livro' )
        print()
        print( 'Local do livro antes da perca' )
        print( 'B - Biblioteca' )
        print( 'U - Usuario' )
        opcaoLocal = InputStrUpper( 'Local: ', 1 )
        print()
        print( 'Registro da perca' )
        id_livro = InputInt( 'Digite o ID do livro: ' )

        consultaLivro = VerificaLivro( cursor, id_livro )
        if not consultaLivro:
            return

        if opcaoLocal == 'B':
            quantidade = InputInt( 'Quantidade de perca: ' )

            cursor.execute(
                "UPDATE Livros SET qtd_atual = ?, qtd_total = ? WHERE id = ?",
                ( consultaLivro[ LIVROS_QTD_ATUAL ] - quantidade, consultaLivro[ LIVROS_QTD_TOTAL ] - quantidade, id_livro )
            )

            cursor.execute(
                "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao ) VALUES ( ?, ?, ?, ?, ?, ? )",
                ( id_livro, 1, 'P', quantidade, None, None )
            )

            conexaoBiblioteca.commit()

        else:
            id_usuario = InputInt( 'ID do usuario: ' )

            if not VerificaUsuario( cursor, id_usuario ):
                return

            cursor.execute(
                "UPDATE Livros SET qtd_atual = ?, qtd_total = ? WHERE id = ?",
                ( consultaLivro[ LIVROS_QTD_ATUAL ] - 1, consultaLivro[ LIVROS_QTD_TOTAL ] - 1, id_livro )
            )

            cursor.execute(
                "UPDATE Usuarios SET status = ? WHERE id = ?",
                ( 'SIM', id_usuario )
            )

            cursor.execute(
                "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao ) VALUES ( ?, ?, ?, ?, ?, ? )",
                ( id_livro, id_usuario, 'P', 1, None, None )
            )

            conexaoBiblioteca.commit()

    else:
        LimparTela()

        print( 'Reposição do livro' )
        id_usuario = InputInt( 'ID do usuario: ' )

        if not VerificaUsuario( cursor, id_usuario ):
            return

        id_livro = InputInt( 'ID do livro..: ' )

        consultaLivro = VerificaLivro( cursor, id_livro )
        if not consultaLivro:
            return

        cursor.execute(
            "SELECT * FROM Gerenciamento WHERE id_usuario = ? AND movimentacao = ? AND id_livro = ?",
            ( id_usuario, 'P', id_livro )
        )
        consultaPerca = cursor.fetchone()

        if not consultaPerca:
            print( 'Não há registro de perda do livro pelo usuário' )
            input()
            return
        
        cursor.execute(
            "UPDATE Livros SET qtd_atual = ?, qtd_total = ? WHERE id = ?",
            ( consultaLivro[ LIVROS_QTD_ATUAL ] + 1, consultaLivro[ LIVROS_QTD_TOTAL ] + 1, id_livro )
        )

        cursor.execute(
            "UPDATE Usuarios SET status = ? WHERE id = ?",
            ( 'NAO', id_usuario )
        )

        cursor.execute(
            "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao ) VALUES ( ?, ?, ?, ?, ?, ? )",
            ( id_livro, id_usuario, 'D', 1, None, None )
        )

        conexaoBiblioteca.commit()
        print( 'Reposição do livro realizada com sucesso')

    input()


def InicializaBiblioteca( cursor, conexaoBiblioteca ):
    
    cursor.execute(
        "SELECT * FROM Usuarios"
    )
    consultaUsuario = cursor.fetchone()

    if not consultaUsuario:
        return 
        
    cursor.execute(
        "INSERT INTO Usuarios ( usuario, data_nascimento, endereco, cidade, email, status ) VALUES ( ?, ?, ?, ?, ?, ? )",
        ( 'BIBLIOTECA', None, '', '', '', 'NAO' )
    )
    conexaoBiblioteca.commit()


def VerificaUsuario( cursor, id_usuario ):

    cursor.execute(
        "SELECT * FROM Usuarios WHERE id = ?",
        ( id_usuario, )
    )
    consultaUsuario = cursor.fetchone()

    if not consultaUsuario:
        print( 'ID do Usuario não encontrado' )
        input()
        return False

    return consultaUsuario


def VerificaLivro( cursor, id_livro ):
    cursor.execute(
        "SELECT * FROM livros WHERE id = ?",
        ( id_livro, )
    )
    consultaLivro = cursor.fetchone()

    if not consultaLivro:
        print( 'ID do Livro não encontrado' )
        input()
        return False

    return consultaLivro



if __name__ == "__main__":
    Main()
