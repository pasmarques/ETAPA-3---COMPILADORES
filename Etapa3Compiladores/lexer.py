# Aluno: Pedro Affonso Silva Marques
# Código do analisador léxico da linguagem fictícia cic 2024.1

# Import dos módulos para manipular erros e arquivo, solicitando dependências do SO
import os
import sys

# Definição das classes Token e Erro
# Aqui a ideia foi basicamente juntar os dois principais pontos solicitados pela professora como objetos
# Visando a manipulação de cada token e erro para impressão das tabelas e relatórios de erro criei :

# Classe que simula um token da linguagem cic 2024.1
class Token:
    def __init__(self, tipo, valor, linha, coluna):
        self.tipo = tipo      # Tipo do token (identificador, palavra reservada, operador, etc.)
        self.valor = valor    # Valor do token (se aplicável)
        self.linha = linha    # Número da linha onde o token foi encontrado
        self.coluna = coluna  # Número da coluna onde o token foi encontrado
        
# Classe que simula um erro da linguagem cic 2024.1
class Erro:
    def __init__(self, msg, linha, coluna):
        self.msg = msg # Mensagem de erro
        self.linha = linha        # Número da linha onde o erro foi encontrado
        self.coluna = coluna      # Número da coluna onde o erro foi encontrado
        
    def __str__(self):
        return f'Erro linha {self.linha} coluna {self.coluna}: {self.msg}'
    
def criar_token(estado, lexema, linha, coluna):
    # Dicionário que mapeia estados para tipos de tokens
    tipos_tokens = {
        'q2': 'TK_INT',
        'q7': 'TK_FLOAT',
        'q16': 'TK_DATA',
        'q21': 'TK_ENDERECO',
        'q24': 'TK_CADEIA',
        'q30': 'TK_ID',
        'q32': 'TK_MENOS',
        'q33': 'TK_TIL',
        'q34': 'TK_MAIS',
        'q35': 'TK_ASTERISCO',
        'q36': 'TK_PORCENTO',
        'q37': 'TK_OR',
        'q39': 'TK_COMENTARIO',
        'q42': 'TK_ATRIBUICAO',
        'q43': 'TK_DIFERENTE',
        'q45': 'TK_IGUAL', 
        'q49': 'TK_MAIORIGUAL',
        'q50': 'TK_&',
        'q51': 'TK_RESERVADAS',
        'q52': 'TK_MENOR',
        'q53': 'TK_MENORIGUAL',
        'q54': 'TK_MAIOR',
        'q55': 'TK_DOISPONTOS',
        'q56': 'TK_ABREPAR',
        'q57': 'TK_FECHAPAR',
    }

    # Obtém o tipo de token do estado atual
    tokenDoEstado = tipos_tokens.get(estado, 'Desconhecido') # Se o estado não for reconhecido, assume 'Desconhecido'

    # Verifica se o token é um identificador reservado
    if tokenDoEstado == "TK_RESERVADAS":
        tokenDoEstado = verifica_se_e_reservado(lexema)

    # Retorna o  objeto token com o tipo, valor, linha e coluna
    return Token(tokenDoEstado, lexema, linha, coluna)

# Cria objeto erro
def criar_erro(lexema, linha, coluna):
    return Erro(lexema, linha, coluna)

def defineMsgErro(estado):
    # Dicionário que mapeia estados de erro para mensagens de erro correspondentes
    erroEstados ={
        'ERRO_INICIAL': 'caracter nao inicia token',
        'ERRO_CADEIA': 'cadeia nao fechada',
        'ERRO_DATA': 'data mal formatada',
        'q51': 'palavra reservada nao encontrada',
        'ERRO_ABRE_COMENT': 'comentario aberto de forma errada',
        'ERRO_FLOAT': 'float mal formatado',
        'ERRO_IDKW': 'variavel ou id mal formatado',
        'ERRO_ENDERECO': 'endereco mal formatado'
    }
    
    # Obtém a mensagem de erro correspondente ao estado
    msg = erroEstados.get(estado, 'Caracter nao inicia token')

    # Retorna a mensagem de erro
    return msg

