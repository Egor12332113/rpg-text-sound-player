# RPG Text Sound Player

A simple Python application that plays a sound for each character displayed in a text area, mimicking the style often found in RPG dialogues. This allows users to experience text with an auditory feedback, with customizable sound, speed, and volume.

## Features

* **Character-by-Character Sound:** Plays a selected sound effect for each character as it appears.
* **Customizable Sound:** Load your own sound files (supports .wav, .ogg, and potentially other formats pygame can handle).
* **Adjustable Speed:** Control the delay (in milliseconds) between characters appearing.
* **Volume Control:** Adjust the playback volume of the sound effect.
* **Text Input:**
    * Type or paste text directly into the input area.
    * Load text from `.txt` files.
    * Drag-and-drop `.txt` files onto the input area (if `tkinterdnd2` is available).
* **User-Friendly Interface:** Simple GUI built with Tkinter.

## Requirements

* Python 3.6+
* Pygame: `pygame`
* TkinterDnD2 (for drag-and-drop functionality, optional if not used): `tkinterdnd2`

## Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone [https://github.com/Egor12332113/rpg-text-sound-player.git](https://github.com/Egor12332113/rpg-text-sound-player.git)
    cd rpg-text-sound-player.git
    ```
    (Replace `rpg-text-sound-player.git` with the actual name of your repository)

2.  **Install the required libraries:**
    It's recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment (optional but recommended)
    # python -m venv venv
    # source venv/bin/activate  # On Windows: venv\Scripts\activate

    pip install -r requirements.txt
    ```
    Or, install manually:
    ```bash
    pip install pygame tkinterdnd2
    ```
    *(Note: `tkinter` usually comes bundled with Python standard distributions.)*

## How to Run

1.  Make sure you have a sound file ready (e.g., a short `.wav` or `.ogg` blip).
2.  Run the script from your terminal:
    ```bash
    python rpg_sound_text_player.py
    ```
    (Replace `rpg_sound_text_player.py` with the actual name of your Python script if it's different.)

## Usage

1.  **Select Sound File:** Click the "Выбрать звук (.wav)" (Select Sound) button to choose a sound file. The program primarily filters for `.wav` but should also accept other formats like `.ogg` if selected via "All files".
2.  **Adjust Interval (мс):** Use the slider or type in the entry box to set the delay in milliseconds between each character appearing. Lower values mean faster text.
3.  **Adjust Volume:** Use the slider or type in the entry box to set the sound effect volume (0.0 for mute, 1.0 for full volume).
4.  **Input Text:**
    * Type or paste your desired text into the "Введите или перетащите текст сюда" (Enter or drag text here) input area.
    * Click "Загрузить текст из файла (.txt)" (Load text from file) to load text from a `.txt` file.
    * If `tkinterdnd2` is working, you can drag and drop a `.txt` file directly onto this input area.
5.  **Play:** Click the "Воспроизвести" (Play) button. The text will appear character by character in the "Результат" (Result) area below, with the selected sound playing for each character.
6.  **Stop:** Click the "Остановить" (Stop) button to halt the playback at any time.

---

Managed by Egor12332113.
