import locale

texts = {
    "chinese": {
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
    "english": {
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
    lang_code, _ = locale.getlocale()
    print(lang_code)
    if lang_code == None:
        return "english"
    elif lang_code.find("chinese") != -1:
        return "chinese"
    else:
        return "english"