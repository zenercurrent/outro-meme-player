import pyaudio
import wave

from threading import Thread

CHUNK = 1024
O_DEVICE_INDEX = 13
I_DEVICE_INDEX = 6

p = pyaudio.PyAudio()
wf = wave.open("outro.wav", "rb")
ostream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(),
                 rate=wf.getframerate(),
                 output_device_index=O_DEVICE_INDEX,
                 output=True)


class MicLoopbackThread(Thread):

    def __init__(self, ostream):
        super().__init__()
        self.ostream = ostream

    def run(self):
        print("Starting Loopback Thread")
        istream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         input_device_index=I_DEVICE_INDEX,
                         input=True)
        ostream2 = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                          channels=wf.getnchannels(),
                          rate=wf.getframerate(),
                          output_device_index=O_DEVICE_INDEX,
                          output=True)

        data = istream.read(CHUNK)
        while data != '':
            ostream2.write(data)
            data = istream.read(CHUNK)


data = wf.readframes(CHUNK)
loopback = MicLoopbackThread(ostream)
loopback.start()

while data != '':
    ostream.write(data)
    data = wf.readframes(CHUNK)

ostream.stop_stream()
ostream.close()

p.terminate()

print("Program ended")
