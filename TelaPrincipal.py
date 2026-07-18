from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QTextEdit, QPushButton, QDateEdit, QSpinBox,
    QLineEdit, QMessageBox, QLabel, QStackedWidget, QComboBox,
    QFormLayout, QGroupBox, QSizePolicy, QHeaderView, QAbstractItemView, QFrame,
    QCompleter, QApplication
)
from PySide6.QtCore import QTimer, Qt, QDate, QRegularExpression, QEvent, QStringListModel
from PySide6.QtGui import (
    QIntValidator, QTextCursor, QIcon, QBrush, QColor, QFont,
    QKeySequence, QShortcut, QDoubleValidator, QValidator, QRegularExpressionValidator,
    QFontMetrics
)
from datetime import datetime
from layout_config import (
    create_page_layout,
    create_row_layout,
    create_page_title,
    create_form_group,
    create_action_row,
    create_readonly_label,
    create_date_edit,
    create_table_widget
)
from utils import add_business_days
from utils.constants import (
    CATALOG_TABLE_HEADERS,
    USERS_TABLE_HEADERS,
    LOAN_BOOK_TABLE_HEADERS,
    BUSINESS_DAYS_LOAN
)


class TelaPrincipal( QWidget ):
    
    def __init__( self, funcoes ):
        
        super().__init__()

        self.funcoes = funcoes

        self.setWindowTitle( 'Sistema de controle bibliotecário' )
        
        # Define tamanho proporcionalmente ajustável usando a área disponível da tela
        screen = QApplication.instance().primaryScreen()
        available_geometry = screen.availableGeometry()
        
        screen_width = available_geometry.width()
        screen_height = available_geometry.height()
        
        # Dimensiona a janela com 85% da tela disponível, com máximos sensatos
        janela_width = min( int( screen_width * 0.85 ), 1200 )
        janela_height = min( int( screen_height * 0.85 ), 800 )
        
        self.resize( janela_width, janela_height )
        
        # Centraliza a janela na área disponível da tela
        x = available_geometry.left() + ( screen_width - janela_width ) // 2
        y = available_geometry.top() + ( screen_height - janela_height ) // 4
        self.move( x, y )

        self.Layout_Principal = QHBoxLayout()

        Layout_Esqueda = QVBoxLayout()

        self.Botao_Usuario = QPushButton( 'Usuário' )
        self.Botao_Livro = QPushButton( 'Livro' )
        self.Botao_Movimentacao = QPushButton( 'Movimentação' )
        self.Botao_Configuracao = QPushButton( 'Configuração' )

        self.Submenu_Usuario = QFrame()
        self.Submenu_Usuario.setFrameShape( QFrame.Shape.StyledPanel )
        self.Submenu_Usuario.setStyleSheet( 'background-color: #2b2b2b; border: 1px solid #444444; border-radius: 4px;' )
        submenu_layout_usuario = QVBoxLayout( self.Submenu_Usuario )
        submenu_layout_usuario.setContentsMargins( 10, 6, 10, 6 )
        submenu_layout_usuario.setSpacing( 4 )
        self.Botao_Registrar_Usuario = QPushButton( 'Registrar Usuário' )
        self.Botao_Lista_Usuarios = QPushButton( 'Lista de Usuários' )
        submenu_layout_usuario.addWidget( self.Botao_Registrar_Usuario )
        submenu_layout_usuario.addWidget( self.Botao_Lista_Usuarios )
        self.Submenu_Usuario.setVisible( False )

        self.Submenu_Livro = QFrame()
        self.Submenu_Livro.setFrameShape( QFrame.Shape.StyledPanel )
        self.Submenu_Livro.setStyleSheet( 'background-color: #2b2b2b; border: 1px solid #444444; border-radius: 4px;' )
        submenu_layout_livro = QVBoxLayout( self.Submenu_Livro )
        submenu_layout_livro.setContentsMargins( 10, 6, 10, 6 )
        submenu_layout_livro.setSpacing( 4 )
        self.Botao_Registrar_Livro = QPushButton( 'Registrar Livro' )
        self.Botao_Catalogo = QPushButton( 'Catálogo' )
        submenu_layout_livro.addWidget( self.Botao_Registrar_Livro )
        submenu_layout_livro.addWidget( self.Botao_Catalogo )
        self.Submenu_Livro.setVisible( False )

        self.Submenu_Movimentacao = QFrame()
        self.Submenu_Movimentacao.setFrameShape( QFrame.Shape.StyledPanel )
        self.Submenu_Movimentacao.setStyleSheet( 'background-color: #2b2b2b; border: 1px solid #444444; border-radius: 4px;' )
        submenu_layout_movimentacao = QVBoxLayout( self.Submenu_Movimentacao )
        submenu_layout_movimentacao.setContentsMargins( 10, 6, 10, 6 )
        submenu_layout_movimentacao.setSpacing( 4 )
        self.Botao_Adiciona_Livro = QPushButton( 'Adicionar Livro' )
        self.Botao_Empresta_Livro = QPushButton( 'Emprestar Livro' )
        self.Botao_Devolve_Livro = QPushButton( 'Devolver Livro' )
        self.Botao_Registro_Perca = QPushButton( 'Registro Perda' )
        submenu_layout_movimentacao.addWidget( self.Botao_Adiciona_Livro )
        submenu_layout_movimentacao.addWidget( self.Botao_Empresta_Livro )
        submenu_layout_movimentacao.addWidget( self.Botao_Devolve_Livro )
        submenu_layout_movimentacao.addWidget( self.Botao_Registro_Perca )
        self.Submenu_Movimentacao.setVisible( False )

        grupo_usuario = QWidget()
        layout_grupo_usuario = QVBoxLayout( grupo_usuario )
        layout_grupo_usuario.setContentsMargins( 0, 0, 0, 0 )
        layout_grupo_usuario.setSpacing( 4 )
        layout_grupo_usuario.addWidget( self.Botao_Usuario )
        layout_grupo_usuario.addWidget( self.Submenu_Usuario )

        grupo_livro = QWidget()
        layout_grupo_livro = QVBoxLayout( grupo_livro )
        layout_grupo_livro.setContentsMargins( 0, 0, 0, 0 )
        layout_grupo_livro.setSpacing( 4 )
        layout_grupo_livro.addWidget( self.Botao_Livro )
        layout_grupo_livro.addWidget( self.Submenu_Livro )

        grupo_movimentacao = QWidget()
        layout_grupo_movimentacao = QVBoxLayout( grupo_movimentacao )
        layout_grupo_movimentacao.setContentsMargins( 0, 0, 0, 0 )
        layout_grupo_movimentacao.setSpacing( 4 )
        layout_grupo_movimentacao.addWidget( self.Botao_Movimentacao )
        layout_grupo_movimentacao.addWidget( self.Submenu_Movimentacao )

        Layout_Esqueda.addWidget( grupo_usuario )
        Layout_Esqueda.addWidget( grupo_livro )
        Layout_Esqueda.addWidget( grupo_movimentacao )
        Layout_Esqueda.addStretch()
        Layout_Esqueda.addWidget( self.Botao_Configuracao )

        self.Stack = QStackedWidget()
        self.LayoutInicializacao()
        self.LayoutRegistroLivro()
        self.LayoutRegistroUsuario()
        self.LayoutListaUsuarios()
        self.LayoutAdicionaLivro()
        self.LayoutEmprestaLivro()
        self.LayoutDevolveLivro()
        self.LayoutCatalogo()
        self.LayoutRegistroPerca()
        self.LayoutConsultaMovimentacao()
        self.LayoutConfiguracao()

        self.Layout_Principal.addLayout( Layout_Esqueda, 2 )
        self.Layout_Principal.addWidget( self.Stack, 8 )

        self.setLayout( self.Layout_Principal )
        self.Stack.currentChanged.connect( self._on_page_changed )

        self.Botao_Usuario.clicked.connect( lambda: self._show_submenu( 'usuario' ) )
        self.Botao_Livro.clicked.connect( lambda: self._show_submenu( 'livro' ) )
        self.Botao_Movimentacao.clicked.connect( lambda: self._show_submenu( 'movimentacao' ) )
        self.Botao_Registrar_Usuario.clicked.connect( lambda: self.Stack.setCurrentIndex( 2 ) )
        self.Botao_Lista_Usuarios.clicked.connect( lambda: self.Stack.setCurrentIndex( 3 ) )
        self.Botao_Registrar_Livro.clicked.connect( lambda: self.Stack.setCurrentIndex( 1 ) )
        self.Botao_Catalogo.clicked.connect( lambda: self.Stack.setCurrentIndex( 7 ) )
        self.Botao_Adiciona_Livro.clicked.connect( lambda: self.Stack.setCurrentIndex( 4 ) )
        self.Botao_Empresta_Livro.clicked.connect( lambda: self.Stack.setCurrentIndex( 5 ) )
        self.Botao_Devolve_Livro.clicked.connect( lambda: self.Stack.setCurrentIndex( 6 ) )
        self.Botao_Registro_Perca.clicked.connect( lambda: self.Stack.setCurrentIndex( 8 ) )
        # adicionar atalho para consulta movimentação: cria botão na submenu
        self.Botao_Consulta_Movimentacao = QPushButton( 'Movimentação' )
        submenu_layout_movimentacao.addWidget( self.Botao_Consulta_Movimentacao )
        self.Botao_Consulta_Movimentacao.clicked.connect( lambda: self.Stack.setCurrentIndex( 9 ) )
        self.Botao_Configuracao.clicked.connect( lambda: [ self._show_submenu( None ), self.Stack.setCurrentIndex( 10 ) ] )

    def _on_page_changed( self, index ):
        if index == 3:
            self._refresh_lista_usuarios()
        if index == 7:
            self._refresh_catalogo()

    def _show_submenu( self, submenu_name ):
        self.Submenu_Usuario.setVisible( submenu_name == 'usuario' )
        self.Submenu_Livro.setVisible( submenu_name == 'livro' )
        self.Submenu_Movimentacao.setVisible( submenu_name == 'movimentacao' )

        if submenu_name != 'usuario':
            self.Submenu_Usuario.setVisible( False )
        if submenu_name != 'livro':
            self.Submenu_Livro.setVisible( False )
        if submenu_name != 'movimentacao':
            self.Submenu_Movimentacao.setVisible( False )

    def _create_id_display( self, value='' ):
        container = QWidget()
        row = QHBoxLayout()
        row.setContentsMargins( 0, 0, 0, 0 )
        row.setSpacing( 4 )

        label = QLabel( 'ID:' )
        label.setStyleSheet( 'font-weight: bold;' )
        value_label = create_readonly_label( value )

        row.addWidget( label )
        row.addWidget( value_label )
        row.addStretch()
        container.setLayout( row )
        return container, value_label

    def _refresh_lista_usuarios( self ):
        if not hasattr( self, 'tabela_usuarios' ):
            return

        usuarios = self.funcoes.get_usuarios_com_status()
        self.tabela_usuarios.setRowCount( len( usuarios ) )

        for linha, usuario in enumerate( usuarios ):
            self.tabela_usuarios.setItem( linha, 0, QTableWidgetItem( str( usuario[ 'nome' ] ) ) )
            self.tabela_usuarios.setItem( linha, 1, QTableWidgetItem( str( usuario[ 'idade' ] ) ) )
            self.tabela_usuarios.setItem( linha, 2, QTableWidgetItem( str( usuario[ 'qtd_emprestada' ] ) ) )
            self.tabela_usuarios.setItem( linha, 3, QTableWidgetItem( str( usuario[ 'status' ] ) ) )

    def _refresh_catalogo( self ):
        if not hasattr( self, 'tabela_catalogo' ):
            return

        livros = self.funcoes.get_catalogo_livros()
        self.tabela_catalogo.setRowCount( len( livros ) )

        for linha, livro in enumerate( livros ):
            titulo = livro[ 1 ] if len( livro ) > 1 else ''
            autor = livro[ 2 ] if len( livro ) > 2 else ''
            ano = livro[ 3 ] if len( livro ) > 3 else ''
            qtd_atual = livro[ 4 ] if len( livro ) > 4 else 0
            qtd_total = livro[ 5 ] if len( livro ) > 5 else 0
            status = 'Disponível' if qtd_atual > 0 else 'Indisponível'

            self.tabela_catalogo.setItem( linha, 0, QTableWidgetItem( str( titulo ) ) )
            self.tabela_catalogo.setItem( linha, 1, QTableWidgetItem( str( autor ) ) )
            self.tabela_catalogo.setItem( linha, 2, QTableWidgetItem( str( ano ) ) )
            self.tabela_catalogo.setItem( linha, 3, QTableWidgetItem( str( qtd_total ) ) )
            self.tabela_catalogo.setItem( linha, 4, QTableWidgetItem( status ) )

    def _create_action_row( self, *widgets ):
        return create_action_row( *widgets )

    def _create_autocomplete_field( self, values, placeholder='' ):
        field = QLineEdit()
        field.setClearButtonEnabled( True )
        if placeholder:
            field.setPlaceholderText( placeholder )

        suggestions = sorted( { value for value in values if value }, key=lambda item: item.lower() )
        model = QStringListModel( suggestions )
        completer = QCompleter( model, field )
        completer.setCaseSensitivity( Qt.CaseSensitivity.CaseInsensitive )
        completer.setFilterMode( Qt.MatchFlag.MatchContains )
        completer.setMaxVisibleItems( 5 )
        field.setCompleter( completer )
        return field

    def _create_page_title( self, text ):
        return create_page_title( text )

    def _create_form_group( self, text ):
        return create_form_group( text )

    def _configure_combo_box_width( self, combo_box ):
        if combo_box.count() == 0:
            return

        metrics = QFontMetrics( combo_box.font() )
        longest_text = max(
            combo_box.itemText( index )
            for index in range( combo_box.count() )
        )
        width = metrics.horizontalAdvance( longest_text ) + 40
        combo_box.setMinimumWidth( width )
        combo_box.setSizeAdjustPolicy( QComboBox.SizeAdjustPolicy.AdjustToContents )
        combo_box.setSizePolicy( QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed )

    def _create_standard_table( self, rows=0, columns=0, headers=None ):
        table = QTableWidget()
        table.setRowCount( rows )
        table.setColumnCount( columns )
        if headers:
            table.setHorizontalHeaderLabels( headers )
        table.setAlternatingRowColors( True )
        table.setSelectionBehavior( QAbstractItemView.SelectionBehavior.SelectRows )
        table.setSelectionMode( QAbstractItemView.SelectionMode.SingleSelection )
        table.setEditTriggers( QAbstractItemView.EditTrigger.NoEditTriggers )
        table.setWordWrap( True )
        table.verticalHeader().setVisible( False )
        table.horizontalHeader().setSectionResizeMode( QHeaderView.ResizeMode.ResizeToContents )
        table.horizontalHeader().setMinimumSectionSize( 120 )
        table.horizontalHeader().setDefaultAlignment( Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter )
        table.setVerticalScrollBarPolicy( Qt.ScrollBarPolicy.ScrollBarAsNeeded )
        table.setHorizontalScrollBarPolicy( Qt.ScrollBarPolicy.ScrollBarAsNeeded )
        table.setMinimumHeight( 320 )
        table.setSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding )
        table.setStyleSheet( """
            QTableWidget {
                background-color: #1f1f1f;
                color: #f5f5f5;
                alternate-background-color: #2b2b2b;
                selection-background-color: #5b8def;
                selection-color: #ffffff;
                gridline-color: #444444;
            }
            QHeaderView::section {
                background-color: #303030;
                color: #f5f5f5;
                padding: 8px;
                border: 1px solid #444444;
            }
        """ )
        return table

    def _reset_form_fields( self, fields, first_field=None ):
        for field in fields:
            if isinstance( field, QLineEdit ):
                field.clear()
            elif isinstance( field, QTextEdit ):
                field.clear()
            elif isinstance( field, QComboBox ):
                field.setCurrentIndex( 0 )
            elif isinstance( field, QSpinBox ):
                field.setValue( field.minimum() )
            elif isinstance( field, QDateEdit ):
                field.setDate( QDate.currentDate() )

        if first_field is not None:
            QTimer.singleShot( 0, lambda: first_field.setFocus() )

    def LayoutInicializacao( self ):
        
        pagina_inicializacao = QWidget()
        layout_inicializacao = QVBoxLayout()
        titulo = QLabel( 'Selecione uma das opções ao lado' )

        layout_inicializacao.addWidget( titulo, alignment = Qt.AlignmentFlag.AlignCenter )
        pagina_inicializacao.setLayout( layout_inicializacao )
        self.Stack.addWidget( pagina_inicializacao )

    def LayoutListaUsuarios( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Lista de Usuários' )
        self.tabela_usuarios = self._create_standard_table(
            rows=0,
            columns=4,
            headers=[ 'Nome', 'Idade', 'Livros em posse', 'Status' ]
        )
        self.tabela_usuarios.setColumnWidth( 0, 220 )
        self.tabela_usuarios.setColumnWidth( 1, 90 )
        self.tabela_usuarios.setColumnWidth( 2, 140 )

        layout.addWidget( titulo )
        layout.addWidget( self.tabela_usuarios )
        layout.addStretch()

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )
        self._refresh_lista_usuarios()
    
    def LayoutRegistroLivro( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = create_page_title( 'Registro de Livros' )

        id_container, id_livro = self._create_id_display()
        try:
            id_livro.setText( str( self.funcoes.get_next_livro_id() ) )
        except Exception:
            id_livro.setText( '' )
        self.id_livro_label = id_livro

        titulo_livro = QLineEdit()
        titulo_livro.setMaxLength( 100 )
        titulo_livro.setPlaceholderText( 'Digite o título do livro' )
        titulo_livro.setClearButtonEnabled( True )

        autor_livro = QLineEdit()
        autor_livro.setMaxLength( 100 )
        autor_livro.setPlaceholderText( 'Digite o autor do livro' )
        autor_livro.setClearButtonEnabled( True )

        self.ano_publicacao = QLineEdit()
        self.ano_publicacao.setMaxLength( 4 )
        self.ano_publicacao.setValidator(
            QIntValidator( 0, datetime.now().year, self.ano_publicacao )
        )

        self.mensagem_validacao_ano = QLabel()
        self.mensagem_validacao_ano.setStyleSheet( 'color: #c62828; font-size: 10pt;' )

        sinopse = QTextEdit()
        sinopse.setPlaceholderText( 'Digite a sinopse do livro aqui' )

        self.AdicionaEnterNavegacao( titulo_livro )
        self.AdicionaEnterNavegacao( autor_livro )
        self.AdicionaEnterNavegacao( self.ano_publicacao )
        self.AdicionaEnterNavegacao( sinopse )

        botao_registrar = QPushButton( 'Registrar' )
        botao_registrar.setDefault( True )
        botao_registrar.setFixedWidth( 120 )

        form_group, form_layout = create_form_group( 'Informações do livro' )
        form_layout.addRow( '', id_container )
        form_layout.addRow( 'Título:', titulo_livro )
        form_layout.addRow( 'Autor:', autor_livro )

        ano_row = QWidget()
        ano_row_layout = QHBoxLayout()
        ano_row_layout.setContentsMargins( 0, 0, 0, 0 )
        ano_row_layout.addWidget( self.ano_publicacao )
        ano_row_layout.addWidget( self.mensagem_validacao_ano )
        ano_row_layout.addStretch()
        ano_row.setLayout( ano_row_layout )
        form_layout.addRow( 'Ano da publicação:', ano_row )

        form_layout.addRow( 'Sinopse:', sinopse )

        layout.addWidget( titulo )
        layout.addWidget( form_group )
        layout.addLayout( self._create_action_row( botao_registrar ) )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        hDadosRegistroLivro = {
            'titulo'    : titulo_livro,
            'autor'     : autor_livro,
            'publicacao': self.ano_publicacao,
            'sinopse'   : sinopse
        }

        self.ano_publicacao.textChanged.connect( self.MsgValidaAno )
        botao_registrar.clicked.connect( lambda: self.RegistrarDados(
            self.funcoes.SalvarRegistroLivro,
            hDadosRegistroLivro,
            [ titulo_livro, autor_livro, self.ano_publicacao, sinopse ],
            titulo_livro
        ) )
    
    def LayoutRegistroUsuario( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Registro de Usuários' )

        id_container, id_usuario = self._create_id_display()
        try:
            id_usuario.setText( str( self.funcoes.get_next_usuario_id() ) )
        except Exception:
            id_usuario.setText( '' )
        self.id_usuario_label = id_usuario

        nome_usuario = QLineEdit()
        nome_usuario.setMaxLength( 100 )
        nome_usuario.setPlaceholderText( 'Digite o nome' )
        nome_usuario.setClearButtonEnabled( True )

        data_nascimento = create_date_edit( min_date=QDate( 1900, 1, 1 ), max_date=QDate.currentDate() )

        endereco = QLineEdit()
        endereco.setMaxLength( 100 )
        endereco.setPlaceholderText( 'Digite o endereço' )
        endereco.setClearButtonEnabled( True )

        bairro = QLineEdit()
        bairro.setMaxLength( 100 )
        bairro.setPlaceholderText( 'Digite o bairro' )
        bairro.setClearButtonEnabled( True )

        cidade = QLineEdit()
        cidade.setMaxLength( 100 )
        cidade.setPlaceholderText( 'Digite a cidade' )
        cidade.setClearButtonEnabled( True )

        estado = QLineEdit()
        estado.setMaxLength( 100 )
        estado.setPlaceholderText( 'Digite o estado' )
        estado.setClearButtonEnabled( True )

        telefone = QLineEdit()
        telefone.setInputMask( '(99) 99999-9999' )
        telefone.setClearButtonEnabled( True )

        email = QLineEdit()
        email.setMaxLength( 100 )
        email.setPlaceholderText( 'Digite o email' )
        email.setClearButtonEnabled( True )
        email_regexp = QRegularExpression( r'^[^@\s]+@[^@\s]+\.[^@\s]+$' )
        email_validator = QRegularExpressionValidator( email_regexp, email )
        email.setValidator( email_validator )

        cep = QLineEdit()
        cep.setInputMask( '99999-999' )
        cep.setClearButtonEnabled( True )

        botao_registrar = QPushButton( 'Registrar' )
        botao_registrar.setDefault( True )
        botao_registrar.setFixedWidth( 120 )

        for widget in (nome_usuario, data_nascimento, cep, endereco, bairro, cidade, estado, telefone, email, botao_registrar):
            self.AdicionaEnterNavegacao( widget )

        form_group, form_layout = create_form_group( 'Dados do usuário' )
        form_layout.addRow( '', id_container )
        form_layout.addRow( 'Nome:', nome_usuario )
        form_layout.addRow( 'Data de nascimento:', data_nascimento )
        form_layout.addRow( 'CEP:', cep )
        form_layout.addRow( 'Endereço:', endereco )
        form_layout.addRow( 'Bairro:', bairro )
        form_layout.addRow( 'Cidade:', cidade )
        form_layout.addRow( 'Estado:', estado )
        form_layout.addRow( 'Telefone:', telefone )
        form_layout.addRow( 'Email:', email )

        layout.addWidget( titulo )
        layout.addWidget( form_group )
        layout.addLayout( self._create_action_row( botao_registrar ) )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        hDadosRegistroUsuario = {
            'id'        : id_usuario,
            'nome'      : nome_usuario,
            'nascimento': data_nascimento,
            'endereco'  : endereco,
            'bairro'    : bairro,
            'cidade'    : cidade,
            'estado'    : estado,
            'telefone'  : telefone,
            'email'     : email,
            'cep'       : cep
        }

        botao_registrar.clicked.connect( lambda: self.RegistrarDados(
            self.funcoes.SalvarRegistroUsuario,
            hDadosRegistroUsuario,
            [ nome_usuario, data_nascimento, cep, endereco, bairro, cidade, estado, telefone, email ],
            nome_usuario
        ) )
    
    def LayoutAdicionaLivro( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Adicionar Livro' )

        titulo_livro = self._create_autocomplete_field(
            self.funcoes.get_livros_cadastrados(),
            placeholder='Digite o título do livro'
        )
        titulo_livro.setMaxLength( 100 )

        forma_entrada = QComboBox()
        forma_entrada.addItems( [ 'Doação', 'Compra', 'Reposição' ] )
        self._configure_combo_box_width( forma_entrada )

        data_entrada = create_date_edit( min_date=None, max_date=None )
        data_entrada.setDate( QDate.currentDate() )

        quantidade = QSpinBox()
        quantidade.setRange( 1, 100 )

        botao_registrar = QPushButton( 'Registrar' )
        botao_registrar.setDefault( True )
        botao_registrar.setFixedWidth( 120 )

        self.AdicionaEnterNavegacao( titulo_livro )
        self.AdicionaEnterNavegacao( forma_entrada )
        self.AdicionaEnterNavegacao( data_entrada )
        self.AdicionaEnterNavegacao( quantidade )
        self.AdicionaEnterNavegacao( botao_registrar )

        form_group, form_layout = self._create_form_group( 'Dados da entrada' )
        form_layout.addRow( 'Livro:', titulo_livro )
        form_layout.addRow( 'Adquirido por:', forma_entrada )
        form_layout.addRow( 'Data de aquisição:', data_entrada )
        form_layout.addRow( 'Quantidade:', quantidade )

        layout.addWidget( titulo )
        layout.addWidget( form_group )
        layout.addLayout( self._create_action_row( botao_registrar ) )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        hDadosAdicaoLivro = {
            'titulo'       : titulo_livro,
            'forma_entrada': forma_entrada,
            'data_entrada' : data_entrada,
            'quantidade'   : quantidade
        }
        botao_registrar.clicked.connect( lambda: self.RegistrarDados(
            self.funcoes.SalvarAdicaoLivro,
            hDadosAdicaoLivro,
            [ titulo_livro, forma_entrada, data_entrada, quantidade ],
            titulo_livro
        ) )
    
    def LayoutEmprestaLivro( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Emprestar Livro' )

        id_usuario = self._create_autocomplete_field(
            self.funcoes.get_usuarios_cadastrados_nomes(),
            placeholder='Digite o nome do usuário'
        )

        titulo_livro = self._create_autocomplete_field(
            self.funcoes.get_livros_cadastrados(),
            placeholder='Digite o título do livro'
        )
        titulo_livro.setMaxLength( 100 )

        data_emprestimo = QDateEdit()
        data_emprestimo.setCalendarPopup( True )
        data_emprestimo.setDisplayFormat( 'dd/MM/yyyy' )
        data_emprestimo.setDate( QDate.currentDate() )
        data_emprestimo.setFixedWidth( 110 )

        data_devolucao = QDateEdit()
        data_devolucao.setCalendarPopup( True )
        data_devolucao.setDisplayFormat( 'dd/MM/yyyy' )
        data_devolucao.setDate( QDate.currentDate().addDays( 14 ) )
        data_devolucao.setFixedWidth( 110 )

        quantidade = QSpinBox()
        quantidade.setRange( 1, 100 )

        tabela_selecao = self._create_standard_table(
            rows=6,
            columns=5,
            headers=[ 'Livro', 'Autor', 'Ano', 'Disponível', 'Local' ]
        )

        botao_registrar = QPushButton( 'Registrar' )
        botao_registrar.setDefault( True )
        botao_registrar.setFixedWidth( 120 )

        for widget in (id_usuario, titulo_livro, data_emprestimo, data_devolucao, quantidade, botao_registrar):
            self.AdicionaEnterNavegacao( widget )

        form_group, form_layout = self._create_form_group( 'Detalhes do empréstimo' )
        form_layout.addRow( 'Usuário:', id_usuario )
        form_layout.addRow( 'Livro:', titulo_livro )
        form_layout.addRow( 'Data do empréstimo:', data_emprestimo )
        form_layout.addRow( 'Data de devolução:', data_devolucao )
        form_layout.addRow( 'Quantidade:', quantidade )

        layout.addWidget( titulo )
        layout.addWidget( form_group )
        layout.addWidget( tabela_selecao )
        layout.addLayout( self._create_action_row( botao_registrar ) )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        hDadosEmprestimo = {
            'id'             : id_usuario,
            'data_emprestimo': data_emprestimo,
            'data_devolucao' : data_devolucao,
            'livro'          : titulo_livro,
            'quantidade'     : quantidade
        }
        botao_registrar.clicked.connect( lambda: self.RegistrarDados(
            self.funcoes.SalvarEmprestimo,
            hDadosEmprestimo,
            [ id_usuario, titulo_livro, data_emprestimo, data_devolucao, quantidade ],
            id_usuario
        ) )
    
    def LayoutDevolveLivro( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Devolver Livro' )

        id_usuario = self._create_autocomplete_field(
            self.funcoes.get_usuarios_cadastrados_nomes(),
            placeholder='Digite o nome do usuário'
        )

        titulo_livro = self._create_autocomplete_field(
            self.funcoes.get_livros_cadastrados(),
            placeholder='Digite o título do livro'
        )
        titulo_livro.setMaxLength( 100 )
        titulo_livro.setPlaceholderText( 'Digite o título do livro' )
        titulo_livro.setClearButtonEnabled( True )

        data_emprestimo = QDateEdit()
        data_emprestimo.setCalendarPopup( True )
        data_emprestimo.setDisplayFormat( 'dd/MM/yyyy' )
        data_emprestimo.setFixedWidth( 110 )

        data_devolucao = QDateEdit()
        data_devolucao.setCalendarPopup( True )
        data_devolucao.setDisplayFormat( 'dd/MM/yyyy' )
        data_devolucao.setFixedWidth( 110 )

        quantidade = QSpinBox()
        quantidade.setRange( 1, 100 )

        multa = QLineEdit()
        multa.setValidator( QDoubleValidator( 0.0, 100.0, 2 ) )
        multa.setPlaceholderText( 'R$ 0.00' )

        botao_registrar = QPushButton( 'Registrar' )
        botao_registrar.setDefault( True )
        botao_registrar.setFixedWidth( 120 )

        for widget in (id_usuario, titulo_livro, data_emprestimo, data_devolucao, quantidade, multa, botao_registrar):
            self.AdicionaEnterNavegacao( widget )

        form_group, form_layout = self._create_form_group( 'Detalhes da devolução' )
        form_layout.addRow( 'Usuário:', id_usuario )
        form_layout.addRow( 'Título do livro:', titulo_livro )
        form_layout.addRow( 'Data do empréstimo:', data_emprestimo )
        form_layout.addRow( 'Data da devolução:', data_devolucao )
        form_layout.addRow( 'Quantidade:', quantidade )
        form_layout.addRow( 'Multa por atraso:', multa )

        layout.addWidget( titulo )
        layout.addWidget( form_group )
        layout.addLayout( self._create_action_row( botao_registrar ) )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        hDadosDevolucao = {
            'id_usuario'     : id_usuario,
            'titulo_livro'   : titulo_livro,
            'data_emprestimo': data_emprestimo,
            'data_devolucao' : data_devolucao,
            'quantidade'     : quantidade,
            'multa'          : multa
        }
        botao_registrar.clicked.connect( lambda: self.RegistrarDados(
            self.funcoes.SalvarDevolucao,
            hDadosDevolucao,
            [ id_usuario, titulo_livro, data_emprestimo, data_devolucao, quantidade, multa ],
            id_usuario
        ) )
    
    def LayoutCatalogo( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Catálogo' )

        # Barra de busca e ações
        busca = QLineEdit()
        busca.setPlaceholderText( 'Buscar título, autor ou ano...' )
        botao_buscar = QPushButton( 'Pesquisar' )
        botao_atualizar = QPushButton( 'Atualizar' )

        busca.setMinimumWidth( 240 )

        row = create_row_layout()
        row.addWidget( busca )
        row.addWidget( botao_buscar )
        row.addWidget( botao_atualizar )
        row.addStretch()

        self.tabela_catalogo = self._create_standard_table(
            rows=0,
            columns=5,
            headers=[ 'Título', 'Autor', 'Ano', 'Quantidade', 'Status' ]
        )

        layout.addWidget( titulo )
        layout.addLayout( row )
        layout.addWidget( self.tabela_catalogo )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )
        self._refresh_catalogo()
    
    def LayoutRegistroPerca( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Registro de Perda' )

        titulo_livro = self._create_autocomplete_field(
            self.funcoes.get_livros_cadastrados(),
            placeholder='Digite o título do livro'
        )
        titulo_livro.setMaxLength( 100 )

        data_perca = QDateEdit()
        data_perca.setCalendarPopup( True )
        data_perca.setDisplayFormat( 'dd/MM/yyyy' )
        data_perca.setDate( QDate.currentDate() )

        responsavel_perca = QComboBox()
        responsavel_perca.addItems( [ 'Biblioteca', 'Usuário' ] )
        self._configure_combo_box_width( responsavel_perca )

        usuario_perca = self._create_autocomplete_field(
            self.funcoes.get_usuarios_cadastrados_nomes(),
            placeholder='Digite o nome do usuário'
        )
        usuario_perca.setEnabled( False )

        motivo_perca = QComboBox()
        motivo_perca.addItems( [ 'Estrago', 'Perda', 'Furto' ] )
        self._configure_combo_box_width( motivo_perca )

        botao_registrar = QPushButton( 'Registrar' )
        botao_registrar.setDefault( True )
        botao_registrar.setFixedWidth( 120 )

        for widget in (titulo_livro, data_perca, responsavel_perca, usuario_perca, motivo_perca, botao_registrar):
            self.AdicionaEnterNavegacao( widget )

        # Conectar evento para habilitar/desabilitar campo de usuário
        def on_responsavel_changed( text ):
            usuario_perca.setEnabled( text == 'Usuário' )
            if text != 'Usuário':
                usuario_perca.clear()

        responsavel_perca.currentTextChanged.connect( on_responsavel_changed )

        form_group, form_layout = self._create_form_group( 'Detalhes da perda' )
        form_layout.addRow( 'Livro:', titulo_livro )
        form_layout.addRow( 'Data da perda:', data_perca )
        form_layout.addRow( 'Responsável:', responsavel_perca )
        form_layout.addRow( 'Usuário Responsável:', usuario_perca )
        form_layout.addRow( 'Motivo:', motivo_perca )

        layout.addWidget( titulo )
        layout.addWidget( form_group )
        layout.addLayout( self._create_action_row( botao_registrar ) )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        hDadosRegistroPerda = {
            'titulo'     : titulo_livro,
            'data_perca' : data_perca,
            'responsavel': responsavel_perca,
            'usuario'    : usuario_perca,
            'motivo'     : motivo_perca
        }
        botao_registrar.clicked.connect( lambda: self.RegistrarDados(
            self.funcoes.SalvarRegistroPerda,
            hDadosRegistroPerda,
            [ titulo_livro, data_perca, responsavel_perca, usuario_perca, motivo_perca ],
            titulo_livro
        ) )

    def LayoutConsultaMovimentacao( self ): 
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Consulta de Movimentações' )

        # filtros
        combo_mov = QComboBox()
        combo_mov.addItems( [ 'Todos', 'A - Adição', 'S - Empréstimo', 'E - Devolução', 'P - Perda' ] )
        data_inicio = create_date_edit( min_date=None, max_date=None )
        data_fim = create_date_edit( min_date=None, max_date=None )

        usuario_filtro_tipo = QComboBox()
        usuario_filtro_tipo.addItems( [ 'Nome', 'ID' ] )
        self._configure_combo_box_width( usuario_filtro_tipo )
        usuario_nome = self._create_autocomplete_field(
            self.funcoes.get_usuarios_cadastrados_nomes(),
            placeholder='Nome do usuário'
        )
        usuario_id = QLineEdit()
        usuario_id.setPlaceholderText( 'ID do usuário' )
        usuario_id.setClearButtonEnabled( True )
        usuario_id.setVisible( False )

        livro_filtro_tipo = QComboBox()
        livro_filtro_tipo.addItems( [ 'Nome', 'ID' ] )
        self._configure_combo_box_width( livro_filtro_tipo )
        livro_nome = self._create_autocomplete_field(
            self.funcoes.get_livros_cadastrados(),
            placeholder='Título do livro'
        )
        livro_id = QLineEdit()
        livro_id.setPlaceholderText( 'ID do livro' )
        livro_id.setClearButtonEnabled( True )
        livro_id.setVisible( False )

        botao_filtrar = QPushButton( 'Filtrar' )
        botao_limpar = QPushButton( 'Limpar' )

        filtro_layout = QVBoxLayout()
        filtro_layout.setContentsMargins( 0, 0, 0, 0 )
        filtro_layout.setSpacing( 8 )

        linha1 = create_row_layout()
        linha1.addWidget( QLabel( 'Tipo movimentação' ) )
        linha1.addWidget( combo_mov )
        linha1.addWidget( QLabel( '   Período' ) )
        linha1.addWidget( data_inicio )
        # linha1.addWidget( QLabel( 'até' ) )
        linha1.addWidget( data_fim )
        linha1.addStretch()
        filtro_layout.addLayout( linha1 )

        linha2 = create_row_layout()
        linha2.addWidget( QLabel( 'Usuário' ), 0.9 )
        linha2.addWidget( usuario_filtro_tipo, 1 )
        linha2.addWidget( usuario_nome, 7 )
        linha2.addWidget( usuario_id, 7 )
        linha2.addStretch()
        filtro_layout.addLayout( linha2 )

        linha3 = create_row_layout()
        linha3.addWidget( QLabel( 'Livro    ' ), 0.9 )
        linha3.addWidget( livro_filtro_tipo, 1 )
        linha3.addWidget( livro_nome, 7 )
        linha3.addWidget( livro_id, 7 )
        linha3.addStretch()
        filtro_layout.addLayout( linha3 )

        row = create_row_layout()
        row.addStretch()
        row.addWidget( botao_filtrar )
        row.addWidget( botao_limpar )
        filtro_layout.addLayout( row )

        tabela = self._create_standard_table( rows=0, columns=9, headers=[ 'ID Usuário', 'Nome Usuário', 'ID Livro', 'Título Livro', 'Data Empréstimo', 'Data Vencimento', 'Data Devolução', 'Tipo', 'Quantidade' ] )
        tabela.setMinimumHeight( 360 )
        tabela.setSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding )

        layout.addWidget( titulo )
        layout.addLayout( filtro_layout )
        layout.addWidget( tabela, stretch=1 )

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

        # guardar referências
        self.consulta_tabela_mov = tabela
        self.consulta_combo_mov = combo_mov
        self.consulta_data_inicio = data_inicio
        self.consulta_data_fim = data_fim
        self.consulta_usuario_id = usuario_id
        self.consulta_usuario_nome = usuario_nome
        self.consulta_usuario_filtro_tipo = usuario_filtro_tipo
        self.consulta_livro_id = livro_id
        self.consulta_livro_nome = livro_nome
        self.consulta_livro_filtro_tipo = livro_filtro_tipo

        def _toggle_usuario_filtro():
            tipo = usuario_filtro_tipo.currentText()
            usuario_nome.setVisible( tipo == 'Nome' )
            usuario_id.setVisible( tipo == 'ID' )

        def _toggle_livro_filtro():
            tipo = livro_filtro_tipo.currentText()
            livro_nome.setVisible( tipo == 'Nome' )
            livro_id.setVisible( tipo == 'ID' )

        usuario_filtro_tipo.currentTextChanged.connect( lambda _: _toggle_usuario_filtro() )
        livro_filtro_tipo.currentTextChanged.connect( lambda _: _toggle_livro_filtro() )
        _toggle_usuario_filtro()
        _toggle_livro_filtro()

        def _limpar():
            combo_mov.setCurrentIndex( 0 )
            data_inicio.setDate( QDate.currentDate() )
            data_fim.setDate( QDate.currentDate() )
            usuario_filtro_tipo.setCurrentIndex( 0 )
            livro_filtro_tipo.setCurrentIndex( 0 )
            usuario_id.clear()
            usuario_nome.clear()
            livro_id.clear()
            livro_nome.clear()
            _toggle_usuario_filtro()
            _toggle_livro_filtro()
            tabela.setRowCount( 0 )

        def _carregar():
            mov_text = combo_mov.currentText()
            mov = None if mov_text.startswith( 'Todos' ) else mov_text.split( ' - ' )[0]
            di = self.consulta_data_inicio.date().toString( 'yyyy-MM-dd' )
            df = self.consulta_data_fim.date().toString( 'yyyy-MM-dd' )

            usuario_tipo = self.consulta_usuario_filtro_tipo.currentText()
            ui = self.consulta_usuario_id.text().strip() or None if usuario_tipo == 'ID' else None
            un = self.consulta_usuario_nome.text().strip() or None if usuario_tipo == 'Nome' else None

            livro_tipo = self.consulta_livro_filtro_tipo.currentText()
            li = self.consulta_livro_id.text().strip() or None if livro_tipo == 'ID' else None
            ln = self.consulta_livro_nome.text().strip() or None if livro_tipo == 'Nome' else None

            resultados = self.funcoes.buscar_movimentacoes( movimento=mov, data_inicio=di, data_fim=df, usuario_id=ui, usuario_nome=un, livro_id=li, livro_nome=ln )

            tabela.setRowCount( len( resultados ) )
            for row_idx, r in enumerate( resultados ):
                # r: id_usuario, nome_usuario, id_livro, titulo_livro, data_emprestimo, data_vencimento, data_devolucao, mov, quantidade
                id_usuario, nome_usuario, id_livro, titulo_livro, data_emprestimo, data_vencimento, data_devolucao, mov, quantidade = r
                self.consulta_tabela_mov.setItem( row_idx, 0, QTableWidgetItem( str( id_usuario or '' ) ) )
                self.consulta_tabela_mov.setItem( row_idx, 1, QTableWidgetItem( nome_usuario or '' ) )
                self.consulta_tabela_mov.setItem( row_idx, 2, QTableWidgetItem( str( id_livro or '' ) ) )
                self.consulta_tabela_mov.setItem( row_idx, 3, QTableWidgetItem( titulo_livro or '' ) )
                self.consulta_tabela_mov.setItem( row_idx, 4, QTableWidgetItem( data_emprestimo or '' ) )
                self.consulta_tabela_mov.setItem( row_idx, 5, QTableWidgetItem( data_vencimento or '' ) )
                self.consulta_tabela_mov.setItem( row_idx, 6, QTableWidgetItem( data_devolucao or '' ) )
                self.consulta_tabela_mov.setItem( row_idx, 7, QTableWidgetItem( mov or '' ) )
                self.consulta_tabela_mov.setItem( row_idx, 8, QTableWidgetItem( str( quantidade or '' ) ) )

        botao_limpar.clicked.connect( _limpar )
        botao_filtrar.clicked.connect( _carregar )
    
    def LayoutConfiguracao( self ):
        pagina = QWidget()
        layout = create_page_layout()

        titulo = self._create_page_title( 'Configurações' )
        descricao = QLabel( 'Ajuste as opções do sistema nesta página.' )
        descricao.setWordWrap( True )

        layout.addWidget( titulo )
        layout.addWidget( descricao )
        layout.addStretch()

        pagina.setLayout( layout )
        self.Stack.addWidget( pagina )

    def RegistrarDados( self, salvar_func, dados, limpar_campos=None, primeiro_campo=None ):
        resultado = salvar_func( dados )
        if isinstance( resultado, tuple ) and len( resultado ) == 2:
            sucesso, mensagem = resultado
        else:
            sucesso = False
            mensagem = 'A operação não retornou um resultado esperado.'

        if sucesso:
            QMessageBox.information( self, 'Sucesso', mensagem )
            if limpar_campos:
                self._reset_form_fields( limpar_campos, primeiro_campo )
            try:
                self.RefreshSequentialIds()
            except Exception:
                pass
            try:
                self._refresh_lista_usuarios()
            except Exception:
                pass
        else:
            QMessageBox.warning( self, 'Erro', mensagem )

    def RefreshSequentialIds( self ):
        try:
            if hasattr( self, 'id_usuario_label' ):
                self.id_usuario_label.setText( str( self.funcoes.get_next_usuario_id() ) )
        except Exception:
            pass

        try:
            if hasattr( self, 'id_livro_label' ):
                self.id_livro_label.setText( str( self.funcoes.get_next_livro_id() ) )
        except Exception:
            pass

    def AdicionaEnterNavegacao( self, widget ):
        widget.installEventFilter( self )

    def EventFilter( self, watched, event ):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in ( Qt.Key.Key_Return, Qt.Key.Key_Enter ):
                if isinstance( watched, QPushButton ):
                    watched.click()
                    return True

                self.focusNextChild()
                return True

            if event.key() == Qt.Key.Key_Tab and isinstance( watched, QTextEdit ):
                self.focusNextChild()
                return True

            if event.key() == Qt.Key.Key_Backtab and isinstance( watched, QTextEdit ):
                self.focusPreviousChild()
                return True

        return super().eventFilter( watched, event )

    def MsgValidaAno( self, texto ):

        if not texto:
            self.mensagem_validacao_ano.setText('')
            return

        if not texto.isdigit():
            self.mensagem_validacao_ano.setText('Digite somente números')
            return

        ano = int(texto)
        ano_atual = datetime.now().year
        if ano > ano_atual:
            self.mensagem_validacao_ano.setText(f'Não pode ser maior que {ano_atual}')
        else:
            self.mensagem_validacao_ano.setText('')
        
