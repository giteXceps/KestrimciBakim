from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

# Buzzer'ı GPIO 21'ye bağladık
buzzer = TonalBuzzer(21)

print("Test basliyor... (Durdurmak icin CTRL+C)")

try:
    # Basit bir siren sesi testi (Artan ve azalan frekans)
    while True:
        # Kalın sesten ince sese çık
        for nota in range(220, 880, 10): 
            buzzer.play(Tone(frequency=nota))
            sleep(0.01)
        
        # İnce sesten kalın sese in
        for nota in range(880, 220, -10):
            buzzer.play(Tone(frequency=nota))
            sleep(0.01)

except KeyboardInterrupt:
    print("\nTest durduruldu.")
    buzzer.stop()