def verifica_se_e_reservado(lexema):
    # Imprime uma mensagem para verificar o lexema sendo verificado
    print(f'Verificando lexema: {lexema}')
    
    # Dicionário que mapeia palavras reservadas para seus tokens correspondentes
    palavras_reservadas = {
        'rotina': 'TK_ROTINA',
        'fim_rotina': 'TK_FIM_ROTINA',
        'se': 'TK_SE',
        'senao': 'TK_SENAO',
        'imprima': 'TK_IMPRIMA',
        'leia': 'TK_LEIA',
        'para': 'TK_PARA',
        'enquanto': 'TK_ENQUANTO'
    }
    
    # Retorna o token correspondente ao lexema, ou 'TK_KW_INVALIDA' se não for uma palavra reservada
    return palavras_reservadas.get(lexema, 'TK_KW_INVALIDA')


def abrir_arquivo(nome_arquivo):
    try:
        arquivo = open(nome_arquivo, 'r')  # Tenta abrir o arquivo em modo de leitura
        linhas = arquivo.readlines()  # Lê todas as linhas do arquivo e armazena em uma lista
        arquivo.close()  # Fecha o arquivo após a leitura
        return linhas  # Retorna as linhas lidas do arquivo
    except FileNotFoundError:  # Captura a exceção se o arquivo não for encontrado
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)  # Sai do programa com código de erro 1 em caso de arquivo não encontrado
    except Exception as e:  # Captura qualquer outra exceção não prevista
        print(f"Erro ao abrir o arquivo: {e}")  # Imprime uma mensagem de erro genérica
        sys.exit(1)  # Sai do programa com código de erro 1 em caso de erro não previsto


def proximo_token_e_erros(linhasArq, lista_tokens, lista_erros):
    # Definições de estados e transições omitidas para brevidade

    # Lista de estados de aceitação
    estados_aceitacao = ['q2', 'q7', 'q16', 'q21', 'q24', 'q30', 'q32', 'q33',
                         'q34', 'q35', 'q36', 'q37', 'q39', 'q42', 'q43', 'q45', 
                         'q49', 'q50', 'q51', 'q52', 'q53', 'q54', 'q55', 'q56', 
                         'q57']

    # Lista de estados que não são dígitos
    estados_naoDigito = ['q2', 'q7', 'q21', 'q30', 'q51', 'q52', 'q53', 'q54']

    # Inicializa a linha
    l = 1

    # Indica se estamos ignorando o conteúdo entre <<< e >>>
    ignore_mode = False  
    # Linha onde o modo de ignorar iniciou
    ignore_start_line = 0  
    # Coluna onde o modo de ignorar iniciou
    ignore_start_col = 0  

    # Loop sobre as linhas do arquivo
    for linha in linhasArq:
        c = 0
        estado = 'q0'
        lexema = ''

        # Loop sobre os caracteres da linha
        while c < len(linha):
            caracter = linha[c]

            # Verifica se estamos no modo de ignorar
            if ignore_mode:
                # Se encontrou o fechamento do modo de ignorar
                if caracter == '>' and linha[c+1] == '>' and linha[c+2] == '>':
                    ignore_mode = False
                    c += 2  # Avança para o último '>' de '>>>'
                    continue
                else:
                    c += 1
                    continue

            lexema += caracter
            estado = transicaoAFD(estado, caracter)
            c += 1

            # Verifica se encontrou marcador de comentário
            if caracter == '<' and linha[c:c+2] == '<<':
                ignore_mode = True
                ignore_start_line = l
                ignore_start_col = c - 1  # Contabiliza o primeiro '<'
                c += 2  # Avança para o próximo caracter após '<<'
                continue

            # Verifica se o estado atual é um estado de aceitação
            if estado in estados_aceitacao:
                if estado == 'q39':
                    lexema = ''
                    estado = 'q0'
                    continue
                elif estado in estados_naoDigito: 
                    if estado == 'q51':
                        lexema = lexema[:-1]
                        lexemaReserved = verifica_se_e_reservado(lexema)
                        if lexemaReserved != "TK_KW_INVALIDA":
                            lista_tokens.append(criar_token(estado, lexema, l, c - len(lexema)))
                            lexema = ''
                            estado = 'q0'
                            c -= 1
                            continue
                        elif lexemaReserved == "TK_KW_INVALIDA":
                            msg = defineMsgErro(estado)
                            erro = criar_erro(msg, l, c)
                            lista_erros.append(erro)
                            lexema = ''
                            estado = 'q0'
                            c-=1
                            continue
                    lexema = lexema[:-1]  # Remove o último caractere
                    lista_tokens.append(criar_token(estado, lexema, l, c - len(lexema)))
                    lexema = ''
                    estado = 'q0'
                    c -= 1
                    continue

                lista_tokens.append(criar_token(estado, lexema, l, (c+1)-len(lexema)))
                lexema = ''
                estado = 'q0'
                continue

            # Verifica se o estado atual é um estado de erro
            elif estado == 'ERRO_INICIAL':
                if lexema == ' ' or lexema == "\n" or lexema == '\t':
                    lexema = ''
                    estado = 'q0'
                    continue
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                # Reiniciar o lexema e voltar para o estado inicial
                lexema = ''
                estado = 'q0'
                continue
            elif estado == 'ERRO_CADEIA':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                lexema = ''
                estado = 'q0'
                continue
            elif estado == 'ERRO_DATA':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                lexema = ''
                estado = 'q0'
                c -= 1
                continue
            elif estado == 'ERRO_FLOAT':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                lexema = ''
                estado = 'q0'
                c -= 1
                continue
            elif estado == 'ERRO_IDKW':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                lexema = ''
                estado = 'q0'
                c -= 1
                continue
            elif estado == 'ERRO_ENDERECO':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                lexema = ''
                estado = 'q0'
                c -= 1
                continue
            elif estado == 'ERRO_ENDERECO':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                lexema = ''
                estado = 'q0'
                c -= 1
                continue
            elif estado == 'ERRO_ABRE_COMENT':
                msg = defineMsgErro(estado)
                erro = criar_erro(msg, l, c)
                lista_erros.append(erro)
                # Não retorna token se comentário for aberto e não fechado
                return None

        l += 1

    # Se o modo de ignorar ainda estiver ativado no final do arquivo
    if ignore_mode:
        msg = "Comentario aberto (<<<) sem fechamento (>>>)"
        erro = criar_erro(msg, ignore_start_line, ignore_start_col+1)
        lista_erros.append(erro)

    return None # Se nenhum token for encontrado

