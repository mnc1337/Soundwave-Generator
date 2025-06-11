import soundfile as sf
import numpy as np
import os, platform, subprocess
from datetime import datetime

def get_sample_rate():
    while True:
        value = input("Enter sample rate (from 1 to 768000 Hz): ")
        try:
            rate = int(value)
            if 1 <= rate <= 768000:
                return rate
            else:
                print("Sample rate must be between 1 and 768000 Hz.")
        except ValueError:
            print("Invalid input. Sample rate must be a whole number.")

def get_duration():
    while True:
        value = input("Enter duration (from 1 to 60 seconds): ")
        try:
            duration = int(value)
            if 1 <= duration <= 60:
                return duration
            else:
                print("Duration must be between 1 and 60 seconds.")
        except ValueError:
            print("Invalid input. Duration must be a whole number.")

def get_amplitude():
    while True:
        value = input("Enter amplitude (from 0 to 1): ")
        try:
            amplitude = float(value)
            if 0 <= amplitude <= 1:
                return amplitude
            else:
                print("Amplitude must be between 0 and 1.")
        except ValueError:
            print("Invalid input. Amplitude must be a number between 0 and 1.")

def get_freq_start():
    while True:
        value = input("Enter the lowest frequency point (≥ 1 Hz): ")
        try:
            freq = int(value)
            if freq >= 1:
                return freq
            else:
                print("Lowest frequency must be 0 Hz or higher.")
        except ValueError:
            print("Invalid input. Frequency must be a whole number.")

def get_freq_end(freq_start):
    while True:
        value = input("Enter the highest frequency point (≤ 384000 Hz): ")
        try:
            freq = int(value)
            if freq <= 384000:
                return freq
            elif freq <= freq_start:
                print("Highest frequency must be greater than the starting frequency.")
            else:
                print("Highest frequency must not exceed 384000 Hz.")
        except ValueError:
            print("Invalid input. Frequency must be a whole number.")

def get_yes_no(prompt):
    while True:
        answers = ["Y", "N"]
        answer = input(prompt).strip().upper()
        if answer in answers:
            return answer
        print("Please enter 'Y' or 'N'.")

def generate_wave(sample_rate, duration, amplitude, freq_start, freq_end):
    points = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = np.linspace(freq_start, freq_end, len(points))
    signal = amplitude * np.sin(2 * np.pi * np.cumsum(frequencies) / sample_rate)
    return signal

def save_wave(filename, signal, sample_rate):
    sf.write(filename, signal, sample_rate)

def create_log(filename, sample_rate, duration, amplitude, freq_start, freq_end):
    log_filename = f"{filename}.log"
    abs_path = os.path.abspath(log_filename)
    with open(log_filename, "w") as f:
        f.write(f"Sound file path: {os.path.abspath(filename)};\n")
        f.write(f"Creating date and time(local): {datetime.now()};\n")
        f.write(f"Sample rate: {sample_rate} Hz;\n")
        f.write(f"Duration: {duration} s;\n")
        f.write(f"Amplitude: {amplitude};\n")
        f.write(f"Frequencies range: {freq_start} - {freq_end} Hz.")
    return abs_path

def open_file(filepath):
    system = platform.system()
    if system == "Windows":
        os.startfile(filepath)
    elif system == "Darwin":
        subprocess.run(["open", filepath])
    elif system == "Linux":
        subprocess.run(["xdg-open", filepath])
    else:
        print("OS is unsupported for auto-open.")

def main():
    print("Console program for generating sound waves.")
    
    while True:
        sample_rate = get_sample_rate()
        duration = get_duration()
        amplitude = get_amplitude()
        freq_start = get_freq_start()
        freq_end = get_freq_end(freq_start)

        filename = "test.wav"
        abs_path_soundfile = os.path.abspath(filename)
        if os.path.exists(filename):
            overwrite = get_yes_no("File already exists. Overwrite? (Y/N): ")
            if overwrite == "N":
                print("Aborting operation.")
                continue
        
        signal = generate_wave(sample_rate, duration, amplitude, freq_start, freq_end)
        save_wave(filename, signal, sample_rate)

        write_log = get_yes_no("Do you want to create a log file? (Y/N): ")
        log_path = None
        if write_log == "Y":
            log_path = create_log("test", sample_rate, duration, amplitude, freq_start, freq_end)

        open_now = get_yes_no("Open generated sound file now? (Y/N): ")
        if open_now == "Y":
            open_file(abs_path_soundfile)
        
        if freq_start > freq_end:
            print("Warning: Start (lower) frequency point is greater then highest (end) frequency point. The sound wave will be descending")

        if sample_rate < freq_end * 2:
            print("Warning: Sample rate should be at least 2x the highest frequency for correct sound reproduction.")

        print(f"\nSound file saved at: {abs_path_soundfile}")
        if log_path:
            print(f"Log file saved at: {log_path}")
        else:
            print("Log file was not saved.")

        repeat = get_yes_no("Generate another sound wave? (Y/N): ")
        if repeat == "N":
            print("Exiting program.")
            break
        elif repeat == "Y":
            continue
        else:
            print("Answer is incorrect")

if __name__ == "__main__":
    main()
