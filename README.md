# Log Analysis & Automation Scripts

This repository contains Python scripts designed for log file processing, event handling, and automation. These scripts help analyze log data, extract specific information, and automate certain in-game tasks.

## 📂 Project Overview

### 1. **`search_answer.py`**
   - Scans log files for predefined phrases using regular expressions.
   - Extracts relevant information from logs and saves it to an output file.
   - Handles different text encodings (UTF-8 and ISO-8859-1) for compatibility.

### 2. **`TypeEvent.py`**
   - Automates input handling in games (e.g., Minecraft 1.12.2).
   - Simulates typing responses to in-game events.
   - Uses keyboard and mouse interactions to enter words based on detected chat events.
   - Implements background mode and AFK detection.

### 3. **`unrar_logs.py`**
   - Extracts `.log.gz` files from a specified directory.
   - Ignores the `telemetry` folder during extraction.
   - Saves the extracted log files to a designated output directory.

## 🛠️ Requirements

Ensure you have the following dependencies installed:

```bash
pip install keyboard pynput pywin32
```

Additional system dependencies:
- `winsound` (Windows built-in module)
- `ctypes` (for input blocking)
- `shutil` and `gzip` (for log extraction)

## 🚀 Usage

### Running `search_answer.py`
Modify the `log_dir` and `output_file_path` variables to match your log directory and output destination. Then, run:

```bash
python search_answer.py
```

### Running `TypeEvent.py`
This script is designed to work in the background with a game. Run:

```bash
python TypeEvent.py
```

Press `F7` to toggle the script ON/OFF.

### Running `unrar_logs.py`
Modify the `source_dir` and `destination_dir` variables, then run:

```bash
python unrar_logs.py
```

## ⚠️ Notes
- **For Windows users**: Ensure you have administrative permissions if required.
- **Minecraft automation**: This script was tested with **Minecraft 1.12.2**; functionality may differ in other versions.

## 📜 License
This project is licensed under the MIT License.
