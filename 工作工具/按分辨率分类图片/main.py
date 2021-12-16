# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
import os
from PIL import Image
from shutil import copyfile


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 ⌘F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    old_image_dir = input("输入要处理到图片目录:")
    old_image_dir = old_image_dir.strip()
    new_image_dir = input("输入要保存到位置:")
    new_image_dir = new_image_dir.strip()
    files = os.listdir(old_image_dir)
    for i in files:
        x, y = Image.open(old_image_dir + r"/" + i).size
        new_dir_name = "{x}x{y}".format(x=x, y=y)
        print(new_dir_name)
        # 保存文件
        if not os.path.exists(new_image_dir + r"/" + new_dir_name):
            print(new_dir_name, "不存在")
            os.makedirs(new_image_dir + r"/" + new_dir_name)
        # 保存 把文件从老地方复制到新地方
        copyfile(old_image_dir + r"/" + i, new_image_dir + r"/" + new_dir_name + r"/" + i)
