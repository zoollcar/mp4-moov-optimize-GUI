import locale

texts = {
    "Chinese": {
        "title": "MP4视频优化工具",
        "select_file": "选择需要优化的视频文件：",
        "select": "选择",
        "save_to": "视频保存到：",
        "start_optimize": "开始转换",
        "exit": "退出",
        "progress": "进度: {:.2f}% | 剩余时间: {}",
        "completed": "已完成",
        "no_optimization": "选择的文件*不需要优化*",
        "needs_optimization": "选择的文件*需要优化*",
    },
    "English": {
        "title": "MP4 Video Optimization Tool",
        "select": "select",
        "select_file": "Select video file to optimize: ",
        "save_to": "Save video to: ",
        "start_optimize": "Start Optimize",
        "exit": "Exit",
        "progress": "Progress: {:.2f}% | Remaining time: {}",
        "completed": "Completed",
        "no_optimization": "Selected file *does not need optimization*",
        "needs_optimization": "Selected file *needs optimization*",
    },
}

def getLang():
    # Load language based on system locale
    locale.setlocale(locale.LC_ALL, "")
    lang_code, _ = locale.getlocale(locale.LC_ALL)
    print(lang_code)
    if lang_code == None:
        return "English"
    elif lang_code.find("Chinese") != -1:
        return "Chinese"
    else:
        return "English"