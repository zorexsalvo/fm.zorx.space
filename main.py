import sys
import requests
import threading

STATIONS = [
    ("DEF CON Radio", "http://ice1.somafm.com/defcon-128-mp3"),
    ("Drone Zone", "http://ice1.somafm.com/dronezone-128-mp3"),
    ("Beat Blender", "http://ice1.somafm.com/beatblender-128-mp3"),
    ("Underground 80s", "http://ice1.somafm.com/u80s-128-mp3"),
    ("Groove Salad", "http://ice1.somafm.com/groovesalad-128-mp3"),
    ("Lush", "http://ice1.somafm.com/lush-128-mp3"),
    ("Bossa", "https://somafm.com/tikitime256.pls"),
]

current_index = 0
running = True
station_changed = threading.Event()

def input_listener():
    global current_index, running
    while running:
        cmd = sys.stdin.readline().strip()
        if cmd == ":quit":
            running = False
            station_changed.set()
        elif cmd == ":next":
            current_index = (current_index + 1) % len(STATIONS)
            station_changed.set()
        elif cmd == ":list":
            for i, (name, _) in enumerate(STATIONS):
                sys.stderr.write(f"{i+1}. {name}\n")
                sys.stderr.flush()
        elif cmd.isnumeric():
            current_index = int(cmd) - 1
            station_changed.set()

def stream_station(url):
    """Stream station MP3 bytes to stdout"""
    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=4096):
            if not running or station_changed.is_set():
                break
            if chunk:
                sys.stdout.buffer.write(chunk)
                sys.stdout.buffer.flush()

if __name__ == "__main__":
    sys.stderr.write("🎵 Welcome to fm.zorx.space 🎵\n")
    sys.stderr.write("Commands: :next, :list, :quit, <channel:int>\n\n")

    for i, (name, _) in enumerate(STATIONS):
        sys.stderr.write(f"{i+1}. {name}\n")
        sys.stderr.flush()

    sys.stderr.flush()

    threading.Thread(target=input_listener, daemon=True).start()

    while running:
        name, url = STATIONS[current_index]
        sys.stderr.write(f"\nNow playing: {name}\n")
        sys.stderr.flush()
        station_changed.clear()
        stream_station(url)

