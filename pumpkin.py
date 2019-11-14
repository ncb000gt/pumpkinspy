import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import random
import alsaaudio

print('Starting up Pumpkin Spy!')
OUTPUT_PIN = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)  # read sensor settings from PIR
GPIO.setup(OUTPUT_PIN, GPIO.OUT)  # output signal to GPIO pin 3

m = alsaaudio.Mixer('PCM')
resetVolume = 50
m.setvolume(93)

try:
    def playSound():
        # define stream chunk
        chunk = 1024

        # open a wav format music
        f = wave.open(r"./halloween_audio.wav", "rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)

        # play stream
        while data:
            GPIO.output(3, random.random() > .7 and 1 or 0)
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()

    while True:
        print('Spying...')
        pirIn = GPIO.input(11)

        if pirIn == 0:
            # Nobody around
            GPIO.output(3, 0)
            time.sleep(0.1)
        elif pirIn == 1:
            # Someone around
            playSound()
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
    GPIO.cleanup()
    m.setvolume(resetVolume)
