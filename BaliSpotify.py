from pywinauto import Application, Desktop
import os
import json
import time
import psutil
import subprocess
import asyncio
from winrt.windows.devices.radios import Radio, RadioKind, RadioState

################ DATA ###############

appdata_dir = os.getenv('APPDATA')    #les données sont sauvegardées dans le appdata
data_path = os.path.join(appdata_dir, 'BaliSpotify', 'data.json')

with open(data_path, 'r') as f:
        data = json.load(f)

key = data["key"]
Bluetooth = data["Bluetooth"]

#####################################

async def set_bluetooth(enabled: bool): # ChatGPT : Ok

    radios = await Radio.get_radios_async()

    for radio in radios:

        if radio.kind == RadioKind.BLUETOOTH:

            if enabled and radio.state != RadioState.ON:

                print("Activation du Bluetooth...")
                result = await radio.set_state_async(RadioState.ON)
                print("Bluetooth activé")

            elif not enabled and radio.state != RadioState.OFF:

                print("Désactivation du Bluetooth...")
                result = await radio.set_state_async(RadioState.OFF)
                print("Bluetooth désactivé")

            else:
                print("Bluetooth déjà dans le bon état")

            return True

    print("Aucun adaptateur Bluetooth trouvé")
    return False



def openSpotify_wait(id,timeout,time_pace=2):
    start = time.time()
    dt=1/time_pace


    #lancement spotify
    os.startfile(f"spotify:playlist:{id}")

    #recherche fenêtre
    while time.time() - start <= timeout:
        time.sleep(dt)
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'Spotify.exe':
                pid = proc.info['pid']
                windows = Desktop(backend="uia").windows(process=pid)

                #retrouver la fenêtre visible (et pas les spotify.exe en background)
                for w in windows:
                    if w.is_visible():
                        print(f"Fenêtre Spotify trouvée en {round(time.time() - start,2)}s")
                        return w,pid
    
    print(f"Timeout {timeout}s: fenêtre Spotify non trouvée, arrêt du script...")
    exit()


def Wait_for_button(win,timeout,time_pace=4):
    start = time.time()
    dt=1/time_pace

    while time.time() - start <= timeout:
        time.sleep(dt)
        
        buttons = win.descendants(control_type="Button")
        print(buttons)
        for btn in buttons:
            try:
                if "Plus d'options pour " in btn.element_info.name:  #"– Modifier les informations"  <-- ne fonctionne pas avec des playlists Spotify
                    playlistTitle = btn.element_info.name[20:].strip()  #[:-27]
                    print(f"Playlist trouvée en {round(time.time() - start,2)}s : '{playlistTitle}'")
                    #update nom_playlist:
                    with open(data_path, 'r') as f:
                            data = json.load(f)
                    data["nom_playlist"] = playlistTitle
                    with open(data_path, 'w') as f:
                        json.dump(data, f, indent=4) 
                    #####################
                    start=time.time()
                    for btnPlay in buttons:
                        if  ("Lire" in btnPlay.element_info.name) and (playlistTitle.strip() in btnPlay.element_info.name) :
                            print(f"// bonus log // bouton Play trouvé en {round(time.time() - start,2)}s : '{btnPlay.element_info.name}'")
                            return btnPlay
                    print(f"ERREUR : bouton Play non trouvée après {round(time.time() - start,2)}s, arrêt du script...")
                    return None
            except:
                pass

    print(f"Timeout {timeout}s: bouton Play non trouvée, arrêt du script...")
    exit()



##############################################################

if Bluetooth:
    asyncio.run(set_bluetooth(True))

print(key)

window,_=openSpotify_wait(key,10)

play_button=Wait_for_button(window,5)
#play_button.click_input()


