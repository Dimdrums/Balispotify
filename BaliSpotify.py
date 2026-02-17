from pywinauto import Application, Desktop
import os
import time
import psutil
import subprocess
import asyncio
from winrt.windows.devices.radios import Radio, RadioKind, RadioState


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
        #print(buttons)
        for btn in buttons:
            try:
                if "– Modifier les informations" in btn.element_info.name:
                    playlistTitle = btn.element_info.name[:-27]
                    print(f"Playlist trouvée en {round(time.time() - start,2)}s : '{playlistTitle.strip()}'")
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

#asyncio.run(set_bluetooth(True))

url="https://open.spotify.com/playlist/6MFXJRfwrMzpS0AUnbV7tu?si=97a835f88a2c4bd5"

# playlist_key=url.split("playlist/")[1].split("?")[0]
# #print(playlist_key)

# window,_=openSpotify_wait(playlist_key,10)

# play_button=Wait_for_button(window,5)
# #play_button.click_input()


