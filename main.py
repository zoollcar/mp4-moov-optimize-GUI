import FreeSimpleGUI as sg
import subprocess
import sys

# Define the window's contents
layout = [[sg.Text("中医堂视频流媒体优化工具")],
          [sg.Text('选择需要优化的视频文件：', size=(15, 1)),
                    sg.InputText(key='-file1-'), sg.FileBrowse(button_text="选择", target='-file1-')],
          [sg.Text('视频保存到：', size=(15, 1)), sg.InputText(key='-file2-'),
                  sg.FileSaveAs(button_text="选择", target='-file2-', file_types= (("mp4视频文件", ".mp4"),))],
          [sg.Button('开始转换'), sg.Button('退出')],
          [sg.Output(size=(110,30), background_color='black', text_color='white')]
          ]

# Create the window
window = sg.Window('标题', layout)

def runCommand(cmd, timeout=None, window=None):
	nop = None
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output = ''
	for line in p.stdout:
		line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
		output += line
		print(line)
		window.refresh() if window else nop        # yes, a 1-line if, so shoot me
	sg.popup('已完成')

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == '退出':
        break
    if event == '开始转换':
        print('开始转换', values)
        runCommand(cmd=f'ffmpeg -i "{values["-file1-"]}" -movflags faststart {values["-file2-"]}', window=window)

window.close()