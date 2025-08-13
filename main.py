import subprocess
import sys
import threading
import time

STATIONS = [
    ("Groove Salad", "http://ice1.somafm.com/groovesalad-128-mp3"),
    ("Lush", "http://ice1.somafm.com/lush-128-mp3"),
    ("DEF CON Radio", "http://ice1.somafm.com/defcon-128-mp3")
]

current_index = 0
player_proc = None
running = True

def play_station(url):
    global player_proc
    player_proc = subprocess.Popen(["mpg123", "-q", url])

def input_listener():
    global current_index, running, player_proc
    while running:
        cmd = sys.stdin.readline().strip()
        if cmd == ":quit":
            running = False
            if player_proc:
                player_proc.kill()
        elif cmd == ":next":
            current_index = (current_index + 1) % len(STATIONS)
            if player_proc:
                player_proc.kill()
            print(f"\nSwitching to {STATIONS[current_index][0]}...\n")
            play_station(STATIONS[current_index][1])
        elif cmd == ":list":
            for i, (name, _) in enumerate(STATIONS):
                print(f"{i+1}. {name}")

print("🎵 Welcome to fm.zorx.space 🎵")
print("Commands: :next, :list, :quit\n")
print(f"Now playing: {STATIONS[current_index][0]}\n")

play_station(STATIONS[current_index][1])

threading.Thread(target=input_listener, daemon=True).start()

while running:
    time.sleep(0.2)

print("Goodbye!")

