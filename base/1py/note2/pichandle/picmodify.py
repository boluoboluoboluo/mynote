from PIL import Image   # pip install pillow

# 1. 查看图片信息
def view_image_info(image_path):
    with Image.open(image_path) as img:
        print(f"--- 图片信息 ---")
        print(f"格式 (Format): {img.format}")
        print(f"尺寸 (Size/分辨率): {img.size} (宽 x 高)")
        print(f"色彩模式 (Mode): {img.mode}")

# 2. 改变图片大小 (Resize)
def resize_image(image_path, output_path, new_size):
    with Image.open(image_path) as img:
        # new_size 为元组，例如 (800, 600)
        # Image.Resampling.LANCZOS 提供高质量的缩放效果
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        resized_img.save(output_path)
        print(f"图片大小已调整为: {new_size}")

# 3. 调整单个/区域像素 (Modify Pixels)
def modify_pixels(image_path, output_path):
    with Image.open(image_path) as img:
        # 将图片转换为可修改像素的载体
        pixel_map = img.load()
        
        # 示例：将左上角 50x50 区域的像素全部变成红色
        # 假设图片是 RGB 模式
        for x in range(50):
            for y in range(50):
                if img.mode == 'RGB':
                    pixel_map[x, y] = (255, 0, 0) # (红, 绿, 蓝)
                    
        img.save(output_path)
        print("指定区域的像素已调整。")

# 4. 图片旋转 (Rotate)
def rotate_image(image_path, output_path, angle):
    with Image.open(image_path) as img:
        # angle 为逆时针旋转的角度，expand=True 表示自动扩大画布以展示完整旋转后的图片
        rotated_img = img.rotate(angle, expand=True)
        rotated_img.save(output_path)
        print(f"图片已逆时针旋转 {angle} 度。")

# 5. 图片镜像/翻转 (Mirror/Flip)
def mirror_image(image_path, output_path, direction='horizontal'):
    with Image.open(image_path) as img:
        if direction == 'horizontal':
            # 水平镜像
            mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            # 垂直镜像
            mirrored_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            print("未知方向，请输入 'horizontal' 或 'vertical'")
            return
            
        mirrored_img.save(output_path)
        print(f"图片已完成 {direction} 镜像。")

# --- 使用示例 ---
if __name__ == "__main__":
    input_img = "example.jpg"  # 替换为你的图片路径
    
    # 请确保当前目录下有一张名为 example.jpg 的图片以供测试
    try:
        view_image_info(input_img)
        resize_image(input_img, "resized.jpg", (400, 300))
        modify_pixels(input_img, "pixel_modified.jpg")
        rotate_image(input_img, "rotated.jpg", 90)
        mirror_image(input_img, "mirrored.jpg", direction="horizontal")
    except FileNotFoundError:
        print(f"未找到测试图片 {input_img}，请检查路径。")
