
def move_to_trash(path: str) -> bool:
    '''
    将文件移动到回收站。成功返回True,失败返回False
    :param path:绝对路径。
    :return:
    '''
    import platform
    import send2trash
    if platform.system() == "Windows":
        path = path.replace('/', '\\')
    try:
        send2trash.send2trash(path)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False

def rename_file(prev_absolute_path:str, new_absolute_path:str)->bool:
    '''
    重命名文件或者文件夹
    :param prev_absolute_path:之前的绝对路径名称
    :param new_absolute_path: 之后的绝对路径名称
    :return:
    '''
    import os
    try:
        os.rename(prev_absolute_path, new_absolute_path)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False
if __name__ == '__main__':
    move_to_trash('C:/Users/12957/Desktop/1.jpg')
