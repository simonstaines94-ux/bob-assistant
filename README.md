# BOB Assistant - Text Mode

## How to Run

### Option A - Double click
Double-click `install_and_run.bat` (first time)
Double-click `run_bob.bat` (after that)

### Option B - VS Code
1. Open this folder in VS Code
2. Press Ctrl+` to open terminal
3. Type: python bob_assistant.py

## Commands
| Type this | What Bob does |
|---|---|
| open chrome | Opens Chrome |
| open notepad | Opens Notepad |
| open calculator | Opens Calculator |
| open explorer | Opens File Explorer |
| open spotify | Opens Spotify |
| search weather | Google search |
| youtube lo-fi | YouTube search |
| organize downloads | Sorts your files |
| write a note | New note on Desktop |
| what time is it | Shows time |
| what is the date | Shows date |
| lock | Locks PC |
| volume 60 | Sets volume |
| quit | Exits Bob |

## Add Your Own Apps
Open bob_assistant.py and find CONFIG section.
Add your app like this:
    "telegram": r"C:\Users\YourName\AppData\Roaming\Telegram Desktop\Telegram.exe",
