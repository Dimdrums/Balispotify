from machine import Pin, ADC
import utime

Ts = 0.2
sensor = ADC(26)  # exemple : pin ADC
cap_old_state = True
cap_state = True
cap_filtered_state = True
cap_count = 0
sig_old_state = True
sig_state = True
sig_filtered_state = True
sig_count = 0

def filter_tests (old_state,state,filtered_state,c,duree):
    if filtered_state != state:
        if old_state == state:
            c+= 1
        else:
            c = 0
            
        if c >= duree/Ts:
            filtered_state = state
            c = 0

    return filtered_state,c

while True:
    value = sensor.read_u16()
    print(f"value: {value}")

    if value < 2000:
        cap_state = False
    else:
        cap_state = True
    
    cap_filtered_state,cap_count = filter_tests (cap_old_state,cap_state,cap_filtered_state,cap_count,2) #2sec
    sig_filtered_state,sig_count = filter_tests (sig_old_state,sig_state,sig_filtered_state,sig_count,5) #5sec

    if cap_filtered_state:
        print("on")
    else:
        print("off")
    
    cap_old_cap_state = cap_state
    utime.sleep(Ts)
