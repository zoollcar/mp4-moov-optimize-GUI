import os
import struct

def find_box(file_path, box_type):
    with open(file_path, "rb") as f:
        while True:
            # 读取box的大小和类型
            size, box = struct.unpack(">I4s", f.read(8))
            # 将box大小减去8（已读取的大小）减去4（box类型的大小），得到box的实际大小
            size -= 8
            # 如果box类型匹配，则返回当前位置
            if box == box_type.encode("utf-8"):
                return f.tell() - 8
            # 移动到下一个box的位置
            f.seek(size, os.SEEK_CUR)
            # 如果已到达文件末尾，则退出循环
            if f.tell() == os.fstat(f.fileno()).st_size:
                break
    # 如果未找到指定类型的box，则返回-1
    return -1

def checkIfNeedOptimization(video_file_path):
    if os.path.exists(video_file_path):
        # 查找MOOV和MDAT的位置
        moov_position = find_box(video_file_path, "moov")
        mdat_position = find_box(video_file_path, "mdat")
        if moov_position < mdat_position:
            return True
        else:
            return False
    else:
        return False