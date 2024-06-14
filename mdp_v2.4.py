#!/bin/python3

# Name: MDP_SS
#       Massive Data Proccessor SS??

# Authors: Marcos Vinícius
#          Nemer Mollon

# Descrição:

# Versões
'''
    - 1.0: Versão inicial com as principais funcionalidades criadas
    - 2.0: Otimização da listagem de arquivos, percorrer e organizar a árvores de diretórios.
           Compatibilidade multiplataforma (Windows e Linux/UNIX)
    - 2.1: Adição de tratamento de exceções
    - 2.2: Adicionada a produção de logs
    - 2.3: Adicionada a conversão de arquivos de áudio "alaw"
    - 2.4: Adicionada captura de interrupções
'''

# TODO
'''
    - Adicionar a conversão de formato alaw
        ffmpeg -f alaw -ar 8000 -i audio.alaw -c pcm_s16le saida2.wav
    - Adicionar a função de tradução de textos
    - Criar uma interface gráfica para a aplicação
    - Criar um script para automatizar a instalação das ferramentas necessárias para a execução
    - Comentar o código
'''

import datetime
import os
import re
import signal
import subprocess
from colorama import Fore, Style

# +++++++++++++++++++++
# + Variáveis globais +
# +++++++++++++++++++++

# Salva diretório de trabalho
diretorio_atual = os.getcwd()

# Arquivo único de LOG
arquivo_log = open("log_mdp_ss.log", "a", encoding="utf-8")
escrevendo_log = False

# Cores do terminal
amarelo=Fore.YELLOW
azul=Fore.BLUE
ciano=Fore.CYAN
magenta=Fore.MAGENTA
verde=Fore.GREEN
vermelho=Fore.RED
reset=Fore.RESET
reset_all=Style.RESET_ALL

# Linux/Unix
if os.name == 'posix':
    sep="/"
# Windows
else:
    sep="\\"

# Função para limpar a tela
def cls():
   # Mac ou Linux
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # Windows
      _ = os.system('cls')

# Gerencia interrupções do teclado (Ctrl-C, etc)
def interrupcoes(sinal, frame):
    # Retorna o gerenciamento de sigint
    # signal.signal(signal.SIGINT, original_sigint)
    
    print("\nCtrl-C pressionado! Saindo...")
    
    if escrevendo_log:
        arquivo_log.write("Ctrl-C pressionado.\n")
    else:
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Ctrl-C pressionado.\n")
    
    arquivo_log.close()
    exit(1)
    
    """
    if sinal == signal.SIGINT:
        try:
            opcao = input("Deseja sair? (s/N) ")
            if opcao.lower().startswith("s"):
                exit(1)
        except KeyboardInterrupt:
            print("\nCtrl-C pressionado! Saindo...")
            exit(1)
        except RuntimeError:
            pass
        finally:
            pass
    """

# Interrupções
original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, interrupcoes)

