import soundfile as sf
import numpy as np

sample_rate = 44100
duration = 2
amplitude = 0.75

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

freq_start = 20
freq_end = 20000

frequences = np.linspace(freq_start, freq_end, len(t))
signal = amplitude * np.sin(2 * np.pi * np.cumsum(frequences) / sample_rate)

filename = "test.wav"
sf.write(filename, signal, sample_rate)

data, rate = sf.read(filename)
is_ok = sample_rate == rate
print(f"Is ok: {is_ok}")
print(f"Number of points: {len(data)}")