# Função que simula a transição do afd
# Os estados de erros não estão presentes no autômato, mas eles foram postos aqui para conseguir depurar cada um
def transicaoAFD(estado,caracter):
    
    if estado == 'q0':
        if caracter.isdigit():
            estado = 'q1'
        elif 'A' <= caracter <= 'F':
            estado = 'q18'
        elif caracter == '.':
            estado = 'q8'
        elif caracter == '"':
            estado = 'q22'   
        elif 'a' <= caracter <= 'z':
            estado = 'q28'
        elif caracter == '|':
            estado = 'q37'
        elif caracter == '&':
            estado = 'q50'
        elif caracter == '%':
            estado = 'q36'
        elif caracter == '*':
            estado = 'q35'
        elif caracter == '+':
            estado = 'q34'
        elif caracter == '~':
            estado = 'q33'
        elif caracter == '-':
            estado = 'q32'
        elif caracter == ':':
            estado = 'q55'
        elif caracter == '<':
            estado = 'q40'
        elif caracter == '(':
            estado = 'q56'
        elif caracter == ')':
            estado = 'q57'
        elif caracter == '>':
            estado = 'q48'
        elif caracter == '=':
            estado = 'q44'
        elif caracter == '#':
            estado = 'q38'
        #elif caracter.isspace():
         #   estado = 'q0'
        else:
            estado = 'ERRO_INICIAL'
    elif estado == 'q1':
        if caracter == '.':
            estado = 'q5'
        elif caracter == 'x':
            estado = 'q19'
        elif caracter.isdigit():
            estado = 'q3'
        else:
            estado = 'q2' 
    elif estado == 'q3':
        if caracter == '/':
            estado = 'q27'
        elif caracter == '_':
            estado = 'q13'
        elif caracter == '.':
            estado = 'q5'
        elif caracter.isdigit():
            estado = 'q4'
        else:
            estado = 'q2'
    elif estado == 'q4':
        if caracter == '.':
            estado = 'q5'
        elif caracter.isdigit():
            estado = 'q12'
        else:
            estado = 'q2'
    elif estado == 'q12':
        if caracter.isdigit():
            estado = 'q12'
        else:
            estado = 'q2'  
    elif estado == 'q8':
        if caracter.isdigit():
            estado = 'q5'
        else:
            estado = 'ERRO_FLOAT'
    elif estado == 'q5':
        if caracter.isdigit():
            estado = 'q5'
        elif caracter == 'e':
            estado = 'q9'
        else:
            estado = 'q7' 
    elif estado == 'q6':
        if caracter.isdigit():
            estado = 'q6'
        else:
            estado = 'q7' 
    elif estado == 'q9':
        if caracter.isdigit():
            estado = 'q11'
        elif caracter == '-':
            estado = 'q10'
        else:
            estado = 'ERRO_FLOAT'
    elif estado == 'q10':
        if caracter.isdigit():
            estado = 'q11'
        else:
            estado = 'ERRO_FLOAT'
    elif estado == 'q11':
        if caracter.isdigit():
            estado = 'q11'
        else:
            estado = 'q7'
    elif estado == 'q18':
        if caracter == 'x':
            estado = 'q19'
        else:
            estado = 'ERRO_ENDERECO'
    elif estado == 'q19':
        if caracter.isdigit() or  'A' <= caracter <= 'F':
            estado = 'q20'
        else:
            estado = 'ERRO_ENDERECO'
    elif estado == 'q20':
         if (caracter.isdigit()) or  ('A' <= caracter <= 'F'):
            estado = 'q20'
         else:
            estado = 'q21'
    elif estado == 'q27':
        if caracter.isdigit():
            estado = 'q60'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q60':
        if caracter.isdigit():
            estado = 'q61'
        else:
            estado ='ERRO_DATA'
    elif estado == 'q61':
        if caracter == '/':
            estado = 'q62'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q62':
        if caracter.isdigit():
            estado = 'q26'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q26':
        if caracter.isdigit():
            estado = 'q14'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q14':
        if caracter.isdigit():
            estado = 'q15'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q15':
        if caracter.isdigit():
            estado = 'q16'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q13':
        if caracter.isdigit():
            estado = 'q63'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q63':
        if caracter.isdigit():
            estado = 'q64'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q64':
        if caracter == '_':
            estado = 'q65'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q65':
        if caracter.isdigit():
            estado = 'q26'
        else:
            estado = 'ERRO_DATA'
    elif estado == 'q22':
        if caracter != '\n' and caracter == '"':
            estado = 'q24'
        elif caracter == '\n' :
            estado = 'ERRO_CADEIA'
        else:
            estado='q22'
    elif estado == 'q28':
        if 'A' <= caracter <= 'Z':
            estado = 'q29'
        elif 'a' <= caracter <= 'z':
            estado = 'q58'
        else:
            estado = 'ERRO_IDKW'
    elif estado == 'q29':
        if 'a' <= caracter <= 'z':
            estado = 'q31'
        elif not('a' <= caracter <= 'z') and not ('A' <= caracter <= 'Z'):
            estado = 'q30'
        else:
            estado = 'ERRO_ID_E_KW'
    elif estado == 'q31':
        if 'A' <= caracter <= 'Z':
            estado = 'q29' 
        elif not ('a' <= caracter <= 'z') and not ('A' <= caracter <= 'Z'):
            estado = 'q30'
        else:
            estado = 'ERRO_ID_E_KW'
    elif estado == 'q58':
        if caracter == '_' or 'a' <= caracter <= 'z':
            estado = 'q58'
        else:
            estado = 'q51'
    elif estado == 'q40':
        if caracter == '<':
            estado = 'q46'
        elif caracter == '=':
            estado = 'q41'
        elif caracter == '>':
            estado = 'q43'
        else:
            estado = 'q52'
    elif estado == 'q41':
        if caracter == '=':
            estado = 'q42'
        else:
            estado = 'q53'
    elif estado == 'q48':
        if caracter == '=':
            estado = 'q49'
        else:
            estado = 'q54'
    elif estado == 'q46':
        if caracter == '<':
            estado = 'q47'
        else:
            estado = 'ERRO_ABRE_COMENT'
    elif estado == 'q47':
        if caracter == '>':
            estado = 'q17'
        else:
            estado = 'q47'
    elif estado == 'q17':
        if caracter == '>':
            estado = 'q25'
        else:
            estado = 'q47'
    elif estado == 'q25':
        if caracter == '>':
            estado = 'q39'
        else:
            estado = 'q47'
    elif estado == 'q38':
        if caracter != '\n':
            estado = 'q38'
        else:
            estado = 'q39'

    return estado