def converter_audios_para_wav(diretorio_audios):
    global escrevendo_log
    
    # LOG
    arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} ### Conversão de áudios para WAV ###\n")
    arquivo_log.flush()

    # Entra no diretório dos áudios 
    try:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Acessando o diretório \"{diretorio_audios}\" ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        os.chdir(diretorio_audios)
        
        # LOG
        arquivo_log.write("sucesso.\n")
        arquivo_log.flush()
        escrevendo_log = False
    except:
        # LOG
        arquivo_log.write("falha.\n")
        arquivo_log.flush()
        escrevendo_log = False
        
        print(vermelho + f"Falha ao acessar diretório \"{diretorio_audios}\"" + reset_all)
        input("Pressione enter para continuar...")
        
        return
    
    # Cria o diretório de destino dos WAV
    if not os.path.exists("wav"):
        try:
            # LOG
            arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Criando o diretório WAV ==> ")
            arquivo_log.flush()
            escrevendo_log = True
            
            os.mkdir("wav")
            
            # LOG
            arquivo_log.write("sucesso.\n")
            arquivo_log.flush()
            escrevendo_log = False
        except:
            # LOG
            arquivo_log.write("falha.\n")
            arquivo_log.flush()
            escrevendo_log = False
            
            print(vermelho + "Falha ao criar diretório WAV" + reset_all)
            input("Pressione enter para continuar...")
            
            return
    else:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Diretório WAV já existe.\n")
        arquivo_log.flush()
    
    # LOG
    arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} ### Arquivos PCM ###\n")
    arquivo_log.flush()
    
    print(azul + f"\n{str(datetime.datetime.now()).split('.')[0]} Iniciando a conversão de arquivos de áudio.\n" + reset_all)
    
    print(azul + "### Arquivos PCM ###" + reset_all)
    # Gera a lista de arquivos PCM a ser convertidos e executa a conversão na sequência
    arquivos_pcm = [i for i in os.listdir() if i.lower().endswith(".pcm")]
    total_pcm = len(arquivos_pcm)
    pcm_processados = 0
    falhas = 0
    progresso = 0
    for arquivo_pcm in arquivos_pcm:
        progresso += 1
        print(azul + f"Arquivo {progresso} de {total_pcm}." + reset_all)
        arquivo_wav = f"{arquivo_pcm.split('.pcm')[0]}.wav"
        
        # Evita reprocessamento
        if os.path.exists(f"wav{sep}{arquivo_wav}"):
            print(ciano + f"Arquivo {arquivo_wav} já existe!" + reset_all)
            
            # LOG
            arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Arquivo \"wav{sep}{arquivo_wav}\" já existe!\n")
            arquivo_log.flush()
            
            continue
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Conversão do arquivo {arquivo_pcm} ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        pcm_processados += 1
        print(amarelo + f"Realizando a conversão do arquivo \"{arquivo_pcm}\" ==> " + reset_all, end="", flush=True)
        comando = f"ffmpeg -f s16le -ar 8000 -i \"{arquivo_pcm}\" -ar 44100 \"wav{sep}{arquivo_wav}\""
        resultado = subprocess.run(comando, shell=True, stdout=open("stdout.txt", "w"), stderr=open("stderr.txt", "w"))
        if resultado.returncode == 0:
            print(verde + "sucesso!" + reset_all)
            
            # LOG
            arquivo_log.write("sucesso.\n")
            arquivo_log.flush()
            escrevendo_log = False
        else:
            print(vermelho + "falha!" + reset_all)
            falhas += 1
            
            # LOG
            arquivo_log.write("falha.\n")
            arquivo_log.flush()
            escrevendo_log = False

    if pcm_processados > 0:
        print(verde + f"\n{pcm_processados-falhas} de {total_pcm} áudio(s) PCM convertido(s) para WAV e salvo(s) em: \"{os.getcwd()}{sep}wav\"\n" + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Conversão de {len(arquivos_pcm)} arquivo(s) PCM finalizada com {falhas} falha(s).\n")
        arquivo_log.flush()
    else:
        print(azul + "### Nenhum arquivo PCM processado. ###\n" + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Nenhum arquivo PCM processado.\n")
        arquivo_log.flush()
    
    # LOG
    arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} ### Arquivos ALAW ###\n")
    arquivo_log.flush()
    
    print(azul + "### Arquivos ALAW ###" + reset_all)
    # Gera a lista de arquivos ALAW a ser convertidos e executa a conversão na sequência
    arquivos_alaw = [i for i in os.listdir() if i.lower().endswith(".alaw")]
    total_alaw = len(arquivos_alaw)
    alaw_processados = 0
    falhas = 0
    progresso = 0
    for arquivo_alaw in arquivos_alaw:
        progresso += 1
        print(azul + f"Arquivo {progresso} de {total_alaw}." + reset_all)
        arquivo_wav = f"{arquivo_alaw.split('.alaw')[0]}.wav"
        
        # Evita reprocessamento
        if os.path.exists(f"wav{sep}{arquivo_wav}"):
            print(ciano + f"Arquivo {arquivo_wav} já existe!" + reset_all)
            
            # LOG
            arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Arquivo \"wav{sep}{arquivo_wav}\" já existe!\n")
            arquivo_log.flush()
            
            continue
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Conversão do arquivo {arquivo_alaw} ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        alaw_processados += 1
        print(amarelo + f"Realizando a conversão do arquivo \"{arquivo_alaw}\" ==> " + reset_all, end="", flush=True)
        comando = f"ffmpeg -f alaw -ar 8000 -i \"{arquivo_alaw}\" -c pcm_s16le \"wav{sep}{arquivo_wav}\""
        resultado = subprocess.run(comando, shell=True, stdout=open("stdout.txt", "w"), stderr=open("stderr.txt", "w"))
        if resultado.returncode == 0:
            print(verde + "sucesso!" + reset_all)
            
            # LOG
            arquivo_log.write("sucesso.\n")
            arquivo_log.flush()
            escrevendo_log = False
        else:
            print(vermelho + "falha!" + reset_all)
            falhas += 1
            
            # LOG
            arquivo_log.write("falha.\n")
            arquivo_log.flush()
            escrevendo_log = False

    if alaw_processados > 0:
        print(verde + f"\n{alaw_processados-falhas} de {total_alaw} áudio(s) ALAW convertido(s) para WAV e salvo(s) em: \"{os.getcwd()}{sep}wav\"\n" + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Conversão de {len(arquivos_alaw)} arquivo(s) ALAW finalizada com {falhas} falha(s).\n")
        arquivo_log.flush()
    else:
        print(azul + "### Nenhum arquivo ALAW processado. ###\n" + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Nenhum arquivo ALAW processado.\n")
        arquivo_log.flush()
    
    if (pcm_processados>0) or (alaw_processados>0):
        print(azul + f"{str(datetime.datetime.now()).split('.')[0]} Fim da conversão de arquivos de áudio." + reset_all)
    else:
        print(azul + f"{str(datetime.datetime.now()).split('.')[0]} Nenhum arquivo de áudio processado." + reset_all)
    
    input("Pressione enter para continuar...")
    
    # Deleta os .txt gerados no diretório atual
    arquivos_txt = [i for i in os.listdir() if i.lower().endswith(".txt")]
    for arquivo_txt in arquivos_txt:
        os.remove(arquivo_txt)

def transcrever_audios_wav(diretorio_audios_wav):
    global escrevendo_log
    
    # LOG
    arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} ### Transcrição de arquivos WAV ###\n")
    arquivo_log.flush()

    # Entra no diretório dos áudios WAV
    try:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Acessando o diretório \"{diretorio_audios_wav}\" ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        os.chdir(diretorio_audios_wav)
    
        # LOG
        arquivo_log.write("sucesso.\n")
        arquivo_log.flush()
        escrevendo_log = False
    except:
        # LOG
        arquivo_log.write("falha.\n")
        arquivo_log.flush()
        escrevendo_log = False
        
        print(vermelho + f"Falha ao acessar diretório \"{diretorio_audios_wav}\"" + reset_all)
        input("Pressione enter para continuar...")
        
        return

    # Entra no diretório WAV caso exista
    if os.path.exists("wav"):
        os.chdir("wav")

    # Cria o diretório de destino dos SRT
    if not os.path.exists("srt"):
        try:
            # LOG
            arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Criando o diretório SRT ==> ")
            arquivo_log.flush()
            escrevendo_log = True
            
            os.mkdir("srt")
            
            # LOG
            arquivo_log.write("sucesso.\n")
            arquivo_log.flush()
            escrevendo_log = False
        except:
            # LOG
            arquivo_log.write("falha.\n")
            arquivo_log.flush()
            escrevendo_log = False
            
            print(vermelho + "Falha ao criar diretório SRT" + reset_all)
            input("Pressione enter para continuar...")
            
            return
    else:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Diretório SRT já existe.\n")
        arquivo_log.flush()
    
    print(azul + f"\n{str(datetime.datetime.now()).split('.')[0]} Iniciando a transcrição dos arquivos WAV." + reset_all)
    
    # Gera a lista de arquivos WAV a ser transcritos e executa a transcrição na sequência
    arquivos_wav = [i for i in os.listdir() if i.lower().endswith(".wav")]
    total_wav = len(arquivos_wav)
    processados = 0
    falhas = 0
    progresso = 0
    for arquivo_wav in arquivos_wav:
        progresso += 1
        print(azul + f"Arquivo {progresso} de {total_wav}." + reset_all)
        arquivo_srt = f"{arquivo_wav.split('.wav')[0]}.srt"
        
        # Evita reprocessamento
        if os.path.exists(f"srt{sep}{arquivo_srt}"):
            print(azul + f"Arquivo {arquivo_srt} já existe!\n" + reset_all)
            
            # LOG
            arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Arquivo \"srt{sep}{arquivo_srt}\" já existe!\n")
            arquivo_log.flush()
            
            continue
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Transcrição do arquivo {arquivo_wav} ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        processados += 1
        print(amarelo + f"Realizando a transcrição do arquivo \"{arquivo_wav}\" ==> " + reset_all, end="", flush=True)
        # comando = f"whisper \"{arquivo_wav}\" --output_format txt --model large > \"srt{sep}{arquivo_srt}\""
        comando = f"whisper \"{arquivo_wav}\" --output_format txt --model large"
        saida=open(f"srt{sep}{arquivo_srt}", "w", encoding="utf-8")
        resultado = subprocess.run(comando, shell=True, stdout=saida, stderr=open("stderr.txt","a"))
        if resultado.returncode == 0:
            print(verde + "sucesso!" + reset_all)
            
            # LOG
            arquivo_log.write("sucesso.\n")
            arquivo_log.flush()
            escrevendo_log = False
        else:
            print(vermelho + "falha!" + reset_all)
            
            # LOG
            arquivo_log.write("falha.\n")
            arquivo_log.flush()
            escrevendo_log = False
            falhas += 1
        print()  # Adiciona uma quebra de linha após cada transcrição
    
    if processados > 0:
        print(verde + f"\n{processados-falhas} de {total_wav} arquivo(s) WAV transcrito(s) para SRT e salvo(s) em: {os.getcwd()}{sep}srt\n" + reset_all)
        print(azul + f"{str(datetime.datetime.now()).split('.')[0]} Fim da transcrição dos arquivos WAV." + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Transcrição de {len(arquivos_wav)} arquivo(s) WAV finalizada com {falhas} falha(s).\n")
        arquivo_log.flush()
    else:
        print(azul + "Nenhum arquivo WAV processado.\n" + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Nenhum arquivo WAV processado.\n")
        arquivo_log.flush()
    
    input("Pressione enter para continuar...")
    
    # Deleta os .txt gerados no diretório atual
    arquivos_txt = [i for i in os.listdir() if i.lower().endswith(".txt")]
    for arquivo_txt in arquivos_txt:
        os.remove(arquivo_txt)

def pesquisar_palavras_em_arquivos(palavras_arquivo, diretorio_textos):
    global escrevendo_log
    
    # LOG
    arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} ### Busca de palavras-chave ###\n")
    arquivo_log.flush()
    
    # Tenta abrir o arquivo das palavras-chave através do caminho passado
    arquivo = None
    try:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Abrindo o arquivo de palavras-chave \"{palavras_arquivo}\" ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        arquivo = open(palavras_arquivo, 'r', encoding='utf-8')
        
        # LOG
        arquivo_log.write("sucesso.\n")
        arquivo_log.flush()
        escrevendo_log = False
    except:
        # LOG
        arquivo_log.write("falha.\n")
        arquivo_log.flush()
        escrevendo_log = False
        
        print(vermelho + f"Falha ao abrir arquivo de palavras-chave \"{palavras_arquivo}\"" + reset_all)
        input("Pressione enter para continuar...")
        
        return
    
    # Mensagem de informação para o usuário
    print(azul + f"{str(datetime.datetime.now()).split('.')[0]} Lendo o arquivo de palavras-chave \"{palavras_arquivo}\"." + reset_all)
    
    # Obtém as palavras-chave
    palavras_chave = []
    for linha in arquivo:
        for palavra in linha.split():
            palavras_chave.append(palavra.lower())
    arquivo.close()
    if len(palavras_chave) == 0:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Arquivo de palavras-chave \"{palavras_arquivo}\" vazio.\n")
        arquivo_log.flush()
        
        print(vermelho + f"Arquivo de palavras-chave \"{palavras_arquivo}\" vazio!" + reset_all)
        input("Pressione enter para continuar...")
        
        return
    
    # Entra no diretório dos arquivos SRT
    try:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Acessando o diretório de arquivos SRT \"{diretorio_textos}\" ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        os.chdir(diretorio_textos)
        
        # LOG
        arquivo_log.write("sucesso.\n")
        arquivo_log.flush()
        escrevendo_log = False
    except:
        # LOG
        arquivo_log.write("falha.\n")
        arquivo_log.flush()
        escrevendo_log = False
        
        print(vermelho + f"Falha ao acessar diretório \"{diretorio_textos}\"" + reset_all)
        input("Pressione enter para continuar...")
        
        return
    
    # Entra no diretório SRT caso exista
    if os.path.exists("srt"):
        os.chdir("srt")

    print(azul + f"{str(datetime.datetime.now()).split('.')[0]} Iniciando a busca de palavras-chave nos arquivos transcritos." + reset_all)
    arquivos_srt = [i for i in os.listdir() if i.lower().endswith('.srt')]
    processado = (len(arquivos_srt)>0)
    for arquivo_srt in arquivos_srt:
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Buscando no arquivo \"{arquivo_srt}\" ==> ")
        arquivo_log.flush()
        escrevendo_log = True
        
        num_linha = 0
        for linha in open(arquivo_srt, 'r'):#, encoding='utf-8'):
            num_linha += 1
            try:
                for palavra in linha.split(']  ')[1].split():
                    for palavra_chave in palavras_chave:
                        if re.search(rf'\b{re.escape(palavra_chave)}\b', palavra, re.IGNORECASE):
                            print(vermelho + "Palavra chave " + verde + f"{palavra_chave} " + vermelho + "encontrado na linha " + verde + f"{num_linha} " + vermelho + "do arquivo " + verde + f"{arquivo_srt}" + reset_all)
                            print(azul + linha + reset_all)
                            
                            break
            except:
                continue
        
        # LOG
        arquivo_log.write("Concluído.\n")
        arquivo_log.flush()
        escrevendo_log = False

    if processado:
        print(azul + f"{str(datetime.datetime.now()).split('.')[0]} Fim da busca das palavras-chave." + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Busca de palavras-chave no diretório \"{diretorio_textos}\" finalizada.\n")
        arquivo_log.flush()
    else:
        print(azul + "Nenhum arquivo SRT processado!" + reset_all)
        
        # LOG
        arquivo_log.write(f"{str(datetime.datetime.now()).split('.')[0]} Nenhum arquivo SRT processado.\n")
        arquivo_log.flush()
    
    input("Pressione enter para continuar...")

