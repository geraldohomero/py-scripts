import subprocess
import os

def speechToText():
    cwd = os.getcwd()
    mp4_audio = os.path.join(cwd, 'audio.mp4')
    wav_audio = os.path.join(cwd, 'audio.wav')
    
    # Convert MP4 to 16-bit WAV file using ffmpeg
    convert_command = [
        "ffmpeg",
        "-i", mp4_audio,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        wav_audio
    ]
    try:
        subprocess.run(convert_command, check=True)
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure it is installed and in your PATH.")
        return
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg conversion: {e}")
        return
    
    # Update the path to the whisper-cli executable as needed.
    whisper_cli_path = "./whisper.cpp/build/bin/whisper-cli"

    if not os.path.exists(whisper_cli_path):
        print(f"Error: whisper-cli not found at {whisper_cli_path}. Please ensure it is built and the path is correct.")
        return

    # Update the model argument to point to the downloaded ggml model file.
    model_path = "./whisper.cpp/models/ggml-large-v3-turbo.bin"
    if not os.path.exists(model_path):
        print(f"Error: model file not found at {model_path}. Please ensure the model file is downloaded and the path is correct.")
        return

    command = [
        whisper_cli_path,
        "-f", wav_audio,
        "--language", "pt",  # change language if needed
        "--model", model_path,
        "-t", "6",  # Use 6 threads during computation
        "--no-timestamps",  # Remove timestamps
        "--output-txt",  # Ensure output is not a single line of text
        "--duration", "0"  # Process the entire audio track
    ]
    
    try:
        # Run whisper-cli; it will output a transcription file (e.g., "audio.wav.txt")
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print(f"Error: whisper-cli not found at {whisper_cli_path}. Please ensure it is built and the path is correct.")
        return
    except subprocess.CalledProcessError as e:
        print(f"Error during whisper-cli execution: {e}")
        return
    
    # Check if the expected transcription file exists.
    transcription_file = os.path.join(cwd, 'audio.wav.txt')
    if os.path.exists(transcription_file):
        with open(transcription_file, 'r', encoding="utf-8") as infile:
            text = infile.read()
        with open('text.txt', 'w', encoding="utf-8") as outfile:
            outfile.write(text)
        print("Text saved to text.txt")
    else:
        print("Transcription output not found. Please verify your whisper-cli command.")

if __name__ == '__main__':
    speechToText()
