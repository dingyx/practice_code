from PIL import Image
import argparse


# 命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('file')    # 输入文件
parser.add_argument('-o', '--output')   # 输出文件
parser.add_argument('--width', type=int, default=80)    # 输出字符画宽
parser.add_argument('--height', type=int, default=80)    # 输出字符画高

# 获取参数
args = parser.parse_args()
IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output


# 灰度值公式
# gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
# 字符画所使用的字符集，一共有 70 个字符
# 灰度值小（暗）的用列表开头的符号，灰度值大（亮）的用列表末尾的符号
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# RGB值转字符函数 将256灰度映射到70个字符上
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0+1)/length
    return ascii_char[int(gray/unit)]


if __name__ == '__main__':
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    txt = ''
    for h in range(HEIGHT):
        for w in range(WIDTH):
            txt += get_char(*im.getpixel((w, h)))
        txt += '\n'
    print(txt)
    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as file:
            file.write(txt)
    else:
        with open('output.txt', 'w') as file:
            file.write(txt)
