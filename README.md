# SISTEMA DE CONTROLE DE LIVROS NUMA BIBLIOTECA

O projeto foi criada para gerenciar uma biblioteca a partir do zero

No menu principal do projeto, estão disponíveis seguintes opções:

1. Registrar Livro
    *Permite registrar um livro, informando o nome do livro e o nome do autor
2. Registrar Usuário
    * Permite registrar o usuário da biblioteca, informando alguns dados cadastrais
3. Adicionar Livro
    * Faz a verificação se o livro que será adicionado está registrada devidamente, e permite acrescentar mais unidades do livro informado
4. Emprestar Livro
    * Permite emprestar livro para os usuários cadastrados, colocando algumas limitações como não permitir emprestar livro caso o usuário já possua o mesmo livro emprestado, ou caso tenha em posse um livro emprestado que passou do prazo de devolução, ou caso tenha estragado livro e não tenha reposto o livro para a biblioteca
5. Devolver Livro
    *Faz a devolução de livros pegos emprestados pelos usuários, verificando se o usuário realmente tenha pego o livro da biblioteca ou não
6. Catalogar os livros
    * Permite verificar os livros que estão disponíveis e indisponívies para o emprestimo, levando em consideração o estoque atual da biblioteca em relação aos livros
7. Verificar o registro das movimentações dos livros
    * Abre uma tela de consulta de movimentação dos livros, registrando todas as saídas e entradas dos livros, bem como a baixa e adição dos livros há biblioteca
8. Verificar e registrar perda de livros
    * Permite fazer consulta específica a livros que foram dadas baixas, e verificar o responsável pela perca do livro
    * Permite registrar a perca do livro, verificando se a perca foi ocasionada pela biblioteca ou pelos usuários, se for pela biblioteca, irá perguntar a quantidade de baixa do livro, se for um usuário, irá verificar primeiramente se o usuário de fato estava em posse do livro da biblioteca, e assim posteriormente irá registrar a perca do livro no seu cadastro, e no seu cadastro no sistema, irá constar status como pendente, o que irá impossilibitar de pegar um outro livro emprestado até que seja reposta o livro perdido
    * Possui uma opção que irá registrar a reposição do livro perdido pelo usuário, assim que passar por todas as suas validações, o status de pendencia do usuário irá ser baixada

Além dessas opções, o sistema irá fazer uma validação automática dos prazos de vencimentos de devolução dos usuários, caso um usuário esteja em posse de algum livro por mais tempo do que a data prevista de devolução, o status do usuário ficará pendente até que o livro seja devolvida
