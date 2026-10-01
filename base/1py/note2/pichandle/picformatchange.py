import os
from PIL import Image       # pip install pillow

def convert_image(input_path, output_format="WEBP", quality=80):
    """
    转换单张图片的格式
    :param input_path: 输入图片的路径
    :param output_format: 目标格式 (例如 'WEBP', 'JPEG', 'PNG')
    :param quality: 压缩质量 (1-100)，仅对 WebP 和 JPEG 有效
    """
    try:
        # 1. 打开图片
        with Image.open(input_path) as img:
            # 2. 获取不带后缀的文件名
            file_name, _ = os.path.splitext(input_path)
            # 3. 拼接新的输出路径
            output_path = f"{file_name}.{output_format.lower()}"
            
            # 4. 格式特殊处理：JPG不支持透明通道(RGBA)，如果原图是透明的，需要转为RGB
            if output_format.upper() in ["JPEG", "JPG"] and img.mode in ("RGBA", "LA"):
                # 创建一个白色背景的图片
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3]) # 3 是 alpha 通道
                img = background
            
            # 5. 保存并转换格式
            # Pillow 会根据 format 参数自动调用对应的编码器
            img.save(output_path, format=output_format.upper(), quality=quality)
            print(f" 成功转换: {input_path} -> {output_path}")
            
    except Exception as e:
        raise e
        print(f" 转换失败 [{input_path}]:{type(e).__name__ }:{str(e)}")

def batch_convert(folder_path, target_format="WEBP", quality=80):
    """
    批量转换文件夹内的所有图片
    """
    # 支持的常见源图片格式
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    
    if not os.path.exists(folder_path):
        print(" 文件夹路径不存在！")
        return

    print(f"\n正在开始批量转换，目标格式: {target_format}...")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(valid_extensions):
                full_path = os.path.join(root, file)
                convert_image(full_path, target_format, quality)
    print(" 批量转换完成！")

if __name__ == "__main__":
    print("=== Python 图片格式转换工具 ===")
    
    # 交互式输入
    path = input("请输入图片文件路径 或 文件夹路径: ").strip('"').strip() # strip(' " ') 去掉可能不小心复制进去的引号
    target_fmt = input("请输入目标格式 (例如 WEBP, JPG, PNG) [默认 WEBP]: ").strip().upper() or "WEBP"
    target_fmt = "JPEG" if target_fmt == "JPG" else target_fmt
    img_quality = input("请输入图片质量 (1-100) [默认 80]: ").strip()
    
    # 质量默认值处理
    img_quality = int(img_quality) if img_quality.isdigit() else 80

    # 判断是单张图片还是文件夹
    if os.path.isfile(path):
        convert_image(path, target_fmt, img_quality)
    elif os.path.isdir(path):
        batch_convert(path, target_fmt, img_quality)
    else:
        print(" 输入的路径无效，请检查！")
