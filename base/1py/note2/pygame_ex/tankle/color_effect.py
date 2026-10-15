import pygame # type:ignore



# 渐变的背景
# start_color: 顶部深蓝
# end_color: 底部橙红
def create_gradient_surface(width, height, start_color=(30, 50, 100), end_color=(240, 100, 50), direction="vertical"):
    """
    创建一个渐变色的 Surface (提前缓存，极大优化性能)
    :param width: 宽度 (Config.WIDTH)
    :param height: 高度 (Config.HEIGHT)
    :param start_color: 起始颜色 (R, G, B)
    :param end_color: 结束颜色 (R, G, B)
    :param direction: "vertical" (上下渐变) 或 "horizontal" (左右渐变)
    """
    # 1. 创建一个与屏幕同样大小的画布
    gradient_surf = pygame.Surface((width, height))
    
    if direction == "vertical":
        # 上下垂直渐变：遍历高度的每一行
        for y in range(height):
            # pct (比例) 从 0.0 渐变到 1.0
            pct = y / (height - 1) if height > 1 else 0
            
            # 计算当前行的红、绿、蓝通道值（线性插值公式）
            r = int(start_color[0] * (1 - pct) + end_color[0] * pct)
            g = int(start_color[1] * (1 - pct) + end_color[1] * pct)
            b = int(start_color[2] * (1 - pct) + end_color[2] * pct)
            
            # 画一条横线
            pygame.draw.line(gradient_surf, (r, g, b), (0, y), (width, y))
            
    elif direction == "horizontal":
        # 左右水平渐变：遍历宽度的每一列
        for x in range(width):
            pct = x / (width - 1) if width > 1 else 0
            r = int(start_color[0] * (1 - pct) + end_color[0] * pct)
            g = int(start_color[1] * (1 - pct) + end_color[1] * pct)
            b = int(start_color[2] * (1 - pct) + end_color[2] * pct)
            
            # 画一条竖线
            pygame.draw.line(gradient_surf, (r, g, b), (x, 0), (x, height))
            
    return gradient_surf