def printaTokens(listaTokens):
    # Imprime o cabeçalho da tabela
    print("+-----+-----+---------------+---------------------------+")
    print("| LIN | COL |    TOKEN      |           LEXEMA          |")
    print("+-----+-----+---------------+---------------------------+")
   
    # Inicializa a variável para acompanhar a linha anterior
    linha_anterior = None
    
    # Lista de tipos especiais que precisam ser formatados de forma diferente
    tipos_especiais = ['TK_INT', 'TK_FLOAT', 'TK_DATA', 'TK_CADEIA','TK_ENDERECO', 'TK_ID', 'TK_ROTINA', 'TK_FIM_ROTINA', 'TK_SE', 'TK_SENAO', 'TK_IMPRIMA', 'TK_LEIA', 'TK_PARA', 'TK_ENQUANTO']
    
    # Itera sobre os tokens da lista
    for token in listaTokens:
        # Verifica se o token está na mesma linha que o anterior
        if token.linha == linha_anterior:
            linha_str = " "*5  # Se sim, não precisa imprimir o número da linha novamente
        else:
            linha_str = str(token.linha).center(5)  # Se não, imprime o número da linha centralizado
            linha_anterior = token.linha  # Atualiza a linha anterior
            
        # Verifica se o tipo do token é um tipo especial que precisa de formatação diferente
        if token.tipo in tipos_especiais:
            lexema_str = token.valor.center(27)  # Se sim, centraliza o lexema
        else:
            lexema_str = " "*27  # Se não, não há lexema a ser exibido
        
        # Imprime os detalhes do token formatados na tabela
        print(f"|{linha_str}|{str(token.coluna).center(5)}|{token.tipo.center(15)}|{lexema_str}|")
        print("+-----+-----+---------------+---------------------------+")
    
    # Imprime uma nova linha no final
    print("\n")

