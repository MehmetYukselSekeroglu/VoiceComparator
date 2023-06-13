#!/usr/bin/env python3


###########################################################################################################
# 
#       BU ARAC EGITIM AMACLIDIR TAM SURUMDE DEGILDIR BU NEDENLE VERILERE TAM OLARAK GUVENILMEMELIDIR 
#
###########################################################################################################



from resemblyzer import preprocess_wav, VoiceEncoder
import numpy as np
from pydub import AudioSegment
import argparse
import pydub
import random
import os
import sys
import time
from colorama import *


# RENK KODLARI VE KALIN YAZI FONTU
kalın ="\033[1m"
kalın_reset ="\033[0m"
green = Fore.GREEN
blue = Fore.BLUE
color_reset = Fore.RESET
red = Fore.RED
orange = "\033[38;5;208m"



POWERED_BY = "PRIME"
APP_NAME = "Voice Comparator"
TEMP_PATH = "temp"+os.sep
VERSION_INFO = "v0.0.1"


if not os.path.exists(TEMP_PATH):
    os.mkdir(TEMP_PATH)



###########################################################################################################

# TERMINAL UZERINDEN BILGI VERME AMACLI FONKSIYONLAR 


def GetTime():
    """
    herhangi parametre almadan sisteme ait güncel zamanı 
    saat:dakika:saniye olarak döndürür

    Returns:
        str: saat:dakika:saniye
    """
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec
    formatted_time = f"{hour:02d}:{minute:02d}:{second:02d}"
    
    return formatted_time

# BASLIKLARI YAZDIRMAK ICIN 
def TitlePrinter(mesages:str):
    print(f"{kalın}{blue}>> [{mesages}]{kalın_reset}{color_reset}",end="\n\n")

    

# BILGILENDIRMELER ICIN 
def InformationPrinter(mesages:str):
    
    print(f"{kalın}{blue}[{GetTime()}]{kalın}[INFO]: {green}{mesages} {color_reset}{kalın_reset}")


# HATA MESAJLARI ICIN 
def ErrorPrinter(mesages:str):
    print(f"{kalın}{red}[{GetTime()}]{kalın}[ERROR]: {green}{mesages}{color_reset}{kalın_reset}")

###########################################################################################################

# PROGRAMIN AMACINA YONELIK FONKSYINLAR 




def ConvertAnyAudio_to_wav(target_file_path:str, temp_dir_path:str=TEMP_PATH):
    
    TARGET_FILE_FORMAT = "wav"
    
    if not os.path.exists(target_file_path) or not os.path.exists(temp_dir_path):
        return {"success":"false", "code":"invaid path"}
    
    target_file_extensions = target_file_path.split(".")
    target_file_extensions = target_file_extensions[len(target_file_extensions)-1]

    supported_formats = ["MP3","OGG","FLAC","AAC","AIFF","WMA","WAV"]
    
    if target_file_extensions.upper() not in supported_formats:
        return {"success":"false", "code":"not supported file extensions"}

    LoadedAudio = AudioSegment.from_file(target_file_path, format=target_file_extensions)
    export_name = TEMP_PATH+"exported_file_"+str(random.randint(1,999))+"."+TARGET_FILE_FORMAT
    
    LoadedAudio.export(export_name, format=TARGET_FILE_FORMAT)

    if os.path.exists(export_name):
        return {"success":"true", "path":str(export_name)}
    else:
        return { "success":"false", "code":"export error"}



def CompareSounds(sound_1_path:str, sound_2_path:str):
    if not os.path.exists(sound_1_path) or not os.path.exists(sound_2_path):
        return { "success":"false", "code":"file not found" }
    
    sound_encoder = VoiceEncoder(verbose=False)
    file_1 = preprocess_wav(sound_1_path)
    file_2 = preprocess_wav(sound_2_path)

    encoded_sound1 = sound_encoder.embed_utterance(file_1)
    encoded_sound2 = sound_encoder.embed_utterance(file_2)

    dot_product_size = np.dot(encoded_sound1, encoded_sound2)
    norm_sound1 = np.linalg.norm(encoded_sound1)
    norm_sound2 = np.linalg.norm(encoded_sound2)

    # kosinus benzerliğini hesaplama 
    GetSimilarity = dot_product_size / (norm_sound1 * norm_sound2)
    GetSimilarity = GetSimilarity * 100
    GetSimilarity = int(GetSimilarity)
    return { "success":"true" ,"similarity":str(GetSimilarity) }



###########################################################################################################

# EGER ARAC PROGRAM DEGOL MODUL OLARAK CALISOYPRSA SORUN CIKARTMAMASI ICIN

if __name__ == "__main__":
    init()
    TitlePrinter(f"{APP_NAME} {VERSION_INFO} | {POWERED_BY}")
    parser = argparse.ArgumentParser()

    parser.add_argument("--voice1", help="Target voice1 path", type=str, required=True)
    parser.add_argument("--voice2", help="Target voice2 path", type=str, required=True)

    all_args = parser.parse_args()
    all_args = vars(all_args)
    raw_file_1 = all_args["voice1"]
    raw_file_2 = all_args["voice2"]


    raw_file_1_convert_status = ConvertAnyAudio_to_wav(target_file_path=raw_file_1)
    raw_file_2_convert_status = ConvertAnyAudio_to_wav(target_file_path=raw_file_2)

    InformationPrinter("Converting files to 'vaw' format...")
    if raw_file_1_convert_status["success"] == "false" or raw_file_2_convert_status["success"] == "false":
        ErrorPrinter("File conversion failed.")
        sys.exit(1)

    vaw_file_1 = raw_file_1_convert_status["path"]
    vaw_file_2 = raw_file_2_convert_status["path"]

    InformationPrinter(f"Comparing voice similarity rates...")

    finally_status = CompareSounds(vaw_file_1, vaw_file_2)

    if not finally_status["success"] == "true":
        ErrorPrinter("Audio comparison failed.")
        os.remove(vaw_file_1)
        os.remove(vaw_file_2)
        sys.exit(1)

    InformationPrinter("Transaction successful...")
    InformationPrinter("Cosine similarity is written to the screen...")
    ses_benzerlik_oranı = finally_status["similarity"]


    if int(ses_benzerlik_oranı) < 70:
        color = orange
        metin = "Aynı kişi olma ihtimali düşüktür."
    elif int(ses_benzerlik_oranı) < 60:
        color = red
        metin = "Aynı kişi olma ihtimali çok düşüktür"
    elif int(ses_benzerlik_oranı) >= 70:
        color = green
        metin = "Aynı kişi olma ihtimali çok yüksektir"

    print(f"\n{kalın}{blue}|---------- RESULTS ----------|{color_reset}")
    print(f"{kalın}{blue}| Similarity rate: {color} %{str(ses_benzerlik_oranı)}{color_reset}")
    print(f"{kalın}{blue}| [lang:tr] Tespit bilgisi: {color} {str(metin)}{color_reset}")
    print(f"{kalın}{blue}|-----------------------------|{color_reset}")
    
    os.remove(vaw_file_1)
    os.remove(vaw_file_2)