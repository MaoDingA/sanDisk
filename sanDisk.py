import os
import tkinter as tk
from tkinter import filedialog, messagebox

# 定义视频和音频扩展名
video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.ari', '.dng', '.mxf',
                    '.r3d', '.arw', '.jpg', '.jpeg', '.dpx', '.cine', '.raw']
audio_extensions = ['.wav', '.wave', '.mp3', '.aac', '.ogg', '.flac', '.wma', '.aiff', '.au',
                    '.m4a', '.ape']

# 检查文件是否是媒体文件
def is_media(file, include_audio, ignore_types):
    if include_audio:
        valid_extensions = [ext for ext in video_extensions + audio_extensions if ext not in ignore_types]
    else:
        valid_extensions = [ext for ext in video_extensions if ext not in ignore_types]
    return file.lower().endswith(tuple(valid_extensions))

def list_videos():
    scan_directory = e2.get()
    output_directory = e4.get()
    project_name = e1.get()
    proxy_paths = [e.get() for e in proxy_entries]  # 获取多个代理路径文本框的内容
    include_audio = audio_var.get()
    ignore_types = [ext for ext, var in ignore_types_vars.items() if var.get()]

    output_file = os.path.join(output_directory, f"{project_name}_DiskMata.txt")
    proxy_output_files = [os.path.join(output_directory, f"{project_name}_MataDisk_Proxy{i+1}.txt") for i in range(3)]

    video_found = False
    proxy_found = False

    # 用于记录代理路径的媒体文件
    proxy_media_files = []

    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(scan_directory):
            for file in files:
                if is_media(file, include_audio, ignore_types):
                    video_found = True
                    f.write(f"{os.path.join(root, file)}\n")

    for i, proxy_path in enumerate(proxy_paths):
        if proxy_path:
            proxy_found = True
            with open(proxy_output_files[i], 'w') as pf:
                for root, dirs, files in os.walk(proxy_path):
                    for file in files:
                        if is_media(file, include_audio, ignore_types):
                            proxy_media_files.append(os.path.join(root, file))
                            pf.write(f"{os.path.join(root, file)}\n")

    # 从总文件中排除代理路径的媒体文件
    if proxy_media_files:
        with open(output_file, 'r') as f:
            lines = f.readlines()
        with open(output_file, 'w') as f:
            for line in lines:
                if line.strip() not in proxy_media_files:
                    f.write(line)

    if not video_found:
        result_label.config(text="在指定目录中未找到媒体文件。")
    else:
        result_label.config(text=f"媒体列表已保存在 {output_file}")

    if proxy_found:
        proxy_label.config(text="代理路径的媒体列表已保存在以下文件中：")
        for i, proxy_output_file in enumerate(proxy_output_files):
            proxy_label.config(text=proxy_label.cget("text") + f"\n{proxy_output_file}")
    else:
        proxy_label.config(text="在代理路径中未找到媒体文件。")

    messagebox.showinfo("完成", "扫盘已完成！")

def browse_folder(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

master = tk.Tk()
master.title("扫盘小插件")

label_width = 30
entry_width = 60
button_width = 10

tk.Label(master, text="需要扫盘的项目名称:", width=label_width).grid(row=0, sticky=tk.W)
tk.Label(master, text="该项目的原素材路径:", width=label_width).grid(row=1, sticky=tk.W)
tk.Label(master, text="请输入代理文件路径1:", width=label_width).grid(row=2, sticky=tk.W)
tk.Label(master, text="请输入代理文件路径2:", width=label_width).grid(row=3, sticky=tk.W)
tk.Label(master, text="请输入代理文件路径3:", width=label_width).grid(row=4, sticky=tk.W)
tk.Label(master, text="输出扫盘文件的路径:", width=label_width).grid(row=5, sticky=tk.W)
tk.Label(master, text="是否扫描声音文件:", width=label_width).grid(row=6, sticky=tk.W)

e1 = tk.Entry(master, width=entry_width)
e2 = tk.Entry(master, width=entry_width)
proxy_entries = [tk.Entry(master, width=entry_width) for _ in range(3)]  # 创建三个代理路径的文本框
e4 = tk.Entry(master, width=entry_width)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
for i, entry in enumerate(proxy_entries):
    entry.grid(row=2+i, column=1)
    tk.Button(master, text='浏览', width=button_width, command=lambda entry=entry: browse_folder(entry)).grid(row=2+i, column=2, padx=4)
e4.grid(row=5, column=1)

tk.Button(master, text='浏览', width=button_width, command=lambda: browse_folder(e2)).grid(row=1, column=2, padx=4)
tk.Button(master, text='浏览', width=button_width, command=lambda: browse_folder(e4)).grid(row=5, column=2, padx=4)

audio_var = tk.BooleanVar()
audio_check = tk.Checkbutton(master, text="带声音", variable=audio_var)
audio_check.grid(row=6, column=1, sticky=tk.W)

# 创建一个Frame用于放置封装格式的按钮
frame_formats = tk.Frame(master)
frame_formats.grid(row=7, column=0, columnspan=4)

tk.Label(frame_formats, text="是否有需要忽略的封装格式:").pack(anchor=tk.W)

ignore_types_vars = {}
for i, ext in enumerate(video_extensions):
    var = tk.BooleanVar()
    ignore_types_vars[ext] = var
    tk.Checkbutton(frame_formats, text=ext, variable=var).pack(side=tk.LEFT, anchor=tk.W)

tk.Button(master, text='生成媒体列表', width=label_width, command=list_videos).grid(row=13, column=1, pady=4, sticky=tk.W)

result_label = tk.Label(master, text="", width=entry_width)
result_label.grid(row=14, column=1, sticky=tk.W)

proxy_label = tk.Label(master, text="", width=entry_width)
proxy_label.grid(row=15, column=1, sticky=tk.W)

master.mainloop()