def mostrar_erros(conteudo_arquivo, lista_erros):
    # Imprime cabeçalho
    print("\n\nLista de erros:\n")
    
    # Itera sobre cada linha do conteúdo do arquivo
    for num, linha in enumerate(conteudo_arquivo, start=1):
        # Imprime o número da linha seguido pelo conteúdo da linha
        # rstrip() remove o \n no final da linha
        print(f"[{num}]{linha.rstrip()}")

        # Verifica se há algum erro presente nesta linha
        erro_presente = False
        for erro in lista_erros:
            if erro.linha == num:
                erro_presente = True
                # Marcação de erro na linha (sublinhado)
                marcação = '-' * (erro.coluna - 1) + '^'
                quant_digitos = len(str(num))
                # Imprime a marcação de erro sob a linha com erro
                print(f"{' ' * (quant_digitos+2)}{marcação}")
        
        # Se houver erro nesta linha, imprime as mensagens de erro
        if erro_presente:
            for erro in lista_erros:
                if erro.linha == num:
                    # Calcula a quantidade de espaços necessários para alinhar a mensagem de erro
                    print(f"{' ' * (quant_digitos+2)}erro linha {erro.linha} coluna {erro.coluna}: {erro.msg}")

    print()  # Imprime uma linha em branco no final


def printaQtdUsosToken(listaTokens):
    # Cria um dicionário para contar a quantidade de cada tipo de token
    contagem = {}
    for token in listaTokens:
        if token.tipo in contagem:
            contagem[token.tipo] += 1  # Incrementa o contador se o tipo de token já existe no dicionário
        else:
            contagem[token.tipo] = 1  # Inicia o contador em 1 se o tipo de token é encontrado pela primeira vez
    
    # Ordena os tipos de token por quantidade de uso em ordem decrescente
    contagem_ordenada = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
    
    # Imprime cabeçalho da tabela
    print("+----------------+------+")
    print("|     TOKEN      | USOS |")
    print("+----------------+------+")
    
    # Itera sobre os tipos de token ordenados por quantidade de uso
    for token, usos in contagem_ordenada:
        # Imprime o tipo de token e a quantidade de usos, centralizados na tabela
        print(f"|{token.center(16)}|{str(usos).center(6)}|")
        print("+----------------+------+")
    print("\n")  # Imprime uma linha em branco no final


def analisador_lexico(nome_arquivo):
    # Abre o arquivo fonte especificado
    arquivo_fonte = abrir_arquivo(nome_arquivo)
    
    # Lista para armazenar tokens e erros
    tokens = []
    erros = []
    
    # Função que obtém tokens e erros no arquivo
    proximo_token_e_erros(arquivo_fonte, tokens, erros) 
    
    # Imprime a listagem de tokens reconhecidos
    print("Listagem de tokens reconhecidos:\n")
    printaTokens(tokens)
    
    # Imprime a listagem das quantidades reconhecidas de cada token
    print("Listagem das quantidades reconhecidas de cada token:\n")
    printaQtdUsosToken(tokens)
    
    # Mostra os erros encontrados no arquivo
    mostrar_erros(arquivo_fonte, erros)
    
# Chamada da a função principal com o nome do arquivo
analisador_lexico("codigo_fonte2.cic")