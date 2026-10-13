# Space-Invaders-Yr9
This is an assessment task for Computer Technology, Term 3.

## Brief Overview
Space Invaders is a classic arcade game released in July 1978 by Taito. The main goal of the game is to destroy all the approaching aliens using your lasers before they reach your spaceship. In this modified computer version, arrow keys will replace the joystick movement and the spacebar will replace the button laser shooting.

## Control
- Left arrow -> Move Left
- Right arrow -> Move Right
- Spacebar -> Shoot Laser / Reset Level

## Setup Instructions

1. Download the .exe file from the 'Releases' section on the right hand side OR search for it in the folder 'dist'.
2. (Optional) Move the .exe file into your desktop.

Alternatively, you can download the entire project folder by:

1. Press the green 'Code' button.
1. Download this repository as a ZIP folder by pressing 'Download ZIP'.
1. Find your downloaded folder using File Explorer and unzip it.
1. Install Python on your computer.
1. Open terminal in the folder and run: 
```
pip install -r requirements.txt.
```
6. Run the script using python main.py.


## How To Run The Game

- Run the .exe file downloaded from the 'Releases' section OR found in the folder 'dist'.
- Alternatively, you can run the game from the repository folder with:

```powershell
py main.py
```

### Building a Windows executable with PyInstaller

Install PyInstaller in the Python environment used for the game:

```powershell
py -m pip install pyinstaller
```

From the repository folder, build a single-file executable:

```powershell
py -m PyInstaller --noconfirm --onefile --windowed --name SpaceInvaders `
  --add-data "Graphics;Graphics" `
  --add-data "Font;Font" `
  --add-data "Sounds;Sounds" `
  main.py
```

PyInstaller follows the imports from `main.py` and bundles the project's Python
modules. The `--add-data` options include the graphics, font, and sound folders.
`assets.py` resolves those files both when running from source and when the
executable is running from PyInstaller's temporary extraction directory. Find
the executable in `dist\SpaceInvaders.exe`.

The high score is saved outside the game folder at
`%LOCALAPPDATA%\SpaceInvaders\highscore.txt`, so launching the executable from
the Desktop will not create a new high-score file there. On first launch, an
existing `highscore.txt` in the current working folder is moved to this
location, preserving the saved score.
