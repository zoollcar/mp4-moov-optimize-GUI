import PySimpleGUI as sg
import subprocess
import threading

def run_ffmpeg_command(input_file, output_file):
    command = f'ffmpeg -i "{input_file}" -movflags faststart "{output_file}"'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            window['-OUTPUT_WINDOW-'].print(output.strip(), end='', text_color='white', background_color='black')
    return process.returncode

def execute_ffmpeg_command(input_file, output_file):
    window['-OUTPUT_WINDOW-'].update('')
    return_code = run_ffmpeg_command(input_file, output_file)

    if return_code == 0:
        sg.popup('Command executed successfully!', title='Success', keep_on_top=True)
    else:
        sg.popup_error(f'Error executing command. Return code: {return_code}', title='Error', keep_on_top=True)

def main():
    layout = [
        [sg.Text('Input File:'), sg.InputText(key='-INPUT-', size=(30, 1)), sg.FileBrowse()],
        [sg.Text('Output File:'), sg.InputText(key='-OUTPUT-', size=(30, 1)), sg.FileSaveAs(target='-OUTPUT-')],
        [sg.Button('Run'), sg.Button('Exit')],
        [sg.Text('Command Output:')],
        [sg.Output(size=(60, 10), key='-OUTPUT_WINDOW-', text_color='white', background_color='black')]
    ]

    global window
    window = sg.Window('FFmpeg GUI', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Run':
            input_file = values['-INPUT-']
            output_file = values['-OUTPUT-']

            if input_file and output_file:
                threading.Thread(target=execute_ffmpeg_command, args=(input_file, output_file), daemon=True).start()

    window.close()

if __name__ == "__main__":
    main()
