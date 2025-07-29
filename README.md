# Rabito 📸

一个简洁高效的图片格式转换工具，支持多种常见图片格式之间的批量转换。

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ 特性

- 🎯 **多格式支持** - 支持 JPEG、PNG、BMP、GIF、TIFF、WEBP、ICO 等格式
- 📁 **批量转换** - 一次性转换多个文件或整个文件夹
- 🖼️ **尺寸调整** - 支持保持原始尺寸或自定义尺寸
- 🎚️ **质量控制** - JPEG 格式支持质量调节（1-100）
- 🔄 **智能命名** - 自动处理文件名冲突，避免覆盖
- 📊 **进度显示** - 实时显示转换进度和状态
- 🎨 **简洁界面** - 基于 tkinter/ttk 的简洁界面

## 🖥️ 界面预览

<details>
<summary>点击查看截图</summary>

![Rabito界面](screenshot.png)

</details>

## 🚀 快速开始

### 环境要求

- Python 3.6+
- Pillow (PIL)

### 安装依赖

```bash
pip install Pillow
```

## 🎯 使用方法

1. **添加文件** - 点击"选择文件"或"选择文件夹"添加要转换的图片
2. **选择输出** - 设置输出目录和目标格式
3. **调整设置** - 根据需要调整质量、尺寸等参数
4. **开始转换** - 点击"开始转换"，等待完成

## 🔧 支持的格式

| 输入格式 | 输出格式 | 说明 |
|---------|---------|------|
| JPEG | ✅ | 支持质量调节 | 当将包含透明度的 PNG 转换为 JPEG 时，程序会自动添加白色背景 |
| PNG | ✅ | 支持透明度 |
| BMP | ✅ | Windows 位图 |
| GIF | ✅ | 动画GIF |
| TIFF | ✅ | 高质量格式 |
| WEBP | ✅ | 现代Web格式 |
| ICO | ✅ | 图标格式 |

## 🛠️ 开发

### 项目结构
```
Rabito/
├── main.py          # 主程序文件
└── README.md       # 说明文档
```

### 贡献指南
欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)  
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Pillow (PIL)](https://pillow.readthedocs.io/) - 强大的图像处理库
- [Nuitka](https://nuitka.net/) - 优秀的Python编译器
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python标准GUI库

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: [3511528674@qq.com]
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Rabito/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个星标支持一下！**

Made with ❤️ by RabbitMax

</div>
