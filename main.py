import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path


class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Rabito")
        self.root.geometry("800x600")

        # 支持的格式
        self.supported_formats = {
            'JPEG': ['.jpg', '.jpeg'],
            'PNG': ['.png'],
            'BMP': ['.bmp'],
            'GIF': ['.gif'],
            'TIFF': ['.tiff', '.tif'],
            'WEBP': ['.webp'],
            'ICO': ['.ico']
        }

        self.input_files = []
        self.output_dir = ""

        self.setup_ui()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 标题
        title_label = ttk.Label(main_frame, text="Rabito",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # 输入文件选择
        ttk.Label(main_frame, text="输入文件:").grid(row=1, column=0, sticky=tk.W, pady=5)

        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)

        ttk.Button(input_frame, text="选择文件",
                   command=self.select_input_files).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(input_frame, text="选择文件夹",
                   command=self.select_input_folder).grid(row=0, column=1, padx=(10, 0))

        # 文件列表
        self.file_listbox = tk.Listbox(main_frame, height=8)
        self.file_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical")
        scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S), pady=5)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)

        # 清空列表按钮
        ttk.Button(main_frame, text="清空列表",
                   command=self.clear_file_list).grid(row=3, column=0, sticky=tk.W, pady=5)

        # 输出目录选择
        ttk.Label(main_frame, text="输出目录:").grid(row=4, column=0, sticky=tk.W, pady=5)

        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)

        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var,
                  state="readonly").grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="浏览",
                   command=self.select_output_dir).grid(row=0, column=1, padx=(10, 0))

        # 输出格式选择
        ttk.Label(main_frame, text="输出格式:").grid(row=5, column=0, sticky=tk.W, pady=5)

        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.output_format = tk.StringVar(value="JPEG")
        format_combo = ttk.Combobox(format_frame, textvariable=self.output_format,
                                    values=list(self.supported_formats.keys()),
                                    state="readonly", width=15)
        format_combo.grid(row=0, column=0, sticky=tk.W)

        # 质量设置（仅对JPEG有效）
        ttk.Label(format_frame, text="质量:").grid(row=0, column=1, padx=(20, 5))
        self.quality_var = tk.IntVar(value=95)
        quality_scale = ttk.Scale(format_frame, from_=1, to=100,
                                  variable=self.quality_var, orient="horizontal", length=150)
        quality_scale.grid(row=0, column=2, padx=5)

        self.quality_label = ttk.Label(format_frame, text="95")
        self.quality_label.grid(row=0, column=3, padx=5)

        # 质量标签更新
        def update_quality_label(event):
            self.quality_label.config(text=str(int(self.quality_var.get())))

        quality_scale.bind("<Motion>", update_quality_label)
        quality_scale.bind("<ButtonRelease-1>", update_quality_label)

        # 转换选项
        options_frame = ttk.LabelFrame(main_frame, text="转换选项", padding="10")
        options_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.keep_original_size = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="保持原始尺寸",
                        variable=self.keep_original_size).grid(row=0, column=0, sticky=tk.W)

        self.overwrite_existing = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="覆盖已存在文件",
                        variable=self.overwrite_existing).grid(row=0, column=1, padx=(20, 0))

        # 尺寸调整选项
        size_frame = ttk.Frame(options_frame)
        size_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Label(size_frame, text="自定义尺寸:").grid(row=0, column=0, sticky=tk.W)

        ttk.Label(size_frame, text="宽度:").grid(row=0, column=1, padx=(20, 5))
        self.width_var = tk.StringVar()
        width_entry = ttk.Entry(size_frame, textvariable=self.width_var, width=8)
        width_entry.grid(row=0, column=2)

        ttk.Label(size_frame, text="高度:").grid(row=0, column=3, padx=(10, 5))
        self.height_var = tk.StringVar()
        height_entry = ttk.Entry(size_frame, textvariable=self.height_var, width=8)
        height_entry.grid(row=0, column=4)

        # 控制尺寸输入框的状态
        def toggle_size_inputs():
            state = "disabled" if self.keep_original_size.get() else "normal"
            width_entry.config(state=state)
            height_entry.config(state=state)

        self.keep_original_size.trace("w", lambda *args: toggle_size_inputs())
        toggle_size_inputs()

        # 转换按钮和进度条
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        control_frame.columnconfigure(1, weight=1)

        self.convert_button = ttk.Button(control_frame, text="开始转换",
                                         command=self.convert_images)
        self.convert_button.grid(row=0, column=0, sticky=tk.W)

        self.progress = ttk.Progressbar(control_frame, mode='determinate')
        self.progress.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))

        self.status_label = ttk.Label(control_frame, text="就绪")
        self.status_label.grid(row=0, column=2, sticky=tk.E)

        self.copyright = ttk.Label(main_frame, text="©2025 RabbitMax Rabito-图片格式转换器",
                                   font=("Arial", 8), foreground="gray")
        self.copyright.grid(row=8, column=0, columnspan=3, pady=(10, 0))

    def select_input_files(self):
        filetypes = [("所有支持的图片", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.tif;*.webp;*.ico"),
                     ("JPEG文件", "*.jpg;*.jpeg"),
                     ("PNG文件", "*.png"),
                     ("BMP文件", "*.bmp"),
                     ("GIF文件", "*.gif"),
                     ("TIFF文件", "*.tiff;*.tif"),
                     ("WEBP文件", "*.webp"),
                     ("ICO文件", "*.ico"),
                     ("所有文件", "*.*")]

        files = filedialog.askopenfilenames(title="选择图片文件", filetypes=filetypes)

        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="选择包含图片的文件夹")
        if folder:
            # 获取文件夹中所有支持的图片文件
            supported_extensions = []
            for exts in self.supported_formats.values():
                supported_extensions.extend(exts)

            for file_path in Path(folder).rglob("*"):
                if file_path.suffix.lower() in supported_extensions:
                    file_str = str(file_path)
                    if file_str not in self.input_files:
                        self.input_files.append(file_str)
                        self.file_listbox.insert(tk.END, file_path.name)

    def clear_file_list(self):
        self.input_files.clear()
        self.file_listbox.delete(0, tk.END)

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir = directory
            self.output_path_var.set(directory)

    def convert_images(self):
        if not self.input_files:
            messagebox.showwarning("警告", "请先选择输入文件！")
            return

        if not self.output_dir:
            messagebox.showwarning("警告", "请先选择输出目录！")
            return

        # 禁用转换按钮
        self.convert_button.config(state="disabled")

        # 设置进度条
        self.progress["maximum"] = len(self.input_files)
        self.progress["value"] = 0

        successful = 0
        failed = 0

        for i, input_file in enumerate(self.input_files):
            try:
                self.status_label.config(text=f"转换中: {os.path.basename(input_file)}")
                self.root.update()

                # 打开图片
                with Image.open(input_file) as img:
                    # 处理RGBA模式的图片
                    if img.mode == 'RGBA' and self.output_format.get() == 'JPEG':
                        # JPEG不支持透明度，转换为RGB
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background

                    # 尺寸调整
                    if not self.keep_original_size.get():
                        try:
                            width = int(self.width_var.get()) if self.width_var.get() else img.width
                            height = int(self.height_var.get()) if self.height_var.get() else img.height
                            img = img.resize((width, height), Image.Resampling.LANCZOS)
                        except ValueError:
                            pass  # 如果尺寸输入无效，保持原始尺寸

                    # 生成输出文件名
                    base_name = Path(input_file).stem
                    output_ext = self.supported_formats[self.output_format.get()][0]
                    output_file = os.path.join(self.output_dir, f"{base_name}{output_ext}")

                    # 检查文件是否存在
                    if os.path.exists(output_file) and not self.overwrite_existing.get():
                        counter = 1
                        while True:
                            new_name = f"{base_name}_{counter}{output_ext}"
                            output_file = os.path.join(self.output_dir, new_name)
                            if not os.path.exists(output_file):
                                break
                            counter += 1

                    # 保存图片
                    save_kwargs = {}
                    if self.output_format.get() == 'JPEG':
                        save_kwargs['quality'] = int(self.quality_var.get())
                        save_kwargs['optimize'] = True

                    img.save(output_file, **save_kwargs)
                    successful += 1

            except Exception as e:
                print(f"转换失败 {input_file}: {e}")
                failed += 1

            # 更新进度条
            self.progress["value"] = i + 1
            self.root.update()

        # 转换完成
        self.convert_button.config(state="normal")
        self.status_label.config(text="转换完成")

        # 显示结果
        messagebox.showinfo("转换完成",
                            f"转换完成！\n成功: {successful} 个文件\n失败: {failed} 个文件")


def main():
    root = tk.Tk()
    app = ImageConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
