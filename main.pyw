import FreeSimpleGUI as sg
import subprocess
import os
import re
import time
from checkIfNeedOptimization import checkIfNeedOptimization

# Language dictionary
from locales import texts, getLang
lang = getLang()

# Define the window's contents
layout = [
    [sg.Text(texts[lang]["title"])],
    [
        sg.Text(texts[lang]["select_file"]),
        sg.InputText(key="-file1-", change_submits=True),
        sg.FileBrowse(
            button_text=texts[lang]["select"],
            target="-file1-",
            file_types=(("mp4 file", ".mp4"),),
        ),
    ],
    [
        sg.Text(texts[lang]["save_to"]),
        sg.InputText(key="-file2-"),
        sg.FileSaveAs(
            button_text=texts[lang]["select"],
            target="-file2-",
            file_types=(("mp4 file", ".mp4"),),
        ),
    ],
    [sg.Button(texts[lang]["start_optimize"]), sg.Button(texts[lang]["exit"])],
    [sg.Output(size=(110, 30), background_color="black", text_color="white")],
]

# Create the window
window = sg.Window(texts[lang]["title"], layout)

def get_total_duration(input_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_file,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return float(result.stdout)


def runCommand(cmd, window=None):
    total_duration = get_total_duration(values["-file1-"])
    start_time = time.time()
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for line in p.stdout:
        line = line.decode(errors="replace").rstrip()
        # Match the current time from the ffmpeg output
        match = re.search(r"time=(\d+:\d+:\d+\.\d+)", line)
        if match:
            current_time_str = match.group(1)
            current_time_parts = list(map(float, current_time_str.split(":")))
            current_time = (
                current_time_parts[0] * 3600
                + current_time_parts[1] * 60
                + current_time_parts[2]
            )
            # Calculate progress
            percent = (current_time / total_duration) * 100
            # Calculate speed and remaining time
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                speed = current_time / elapsed_time
                remaining_time = (
                    ((total_duration - current_time) / speed)
                    if speed > 0
                    else float("inf")
                )
                # Format remaining time into HH:MM:SS
                remaining_hours, remainder = divmod(remaining_time, 3600)
                remaining_minutes, remaining_seconds = divmod(remainder, 60)
                formatted_remaining_time = f"{int(remaining_hours)}:{int(remaining_minutes):02}:{int(remaining_seconds):02}"
                print(texts[lang]["progress"].format(percent, formatted_remaining_time))
        window.refresh() if window else None
    print(texts[lang]["completed"])
    sg.popup(texts[lang]["completed"], button_type=5)


# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == texts[lang]["exit"]:
        break
    if event == "-file1-":
        if os.path.exists(values["-file1-"]):
            if checkIfNeedOptimization(values["-file1-"]):
                print(texts[lang]["no_optimization"])
            else:
                print(texts[lang]["needs_optimization"])
    if event == texts[lang]["start_optimize"]:
        print(texts[lang]["start_optimize"], values)
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            values["-file1-"],
            "-movflags",
            "faststart",
            "-progress",
            "pipe:1" "-nostats",
            values["-file2-"],
        ]
        runCommand(cmd, window=window)

window.close()
