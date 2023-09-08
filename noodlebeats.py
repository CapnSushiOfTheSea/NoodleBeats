import time
import winsound
import tkinter as tk
from tkinter import filedialog
import os

def play_note(note, duration):
    notes_freq = {
        'C': 261.63,
        'C#': 277.18,
        'D': 293.66,
        'D#': 311.13,
        'E': 329.63,
        'F': 349.23,
        'F#': 369.99,
        'G': 392.00,
        'G#': 415.30,
        'A': 440.00,
        'A#': 466.16,
        'B': 493.88
    }

    print(str(note))
    winsound.Beep(int(notes_freq[note] * 2), int(duration * 1000))

def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a .nob file", filetypes=[("NoodleBeats Files", "*.nob")])

    if not file_path:
        print("No file selected.")
        return

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines or not lines[0].strip() == "!! NOODLEBEATS FILE !!":
                print("Hmm... This doesn't seem to be a proper NoodleBeats file.")
                return

            title = ""
            artist = ""
            has_begin = False

            for line in lines:
                if line.startswith("$BEGIN"):
                    has_begin = True
                    break

            if not has_begin:
                print("Hmm... This doesn't seem to be a proper NoodleBeats file.")
                return

            for line in lines:
                if line.startswith("$TITLE"):
                    title = line.split('"')[1]
                elif line.startswith("$ARTIST"):
                    artist = line.split('"')[1]
                elif line.startswith("$BEGIN"):
                    break

            if not title and not artist:
                title = os.path.splitext(os.path.basename(file_path))[0]
                artist = "Unknown Artist"

            print(f'Song: "{title}" by {artist}')
            print('===============')

            for line in lines:
                if line.startswith("$BEGIN") or not line.strip():
                    continue
                parts = line.strip().split(', ')
                if len(parts) == 2:
                    note, duration = parts
                    play_note(note, float(duration))
                    time.sleep(float(duration))
                else:
                    continue

            print('===============\nComplete!')

    except FileNotFoundError:
        print(f"The file '{file_path}' could not be found.")
    
    except KeyboardInterrupt:
        print(f"Abort.")

if __name__ == "__main__":
    main()