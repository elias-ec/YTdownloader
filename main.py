import art, os, requests
from colorama import Fore
import youtube_dl, platform
import subprocess
import tkinter as tk
import moviepy.editor
import json

root = tk.Tk()
root.withdraw()
global ytLink
ytLink = root.clipboard_get()
global defaultOrCustom
defaultOrCustom = ''
global tryDownloadAgain
tryDownloadAgain= False
global newWindow
newWindow = True;

def Welcome():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    global newWindow
    if newWindow == True:
        print(Fore.RED + (art.text2art("YTdownloader", 'big')))
    else: print('\n')
    global defaultOrCustom
    defaultOrCustom = input(Fore.WHITE + "Press ENTER for default download or 'c' for custom download: ")


def CheckInternetConnectivity():
    response = requests.get("https://www.youtube.com/")
    if response.status_code == 200:
        print(Fore.GREEN + "Info: Internet Connectivity...FOUND")
    else:
        print(Fore.RED + "ERROR: Internet connectivity...NOT FOUND")
        exit(0)


def Download(url, path, isPlaylist=True):
    curr_path = os.getcwd()
    os.chdir(path)
    if not isPlaylist:
        subprocess.call("youtube-dl --no-playlist -bestvideo+bestaudio {0}".format(url))
    else:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    print(Fore.GREEN + "Info: Video saved at '{0}'".format(os.getcwd()))
    os.chdir(curr_path)


def Download_list(url_list, path):
    curr_path = os.getcwd()
    os.chdir(path)
    ydl_opts = {}
    for video in url_list:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url.strip()])
    print(Fore.GREEN + "INFO: Videos saved at '{0}'".format(os.getcwd()))
    os.chdir(curr_path)


def PrepareDownload(path):
    global defaultOrCustom
    if defaultOrCustom == '' and tryDownloadAgain == False:
        global url
        url = root.clipboard_get()
    elif defaultOrCustom == 'c' and tryDownloadAgain == False:
        url = input(Fore.WHITE + 'Enter URL (For multiple urls, separate them by commas): ')
    print("URL: " + url)
    if "youtube.com" in url:
        if "list = " in url and "watch" in url:
            def Choice():
                choice = input("Do you want to download the whole playlist (y/n): ")
                if "y" in choice.lower():
                    print(Fore.GREEN + "INFO: Downloading playlist.")
                    try:
                        Download(url, path)
                    except:
                        TryDownloadAgain(path)
                elif "n" in choice.lower():
                    print(Fore.GREEN + "INFO: Downloading video.")
                    try:
                        Download(url, path, False)
                    except:
                        TryDownloadAgain(path)
                else:
                    print(Fore.RED + "[ERROR] Invalid choice {0}".format(
                        choice) + "\n-->Please try again: Do you want to download the whole playlist (y/n): ")
                    Choice()

            Choice()
        elif "list = " in url:
            print(Fore.GREEN + "INFO: Downloading youtube playlist.")
            try:
                Download(url, path)
            except:
                TryDownloadAgain(path)
        elif "watch" in url:
            print(Fore.GREEN + "INFO: Downloading youtube video.")
            try:
                Download(url, path)
            except:
                TryDownloadAgain(path)
        elif "," in url:
            print(Fore.GREEN + "INFO: Downloading all youtube videos.")
            try:
                Download_list(url.split(","), path)
            except:
                TryDownloadAgain(path)
        else:
            print(Fore.RED + "ERROR: This youtube URL does not seem to point to any video or playlist.")
            TryDownloadAgain(path)
    else:
        TryDownloadAgain(path)


def TryDownloadAgain(path):
    print(Fore.RED + "ERROR: Download failed...\n--> Please try again...")
    global tryDownloadAgain
    tryDownloadAgain = True;
    def Else():
        tryagain = input(Fore.WHITE + "Enter URL (For multiple urls, separate them by commas): ")
        if tryagain == '':
            global url
            url = root.clipboard_get()
            try:
                PrepareDownload(path)
                # Download(url, path, False)
            except:
                print(Fore.RED + "ERROR: Please try again...")
                Else()
        else:
            url = tryagain
            try:
                PrepareDownload(path)
                # Download(url, path, False)
            except:
                print(Fore.RED + "ERROR: Please try again...")
                Else()

    Else()


def Start():
    global defaultOrCustom
    if defaultOrCustom == '':  # DEFAULT DOWNLOAD
        global path
        path = 'C:/Users/ecman/Videos/'
        if os.path.exists(path):
            path = os.path.join(path, 'YTdownloads')
            if not os.path.exists(path):
                try:
                    os.mkdir("YTdownloads")
                except:
                    print(Fore.RED + "ERROR: Invalid path: '" + path + "'!! \n --> Try to create the folder 'YTdownloads' in your path... ")
                    exit()
        else:
            print(Fore.RED + "ERROR: Invalid path: '" + path + "'!!")
            exit()  # Try again! ! !!
        print(Fore.WHITE + "Path: " + path)
        #
        PrepareDownload(path)

    elif defaultOrCustom.lower() == 'c':  # CUSTOM DOWNLOAD
        path = 'C:/Users/ecman/Videos/'
        pathInput = input(Fore.WHITE + "Enter path where you want to save video (press ENTER to save at default Videos folder): ")
        if pathInput != '':
            path = pathInput  # Custom path
        if os.path.exists(path):
            path = os.path.join(path, 'YTdownloads')
            if not os.path.exists(path):
                try:
                    os.mkdir("YTdownloads")
                except:
                    print(Fore.RED + "ERROR: Invalid path: '" + path + "'!! \n --> Try to create the folder 'YTdownloads' in your path... ")
                    exit()
        else:
            print(Fore.RED + "ERROR: Invalid path: '" + path + "'!!")
            exit()
        print(Fore.WHITE + "Path: " + path)
        #
        PrepareDownload(path)

    else:
        defaultOrCustom = input(Fore.WHITE + "Try again: Press ENTER for default download or 'c' for custom download: ")
        Start()

if __name__ == "__main__":
    Welcome()
    CheckInternetConnectivity()
    Start()

    newWindow = False
    defaultOrCustom = input(Fore.WHITE + "Press 'e' to extrakt audio; Press ENTER for default download or 'c' for custom download of another Video:")
    if defaultOrCustom == ('' or 'c'):
        Start()
    elif defaultOrCustom == 'e':
        global path
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        latestFile = max(paths, key=os.path.getctime)
        print(Fore.GREEN + 'Converting...\n' + 'File: ' + latestFile)
        clip = moviepy.editor.VideoFileClip(latestFile)
        clip.audio.write_audiofile(latestFile[:-4] + '.mp3')
        delVideo = input(Fore.GREEN + 'Video extracted to mp3 file. ' + Fore.WHITE + 'Delete .mp4 file (y/n)')
        if delVideo == 'y':
            try:
                os.remove(latestFile)
            except:
                print(Fore.RED + 'ERROR: Please delete video manually if you wish so.')
            Welcome()
        elif delVideo == 'n':
            Welcome()
        else:
            print(Fore.RED + 'ERROR: Please delete video manually if you wish so.')
            Welcome()
