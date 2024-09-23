import FreeSimpleGUI as sg
import subprocess
import os
import re
import time
import checkIfNeedOptimization

# Define the window's contents
layout = [
    [sg.Text("视频流媒体优化工具")],
    [
        sg.Text("选择需要优化的视频文件：", size=(15, 1)),
        sg.InputText(key="-file1-", change_submits=True),
        sg.FileBrowse(button_text="选择", target="-file1-"),
    ],
    [
        sg.Text("视频保存到：", size=(15, 1)),
        sg.InputText(key="-file2-"),
        sg.FileSaveAs(
            button_text="选择", target="-file2-", file_types=(("mp4视频文件", ".mp4"),)
        ),
    ],
    [sg.Button("开始转换"), sg.Button("退出")],
    # [sg.Output(size=(110, 30), background_color="black", text_color="white")],
]

# Create the window
window = sg.Window("标题", layout)


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
                speed = current_time / elapsed_time  # 当前处理速度（秒/秒）
                remaining_time = (
                    (total_duration - current_time) / speed
                    if speed > 0
                    else float("inf")
                )

                # Format remaining time into HH:MM:SS
                remaining_hours, remainder = divmod(remaining_time, 3600)
                remaining_minutes, remaining_seconds = divmod(remainder, 60)
                formatted_remaining_time = f"{int(remaining_hours)}:{int(remaining_minutes):02}:{int(remaining_seconds):02}"

                print(
                    f"进度: {percent:.2f}% | 剩余时间: {formatted_remaining_time}"
                )
        window.refresh() if window else None
    sg.popup("已完成", button_type=5)  # 5: POPUP_BUTTONS_NO_BUTTONS

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == "退出":
        break
    if event == '-file1-':
        if os.path.exists(values['-file1-']):
            if checkIfNeedOptimization.checkIfNeedOptimization(values["-file1-"]):
                print('选择的文件*不需要优化*')
            else:
                print('选择的文件*需要优化*')
    if event == "开始转换":
        print("开始转换", values)
        cmd = [
            "ffmpeg",
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
