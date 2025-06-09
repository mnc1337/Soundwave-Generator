import soundfile as sf
import numpy as np
import os, platform, subprocess
from datetime import datetime

def main():
    print("It`s a console program for generating sound waves. According to the given parameters(if they are correct) it will generate sound wave.")
    sample_rate = input("Enter sample rate(Hz): ")
    duration = input("Enter duration(seconds): ")
    amplitude = input("Enter amplitude(number from 0 to 1): ")
    freq_start = input("Enter the lowest point of frequency(Hz): ")
    freq_end = input("Enter the highest point of frequency(Hz): ")

    inputs = [sample_rate, duration, amplitude, freq_start, freq_end]

    if not all(inputs):
        print("Error. Some of inputs are null.")
        input("Press Enter key to close this tab... ")
        return False
    
    try:
        sample_rate = int(sample_rate)
        duration = int(duration)
        amplitude = float(amplitude)
        freq_start = int(freq_start)
        freq_end = int(freq_end)

    except ValueError as value_err:
        print("Value error")
        print(f"Exception: {str(value_err)}")
        input("Press Enter key to close this tab... ")
        return False

    if 384000 >= sample_rate >= 500 and 10 >= duration >= 1 and 1 >= amplitude >= 0 and freq_start >= 0 and freq_end <= 192000 and freq_start < freq_end:
        points = np.linspace(0, duration, sample_rate * duration, endpoint=False)
        frequences = np.linspace(freq_start, freq_end, len(points))

        signal = amplitude * np.sin(2 * np.pi * np.cumsum(frequences) / sample_rate)

        user_answer_rewrite = input("If file with the same name exists in current directory, the program will rewrite it. Do you agree to continue?(Y/N): ")
        if user_answer_rewrite.upper() == "Y":
            name = "test"
            filename = f"{name}.wav"
            abs_path_soundfile = os.path.abspath(filename)
            abs_path_logfile = None
            sf.write(filename, signal, sample_rate)
            data, sample_rate_ = sf.read(filename)
            user_answer_writelog = input("Do you want to create a log file, which contains sound file features?(Y/N): ")
            log_saved = False
                
            if user_answer_writelog.upper() == "Y":
                log_filename = f"{name}.log"
                log_file_path = os.path.join(os.path.dirname(filename), log_filename)
                abs_path_logfile = os.path.abspath(log_file_path)
                with open(log_file_path, "w") as f:
                    f.write(f"Sound file path: {abs_path_soundfile};\n")
                    f.write(f"Creating date and time(local): {datetime.now()};\n")
                    f.write(f"Sample rate: {sample_rate_} Hz;\n")
                    f.write(f"Duration: {duration} s;\n")
                    f.write(f"Amplitude: {amplitude};\n")
                    f.write(f"Frequences range: {freq_start} - {freq_end} Hz.")

                log_saved = True

            elif user_answer_writelog.upper() == "N":
                pass

            else:
                print("Type of answer is incorrect")
                
            user_answer_open = input("Do you want to open generated sound file immediately?(Y/N): ")
                
            if user_answer_open.upper() == "Y":
                system = platform.system()

                if system == "Windows":
                    os.startfile(abs_path_soundfile)
                elif system == "Darwin":
                    subprocess.run(["open", abs_path_soundfile])
                elif system == "Linux":
                    subprocess.run(["xdg-open", abs_path_soundfile])
                else:
                    print("OS is unsupported for auto-open:(")
                    
            elif user_answer_open.upper() == "N":
                print("File opening was rejected")
                
            else:
                print("Type of answer is incorrect")


            if sample_rate < freq_end * 2:
                print("Warning: sample rate should be at least 2 times greater than the highest frequency point for normal sound.")
            
            print(f"Sound file was saved. Path: {abs_path_soundfile}")
            if log_saved:
                print(f"Log file was saved. Path: {abs_path_logfile}")
                input("Press Enter key to close this tab...")
            else:
                print("Log file was not saved")
                input("Press Enter key to close this tab... ")
            return True
            
        elif user_answer_rewrite.upper() == "N":
            print("Continuing was rejected")
            print("File was not saved")
            input("Press Enter key to close this tab... ")
            return False
            
        else:
            print("Type of answer is incorrect")
            print("File was not saved")
            input("Press Enter key to close this tab... ")
            return False
        
    else:
        print("Error. Some of inputs have incorrect values. Correct values:")
        print("Sample rate: [500; 384000]")
        print("Duration: [1; 10]")
        print("Amplitude: [0; 1]")
        print("Frequency(from lowest to highest point): [0; 192000]")
        input("Press Enter key to close this tab...")
        return False

if __name__ == "__main__":
    main()