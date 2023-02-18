from datetime import timedelta
from glob import glob
from cv2 import VideoCapture,CAP_PROP_FRAME_HEIGHT,CAP_PROP_FRAME_COUNT,CAP_PROP_FPS,CAP_PROP_FRAME_WIDTH,CAP_PROP_POS_MSEC,imwrite
from pandas import DataFrame
from os.path import exists,basename,join
from os import stat,mkdir
from colorama import Fore, init, Style

bright = Style.BRIGHT
green, blue, red, cyan, reset = Fore.GREEN + bright, Fore.BLUE + bright, Fore.RED + bright, Fore.CYAN, Fore.RESET
init(convert=True, autoreset=True)

data_list = []

def fun(path):
    f_url = basename(path)  
    return f'<a href="{path}" target="_blank" >{f_url}</a>'

def video_duation(filename):
    data = VideoCapture(filename)
    height = data.get(CAP_PROP_FRAME_HEIGHT)
    width = data.get(CAP_PROP_FRAME_WIDTH)
    frames = data.get(CAP_PROP_FRAME_COUNT)
    fps = data.get(CAP_PROP_FPS)
    seconds = round(frames / fps)
    video_time = timedelta(seconds=seconds)
    return str(video_time),f'{int(width)}*{int(height)}'

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def video_size(filename):
    return convert_bytes(stat(filename).st_size)

def video_name(filename):
    return basename(filename)

def video_thumb(filename,folder_name):
    try:
        minutes,seconds = 1,0
        data = VideoCapture(filename)
        t_msec = 1000*(minutes*60 + seconds)
        data.set(CAP_PROP_POS_MSEC, t_msec)
        _, frame = data.read()
        file_name = join(thumb_folder,folder_name,f'{video_name(filename)}.png')
        imwrite(file_name, frame)
    except:
        minutes,seconds = 0,1
        data = VideoCapture(filename)
        t_msec = 1000*(minutes*60 + seconds)
        data.set(CAP_PROP_POS_MSEC, t_msec)
        _, frame = data.read()
        file_name = join(thumb_folder,folder_name,f'{video_name(filename)}.png')
        imwrite(file_name, frame)
    return file_name

def thumb_sub_folder(folder_name):
    folder_path = join(thumb_folder,folder_name)
    # print(folder_path)
    if not exists(folder_path):
        mkdir(folder_path)

def main(filename,folder_name):
    file_duration,dimentions = video_duation(filename)
    data_dict = {
        "file_name":video_name(filename),
        "file_duration":file_duration,
        "file_dimention":dimentions,
        "file_size":video_size(filename),
        "thumbnail":video_thumb(filename,folder_name),
        "main_path": filename
    }
    data_list.append(data_dict)

def credit():
    credit_text = f"""
               {red}BLUEPRINT OF VIDEO FILES
{green}               
     ██▀███   ▄▄▄       ██░ ██  █    ██  ██▓    
    ▓██ ▒ ██▒▒████▄    ▓██░ ██▒ ██  ▓██▒▓██▒    
    ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▀▀██░▓██  ▒██░▒██░    
    ▒██▀▀█▄  ░██▄▄▄▄██ ░▓█ ░██ ▓▓█  ░██░▒██░    
    ░██▓ ▒██▒ ▓█   ▓██▒░▓█▒░██▓▒▒█████▓ ░██████▒
    ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░
      ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░▒░ ░░░▒░ ░ ░ ░ ░ ▒  ░
      ░░   ░   ░   ▒    ░  ░░ ░ ░░░ ░ ░   ░ ░   
       ░           ░  ░ ░  ░  ░   ░         ░  ░ {blue}code generated by Rahul.p\n
    """
    print(credit_text)

credit()
thumb_folder = 'thumbnails'
[mkdir(thumb_folder)if not exists(thumb_folder) else None]
path = input("[+] Enter path or drag and drop the folder : ").replace('"','')

if path=='':
     path = input("[+] Enter path or drag and drop the folder : ").replace('"','')
# path= r'D:\work\thum_file\test'

files_name = glob(f"{path}/*.mp4")+glob(f"{path}/*.mkv")+glob(f"{path}/*.avi")
if files_name:
    print("[+] Processing main folder files")
    for file in files_name:
        print(f"{blue}[+] Processing file {green}{file}")
        main(file,'')

folder_data = glob(f'{path}/*/**/',recursive=True)
for folder in folder_data:
    try:
        folder_name = folder.replace(path,"")[1:]
        print(f'{cyan}[F] processing folder - {blue}{folder_name}')
        thumb_sub_folder(folder_name)
        file_data = glob(f'{folder}/*.mp4')+glob(f'{folder}/*.mkv')
        for file in file_data:
            print(f"{blue}[+] Processing file {green}{file}")
            thumb_sub_folder(folder_name)
            main(file,folder_name)
    except Exception as e:
        print(f"{red}[-] Error - {e}")
        continue


df = DataFrame(data=data_list)
# df.to_html("files.html",escape=False,index=False,formatters=dict(thumbnail=fun),justify='center')
df.to_excel("files.xlsx",index=False)

