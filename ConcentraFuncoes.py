from datetime import datetime, timedelta
import os
import sqlite3
from utils import *
from utils.constants import BUSINESS_DAYS_LOAN

class ConcentraFuncoes:

    def __init__( self ):

        db_path = os.path.join( os.path.dirname( __file__ ), 'biblioteca.db' )
        self.conexaoBiblioteca = sqlite3.connect( db_path )
        self.cursor            = self.conexaoBiblioteca.cursor()

        self.VerificaBiblioteca( self.cursor )
        self.InicializaBiblioteca( self.cursor, self.conexaoBiblioteca )
        self.AtualizaStatusUsuarios( self.cursor, self.conexaoBiblioteca )
    
    def InicializaBiblioteca( self, cursor, conexaoBiblioteca ):
    
        cursor.execute(
            "SELECT * FROM Usuarios"
        )
        consultaUsuario = cursor.fetchone()

        if consultaUsuario:
            return 
            
        cursor.execute(
            "INSERT INTO Usuarios ( usuario, data_nascimento, endereco, bairro, cidade, estado, cep, email, status, telefone ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
            ( 'BIBLIOTECA', None, '', '', '', '', None, '', 'NAO', 0 )
        )
        conexaoBiblioteca.commit()
    
    def _calcular_idade( self, data_nascimento ):
        if not data_nascimento:
            return ''

        try:
            if isinstance( data_nascimento, str ):
                nascimento = datetime.strptime( data_nascimento, "%Y-%m-%d" ).date()
            else:
                nascimento = data_nascimento

            hoje = datetime.now().date()
            idade = hoje.year - nascimento.year - ( ( hoje.month, hoje.day ) < ( nascimento.month, nascimento.day ) )
            return str( idade )
        except Exception:
            return ''

    def AtualizaStatusUsuarios( self, cursor, conexaoBiblioteca ):

        cursor.execute(
            "SELECT * FROM Gerenciamento WHERE movimento = ?",
            ( 'S', )
        )
        registros = cursor.fetchall()

        if not registros:
            return
        
        for registro in registros:
            if registro[ Gerenciamento.DATA_VCTO ] == None:
                continue

            if datetime.strptime( registro[ Gerenciamento.DATA_VCTO ], "%Y-%m-%dT%H:%M:%S.%f" ).date() < datetime.now().date():
                cursor.execute(
                    "UPDATE Usuarios SET status = ? WHERE id = ?",
                    ( 'SIM', registro[ Gerenciamento.ID_USUARIO ] )
                )

        conexaoBiblioteca.commit()

    def VerificaBiblioteca( self, cursor ):
        cursor.execute( 
            """
            CREATE TABLE IF NOT EXISTS Livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro TEXT NOT NULL,
                autor TEXT,
                qtd_atual INTEGER NOT NULL,
                qtd_total INTEGER NOT NULL,
                ano_publicacao INTEGER,
                sinopse
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
                data_devolucao TEXT,
                motivo TEXT
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
                bairro TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep INTEGER,
                email TEXT NOT NULL,
                status TEXT NOT NULL,
                telefone INTEGER NOT NULL
                )
            """
        )

    def SalvarRegistroLivro( self, dados ):

        titulo          = dados[ 'titulo'     ].text().strip()
        autor           = dados[ 'autor'      ].text().strip()
        publicacao_text = dados[ 'publicacao' ].text().strip()
        sinopse         = dados[ 'sinopse'    ].toPlainText().strip()

        if not titulo or not autor:
            return False, 'Título e autor são obrigatórios.'

        if not publicacao_text:
            return False, 'Ano de publicação obrigatório.'

        try:
            publicacao = int( publicacao_text )
        except ValueError:
            return False, 'Ano de publicação deve ser um número válido.'

        ano_atual = datetime.now().year
        if publicacao > ano_atual:
            return False, f'Ano de publicação não pode ser maior que { ano_atual }.'

        self.cursor.execute(
            "SELECT id FROM Livros WHERE livro = ? AND autor = ?",
            ( titulo, autor )
        )
        existente = self.cursor.fetchone()

        if existente:
            return False, 'Livro já cadastrado.'

        self.cursor.execute(
            "INSERT INTO Livros ( livro, autor, qtd_atual, qtd_total, ano_publicacao, sinopse ) VALUES ( ?, ?, ?, ?, ?, ? )",
            ( titulo, autor, 0, 0, publicacao, sinopse )
        )
        self.conexaoBiblioteca.commit()

        return True, f'Livro "{ titulo }" registrado com sucesso.'

    def SalvarRegistroUsuario( self, dados ):
        nome           = dados[ 'nome'       ].text().strip()
        nascimento     = dados[ 'nascimento' ].date()
        endereco       = dados[ 'endereco'   ].text().strip()
        bairro         = dados[ 'bairro'     ].text().strip()
        cidade         = dados[ 'cidade'     ].text().strip()
        estado         = dados[ 'estado'     ].text().strip()
        telefone_text  = dados[ 'telefone'   ].text().strip()
        email          = dados[ 'email'      ].text().strip()
        cep_text       = dados[ 'cep'        ].text().strip()

        if not nome:
            return False, 'Nome é obrigatório.'

        if not nascimento.isValid():
            return False, 'Data de nascimento inválida.'

        nascimento = nascimento.toString( 'yyyy-MM-dd' )

        if not endereco:
            return False, 'Endereço é obrigatório.'

        if not cidade:
            return False, 'Cidade é obrigatória.'

        if not email or '@' not in email or '.' not in email:
            return False, 'Email inválido.'

        cep_digits = ''.join( [ c for c in cep_text if c.isdigit() ] )
        if len( cep_digits ) != 8:
            return False, 'CEP deve ter 8 dígitos.'

        telefone_digits = ''.join( [ c for c in telefone_text if c.isdigit() ] )
        if len( telefone_digits ) < 10:
            return False, 'Telefone inválido.'

        self.cursor.execute(
            "SELECT * FROM Usuarios WHERE usuario = ? AND data_nascimento = ? AND endereco = ? AND cidade = ? AND email = ?",
            ( nome, nascimento, endereco, cidade, email )
        )
        existe = self.cursor.fetchone()

        if existe:
            return False, 'Usuário já cadastrado.'

        self.cursor.execute(
            "INSERT INTO Usuarios ( usuario, data_nascimento, endereco, cidade, bairro, estado, cep, email, status, telefone ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
            ( nome, nascimento, endereco, cidade, bairro, estado, int( cep_digits ), email, 'NAO', int( telefone_digits ) )
        )
        self.conexaoBiblioteca.commit()

        return True, f'Usuário "{ nome }" cadastrado com sucesso.'

    def SalvarAdicaoLivro( self, dados ):
        titulo       = dados[ 'titulo'       ].text().strip()
        forma        = dados[ 'forma_entrada' ].currentText().strip()
        data_entrada = dados[ 'data_entrada' ].date()
        quantidade   = dados[ 'quantidade'   ].value()

        if not titulo:
            return False, 'Título do livro obrigatório.'

        if not data_entrada.isValid():
            return False, 'Data de aquisição inválida.'

        if quantidade < 1:
            return False, 'Quantidade deve ser maior que zero.'

        self.cursor.execute(
            "SELECT id, qtd_atual, qtd_total FROM Livros WHERE livro = ?",
            ( titulo, )
        )
        livro = self.cursor.fetchone()

        if not livro:
            return False, 'Livro não cadastrado.'

        novo_qtd_atual = livro[ 1 ] + quantidade
        novo_qtd_total = livro[ 2 ] + quantidade

        self.cursor.execute(
            "UPDATE Livros SET qtd_atual = ?, qtd_total = ? WHERE id = ?",
            ( novo_qtd_atual, novo_qtd_total, livro[ 0 ] )
        )

        self.cursor.execute(
            "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao, motivo ) VALUES ( ?, ?, ?, ?, ?, ?, ? )",
            ( livro[ 0 ], 0, 'A', quantidade, data_entrada.toString( 'yyyy-MM-dd' ), None, forma )
        )
        self.conexaoBiblioteca.commit()

        return True, f'Adição de { quantidade } exemplar(es) de "{ titulo }" registrada com sucesso.'

    def SalvarDevolucao( self, dados ):
        id_usuario_text = dados[ 'id_usuario' ].text().strip()
        titulo_livro    = dados[ 'titulo_livro' ].text().strip()
        data_devolucao  = dados[ 'data_devolucao' ].date()
        quantidade      = dados[ 'quantidade' ].value()
        multa_text      = dados[ 'multa' ].text().strip()

        if not id_usuario_text:
            return False, 'Usuário obrigatório.'

        if id_usuario_text.isdigit():
            id_usuario = int( id_usuario_text )
        else:
            id_usuario = self.get_usuario_id_por_nome( id_usuario_text )
            if id_usuario is None:
                return False, 'Usuário não encontrado.'

        if not titulo_livro:
            return False, 'Título do livro obrigatório.'

        if not data_devolucao.isValid():
            return False, 'Data de devolução inválida.'

        if quantidade < 1:
            return False, 'Quantidade deve ser maior que zero.'

        self.cursor.execute(
            "SELECT id FROM Usuarios WHERE id = ?",
            ( id_usuario, )
        )
        usuario = self.cursor.fetchone()

        if not usuario:
            return False, 'Usuário não cadastrado.'

        self.cursor.execute(
            "SELECT id, qtd_atual FROM Livros WHERE livro = ?",
            ( titulo_livro, )
        )
        livro = self.cursor.fetchone()

        if not livro:
            return False, 'Livro não cadastrado.'

        self.cursor.execute(
            "SELECT operacao, quantidade, data_vencimento FROM Gerenciamento WHERE id_livro = ? AND id_usuario = ? AND movimento = ? AND data_devolucao IS NULL",
            ( livro[ 0 ], id_usuario, 'S' )
        )
        movimento = self.cursor.fetchone()

        if not movimento:
            return False, 'Empréstimo não encontrado para esse usuário e livro.'

        emprestimo_quantidade = movimento[ 1 ]
        if quantidade != emprestimo_quantidade:
            return False, 'A quantidade de devolução deve ser igual à quantidade emprestada.'

        data_devolucao_text = data_devolucao.toString( 'yyyy-MM-dd' )
        motivo = f'Multa: { multa_text }' if multa_text else None

        self.cursor.execute(
            "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao, motivo ) VALUES ( ?, ?, ?, ?, ?, ?, ? )",
            ( livro[ 0 ], id_usuario, 'E', quantidade, movimento[ 2 ], data_devolucao_text, motivo )
        )

        self.cursor.execute(
            "UPDATE Livros SET qtd_atual = qtd_atual + ? WHERE id = ?",
            ( quantidade, livro[ 0 ] )
        )

        self.cursor.execute(
            "UPDATE Gerenciamento SET data_devolucao = ? WHERE operacao = ?",
            ( data_devolucao_text, movimento[ 0 ] )
        )

        self.conexaoBiblioteca.commit()

        return True, f'Livro "{ titulo_livro }" devolvido com sucesso.'

    def SalvarEmprestimo( self, dados ):
        id_usuario_text   = dados[ 'id'             ].text().strip()
        data_emprestimo   = dados[ 'data_emprestimo' ].date()
        livro_item        = dados[ 'livro'          ]
        quantidade        = dados[ 'quantidade'     ].value()

        if not id_usuario_text:
            return False, 'Usuário obrigatório.'

        if id_usuario_text.isdigit():
            id_usuario = int( id_usuario_text )
        else:
            id_usuario = self.get_usuario_id_por_nome( id_usuario_text )
            if id_usuario is None:
                return False, 'Usuário não encontrado.'

        if not data_emprestimo.isValid():
            return False, 'Data de empréstimo inválida.'

        if quantidade < 1:
            return False, 'Quantidade deve ser maior que zero.'

        data_emprestimo_py = date(
            data_emprestimo.year(),
            data_emprestimo.month(),
            data_emprestimo.day()
        )
        data_devolucao_py = add_business_days( data_emprestimo_py, BUSINESS_DAYS_LOAN )

        livro_titulo = ''

        if isinstance( livro_item, str ):
            livro_titulo = livro_item.strip()
        elif hasattr( livro_item, 'text' ):
            livro_titulo = livro_item.text().strip()
        else:
            livro_titulo = str( livro_item ).strip()

        if not livro_titulo or livro_titulo == '0':
            return False, 'Título do livro não informado.'

        self.cursor.execute(
            "SELECT id FROM Usuarios WHERE id = ?",
            ( id_usuario, )
        )
        usuario = self.cursor.fetchone()

        if not usuario:
            return False, 'Usuário não cadastrado.'

        self.cursor.execute(
            "SELECT id, qtd_atual FROM Livros WHERE livro = ?",
            ( livro_titulo, )
        )
        livro = self.cursor.fetchone()

        if not livro:
            return False, 'Livro não cadastrado.'

        if livro[ 1 ] < quantidade:
            return False, 'Não há exemplares suficientes disponíveis.'

        self.cursor.execute(
            "SELECT 1 FROM Gerenciamento WHERE id_usuario = ? AND movimento = ? AND data_devolucao IS NULL",
            ( id_usuario, 'S' )
        )
        emprestimo_aberto = self.cursor.fetchone()

        if emprestimo_aberto:
            return False, 'O usuário já possui um livro emprestado e não pode pegar outro até devolver.'

        self.cursor.execute(
            "SELECT 1 FROM Gerenciamento WHERE id_livro = ? AND id_usuario = ? AND movimento = ? AND data_devolucao IS NULL",
            ( livro[ 0 ], id_usuario, 'S' )
        )
        existente = self.cursor.fetchone()

        if existente:
            return False, 'O usuário já possui esse livro emprestado.'

        self.cursor.execute(
            "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao, motivo ) VALUES ( ?, ?, ?, ?, ?, ?, ? )",
            ( livro[ 0 ], id_usuario, 'S', quantidade, data_devolucao_py.isoformat(), None, 'Empréstimo' )
        )

        self.cursor.execute(
            "UPDATE Livros SET qtd_atual = qtd_atual - ? WHERE id = ?",
            ( quantidade, livro[ 0 ] )
        )

        self.conexaoBiblioteca.commit()

        return True, f'Empréstimo de { quantidade } exemplar(es) do livro "{ livro_titulo }" registrado com sucesso.'

    def SalvarRegistroPerda( self, dados ):
        titulo_livro      = dados[ 'titulo'      ].text().strip()
        data_perca        = dados[ 'data_perca'  ].date()
        responsavel       = dados[ 'responsavel' ].currentText().strip()
        motivo_perca      = dados[ 'motivo'      ].currentText().strip()
        usuario_responsavel = dados.get( 'usuario' )

        if not titulo_livro:
            return False, 'Título do livro obrigatório.'

        if not data_perca.isValid():
            return False, 'Data de perda inválida.'

        if responsavel == 'Usuário':
            if not usuario_responsavel:
                return False, 'Usuário responsável obrigatório.'
            
            usuario_text = usuario_responsavel.text().strip() if hasattr(usuario_responsavel, 'text') else str(usuario_responsavel).strip()
            
            if not usuario_text:
                return False, 'Nome do usuário obrigatório.'

        self.cursor.execute(
            "SELECT id, qtd_atual, qtd_total FROM Livros WHERE livro = ?",
            ( titulo_livro, )
        )
        livro = self.cursor.fetchone()

        if not livro:
            return False, 'Livro não cadastrado.'

        novo_qtd_atual = max( 0, livro[ 1 ] - 1 )
        novo_qtd_total = max( 0, livro[ 2 ] - 1 )

        self.cursor.execute(
            "UPDATE Livros SET qtd_atual = ?, qtd_total = ? WHERE id = ?",
            ( novo_qtd_atual, novo_qtd_total, livro[ 0 ] )
        )

        motivo_text = f'{ responsavel } - { motivo_perca }'
        self.cursor.execute(
            "INSERT INTO Gerenciamento ( id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao, motivo ) VALUES ( ?, ?, ?, ?, ?, ?, ? )",
            ( livro[ 0 ], 0, 'P', 1, None, data_perca.toString( 'yyyy-MM-dd' ), motivo_text )
        )

        self.conexaoBiblioteca.commit()

        return True, f'Perda do livro "{ titulo_livro }" registrada com sucesso.'

    def get_next_usuario_id( self ) -> int:
        self.cursor.execute(
            "SELECT MAX(id) FROM Usuarios"
        )
        r = self.cursor.fetchone()
        if not r or r[0] is None:
            return 1
        return int(r[0]) + 1

    def get_next_livro_id( self ) -> int:
        self.cursor.execute(
            "SELECT MAX(id) FROM Livros"
        )
        r = self.cursor.fetchone()
        if not r or r[0] is None:
            return 1
        return int(r[0]) + 1

    def get_catalogo_livros( self ):
        self.cursor.execute(
            "SELECT id, livro, autor, ano_publicacao, qtd_atual, qtd_total FROM Livros"
        )
        return self.cursor.fetchall()

    def get_available_books( self ):
        self.cursor.execute(
            "SELECT id, livro, autor, ano_publicacao, qtd_atual FROM Livros WHERE qtd_atual > 0"
        )
        return self.cursor.fetchall()

    def get_livros_cadastrados( self ):
        self.cursor.execute(
            "SELECT livro FROM Livros ORDER BY livro COLLATE NOCASE ASC"
        )
        return [ row[ 0 ] for row in self.cursor.fetchall() if row[ 0 ] ]

    def get_usuarios_cadastrados_nomes( self ):
        self.cursor.execute(
            "SELECT usuario FROM Usuarios WHERE usuario != ? ORDER BY usuario COLLATE NOCASE ASC",
            ( 'BIBLIOTECA', )
        )
        return [ row[ 0 ] for row in self.cursor.fetchall() if row[ 0 ] ]

    def get_usuario_id_por_nome( self, nome ):
        nome = ( nome or '' ).strip()
        if not nome:
            return None
        self.cursor.execute(
            "SELECT id FROM Usuarios WHERE lower(usuario) = lower(?) LIMIT 1",
            ( nome, )
        )
        usuario = self.cursor.fetchone()
        if usuario:
            return int( usuario[ 0 ] )
        self.cursor.execute(
            "SELECT id FROM Usuarios WHERE lower(usuario) LIKE lower(?) LIMIT 1",
            ( f'%{ nome }%', )
        )
        usuario = self.cursor.fetchone()
        if usuario:
            return int( usuario[ 0 ] )
        return None

    def get_livro_id_por_nome( self, nome ):
        nome = ( nome or '' ).strip()
        if not nome:
            return None
        self.cursor.execute(
            "SELECT id FROM Livros WHERE lower(livro) = lower(?) LIMIT 1",
            ( nome, )
        )
        livro = self.cursor.fetchone()
        if livro:
            return int( livro[ 0 ] )
        self.cursor.execute(
            "SELECT id FROM Livros WHERE lower(livro) LIKE lower(?) LIMIT 1",
            ( f'%{ nome }%', )
        )
        livro = self.cursor.fetchone()
        if livro:
            return int( livro[ 0 ] )
        return None

    def get_usuarios_cadastrados( self ):
        self.cursor.execute(
            "SELECT id, usuario, data_nascimento, endereco, cidade, bairro, estado, cep, email, status, telefone FROM Usuarios WHERE usuario != ?",
            ( 'BIBLIOTECA', )
        )
        return self.cursor.fetchall()

    def get_usuarios_com_status( self ):
        usuarios = self.get_usuarios_cadastrados()
        dados = []

        for usuario in usuarios:
            id_usuario = usuario[ 0 ]
            nome = usuario[ 1 ]
            idade = self._calcular_idade( usuario[ 2 ] )

            self.cursor.execute(
                "SELECT COALESCE( SUM( quantidade ), 0 ) FROM Gerenciamento WHERE id_usuario = ? AND movimento = ? AND data_devolucao IS NULL",
                ( id_usuario, 'S' )
            )
            qtd_emprestada = self.cursor.fetchone()[ 0 ] or 0

            status = 'Pode pegar novo livro' if qtd_emprestada == 0 else 'Bloqueado até devolução'
            dados.append( {
                'id': id_usuario,
                'nome': nome,
                'idade': idade,
                'qtd_emprestada': int( qtd_emprestada ),
                'status': status
            } )

        return dados

    def buscar_movimentacoes( self, movimento=None, data_inicio=None, data_fim=None, usuario_id=None, usuario_nome=None, livro_id=None, livro_nome=None ):

        def _parse_date( val ):
            if not val:
                return None
            from datetime import datetime, date
            if isinstance( val, date ) and not isinstance( val, datetime ):
                return val
            if isinstance( val, datetime ):
                return val.date()
            try:
                return datetime.fromisoformat( val ).date()
            except Exception:
                try:
                    return datetime.strptime( val, "%Y-%m-%d" ).date()
                except Exception:
                    return None

        data_inicio_dt = _parse_date( data_inicio )
        data_fim_dt = _parse_date( data_fim )

        sql = "SELECT operacao, id_livro, id_usuario, movimento, quantidade, data_vencimento, data_devolucao, motivo FROM Gerenciamento"
        params = []
        if movimento:
            sql += " WHERE movimento = ?"
            params.append( movimento )

        self.cursor.execute( sql, tuple( params ) )
        registros = self.cursor.fetchall()

        resultados = []
        for operacao, id_livro, id_usuario, mov, quantidade, data_vencimento, data_devolucao, motivo in registros:
            # busca títulos e nomes
            titulo_livro_db = None
            nome_usuario_db = None

            self.cursor.execute( "SELECT livro FROM Livros WHERE id = ?", ( id_livro, ) )
            r = self.cursor.fetchone()
            if r:
                titulo_livro_db = r[ 0 ]

            self.cursor.execute( "SELECT usuario FROM Usuarios WHERE id = ?", ( id_usuario, ) )
            r = self.cursor.fetchone()
            if r:
                nome_usuario_db = r[ 0 ]

            # Filtrar por ids
            if usuario_id:
                try:
                    if int( usuario_id ) != int( id_usuario ):
                        continue
                except Exception:
                    pass

            if livro_id:
                try:
                    if int( livro_id ) != int( id_livro ):
                        continue
                except Exception:
                    pass

            # Filtrar por nomes (substring, case-insensitive)
            if usuario_nome and nome_usuario_db:
                if usuario_nome.lower() not in nome_usuario_db.lower():
                    continue

            if livro_nome and titulo_livro_db:
                if livro_nome.lower() not in titulo_livro_db.lower():
                    continue

            # Filtrar por intervalo de datas (aplica-se a data_vencimento ou data_devolucao quando existir)
            from datetime import datetime
            def _date_in_range( dt_str ):
                if not dt_str:
                    return False
                try:
                    dt = datetime.fromisoformat( dt_str ).date()
                except Exception:
                    try:
                        dt = datetime.strptime( dt_str, "%Y-%m-%d" ).date()
                    except Exception:
                        return False
                if data_inicio_dt and dt < data_inicio_dt:
                    return False
                if data_fim_dt and dt > data_fim_dt:
                    return False
                return True

            if data_inicio_dt or data_fim_dt:
                ok = False
                if _date_in_range( data_vencimento ):
                    ok = True
                if _date_in_range( data_devolucao ):
                    ok = True
                if not ok:
                    continue

            # tenta inferir data do empréstimo quando for movimento de empréstimo ('S') e houver data_vencimento
            data_emprestimo_iso = None
            if mov == 'S' and data_vencimento:
                try:
                    from datetime import datetime, timedelta
                    venc = datetime.fromisoformat( data_vencimento ).date()
                    dias = 0
                    current = venc
                    while dias < BUSINESS_DAYS_LOAN:
                        current -= timedelta( days=1 )
                        if current.weekday() < 5:
                            dias += 1
                    data_emprestimo_iso = current.isoformat()
                except Exception:
                    data_emprestimo_iso = None

            resultados.append( ( id_usuario, nome_usuario_db, id_livro, titulo_livro_db, data_emprestimo_iso, data_vencimento, data_devolucao, mov, quantidade ) )

        return resultados
