import os
import time
import asyncio
import threading
import itertools
import sys
from colorama import Fore, Style, init
import yt_dlp

init(autoreset=True)

spinner_done = False

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def centralizar_texto(texto, largura=80):
    return texto.center(largura)

def mostrar_banner_verde_musgo():
    clear_cmd()
    banner = [
        "• ▌ ▄ ·. ▪   ▐ ▄  ▄▄ •             ",
        "·██ ▐███▪██ •█▌▐█▐█ ▀ ▪▪     ▪     ",
        "▐█ ▌▐▌▐█·▐█·▐█▐▐▌▄█ ▀█▄ ▄█▀▄  ▄█▀▄ ",
        "██ ██▌▐█▌▐█▌██▐█▌▐█▄▪▐█▐█▌.▐▌▐█▌.▐▌",
        "▀▀  █▪▀▀▀ ▀▀▀▀▀ █▪·▀▀▀▀  ▀█▄▀▪ ▀█▄▀▪"
    ]
    largura_terminal = os.get_terminal_size().columns
    for linha in banner:
        print(Fore.GREEN + centralizar_texto(linha, largura_terminal))
        time.sleep(0.05)
    print(Fore.WHITE + centralizar_texto("Painel YouTube Downloader - by @gqai", largura_terminal) + Style.RESET_ALL)

async def digitar_texto_animado(texto, delay=0.002, cor=Fore.LIGHTMAGENTA_EX):
    for linha in texto.splitlines():
        for caractere in linha:
            print(cor + caractere, end='', flush=True)
            await asyncio.sleep(delay)
        print()

async def mostrar_creditos():
    clear_cmd()
    mostrar_banner_verde_musgo()
    ascii_art = r"""
                     :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!           
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!                                       
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!   
             :X- M$$$$       `"T#$T~!8$WUXU~ 
            :%`  ~#$$$m:        ~!~ ?$$$$$$ 
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*" 
.....   -~~:<` !    ~?T#$$@@W@*?$$      /` 
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    : 
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!` 
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~ 
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! ` 
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM! 
$R@i.~~ !     :   ~$$$$$B$$en:`` 
?MXT@Wx.~    :     ~"##*$$$$M~ 
    """
    await digitar_texto_animado(ascii_art, delay=0.0008, cor=Fore.LIGHTMAGENTA_EX)
    texto_credito = (
        "\n\nProjeto feito por @gqai (mingoo) com intuito de aprendizado\n"
        "https://instagram.com/mingoocry"
    )
    await digitar_texto_animado(texto_credito, delay=0.01, cor=Fore.WHITE)
    input(Fore.WHITE + "\nPressione Enter para voltar ao menu...")

def spinner(texto="Baixando..."):
    for simbolo in itertools.cycle('|/-\\'):
        if spinner_done:
            break
        sys.stdout.write(f'\r{Fore.YELLOW}{texto} {simbolo}{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 50 + '\r')  # Limpa a linha

def baixar_video(url):
    global spinner_done
    pasta_videos = os.path.join(os.path.expanduser("~"), "Videos")
    os.makedirs(pasta_videos, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(pasta_videos, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'windowsfilenames': True,
        'quiet': True,
    }

    spinner_done = False
    spinner_thread = threading.Thread(target=spinner, args=("Baixando vídeo...",))
    spinner_thread.start()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            spinner_done = True
            spinner_thread.join()
            print(f"\n✅ Vídeo salvo em: {pasta_videos}")
        except Exception as e:
            spinner_done = True
            spinner_thread.join()
            print(f"\n❌ Erro ao baixar vídeo: {e}")

def baixar_audio(url):
    global spinner_done
    pasta_musicas = os.path.join(os.path.expanduser("~"), "Music")
    os.makedirs(pasta_musicas, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_musicas, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'windowsfilenames': True,
        'quiet': True,
    }

    spinner_done = False
    spinner_thread = threading.Thread(target=spinner, args=("Baixando áudio...",))
    spinner_thread.start()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            spinner_done = True
            spinner_thread.join()
            print(f"\n✅ Áudio salvo em: {pasta_musicas}")
        except Exception as e:
            spinner_done = True
            spinner_thread.join()
            print(f"\n❌ Erro ao baixar áudio: {e}")

def main():
    while True:
        mostrar_banner_verde_musgo()
        print(Fore.WHITE + "\n1 - Baixar vídeo")
        print("2 - Baixar áudio")
        print("3 - Créditos")
        print("0 - Sair" + Style.RESET_ALL)

        escolha = input(Fore.LIGHTCYAN_EX + "\nEscolha uma opção: " + Style.RESET_ALL).strip()

        if escolha == '1':
            url = input(Fore.YELLOW + "\nCole a URL do vídeo: " + Style.RESET_ALL).strip()
            baixar_video(url)
            input(Fore.WHITE + "\nPressione Enter para continuar...")

        elif escolha == '2':
            url = input(Fore.YELLOW + "\nCole a URL do vídeo: " + Style.RESET_ALL).strip()
            baixar_audio(url)
            input(Fore.WHITE + "\nPressione Enter para continuar...")

        elif escolha == '3':
            asyncio.run(mostrar_creditos())

        elif escolha == '0':
            print(Fore.GREEN + "\nEncerrando programa. Até logo!")
            break
        else:
            print(Fore.RED + "\nOpção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    main()
