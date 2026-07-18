import os
from datetime import datetime, date, timedelta

def LimparTela():
    os.system( 'cls' if os.name == 'nt' else 'clear' )

def add_business_days(start_date: date, business_days: int) -> date:
    current = start_date
    days_added = 0

    while days_added < business_days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days_added += 1

    return current

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