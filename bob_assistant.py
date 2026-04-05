"""
╔══════════════════════════════════════════╗
║         BOB - Windows AI Assistant       ║
║         Text Mode (no microphone)        ║
║         Press Ctrl+C to quit             ║
╚══════════════════════════════════════════╝
"""

import os
import sys
import time
import subprocess
import webbrowser
import shutil
import datetime
import threading

# ── Text-to-speech (optional) ──────────────────────────────────────────────────
try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    TTS_ENABLED = True
except ImportError:
    TTS_ENABLED = False

# ── CONFIG — Edit app paths to match your PC ───────────────────────────────────
CONFIG = {
    "apps": {
        "vs code":       r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "notepad":       r"notepad.exe",
        "chrome":        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "explorer":      r"explorer.exe",
        "calculator":    r"calc.exe",
        "task manager":  r"taskmgr.exe",
        "spotify":       r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
        "word":          r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel":         r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "paint":         r"mspaint.exe",
        "cmd":           r"cmd.exe",
        "powershell":    r"powershell.exe",
        "opera":         r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera\launcher.exe",
        "edge":          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    },
    "downloads_folder": os.path.expanduser("~/Downloads"),
    "organized_folder": os.path.expanduser("~/Downloads/Organized"),
}

# ── File categories ────────────────────────────────────────────────────────────
FILE_TYPES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos":    [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Audio":     [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv"],
    "Archives":  [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code":      [".py", ".js", ".html", ".css", ".java", ".cpp", ".json", ".ts"],
    "Others":    []
}

# ── Speak ──────────────────────────────────────────────────────────────────────
def speak(text):
    print(f"\n  [BOB] {text}")
    if TTS_ENABLED:
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

# ── Open app ───────────────────────────────────────────────────────────────────
def open_app(name):
    for app, path in CONFIG["apps"].items():
        if app in name or name in app:
            path = os.path.expandvars(path)
            try:
                subprocess.Popen(path)
                speak(f"Opening {app}.")
                return True
            except:
                speak(f"Could not open {app}. Check the path in CONFIG.")
                return False
    speak(f"App not found. You can add it to CONFIG in the script.")
    return False

# ── Web ────────────────────────────────────────────────────────────────────────
def web_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    speak(f"Searching for {query}.")

def open_youtube(query=""):
    if query:
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        speak(f"Searching YouTube for {query}.")
    else:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

# ── Organize downloads ─────────────────────────────────────────────────────────
def organize_downloads():
    src = CONFIG["downloads_folder"]
    dst = CONFIG["organized_folder"]
    moved = 0
    for fname in os.listdir(src):
        fpath = os.path.join(src, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            folder = "Others"
            for cat, exts in FILE_TYPES.items():
                if ext in exts:
                    folder = cat
                    break
            dest_dir = os.path.join(dst, folder)
            os.makedirs(dest_dir, exist_ok=True)
            try:
                shutil.move(fpath, os.path.join(dest_dir, fname))
                moved += 1
            except:
                pass
    speak(f"Done. Organized {moved} files into folders.")

# ── Create note ────────────────────────────────────────────────────────────────
def create_note():
    desktop = os.path.expanduser("~/Desktop")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(desktop, f"note_{ts}.txt")
    with open(path, "w") as f:
        f.write(f"Note — {datetime.datetime.now().strftime('%A, %B %d %Y %I:%M %p')}\n\n")
    try:
        subprocess.Popen(["notepad.exe", path])
    except:
        pass
    speak("Note created on your desktop.")

# ── System ─────────────────────────────────────────────────────────────────────
def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    speak("PC locked.")

def set_volume(level):
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        speak(f"Volume set to {level}%.")
    except:
        speak("Volume control needs pycaw. Run: pip install pycaw comtypes")

# ── Command processor ──────────────────────────────────────────────────────────
def process_command(command):
    command = command.lower().strip()
    # remove wake word if typed
    command = command.replace("bob,", "").replace("bob", "").strip()

    if not command:
        speak("Yes? What do you need?")
        return

    # Open apps
    if any(w in command for w in ["open", "launch", "start", "run"]):
        for app in CONFIG["apps"]:
            if app in command:
                open_app(app)
                return

    # YouTube
    if "youtube" in command:
        query = command.replace("youtube","").replace("open","").replace("play","").replace("search","").strip()
        open_youtube(query)
        return

    # Search
    if "search" in command or "google" in command:
        query = command.replace("search","").replace("google","").replace("for","").strip()
        web_search(query)
        return

    # Organize
    if "organize" in command or "clean" in command:
        speak("Organizing your Downloads folder now.")
        threading.Thread(target=organize_downloads, daemon=True).start()
        return

    # Note
    if "note" in command or "write" in command:
        create_note()
        return

    # Lock
    if "lock" in command:
        lock_pc()
        return

    # Time
    if "time" in command:
        speak(f"It is {datetime.datetime.now().strftime('%I:%M %p')}.")
        return

    # Date
    if "date" in command or "day" in command:
        speak(f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.")
        return

    # Volume
    if "volume" in command:
        for word in command.split():
            if word.isdigit():
                set_volume(int(word))
                return
        speak("Say a number. Example: volume 60.")
        return

    # Shutdown
    if "shutdown" in command or "shut down" in command:
        speak("Shutting down in 10 seconds.")
        time.sleep(10)
        os.system("shutdown /s /t 0")
        return

    # Restart
    if "restart" in command:
        speak("Restarting in 10 seconds.")
        time.sleep(10)
        os.system("shutdown /r /t 0")
        return

    # Greet
    if any(w in command for w in ["hello", "hi", "hey"]):
        speak("Hey! What do you need?")
        return

    # Help
    if "help" in command or "what can you do" in command:
        speak("I can open apps, search Google, open YouTube, organize downloads, create notes, check time and date, lock your PC, and control volume.")
        return

    # Exit
    if any(w in command for w in ["quit", "exit", "bye", "goodbye", "stop"]):
        speak("Goodbye!")
        sys.exit()

    speak("I didn't get that. Try: open chrome, search python, what time is it, or organize downloads.")

# ── Main text loop ─────────────────────────────────────────────────────────────
def main():
    print("""
╔══════════════════════════════════════════╗
║         BOB - Windows AI Assistant       ║
║                                          ║
║  Type your command and press Enter       ║
║  Example: open chrome                    ║
║  Example: search the weather             ║
║  Example: what time is it                ║
║  Example: organize downloads             ║
║                                          ║
║  Type 'help' for all commands            ║
║  Type 'quit' to exit                     ║
╚══════════════════════════════════════════╝
    """)

    if TTS_ENABLED:
        speak("Bob is online. Type your command.")
    else:
        print("  [BOB] Online. Type your command.\n")

    while True:
        try:
            user_input = input("\n  You: ").strip()
            if user_input:
                process_command(user_input)
        except KeyboardInterrupt:
            speak("Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main()
