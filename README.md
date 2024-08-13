# Some tools for SimpRead.
## extract_base64_images
### Why
简悦提供的增强下载在Obsidian中保存格式为Base64编码，在编辑模式下阅读时占用篇幅过大，导致无法使用右侧进度条跳转。

本工具提供了自动将Base64编码图片转换为原始格式图片并保存的方法，可以有效解决上述问题。
### How to use
**本方法默认使用者有基础的Python程序调用能力**

修改input_folder和output_file，input_file为简悦文章导出的文件夹地址，output_file为图片存储的文件夹地址;

保存之后直接使用Python调用即可。
```
python extract_base64_images.py
```