def main():
    global escrevendo_log
    
    while True:
        escrevendo_log = False
        cls()
        
        # Volta sempre pro diretório inicial
        os.chdir(diretorio_atual)
        
        print(ciano + "Diretório atual:" + os.getcwd() + reset_all + "\n")
        print(ciano + "Selecione a ação que deseja realizar:" + reset_all)
        print(magenta + "1. Converter áudios para WAV" + reset_all)
        print(magenta + "2. Transcrever áudios WAV" + reset_all)
        print(magenta + "3. Pesquisar palavras em arquivos de texto" + reset_all)
        print(magenta + "0. Sair" + reset_all)

        escolha = input("Opção: ")

        if escolha == "1":
            diretorio_audios = input("\nDigite o diretório onde estão os áudios a serem convertidos: ")
            if diretorio_audios == "":
                diretorio_audios = os.getcwd()
            converter_audios_para_wav(diretorio_audios)
        
        elif escolha == "2":
            diretorio_audios_wav = input("\nDigite o diretório onde estão os áudios WAV: ")
            if diretorio_audios_wav == "":
                diretorio_audios_wav = os.getcwd()
            transcrever_audios_wav(diretorio_audios_wav)
        
        elif escolha == "3":
            palavras_arquivo = input("\nDigite o caminho para o arquivo de palavras: ")
            if palavras_arquivo == "":
                palavras_arquivo = os.getcwd()+sep+"palavras_chave.txt"
            
            diretorio_textos = input("Digite o diretório de arquivos de texto transcritos: ")
            if diretorio_textos == "":
                diretorio_textos = os.getcwd()
            
            pesquisar_palavras_em_arquivos(palavras_arquivo, diretorio_textos)
        
        elif escolha == "0":
            break
        
        else:
            print(vermelho + "Opção inválida! Tente novamente." + reset_all)
            input()
    
    arquivo_log.close()

if __name__ == "__main__":
   main()
