import sys
import requests
import threading
import shutil

STATIONS = [
    ("DEF CON Radio", "http://ice1.somafm.com/defcon-128-mp3"),
    ("Drone Zone", "http://ice1.somafm.com/dronezone-128-mp3"),
    ("Beat Blender", "http://ice1.somafm.com/beatblender-128-mp3"),
    ("Underground 80s", "http://ice1.somafm.com/u80s-128-mp3"),
    ("Groove Salad", "http://ice1.somafm.com/groovesalad-128-mp3"),
    ("Lush", "http://ice1.somafm.com/lush-128-mp3"),
    ("Bossa", "https://ice1.somafm.com/bossa-128-mp3"),
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

def center_message(message):
    """Center a message in the terminal"""
    columns = shutil.get_terminal_size().columns
    padding = (columns - len(message)) // 2
    return ' ' * padding + message

def color_text(text, color_code='93'):
    """Color a text with ANSI escape codes"""
    return f'\033[{color_code}m{text}\033[0m'

if __name__ == "__main__":
    app_name = color_text("fm.zorx.space")
    message = f"🎵 Welcome to {app_name} 🎵\n"
    sys.stderr.write("\n" + center_message(message))
    sys.stderr.write(
        center_message("Commands: :next, :list, :quit, <channel:int>\n\n")
    )

    for i, (name, _) in enumerate(STATIONS):
        sys.stderr.write(center_message(f"{i+1}. {name}\n"))
        sys.stderr.flush()

    sys.stderr.flush()

    threading.Thread(target=input_listener, daemon=True).start()

    while running:
        name, url = STATIONS[current_index]
        sys.stderr.write("\n" + center_message(f"Now playing: {name}") + "\n\n\n")
        sys.stderr.flush()
        station_changed.clear()
        stream_station(url)

