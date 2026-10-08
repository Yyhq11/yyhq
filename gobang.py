"""
优雅五子棋 — 双人对战 / 人机对战
使用 pygame 实现的五子棋游戏，左侧棋盘 + 右侧信息面板
"""

import pygame
import sys
import random
import time
import math

# ==================== 常量定义 ====================

BOARD_SIZE = 15                              # 棋盘行列数
WINDOW_WIDTH = 900                           # 窗口宽度
WINDOW_HEIGHT = 640                          # 窗口高度

# ========== 配色方案 ==========

# 背景 & 面板
COLOR_BG = (245, 240, 232)                   # 柔和暖白背景
COLOR_PANEL_BG = (250, 246, 240)             # 右侧面板底色（更白净）
COLOR_PANEL_BORDER = (200, 185, 155)         # 面板边框

# 棋盘
COLOR_BOARD_BASE = (228, 197, 123)           # 棋盘底色（柔和木色）
COLOR_BOARD_BASE_LIGHT = (238, 210, 140)     # 棋盘底色渐变浅色
COLOR_BOARD_BORDER_OUTER = (150, 115, 60)    # 棋盘外边框（深木色）
COLOR_BOARD_BORDER_INNER = (185, 140, 75)    # 棋盘内边框（中木色）
COLOR_GRID_LINE = (55, 50, 40)               # 网格线（暖黑）

# 文字
COLOR_TEXT_TITLE = (65, 50, 30)              # 标题文字
COLOR_TEXT_BODY = (85, 70, 45)               # 正文文字
COLOR_TEXT_LIGHT = (140, 120, 90)            # 浅色文字
COLOR_TEXT_ACCENT = (170, 95, 45)            # 强调文字（暖棕）
COLOR_GOLD = (220, 175, 55)                  # 金色（黑棋胜利用）

# 棋子
COLOR_BLACK = (30, 30, 30)
COLOR_WHITE = (242, 242, 242)

# 按钮
COLOR_BTN_RESTART = (130, 180, 125)           # 再来一局（柔和绿）
COLOR_BTN_RESTART_HOVER = (150, 205, 145)
COLOR_BTN_UNDO = (175, 145, 105)              # 悔棋（暖棕）
COLOR_BTN_UNDO_HOVER = (200, 165, 120)
COLOR_BTN_QUIT = (190, 105, 95)               # 退出（柔和红）
COLOR_BTN_QUIT_HOVER = (215, 125, 110)
COLOR_BTN_TEXT = (255, 255, 255)              # 按钮文字
COLOR_BTN_DISABLED = (185, 180, 170)          # 禁用态
COLOR_TOAST_BG = (90, 80, 60, 220)            # 提示背景
COLOR_TOAST_TEXT = (255, 245, 220)            # 提示文字

# ---- 内部绘制硬编码颜色的常量提取 ----
# 面板内部
COLOR_PANEL_SEPARATOR = (215, 205, 180)
COLOR_PANEL_BOX_BG = (240, 234, 222)
COLOR_FORBIDDEN_TEXT = (185, 55, 55)
COLOR_WIN_BLACK_TEXT = (40, 40, 40)
COLOR_WIN_WHITE_TEXT = (175, 90, 45)
COLOR_TURN_BLACK_TEXT = (35, 35, 35)
COLOR_TURN_WHITE_TEXT = (140, 95, 55)
COLOR_AI_THINKING = (170, 95, 45)
COLOR_AI_THINKING_DIM = (130, 75, 35)
# 模式选择/难度选择界面棋盘图标
COLOR_ICON_BOARD = (228, 197, 123, 180)
COLOR_ICON_BORDER = (150, 115, 60, 180)
COLOR_ICON_GRID = (55, 50, 40, 120)
COLOR_ICON_BLACK = (30, 30, 30, 200)
COLOR_ICON_WHITE = (242, 242, 242, 220)
# 胜利横幅
COLOR_BANNER_BLACK_BG = (22, 22, 22, 225)
COLOR_BANNER_BLACK_TEXT = (255, 220, 80)
COLOR_BANNER_BLACK_ACCENT = (255, 215, 70)
COLOR_BANNER_WHITE_BG = (255, 250, 238, 225)
COLOR_BANNER_WHITE_TEXT = (190, 65, 30)
# 最后一步/胜利连线标记
COLOR_LAST_MOVE = (220, 55, 35)
COLOR_WIN_LINE_BASE = (255, 200, 60)
COLOR_WIN_LINE_INNER = (255, 245, 140)
COLOR_WIN_LINE_GLOW = (255, 220, 80)
# 悬停预览
COLOR_HOVER_BLACK = (40, 40, 40)
COLOR_HOVER_WHITE = (220, 220, 220)
COLOR_HOVER_BLACK_ALPHA = 100
COLOR_HOVER_WHITE_ALPHA = 80
# 模式切换按钮
COLOR_BTN_MODE = (100, 145, 180)
COLOR_BTN_MODE_HOVER = (120, 170, 205)

# ---- 按钮（已在前面定义，这里确保顺序）----

# ==================== 主题系统 ====================

THEME_NAMES = ["classic", "dark", "eyecare", "cyberpunk", "minimal"]
THEME_LABELS = {
    "classic":   "经典木纹",
    "dark":      "暗黑围棋",
    "eyecare":   "护眼浅绿",
    "cyberpunk": "赛博朋克",
    "minimal":   "极简素白",
}
THEME_PREVIEW_COLORS = {
    "classic":   (228, 197, 123),
    "dark":      (55, 50, 45),
    "eyecare":   (195, 210, 180),
    "cyberpunk": (30, 20, 50),
    "minimal":   (235, 230, 225),
}

_current_theme = "classic"

# 全部5套主题配色字典
THEME_COLORS = {
    # ────────── 经典木纹（默认）──────────
    "classic": dict(
        COLOR_BG=(245, 240, 232),
        COLOR_PANEL_BG=(250, 246, 240),
        COLOR_PANEL_BORDER=(200, 185, 155),
        COLOR_BOARD_BASE=(228, 197, 123),
        COLOR_BOARD_BASE_LIGHT=(238, 210, 140),
        COLOR_BOARD_BORDER_OUTER=(150, 115, 60),
        COLOR_BOARD_BORDER_INNER=(185, 140, 75),
        COLOR_GRID_LINE=(55, 50, 40),
        COLOR_TEXT_TITLE=(65, 50, 30),
        COLOR_TEXT_BODY=(85, 70, 45),
        COLOR_TEXT_LIGHT=(140, 120, 90),
        COLOR_TEXT_ACCENT=(170, 95, 45),
        COLOR_GOLD=(220, 175, 55),
        COLOR_BLACK=(30, 30, 30),
        COLOR_WHITE=(242, 242, 242),
        COLOR_BTN_RESTART=(130, 180, 125),
        COLOR_BTN_RESTART_HOVER=(150, 205, 145),
        COLOR_BTN_UNDO=(175, 145, 105),
        COLOR_BTN_UNDO_HOVER=(200, 165, 120),
        COLOR_BTN_QUIT=(190, 105, 95),
        COLOR_BTN_QUIT_HOVER=(215, 125, 110),
        COLOR_BTN_TEXT=(255, 255, 255),
        COLOR_BTN_DISABLED=(185, 180, 170),
        COLOR_TOAST_BG=(90, 80, 60, 220),
        COLOR_TOAST_TEXT=(255, 245, 220),
        COLOR_PANEL_SEPARATOR=(215, 205, 180),
        COLOR_PANEL_BOX_BG=(240, 234, 222),
        COLOR_FORBIDDEN_TEXT=(185, 55, 55),
        COLOR_WIN_BLACK_TEXT=(40, 40, 40),
        COLOR_WIN_WHITE_TEXT=(175, 90, 45),
        COLOR_TURN_BLACK_TEXT=(35, 35, 35),
        COLOR_TURN_WHITE_TEXT=(140, 95, 55),
        COLOR_AI_THINKING=(170, 95, 45),
        COLOR_AI_THINKING_DIM=(130, 75, 35),
        COLOR_ICON_BOARD=(228, 197, 123, 180),
        COLOR_ICON_BORDER=(150, 115, 60, 180),
        COLOR_ICON_GRID=(55, 50, 40, 120),
        COLOR_ICON_BLACK=(30, 30, 30, 200),
        COLOR_ICON_WHITE=(242, 242, 242, 220),
        COLOR_BANNER_BLACK_BG=(22, 22, 22, 225),
        COLOR_BANNER_BLACK_TEXT=(255, 220, 80),
        COLOR_BANNER_BLACK_ACCENT=(255, 215, 70),
        COLOR_BANNER_WHITE_BG=(255, 250, 238, 225),
        COLOR_BANNER_WHITE_TEXT=(190, 65, 30),
        COLOR_LAST_MOVE=(220, 55, 35),
        COLOR_WIN_LINE_BASE=(255, 200, 60),
        COLOR_WIN_LINE_INNER=(255, 245, 140),
        COLOR_WIN_LINE_GLOW=(255, 220, 80),
        COLOR_HOVER_BLACK=(40, 40, 40),
        COLOR_HOVER_WHITE=(220, 220, 220),
        COLOR_HOVER_BLACK_ALPHA=100,
        COLOR_HOVER_WHITE_ALPHA=80,
        COLOR_BTN_MODE=(100, 145, 180),
        COLOR_BTN_MODE_HOVER=(120, 170, 205),
    ),
    # ────────── 暗黑围棋 ──────────
    "dark": dict(
        COLOR_BG=(35, 35, 40),
        COLOR_PANEL_BG=(45, 45, 50),
        COLOR_PANEL_BORDER=(80, 80, 90),
        COLOR_BOARD_BASE=(55, 50, 45),
        COLOR_BOARD_BASE_LIGHT=(65, 60, 55),
        COLOR_BOARD_BORDER_OUTER=(40, 38, 35),
        COLOR_BOARD_BORDER_INNER=(70, 65, 60),
        COLOR_GRID_LINE=(120, 115, 110),
        COLOR_TEXT_TITLE=(220, 215, 200),
        COLOR_TEXT_BODY=(200, 195, 180),
        COLOR_TEXT_LIGHT=(150, 145, 135),
        COLOR_TEXT_ACCENT=(255, 200, 120),
        COLOR_GOLD=(255, 200, 60),
        COLOR_BLACK=(18, 18, 20),
        COLOR_WHITE=(238, 240, 245),
        COLOR_BTN_RESTART=(80, 120, 90),
        COLOR_BTN_RESTART_HOVER=(100, 145, 110),
        COLOR_BTN_UNDO=(120, 100, 80),
        COLOR_BTN_UNDO_HOVER=(145, 120, 95),
        COLOR_BTN_QUIT=(145, 80, 75),
        COLOR_BTN_QUIT_HOVER=(170, 100, 90),
        COLOR_BTN_TEXT=(230, 225, 215),
        COLOR_BTN_DISABLED=(90, 90, 95),
        COLOR_TOAST_BG=(60, 60, 65, 230),
        COLOR_TOAST_TEXT=(230, 225, 210),
        COLOR_PANEL_SEPARATOR=(100, 100, 105),
        COLOR_PANEL_BOX_BG=(60, 60, 65),
        COLOR_FORBIDDEN_TEXT=(255, 100, 90),
        COLOR_WIN_BLACK_TEXT=(220, 215, 200),
        COLOR_WIN_WHITE_TEXT=(255, 200, 120),
        COLOR_TURN_BLACK_TEXT=(210, 205, 195),
        COLOR_TURN_WHITE_TEXT=(240, 220, 160),
        COLOR_AI_THINKING=(255, 200, 120),
        COLOR_AI_THINKING_DIM=(200, 150, 80),
        COLOR_ICON_BOARD=(55, 50, 45, 180),
        COLOR_ICON_BORDER=(40, 38, 35, 180),
        COLOR_ICON_GRID=(120, 115, 110, 120),
        COLOR_ICON_BLACK=(18, 18, 20, 200),
        COLOR_ICON_WHITE=(238, 240, 245, 220),
        COLOR_BANNER_BLACK_BG=(15, 15, 18, 240),
        COLOR_BANNER_BLACK_TEXT=(255, 200, 60),
        COLOR_BANNER_BLACK_ACCENT=(255, 220, 80),
        COLOR_BANNER_WHITE_BG=(35, 35, 40, 240),
        COLOR_BANNER_WHITE_TEXT=(255, 200, 120),
        COLOR_LAST_MOVE=(255, 130, 60),
        COLOR_WIN_LINE_BASE=(255, 200, 60),
        COLOR_WIN_LINE_INNER=(255, 245, 140),
        COLOR_WIN_LINE_GLOW=(255, 180, 50),
        COLOR_HOVER_BLACK=(60, 60, 65),
        COLOR_HOVER_WHITE=(200, 200, 210),
        COLOR_HOVER_BLACK_ALPHA=140,
        COLOR_HOVER_WHITE_ALPHA=120,
        COLOR_BTN_MODE=(60, 100, 120),
        COLOR_BTN_MODE_HOVER=(80, 125, 150),
    ),
    # ────────── 护眼浅绿 ──────────
    "eyecare": dict(
        COLOR_BG=(225, 235, 220),
        COLOR_PANEL_BG=(235, 242, 230),
        COLOR_PANEL_BORDER=(170, 190, 160),
        COLOR_BOARD_BASE=(195, 210, 180),
        COLOR_BOARD_BASE_LIGHT=(205, 220, 190),
        COLOR_BOARD_BORDER_OUTER=(120, 140, 110),
        COLOR_BOARD_BORDER_INNER=(150, 170, 140),
        COLOR_GRID_LINE=(80, 90, 75),
        COLOR_TEXT_TITLE=(60, 75, 50),
        COLOR_TEXT_BODY=(75, 90, 65),
        COLOR_TEXT_LIGHT=(120, 140, 110),
        COLOR_TEXT_ACCENT=(90, 120, 55),
        COLOR_GOLD=(175, 190, 90),
        COLOR_BLACK=(35, 40, 32),
        COLOR_WHITE=(245, 248, 240),
        COLOR_BTN_RESTART=(140, 180, 125),
        COLOR_BTN_RESTART_HOVER=(160, 205, 145),
        COLOR_BTN_UNDO=(160, 155, 120),
        COLOR_BTN_UNDO_HOVER=(185, 175, 140),
        COLOR_BTN_QUIT=(185, 125, 115),
        COLOR_BTN_QUIT_HOVER=(210, 145, 130),
        COLOR_BTN_TEXT=(255, 255, 250),
        COLOR_BTN_DISABLED=(200, 205, 195),
        COLOR_TOAST_BG=(80, 95, 65, 220),
        COLOR_TOAST_TEXT=(245, 250, 240),
        COLOR_PANEL_SEPARATOR=(190, 205, 180),
        COLOR_PANEL_BOX_BG=(240, 245, 235),
        COLOR_FORBIDDEN_TEXT=(195, 70, 60),
        COLOR_WIN_BLACK_TEXT=(45, 55, 40),
        COLOR_WIN_WHITE_TEXT=(95, 125, 65),
        COLOR_TURN_BLACK_TEXT=(40, 48, 35),
        COLOR_TURN_WHITE_TEXT=(100, 130, 70),
        COLOR_AI_THINKING=(90, 120, 55),
        COLOR_AI_THINKING_DIM=(70, 95, 42),
        COLOR_ICON_BOARD=(195, 210, 180, 180),
        COLOR_ICON_BORDER=(150, 170, 140, 180),
        COLOR_ICON_GRID=(80, 90, 75, 120),
        COLOR_ICON_BLACK=(35, 40, 32, 200),
        COLOR_ICON_WHITE=(245, 248, 240, 220),
        COLOR_BANNER_BLACK_BG=(40, 50, 35, 230),
        COLOR_BANNER_BLACK_TEXT=(240, 245, 160),
        COLOR_BANNER_BLACK_ACCENT=(220, 230, 140),
        COLOR_BANNER_WHITE_BG=(250, 252, 245, 230),
        COLOR_BANNER_WHITE_TEXT=(95, 125, 65),
        COLOR_LAST_MOVE=(210, 75, 55),
        COLOR_WIN_LINE_BASE=(220, 210, 80),
        COLOR_WIN_LINE_INNER=(255, 250, 160),
        COLOR_WIN_LINE_GLOW=(230, 220, 100),
        COLOR_HOVER_BLACK=(45, 55, 40),
        COLOR_HOVER_WHITE=(210, 220, 200),
        COLOR_HOVER_BLACK_ALPHA=100,
        COLOR_HOVER_WHITE_ALPHA=80,
        COLOR_BTN_MODE=(120, 160, 110),
        COLOR_BTN_MODE_HOVER=(140, 185, 130),
    ),
    # ────────── 赛博朋克 ──────────
    "cyberpunk": dict(
        COLOR_BG=(15, 10, 25),
        COLOR_PANEL_BG=(25, 18, 40),
        COLOR_PANEL_BORDER=(80, 30, 100),
        COLOR_BOARD_BASE=(30, 20, 50),
        COLOR_BOARD_BASE_LIGHT=(40, 28, 60),
        COLOR_BOARD_BORDER_OUTER=(50, 10, 70),
        COLOR_BOARD_BORDER_INNER=(80, 30, 100),
        COLOR_GRID_LINE=(0, 220, 220),
        COLOR_TEXT_TITLE=(0, 255, 200),
        COLOR_TEXT_BODY=(220, 200, 255),
        COLOR_TEXT_LIGHT=(150, 120, 200),
        COLOR_TEXT_ACCENT=(255, 60, 150),
        COLOR_GOLD=(255, 215, 0),
        COLOR_BLACK=(255, 50, 120),
        COLOR_WHITE=(0, 255, 255),
        COLOR_BTN_RESTART=(80, 20, 120),
        COLOR_BTN_RESTART_HOVER=(110, 40, 150),
        COLOR_BTN_UNDO=(100, 30, 80),
        COLOR_BTN_UNDO_HOVER=(130, 50, 110),
        COLOR_BTN_QUIT=(180, 20, 80),
        COLOR_BTN_QUIT_HOVER=(220, 40, 100),
        COLOR_BTN_TEXT=(0, 255, 200),
        COLOR_BTN_DISABLED=(60, 40, 70),
        COLOR_TOAST_BG=(40, 10, 60, 220),
        COLOR_TOAST_TEXT=(0, 255, 220),
        COLOR_PANEL_SEPARATOR=(70, 25, 90),
        COLOR_PANEL_BOX_BG=(35, 25, 55),
        COLOR_FORBIDDEN_TEXT=(255, 100, 80),
        COLOR_WIN_BLACK_TEXT=(255, 60, 150),
        COLOR_WIN_WHITE_TEXT=(0, 255, 220),
        COLOR_TURN_BLACK_TEXT=(255, 60, 150),
        COLOR_TURN_WHITE_TEXT=(0, 255, 220),
        COLOR_AI_THINKING=(255, 60, 150),
        COLOR_AI_THINKING_DIM=(200, 40, 110),
        COLOR_ICON_BOARD=(30, 20, 50, 180),
        COLOR_ICON_BORDER=(80, 30, 100, 180),
        COLOR_ICON_GRID=(0, 220, 220, 120),
        COLOR_ICON_BLACK=(255, 50, 120, 200),
        COLOR_ICON_WHITE=(0, 255, 255, 220),
        COLOR_BANNER_BLACK_BG=(10, 5, 20, 240),
        COLOR_BANNER_BLACK_TEXT=(255, 60, 150),
        COLOR_BANNER_BLACK_ACCENT=(255, 30, 130),
        COLOR_BANNER_WHITE_BG=(20, 15, 35, 240),
        COLOR_BANNER_WHITE_TEXT=(0, 255, 220),
        COLOR_LAST_MOVE=(255, 215, 0),
        COLOR_WIN_LINE_BASE=(255, 60, 150),
        COLOR_WIN_LINE_INNER=(255, 150, 200),
        COLOR_WIN_LINE_GLOW=(255, 30, 130),
        COLOR_HOVER_BLACK=(255, 60, 150),
        COLOR_HOVER_WHITE=(0, 255, 220),
        COLOR_HOVER_BLACK_ALPHA=140,
        COLOR_HOVER_WHITE_ALPHA=100,
        COLOR_BTN_MODE=(120, 20, 150),
        COLOR_BTN_MODE_HOVER=(150, 40, 180),
    ),
    # ────────── 极简素白 ──────────
    "minimal": dict(
        COLOR_BG=(248, 245, 240),
        COLOR_PANEL_BG=(255, 252, 248),
        COLOR_PANEL_BORDER=(210, 205, 195),
        COLOR_BOARD_BASE=(235, 230, 225),
        COLOR_BOARD_BASE_LIGHT=(242, 238, 233),
        COLOR_BOARD_BORDER_OUTER=(170, 160, 150),
        COLOR_BOARD_BORDER_INNER=(195, 188, 178),
        COLOR_GRID_LINE=(155, 150, 142),
        COLOR_TEXT_TITLE=(55, 50, 45),
        COLOR_TEXT_BODY=(75, 70, 65),
        COLOR_TEXT_LIGHT=(150, 145, 140),
        COLOR_TEXT_ACCENT=(120, 90, 60),
        COLOR_GOLD=(190, 160, 80),
        COLOR_BLACK=(25, 25, 25),
        COLOR_WHITE=(250, 250, 250),
        COLOR_BTN_RESTART=(155, 155, 150),
        COLOR_BTN_RESTART_HOVER=(175, 175, 170),
        COLOR_BTN_UNDO=(170, 162, 148),
        COLOR_BTN_UNDO_HOVER=(195, 185, 170),
        COLOR_BTN_QUIT=(185, 140, 135),
        COLOR_BTN_QUIT_HOVER=(210, 160, 150),
        COLOR_BTN_TEXT=(255, 255, 255),
        COLOR_BTN_DISABLED=(220, 218, 212),
        COLOR_TOAST_BG=(90, 85, 78, 220),
        COLOR_TOAST_TEXT=(255, 252, 245),
        COLOR_PANEL_SEPARATOR=(225, 220, 210),
        COLOR_PANEL_BOX_BG=(248, 245, 238),
        COLOR_FORBIDDEN_TEXT=(195, 65, 55),
        COLOR_WIN_BLACK_TEXT=(40, 40, 40),
        COLOR_WIN_WHITE_TEXT=(130, 100, 70),
        COLOR_TURN_BLACK_TEXT=(35, 35, 35),
        COLOR_TURN_WHITE_TEXT=(120, 100, 70),
        COLOR_AI_THINKING=(120, 90, 60),
        COLOR_AI_THINKING_DIM=(95, 70, 45),
        COLOR_ICON_BOARD=(235, 230, 225, 180),
        COLOR_ICON_BORDER=(170, 160, 150, 180),
        COLOR_ICON_GRID=(155, 150, 142, 120),
        COLOR_ICON_BLACK=(25, 25, 25, 200),
        COLOR_ICON_WHITE=(250, 250, 250, 220),
        COLOR_BANNER_BLACK_BG=(25, 25, 25, 225),
        COLOR_BANNER_BLACK_TEXT=(255, 220, 80),
        COLOR_BANNER_BLACK_ACCENT=(255, 215, 70),
        COLOR_BANNER_WHITE_BG=(252, 250, 242, 225),
        COLOR_BANNER_WHITE_TEXT=(120, 90, 60),
        COLOR_LAST_MOVE=(195, 65, 45),
        COLOR_WIN_LINE_BASE=(200, 170, 60),
        COLOR_WIN_LINE_INNER=(240, 220, 110),
        COLOR_WIN_LINE_GLOW=(210, 180, 70),
        COLOR_HOVER_BLACK=(55, 55, 55),
        COLOR_HOVER_WHITE=(210, 210, 210),
        COLOR_HOVER_BLACK_ALPHA=90,
        COLOR_HOVER_WHITE_ALPHA=70,
        COLOR_BTN_MODE=(140, 140, 135),
        COLOR_BTN_MODE_HOVER=(160, 160, 155),
    ),
}


def get_current_theme():
    """返回当前选中的主题名称"""
    return _current_theme


def apply_theme(theme_name):
    """将指定主题的颜色应用到全局 COLOR_XXX 常量"""
    global _current_theme
    if theme_name not in THEME_COLORS:
        return False
    _current_theme = theme_name
    theme = THEME_COLORS[theme_name]
    for key, value in theme.items():
        globals()[key] = value
    # 清除棋子缓存（不同主题的石材渲染可能不同）
    _stone_cache.clear()
    return True

# ==================== 布局参数 ====================

BOARD_AREA_LEFT = 20
BOARD_AREA_TOP = 20
BOARD_PADDING = 28
CELL_SIZE = 34
STONE_RADIUS = CELL_SIZE // 2 - 2

BOARD_LINES_WIDTH = (BOARD_SIZE - 1) * CELL_SIZE    # 476
BOARD_LINES_HEIGHT = (BOARD_SIZE - 1) * CELL_SIZE   # 476
BOARD_BASE_WIDTH = BOARD_LINES_WIDTH + BOARD_PADDING * 2
BOARD_BASE_HEIGHT = BOARD_LINES_HEIGHT + BOARD_PADDING * 2
BORDER_WIDTH = 6
BOARD_TOTAL_WIDTH = BOARD_BASE_WIDTH + BORDER_WIDTH * 2
BOARD_TOTAL_HEIGHT = BOARD_BASE_HEIGHT + BORDER_WIDTH * 2

BOARD_ORIGIN_X = BOARD_AREA_LEFT + BORDER_WIDTH + BOARD_PADDING
BOARD_ORIGIN_Y = BOARD_AREA_TOP + BORDER_WIDTH + BOARD_PADDING
BOARD_BASE_X = BOARD_AREA_LEFT + BORDER_WIDTH
BOARD_BASE_Y = BOARD_AREA_TOP + BORDER_WIDTH
BOARD_BORDER_X = BOARD_AREA_LEFT
BOARD_BORDER_Y = BOARD_AREA_TOP

# 右侧面板
PANEL_LEFT = BOARD_BORDER_X + BOARD_TOTAL_WIDTH + 30
PANEL_TOP = 30
PANEL_WIDTH = WINDOW_WIDTH - PANEL_LEFT - 20
PANEL_HEIGHT = WINDOW_HEIGHT - 60

# 按钮区域
BTN_WIDTH = PANEL_WIDTH - 56
BTN_HEIGHT = 28
BTN_GAP = 5
BTN_LEFT = PANEL_LEFT + 28
BTN_BOX_PAD_Y = 6

# 限时模式
TIME_LIMIT_SECONDS = 30.0                    # 每方初始时间（秒）


# ==================== 初始化 ====================

def init_game():
    """初始化 pygame 和游戏窗口"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("优雅五子棋")
    return screen


# ==================== 棋盘绘制 ====================

def draw_board(screen):
    """绘制完整棋盘：渐变底色 → 外框 → 内框 → 网格 → 星位"""
    screen.fill(COLOR_BG)

    # 右侧面板底色 + 边框
    panel_rect = pygame.Rect(PANEL_LEFT, PANEL_TOP, PANEL_WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(screen, COLOR_PANEL_BG, panel_rect, border_radius=12)
    pygame.draw.rect(screen, COLOR_PANEL_BORDER, panel_rect, 2, border_radius=12)

    # 棋盘外边框
    outer = pygame.Rect(BOARD_BORDER_X, BOARD_BORDER_Y, BOARD_TOTAL_WIDTH, BOARD_TOTAL_HEIGHT)
    pygame.draw.rect(screen, COLOR_BOARD_BORDER_OUTER, outer, border_radius=5)

    # 棋盘内边框
    inner = pygame.Rect(BOARD_BORDER_X + 3, BOARD_BORDER_Y + 3,
                        BOARD_TOTAL_WIDTH - 6, BOARD_TOTAL_HEIGHT - 6)
    pygame.draw.rect(screen, COLOR_BOARD_BORDER_INNER, inner, border_radius=4)

    # 棋盘底色（带微弱渐变）
    base = pygame.Rect(BOARD_BASE_X, BOARD_BASE_Y, BOARD_BASE_WIDTH, BOARD_BASE_HEIGHT)
    base_surf = pygame.Surface((BOARD_BASE_WIDTH, BOARD_BASE_HEIGHT), pygame.SRCALPHA)
    for y in range(BOARD_BASE_HEIGHT):
        t = y / BOARD_BASE_HEIGHT
        r = int(COLOR_BOARD_BASE[0] + (COLOR_BOARD_BASE_LIGHT[0] - COLOR_BOARD_BASE[0]) * t)
        g = int(COLOR_BOARD_BASE[1] + (COLOR_BOARD_BASE_LIGHT[1] - COLOR_BOARD_BASE[1]) * t)
        b = int(COLOR_BOARD_BASE[2] + (COLOR_BOARD_BASE_LIGHT[2] - COLOR_BOARD_BASE[2]) * t)
        pygame.draw.line(base_surf, (r, g, b), (0, y), (BOARD_BASE_WIDTH, y))
    screen.blit(base_surf, (BOARD_BASE_X, BOARD_BASE_Y))

    # 网格线
    for i in range(BOARD_SIZE):
        y = BOARD_ORIGIN_Y + i * CELL_SIZE
        pygame.draw.line(screen, COLOR_GRID_LINE,
                         (BOARD_ORIGIN_X, y),
                         (BOARD_ORIGIN_X + BOARD_LINES_WIDTH, y), 1)
        x = BOARD_ORIGIN_X + i * CELL_SIZE
        pygame.draw.line(screen, COLOR_GRID_LINE,
                         (x, BOARD_ORIGIN_Y),
                         (x, BOARD_ORIGIN_Y + BOARD_LINES_HEIGHT), 1)

    # 星位标记（柔和小圆点）
    stars = [(3, 3), (3, 7), (3, 11),
             (7, 3), (7, 7), (7, 11),
             (11, 3), (11, 7), (11, 11)]
    for col, row in stars:
        cx = BOARD_ORIGIN_X + col * CELL_SIZE
        cy = BOARD_ORIGIN_Y + row * CELL_SIZE
        pygame.draw.circle(screen, COLOR_GRID_LINE, (cx, cy), 4, 1)
        pygame.draw.circle(screen, COLOR_GRID_LINE, (cx, cy), 2)


# ==================== 棋子绘制 ====================

def _create_stone_surface(r, color):
    """预渲染一颗棋子表面（阴影 + 径向渐变球体 + 高光），返回 surface 和绘制偏移"""
    shadow_offset = 3
    total_size = r * 2 + shadow_offset * 2 + 2

    surf = pygame.Surface((total_size, total_size), pygame.SRCALPHA)

    # --- 阴影（椭圆形，模拟立体投影）---
    shadow_sy = r + shadow_offset + 1
    shadow_ellipse = pygame.Surface((r * 2 + 2, r + 4), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_ellipse, (0, 0, 0, 45), shadow_ellipse.get_rect())
    surf.blit(shadow_ellipse, (shadow_offset - 1, r + shadow_offset))

    # --- 球体主体（径向渐变）---
    stone_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)

    if color == 'black':
        # 黑棋：左上光源，深灰到纯黑
        for dy in range(r * 2):
            for dx in range(r * 2):
                dist = math.hypot(dx - r, dy - r)
                if dist <= r:
                    nx, ny = (dx - r) / r, (dy - r) / r
                    # 光源从左上角照射，角度影响 + 径向暗角
                    light_angle = max(0, (-nx - ny) / 2)
                    radial = 1 - (dist / r) * 0.15
                    brightness = (0.35 + 0.65 * light_angle) * radial
                    val = int(25 + 115 * brightness)
                    val = max(15, min(255, val))
                    stone_surf.set_at((dx, dy), (val, val, val, 255))

        # 主高光
        hl_x, hl_y = r - r // 3, r - r // 3
        pygame.draw.circle(stone_surf, (170, 170, 170, 160), (hl_x, hl_y), r // 3)
        pygame.draw.circle(stone_surf, (220, 220, 220, 120), (hl_x - 1, hl_y - 1), r // 5)

    else:
        # 白棋：左上光源，浅灰到纯白
        for dy in range(r * 2):
            for dx in range(r * 2):
                dist = math.hypot(dx - r, dy - r)
                if dist <= r:
                    nx, ny = (dx - r) / r, (dy - r) / r
                    light_angle = max(0, (-nx - ny) / 2)
                    radial = 1 - (dist / r) * 0.12
                    brightness = (0.65 + 0.35 * light_angle) * radial
                    val = int(195 + 60 * brightness)
                    val = max(160, min(255, val))
                    stone_surf.set_at((dx, dy), (val, val, val, 255))

        # 主高光
        hl_x, hl_y = r - r // 3, r - r // 3
        pygame.draw.circle(stone_surf, (255, 255, 255, 200), (hl_x, hl_y), r // 3)
        pygame.draw.circle(stone_surf, (255, 255, 255, 140), (hl_x - 1, hl_y - 1), r // 5)

    surf.blit(stone_surf, (shadow_offset, shadow_offset))
    return surf, shadow_offset


# 预渲染棋子缓存
_stone_cache = {}
def _get_stone_surface(r, color):
    key = (r, color)
    if key not in _stone_cache:
        _stone_cache[key] = _create_stone_surface(r, color)
    return _stone_cache[key]


def draw_stone(screen, row, col, color):
    """绘制完整球形棋子（阴影 + 径向渐变球体 + 高光）"""
    cx = BOARD_ORIGIN_X + col * CELL_SIZE
    cy = BOARD_ORIGIN_Y + row * CELL_SIZE
    r = STONE_RADIUS

    surf, offset = _get_stone_surface(r, color)
    screen.blit(surf, (cx - r - offset, cy - r - offset))


# ==================== 交互辅助 ====================

def get_board_pos(mouse_x, mouse_y):
    """将鼠标坐标转为最近交叉点的 (row, col)，超出范围返回 None"""
    col = round((mouse_x - BOARD_ORIGIN_X) / CELL_SIZE)
    row = round((mouse_y - BOARD_ORIGIN_Y) / CELL_SIZE)
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        cx = BOARD_ORIGIN_X + col * CELL_SIZE
        cy = BOARD_ORIGIN_Y + row * CELL_SIZE
        if math.hypot(mouse_x - cx, mouse_y - cy) <= STONE_RADIUS:
            return row, col
    return None


# ==================== 胜负判断 ====================

def check_win(board, row, col, player):
    """检查 (row, col) 处 player 是否五子连珠，返回 (是否获胜, 连线两端坐标)。
    win_line 格式: (start_row, start_col, end_row, end_col)，失败时为 None。
    """
    for dr, dc in [(0, 1), (1, 0), (1, -1), (1, 1)]:
        # 正向延伸（记录最远端点）
        fr, fc = row, col
        cnt = 1
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            cnt += 1
            fr, fc = r, c
            r += dr; c += dc
        # 反向延伸（记录最远端点）
        br, bc = row, col
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            cnt += 1
            br, bc = r, c
            r -= dr; c -= dc
        if cnt >= 5:
            return True, (br, bc, fr, fc)
    return False, None


# ==================== AI 逻辑 ====================

# 方向向量：水平、垂直、主对角线、副对角线
AI_DIRS = [(0, 1), (1, 0), (1, -1), (1, 1)]

# AI 难度等级
AI_DIFFICULTY_LABELS = {
    'easy':   "简单",
    'medium': "中等",
    'hard':   "困难",
}
AI_DIFFICULTY_DESCRIPTIONS = {
    'easy':   "新手友好",
    'medium': "势均力敌",
    'hard':   "棋逢对手",
}


def _count_line(board, r, c, dr, dc, player):
    """统计从 (r,c) 沿 (dr,dc) 方向连续 player 棋子的数量（不含起点）"""
    cnt = 0
    nr, nc = r + dr, c + dc
    while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
        cnt += 1
        nr += dr
        nc += dc
    return cnt


def _count_open(board, r, c, dr, dc):
    """检查 (r,c) 沿 (dr,dc) 方向端点的空位数"""
    nr, nc = r + dr, c + dc
    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] is None:
        return 1
    return 0


def _evaluate_position(board, r, c, player):
    """评估在 (r,c) 落子对于 player 的价值（进攻分），以及堵截对手的价值（防守分）"""
    opponent = 'white' if player == 'black' else 'black'
    attack_score = 0
    defense_score = 0

    for dr, dc in AI_DIRS:
        # player 方向
        p_cnt = 1 + _count_line(board, r, c, dr, dc, player) + _count_line(board, r, c, -dr, -dc, player)
        p_open = _count_open(board, r + dr * _count_line(board, r, c, dr, dc, player),
                              c + dc * _count_line(board, r, c, dr, dc, player), dr, dc) + \
                 _count_open(board, r - dr * _count_line(board, r, c, -dr, -dc, player),
                              c - dc * _count_line(board, r, c, -dr, -dc, player), -dr, -dc)
        attack_score += _score_line(p_cnt, p_open)

        # opponent 方向（防守：模拟对手在此落子）
        o_cnt = 1 + _count_line(board, r, c, dr, dc, opponent) + _count_line(board, r, c, -dr, -dc, opponent)
        o_open = _count_open(board, r + dr * _count_line(board, r, c, dr, dc, opponent),
                              c + dc * _count_line(board, r, c, dr, dc, opponent), dr, dc) + \
                 _count_open(board, r - dr * _count_line(board, r, c, -dr, -dc, opponent),
                              c - dc * _count_line(board, r, c, -dr, -dc, opponent), -dr, -dc)
        defense_score += _score_line(o_cnt, o_open)

    return attack_score, defense_score


def _score_line(count, open_ends):
    """根据连子数和开放端数打分"""
    if count >= 5:
        return 100000
    if count == 4:
        if open_ends == 2:
            return 50000    # 活四
        elif open_ends == 1:
            return 5000     # 冲四
        return 0
    if count == 3:
        if open_ends == 2:
            return 3000     # 活三
        elif open_ends == 1:
            return 500      # 眠三
        return 0
    if count == 2:
        if open_ends == 2:
            return 200      # 活二
        elif open_ends == 1:
            return 50       # 眠二
        return 0
    if count == 1:
        if open_ends == 2:
            return 10       # 活一
        elif open_ends == 1:
            return 3        # 眠一
        return 0
    return 0


def _get_candidate_moves(board):
    """获取候选落子位置（已有棋子周围2格范围内的空位）"""
    candidates = set()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] is not None:
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] is None:
                            candidates.add((nr, nc))
    if not candidates:
        # 棋盘为空，下天元
        candidates.add((BOARD_SIZE // 2, BOARD_SIZE // 2))
    return candidates


def _filter_forbidden_moves(board, candidates, player):
    """过滤 AI 候选落子中的禁手点。白棋无限制，黑棋须主动避开禁手。"""
    if player != 'black':
        return candidates

    safe = []
    for r, c in candidates:
        board[r][c] = 'black'
        # 五连优先于禁手：能赢就不算禁手
        is_win, _ = check_win(board, r, c, 'black')
        if is_win:
            safe.append((r, c))
        else:
            forbidden = detect_forbidden(board, r, c)
            if forbidden is None:
                safe.append((r, c))
        board[r][c] = None

    # 极端情况：所有候选都是禁手点，回退到原始列表
    if not safe:
        return candidates
    return safe


# ==================== AI 难度级别 ====================

def ai_move_easy(board, ai_color):
    """
    简单 AI：仅当对手即将成四（冲四/活四）时堵截，其余随机落子。
    适合新手练手。
    """
    candidates = list(_get_candidate_moves(board))
    if not candidates:
        return None

    safe = _filter_forbidden_moves(board, candidates, ai_color)

    win_moves = []
    threat_moves = []

    for r, c in safe:
        board[r][c] = ai_color
        is_win, _ = check_win(board, r, c, ai_color)
        if is_win:
            win_moves.append((r, c))
        else:
            _, defense = _evaluate_position(board, r, c, ai_color)
            if defense >= 5000:   # 对手有冲四或活四，必须堵
                threat_moves.append((r, c))
        board[r][c] = None

    if win_moves:
        row, col = random.choice(win_moves)
    elif threat_moves:
        row, col = random.choice(threat_moves)
    else:
        row, col = random.choice(safe)

    return row, col


def ai_move_medium(board, ai_color):
    """
    中等 AI：兼顾进攻与防守，是原有算法。
    优先防守对手杀招，其次寻求自己的活四/冲三。
    """
    candidates = list(_get_candidate_moves(board))
    if not candidates:
        return None

    safe = _filter_forbidden_moves(board, candidates, ai_color)

    scored = []
    for r, c in safe:
        attack, defense = _evaluate_position(board, r, c, ai_color)

        if defense >= 50000:        # 对手活四，必须堵
            total = defense * 10
        elif defense >= 5000:       # 对手冲四，必须堵
            total = defense * 5
        elif attack >= 50000:       # AI 自己能活四，优先下
            total = attack * 3
        else:
            total = defense * 1.2 + attack

        scored.append((total, r, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return None

    top_score = scored[0][0]
    top_n = [s for s in scored if s[0] >= top_score * 0.95]
    if len(top_n) > 3:
        top_n = top_n[:3]

    _, row, col = random.choice(top_n)
    return row, col


def ai_move_hard(board, ai_color):
    """
    困难 AI：向前看一步，预判对手的最佳应对。
    对每个候选位置：
      1) 模拟己方落子
      2) 模拟对手在该局势下的最佳落子
      3) 综合评分 = 己方得分 − 对手最佳威胁 × 权重
    确保每次决策在 1.5 秒内完成。
    """
    candidates = list(_get_candidate_moves(board))
    if not candidates:
        return None

    safe = _filter_forbidden_moves(board, candidates, ai_color)
    opponent = 'white' if ai_color == 'black' else 'black'

    scored = []
    for r, c in safe:
        board[r][c] = ai_color

        attack, defense = _evaluate_position(board, r, c, ai_color)

        # 直接获胜
        is_win, _ = check_win(board, r, c, ai_color)
        if is_win:
            net = 1000000
        elif defense >= 50000:  # 必须堵截对手杀招
            net = defense * 10 + attack
        else:
            # 向前看一步：评估对手所有候选的最佳威胁
            opp_cands = list(_get_candidate_moves(board))
            opp_best = 0
            for or_, oc in opp_cands:
                board[or_][oc] = opponent
                oa, od = _evaluate_position(board, or_, oc, opponent)
                # 对手能直接赢且不止一处 → 极度危险
                if oa > opp_best:
                    opp_best = oa
                    if opp_best >= 100000:
                        # 对手可直接五连，提前中止搜索
                        board[or_][oc] = None
                        break
                board[or_][oc] = None

            # 综合：己方进攻 + 防守 − 对手威胁
            net = attack + defense * 0.8 - opp_best * 0.65

        board[r][c] = None
        scored.append((net, r, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return None

    top_score = scored[0][0]
    top_n = [s for s in scored if s[0] >= top_score * 0.95]
    if len(top_n) > 3:
        top_n = top_n[:3]

    _, row, col = random.choice(top_n)
    return row, col


# 统一调度入口
def ai_move(board, ai_color, difficulty='medium'):
    """AI 决策调度：根据难度调用对应的 AI 算法"""
    if difficulty == 'easy':
        return ai_move_easy(board, ai_color)
    elif difficulty == 'hard':
        return ai_move_hard(board, ai_color)
    else:
        return ai_move_medium(board, ai_color)


# ==================== 禁手规则 ====================

def _line_info(board, row, col, player, dr, dc):
    """统计在 (row,col) 沿 (dr,dc) 方向上连续的 player 棋子数、两端坐标与开放端数。
    返回: (total, 正向端点行, 正向端点列, 反向端点行, 反向端点列, open_ends)
    （保留用于 check_win / 视觉连线等，不影响新的禁手检测）
    """
    fr, fc = row, col
    total = 1
    r, c = row + dr, col + dc
    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
        total += 1
        fr, fc = r, c
        r += dr; c += dc
    br, bc = row, col
    r, c = row - dr, col - dc
    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
        total += 1
        br, bc = r, c
        r -= dr; c -= dc
    open_ends = 0
    nr, nc = fr + dr, fc + dc
    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] is None:
        open_ends += 1
    nr, nc = br - dr, bc - dc
    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] is None:
        open_ends += 1
    return total, fr, fc, br, bc, open_ends


def _scan_line(board, row, col, dr, dc):
    """扫描沿 (dr,dc) 方向从 row,col 出发各 6 格范围内的格子值。
    返回 (cells, center_idx)：cells 为值列表，center_idx 为落子点索引。
    'WALL' 表示出界，None 表示空位，'black'/'white' 表示对应棋子。
    """
    cells = []
    for d in range(-6, 7):
        r, c = row + d * dr, col + d * dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            cells.append(board[r][c])
        else:
            cells.append('WALL')
    return cells, 6


def _has_n_consecutive(cells, n, center):
    """扫描 cells 中是否存在 ≥ n 个连续 'black'，且该连续段必须包含 center 位置。"""
    cur = 0
    start = 0
    for i, cell in enumerate(cells):
        if cell == 'black':
            if cur == 0:
                start = i
            cur += 1
            if cur >= n and start <= center < start + cur:
                return True
        else:
            cur = 0
    return False


def _is_live_three(cells, center):
    """判定 cells[center] 是否属于一个由本次落子新形成的活三。
    活三定义：3 子中存在一个空位，填入后恰好形成两端均开放的 4 连。
    能正确处理连三 (B B X / X B B) 与跳活三 (B B . X / X . B B / B . X B / B X . B)。"""
    black_count = sum(1 for c in cells if c == 'black')
    if black_count != 3:
        return False

    for idx, val in enumerate(cells):
        if val is not None:
            continue
        if abs(idx - center) > 5:
            continue

        # 在 idx 处模拟落一黑子，统计左右连续黑子数
        left = 0
        for i in range(idx - 1, -1, -1):
            if cells[i] == 'black':
                left += 1
            else:
                break
        right = 0
        for i in range(idx + 1, len(cells)):
            if cells[i] == 'black':
                right += 1
            else:
                break

        span_left = idx - left
        span_right = idx + right

        # 恰好形成 4 连，且两端均开放（必须在棋盘内且为空）→ 活四 → 原形是活三
        if left + 1 + right != 4:
            continue
        left_end = span_left - 1
        right_end = span_right + 1
        if not (0 <= left_end < len(cells) and cells[left_end] is None):
            continue
        if not (0 <= right_end < len(cells) and cells[right_end] is None):
            continue

        # ★ 关键检查：落子点 center 必须在这个活四范围内（即本次落子是活三的一部分）
        if span_left <= center <= span_right:
            return True
    return False


def _is_four(cells, center):
    """判定 cells[center] 是否属于一个由本次落子新形成的「四」（4 子能发展成五）。
    覆盖连四与跳四，用于四四禁手统计。"""
    # 1. 连续四（活四 / 冲四）：≥4 连，且必须包含 center
    cur = 0
    start = 0
    for i, cell in enumerate(cells):
        if cell == 'black':
            if cur == 0:
                start = i
            cur += 1
            if cur >= 4 and start <= center < start + cur:
                return True
        else:
            cur = 0

    # 2. 跳四：在某个空位落子后形成 ≥5 连，且该 5 连必须包含 center
    black_count = sum(1 for c in cells if c == 'black')
    if black_count >= 4:
        for idx, val in enumerate(cells):
            if val is not None:
                continue
            if abs(idx - center) > 5:
                continue
            left = 0
            for i in range(idx - 1, -1, -1):
                if cells[i] == 'black':
                    left += 1
                else:
                    break
            right = 0
            for i in range(idx + 1, len(cells)):
                if cells[i] == 'black':
                    right += 1
                else:
                    break

            span_left = idx - left
            span_right = idx + right

            if left + 1 + right < 5:
                continue

            # ★ 关键检查：落子点 center 必须在 ≥5 连范围内
            if span_left <= center <= span_right:
                return True

    return False


def detect_forbidden(board, row, col):
    """检测黑棋在 (row,col) 落子后是否构成禁手。
    返回值：None（无禁手） / 'long'（长连） / 'double-four'（四四） / 'double-three'（三三）
    注意：调用方应先确认此处非五连，再调用本函数。五连优先于禁手。
    """
    four_count = 0
    three_count = 0

    for dr, dc in [(0, 1), (1, 0), (1, -1), (1, 1)]:
        cells, center = _scan_line(board, row, col, dr, dc)

        # 长连禁手（连续 ≥6 子，且必须包含当前落子点）
        if _has_n_consecutive(cells, 6, center):
            return 'long'

        # 统计四（连四或跳四；四的优先级高于活三，使用 elif 避免重复计算）
        if _is_four(cells, center):
            four_count += 1
        elif _is_live_three(cells, center):
            three_count += 1

    # 四四禁手：同时形成 ≥2 个四
    if four_count >= 2:
        return 'double-four'
    # 三三禁手：同时形成 ≥2 个活三
    if three_count >= 2:
        return 'double-three'

    return None


# 禁手类型 -> 中文提示映射
FORBIDDEN_MESSAGES = {
    'long':         "长连禁手！黑棋连成六子，此手无效，请重新落子",
    'double-four':  "四四禁手！黑棋此手形成两个「四」，此手无效",
    'double-three': "三三禁手！黑棋此手同时形成两个活三，请重新落子",
}

# 禁手判负时的胜利原因描述
FORBIDDEN_WIN_MESSAGES = {
    'long':          "黑棋长连禁手，白胜",
    'double-four':   "黑棋四四禁手，白胜",
    'double-three':  "黑棋三三禁手，白胜",
    'five-override': "黑棋五连！禁手不生效，黑胜",
    'timeout_black': "黑方超时，白棋获胜",
    'timeout_white': "白方超时，黑棋获胜",
}


# ==================== 字体加载 ====================

def _load_fonts():
    """加载字体资源，返回 (title, subtitle, body, small)"""
    names = ["microsoftyahei", "simhei", "simsun", "notosanscjk"]
    for name in names:
        try:
            return (
                pygame.font.SysFont(name, 34, bold=True),
                pygame.font.SysFont(name, 26, bold=True),
                pygame.font.SysFont(name, 20),
                pygame.font.SysFont(name, 16),
            )
        except Exception:
            continue
    # 回退到默认字体
    return (
        pygame.font.Font(None, 34),
        pygame.font.Font(None, 26),
        pygame.font.Font(None, 20),
        pygame.font.Font(None, 16),
    )


# ==================== UI 绘制 ====================

def _draw_rounded_rect_alpha(screen, rect, color, border_radius=0):
    """绘制带透明度的圆角矩形"""
    s = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(s, color, s.get_rect(), border_radius=border_radius)
    screen.blit(s, rect)


def draw_panel(screen, current_player, move_count, game_over=False, winner=None,
               game_mode='pvp', ai_thinking=False, anim_t=0, forbidden_reason=None,
               ai_difficulty='medium', black_time=30.0, white_time=30.0,
               time_mode_active=False):
    """绘制右侧信息面板 — 四区域清晰分区布局（紧凑版）"""
    title_font, sub_font, body_font, small_font = _load_fonts()
    try:
        timer_font = pygame.font.SysFont("microsoftyahei", 22, bold=True)
    except Exception:
        timer_font = pygame.font.Font(None, 30)

    pad_x = PANEL_LEFT + 20
    content_w = PANEL_WIDTH - 40
    y = PANEL_TOP + 12

    # ---- 标题 ----
    ts = title_font.render("优雅五子棋", True, COLOR_TEXT_TITLE)
    screen.blit(ts, (PANEL_LEFT + PANEL_WIDTH // 2 - ts.get_width() // 2, y))
    y += title_font.get_height() + 3

    # 标题下粗分割线
    pygame.draw.line(screen, COLOR_PANEL_BORDER,
                     (PANEL_LEFT + 20, y), (PANEL_LEFT + PANEL_WIDTH - 20, y), 2)
    y += 5

    # 限时模式面板边框泛红
    if time_mode_active:
        alert_rect = pygame.Rect(PANEL_LEFT + 2, PANEL_TOP + 2,
                                  PANEL_WIDTH - 4, PANEL_HEIGHT - 4)
        pygame.draw.rect(screen, (220, 80, 60, 30), alert_rect, 3, border_radius=12)

    # ================================================================
    #   ZONE 1 — 游戏状态与计时
    # ================================================================
    zone1_top = y
    if ai_thinking:
        zone1_h = 3 + sub_font.get_height() + body_font.get_height() + 16 + 3
    elif game_over and winner is not None:
        has_reason = (forbidden_reason is not None and
                      FORBIDDEN_WIN_MESSAGES.get(forbidden_reason, ""))
        zone1_h = 3 + sub_font.get_height() + 34 + small_font.get_height() + 12 + 3
        if has_reason:
            zone1_h += 22
    else:
        zone1_h = 3 + sub_font.get_height() + 28 + body_font.get_height() + 2 + 52 + 3

    _draw_zone_bg(screen, pygame.Rect(pad_x - 4, zone1_top, content_w + 8, zone1_h))
    y += 3

    if ai_thinking:
        _draw_section_header(screen, sub_font, y, "当前回合", COLOR_TEXT_TITLE)
        y += sub_font.get_height()
        alpha = int(128 + 127 * math.sin(anim_t * 3))
        think_color = COLOR_AI_THINKING if alpha > 160 else COLOR_AI_THINKING_DIM
        ts2 = body_font.render("AI 思考中...", True, think_color)
        screen.blit(ts2, (PANEL_LEFT + PANEL_WIDTH // 2 - ts2.get_width() // 2, y))
        dots = int(anim_t * 2) % 3 + 1
        dt = small_font.render("." * dots, True, think_color)
        screen.blit(dt, (PANEL_LEFT + PANEL_WIDTH // 2 + ts2.get_width() // 2 + 4, y + 4))
        y += ts2.get_height() + 6
    elif game_over and winner is not None:
        _draw_section_header(screen, sub_font, y, "游戏结束", COLOR_TEXT_ACCENT)
        y += sub_font.get_height()
        pulse = 1.0 + 0.06 * math.sin(anim_t * 2.5)
        win_text = "● 黑棋胜利！" if winner == 'black' else "○ 白棋胜利！"
        win_color = COLOR_WIN_BLACK_TEXT if winner == 'black' else COLOR_WIN_WHITE_TEXT
        try:
            win_font_anim = pygame.font.SysFont("microsoftyahei", 22, bold=True)
        except Exception:
            win_font_anim = pygame.font.Font(None, 28)
        ws = win_font_anim.render(win_text, True, win_color)
        screen.blit(ws, (PANEL_LEFT + PANEL_WIDTH // 2 - ws.get_width() // 2, y))
        y += int(22 * pulse) + 4
        cs = small_font.render(f"共落子 {move_count} 手", True, COLOR_TEXT_LIGHT)
        screen.blit(cs, (PANEL_LEFT + PANEL_WIDTH // 2 - cs.get_width() // 2, y))
        y += small_font.get_height() + 4
        if forbidden_reason is not None:
            reason_text = FORBIDDEN_WIN_MESSAGES.get(forbidden_reason, "")
            if reason_text:
                try:
                    reason_font = pygame.font.SysFont("microsoftyahei", 13, bold=True)
                except Exception:
                    reason_font = pygame.font.Font(None, 18)
                rs = reason_font.render(reason_text, True, COLOR_FORBIDDEN_TEXT)
                screen.blit(rs, (PANEL_LEFT + PANEL_WIDTH // 2 - rs.get_width() // 2, y))
                y += 14
        y += 4
    else:
        _draw_section_header(screen, sub_font, y, "当前回合", COLOR_TEXT_TITLE)
        y += sub_font.get_height()

        # 棋子图标
        icon_r = 14
        icon_cx = PANEL_LEFT + PANEL_WIDTH // 2
        _draw_mini_stone(screen, icon_cx, y + icon_r, icon_r, current_player)
        y += icon_r * 2 + 2

        # 回合文字
        turn_text = "● 黑棋回合" if current_player == 'black' else "○ 白棋回合"
        turn_color = COLOR_TURN_BLACK_TEXT if current_player == 'black' else COLOR_TURN_WHITE_TEXT
        ts2 = body_font.render(turn_text, True, turn_color)
        screen.blit(ts2, (PANEL_LEFT + PANEL_WIDTH // 2 - ts2.get_width() // 2, y))
        y += body_font.get_height() + 2

        # ---- 双人计时器（黑白并列）----
        timer_y = y
        timer_w = content_w // 2 - 10
        timer_h = 48
        bar_h = 5
        _draw_player_timer(screen, pad_x, timer_y, timer_w, timer_h, bar_h,
                           'black', black_time, time_mode_active, anim_t,
                           timer_font, small_font)
        _draw_player_timer(screen, pad_x + timer_w + 16, timer_y, timer_w, timer_h, bar_h,
                           'white', white_time, time_mode_active, anim_t,
                           timer_font, small_font)
        y = timer_y + timer_h

    y = zone1_top + zone1_h + 2

    # 分隔线
    pygame.draw.line(screen, COLOR_PANEL_SEPARATOR,
                     (PANEL_LEFT + 20, y), (PANEL_LEFT + PANEL_WIDTH - 20, y), 1)
    y += 5

    # ================================================================
    #   ZONE 2 — 模式与设置
    # ================================================================
    zone2_top = y
    zone2_h = 80 if game_mode == 'pve' else 54
    _draw_zone_bg(screen, pygame.Rect(pad_x - 4, zone2_top, content_w + 8, zone2_h))
    y += 3

    mode_text = "双人对战" if game_mode == 'pvp' else "人机对战"
    _draw_tagged_label(screen, body_font, small_font, pad_x, y,
                       "对战模式", mode_text, COLOR_TEXT_BODY, COLOR_TEXT_ACCENT, content_w)
    y += body_font.get_height() + 2

    if game_mode == 'pve':
        diff_label = AI_DIFFICULTY_LABELS.get(ai_difficulty, "中等")
        _draw_tagged_label(screen, body_font, small_font, pad_x, y,
                           "电脑难度", diff_label, COLOR_TEXT_BODY, COLOR_TEXT_ACCENT, content_w)
        y += body_font.get_height() + 2

    # 主题选择
    theme_label = small_font.render("主题", True, COLOR_TEXT_LIGHT)
    screen.blit(theme_label, (pad_x, y + 1))
    dot_area_x = pad_x + theme_label.get_width() + 10
    dot_size, dot_gap = 13, 5
    theme_rects = {}
    for idx, tname in enumerate(THEME_NAMES):
        dx = dot_area_x + idx * (dot_size + dot_gap)
        dy = y
        theme_rect = pygame.Rect(dx, dy, dot_size, dot_size)
        theme_rects[tname] = theme_rect
        border_color = COLOR_TEXT_ACCENT if tname == get_current_theme() else COLOR_PANEL_BORDER
        pygame.draw.rect(screen, THEME_PREVIEW_COLORS[tname], theme_rect, border_radius=3)
        pygame.draw.rect(screen, border_color, theme_rect,
                         2 if tname == get_current_theme() else 1, border_radius=3)
        if tname == get_current_theme():
            try:
                check_font = pygame.font.SysFont("microsoftyahei", 10, bold=True)
            except Exception:
                check_font = pygame.font.Font(None, 14)
            chk = check_font.render("✓", True, COLOR_TEXT_TITLE)
            screen.blit(chk, (dx + dot_size // 2 - chk.get_width() // 2,
                              dy + dot_size // 2 - chk.get_height() // 2))

    y = zone2_top + zone2_h + 2

    # 分隔线
    pygame.draw.line(screen, COLOR_PANEL_SEPARATOR,
                     (PANEL_LEFT + 20, y), (PANEL_LEFT + PANEL_WIDTH - 20, y), 1)
    y += 5

    # ================================================================
    #   ZONE 3 — 对局信息
    # ================================================================
    zone3_top = y
    zone3_h = 3 + body_font.get_height() + 4 + 3
    _draw_zone_bg(screen, pygame.Rect(pad_x - 4, zone3_top, content_w + 8, zone3_h))
    y += 3
    _draw_labeled_value(screen, body_font, small_font, pad_x, y,
                        "已落子", f"{move_count} 手", COLOR_TEXT_BODY, COLOR_TEXT_ACCENT)
    y = zone3_top + zone3_h + 2

    # 分隔线
    pygame.draw.line(screen, COLOR_PANEL_SEPARATOR,
                     (PANEL_LEFT + 20, y), (PANEL_LEFT + PANEL_WIDTH - 20, y), 1)
    y += 5

    # ================================================================
    #   ZONE 4 — 操作按钮区（含限时模式 Toggle）
    # ================================================================
    toggle_rect = _draw_time_toggle(screen, pad_x, y, content_w,
                                     time_mode_active, small_font, body_font)
    y += toggle_rect.height + 2

    # 操作区标题
    _draw_section_header(screen, sub_font, y, "操作", COLOR_TEXT_TITLE)
    y += sub_font.get_height() + 10

    # 按钮区域背景框
    box_h = BTN_HEIGHT * 4 + BTN_GAP * 3 + BTN_BOX_PAD_Y * 2
    box_rect = pygame.Rect(pad_x, y, PANEL_WIDTH - 40, box_h)
    pygame.draw.rect(screen, COLOR_PANEL_BOX_BG, box_rect, border_radius=10)
    pygame.draw.rect(screen, COLOR_PANEL_BORDER, box_rect, 1, border_radius=10)

    btn_area_top = y
    return btn_area_top, theme_rects, toggle_rect


# ---- 区域辅助绘制 ----

def _draw_zone_bg(screen, rect):
    """绘制半透明浅色区域背景框"""
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill((*COLOR_PANEL_BOX_BG, 100))
    screen.blit(s, rect)


def _draw_player_timer(screen, x, y, w, h, bar_h, player, remaining, active, anim_t,
                       timer_font, small_font):
    """绘制单个玩家的计时器：标签 + 倒计时数字 + 进度条"""
    # 标签
    label_text = "● 黑棋" if player == 'black' else "○ 白棋"
    label_color = COLOR_TURN_BLACK_TEXT if player == 'black' else COLOR_TURN_WHITE_TEXT
    ls = small_font.render(label_text, True, label_color)
    screen.blit(ls, (x, y))

    # 倒计时数字（00.0 格式）
    secs = max(0.0, remaining)
    # 急促闪烁（<5秒时）
    low_time = secs < 5.0
    show_number = True
    if low_time:
        show_number = (int(anim_t * 2) % 2 == 0)   # 0.5s 间隔闪烁
    if low_time and active:
        num_color = (220, 40, 30)
    else:
        num_color = COLOR_TEXT_BODY
        if remaining <= 0:
            num_color = COLOR_TEXT_LIGHT

    if show_number:
        num_text = f"{secs:04.1f}"
    else:
        num_text = "··.·"
    ns = timer_font.render(num_text, True, num_color)
    screen.blit(ns, (x, y + ls.get_height() + 4))

    # 进度条
    bar_y = y + ls.get_height() + ns.get_height() + 6
    bar_bg = pygame.Rect(x, bar_y, w, bar_h)
    pygame.draw.rect(screen, COLOR_PANEL_SEPARATOR, bar_bg, border_radius=3)

    ratio = max(0.0, min(1.0, remaining / TIME_LIMIT_SECONDS))
    if ratio > 0:
        if ratio > 0.25:
            bar_c = (120, 185, 100)
        elif ratio > 0.1:
            bar_c = (220, 170, 50)
        else:
            bar_c = (220, 70, 55)
        bar_fill = pygame.Rect(x, bar_y, int(w * ratio), bar_h)
        pygame.draw.rect(screen, bar_c, bar_fill, border_radius=3)


def _draw_tagged_label(screen, label_font, value_font, x, y, label, value,
                        label_color, value_color, content_w):
    """绘制标签-值行，值部分用高亮圆角标签样式包裹"""
    ls = label_font.render(label + "：", True, label_color)
    vs = value_font.render(value, True, COLOR_BTN_TEXT)
    screen.blit(ls, (x, y))
    # 值标签背景
    tag_pad_h = 3
    tag_pad_w = 10
    tag_rect = pygame.Rect(x + ls.get_width() + 4, y - tag_pad_h,
                           vs.get_width() + tag_pad_w * 2,
                           vs.get_height() + tag_pad_h * 2)
    pygame.draw.rect(screen, COLOR_TEXT_ACCENT, tag_rect, border_radius=6)
    screen.blit(vs, (tag_rect.x + tag_pad_w, tag_rect.y + tag_pad_h))


def _draw_time_toggle(screen, x, y, w, time_mode_active, small_font, body_font):
    """绘制限时模式 Toggle 滑动开关，返回 rect 用于点击检测"""
    label_text = "限时模式"
    ls = body_font.render(label_text, True, COLOR_TEXT_BODY)
    screen.blit(ls, (x, y + 2))

    # 滑动开关
    toggle_w, toggle_h = 44, 22
    toggle_x = PANEL_LEFT + PANEL_WIDTH - 24 - toggle_w
    knob_r = toggle_h // 2 - 2

    track_rect = pygame.Rect(toggle_x, y + 2, toggle_w, toggle_h)
    if time_mode_active:
        track_color = (120, 185, 100)
        knob_cx = toggle_x + toggle_w - knob_r - 3
    else:
        track_color = (170, 165, 155)
        knob_cx = toggle_x + knob_r + 3

    pygame.draw.rect(screen, track_color, track_rect, border_radius=toggle_h // 2)
    # 滑动手柄
    pygame.draw.circle(screen, (255, 255, 255),
                       (knob_cx, y + 2 + toggle_h // 2), knob_r)
    # 手柄阴影
    pygame.draw.circle(screen, (200, 198, 190),
                       (knob_cx, y + 2 + toggle_h // 2), knob_r, 1)

    # 状态提示文字
    status_text = "开启" if time_mode_active else "关闭"
    st_color = COLOR_TEXT_ACCENT if time_mode_active else COLOR_TEXT_LIGHT
    ss = small_font.render(status_text, True, st_color)
    screen.blit(ss, (toggle_x - ss.get_width() - 8, y + 4))

    # 点击区域（整行都可点击）
    click_rect = pygame.Rect(x, y, w, ls.get_height() + 6)
    return click_rect


def _draw_section_header(screen, font, y, text, color):
    """绘制分节标题（居中，无装饰线更简洁）"""
    surf = font.render(text, True, color)
    screen.blit(surf, (PANEL_LEFT + PANEL_WIDTH // 2 - surf.get_width() // 2, y))


def _draw_labeled_value(screen, label_font, value_font, x, y, label, value, label_color, value_color):
    """绘制"标签：值"格式的一行文字"""
    ls = label_font.render(label + "：", True, label_color)
    vs = value_font.render(value, True, value_color)
    screen.blit(ls, (x, y))
    screen.blit(vs, (x + ls.get_width() + 4, y + (ls.get_height() - vs.get_height()) // 2))


def _draw_mini_stone(screen, cx, cy, r, color):
    """绘制小棋子图标（完整球形）"""
    size = r * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    if color == 'black':
        for dy in range(size):
            for dx in range(size):
                dist = math.hypot(dx - r, dy - r)
                if dist <= r:
                    nx, ny = (dx - r) / r, (dy - r) / r
                    radial = 1 - (dist / r) * 0.15
                    brightness = (0.35 + 0.65 * max(0, (-nx - ny) / 2)) * radial
                    val = int(25 + 115 * brightness)
                    val = max(15, min(255, val))
                    surf.set_at((dx, dy), (val, val, val, 255))
        hl_x, hl_y = r - r // 3, r - r // 3
        pygame.draw.circle(surf, (170, 170, 170, 160), (hl_x, hl_y), max(r // 3, 2))
    else:
        for dy in range(size):
            for dx in range(size):
                dist = math.hypot(dx - r, dy - r)
                if dist <= r:
                    nx, ny = (dx - r) / r, (dy - r) / r
                    radial = 1 - (dist / r) * 0.12
                    brightness = (0.65 + 0.35 * max(0, (-nx - ny) / 2)) * radial
                    val = int(195 + 60 * brightness)
                    val = max(160, min(255, val))
                    surf.set_at((dx, dy), (val, val, val, 255))
        hl_x, hl_y = r - r // 3, r - r // 3
        pygame.draw.circle(surf, (255, 255, 255, 200), (hl_x, hl_y), max(r // 3, 2))

    screen.blit(surf, (cx - r, cy - r))


# ==================== 按钮 ====================

def _get_button_rects(btn_area_top):
    """返回四个按钮的 (rect, name, color, hover_color) 列表"""
    btns = []
    names = ["切换模式", "再来一局", "悔棋", "退出游戏"]
    colors = [
        (COLOR_BTN_MODE, COLOR_BTN_MODE_HOVER),
        (COLOR_BTN_RESTART, COLOR_BTN_RESTART_HOVER),
        (COLOR_BTN_UNDO, COLOR_BTN_UNDO_HOVER),
        (COLOR_BTN_QUIT, COLOR_BTN_QUIT_HOVER),
    ]
    for i, name in enumerate(names):
        bx = BTN_LEFT
        by = btn_area_top + BTN_BOX_PAD_Y + i * (BTN_HEIGHT + BTN_GAP)
        rect = pygame.Rect(bx, by, BTN_WIDTH, BTN_HEIGHT)
        btns.append((rect, name, colors[i][0], colors[i][1]))
    return btns


def draw_buttons(screen, mouse_pos, game_over, move_count, btn_area_top, toast_msg=None):
    """绘制四个功能按钮（带悬浮效果 + 可选提示消息）"""
    btns = _get_button_rects(btn_area_top)
    _, small_font = _load_fonts()[0], _load_fonts()[3]

    for rect, name, normal_color, hover_color in btns:
        mouse_on = rect.collidepoint(mouse_pos)

        # 悔棋按钮：无棋可悔或游戏结束时禁用
        is_undo = (name == "悔棋")
        disabled = is_undo and (move_count == 0 or game_over)

        # 选择颜色
        if disabled:
            fill = COLOR_BTN_DISABLED
        elif mouse_on:
            fill = hover_color
        else:
            fill = normal_color

        # 绘制圆角矩形主体
        pygame.draw.rect(screen, fill, rect, border_radius=10)

        # 悬浮时加亮边
        if mouse_on and not disabled:
            lighter = tuple(min(c + 40, 255) for c in hover_color)
            pygame.draw.rect(screen, lighter, rect, 2, border_radius=10)

        # 文字
        text_surf = small_font.render(name, True, COLOR_BTN_TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    # 提示消息
    if toast_msg:
        toast_surf = small_font.render(toast_msg, True, COLOR_TOAST_TEXT)
        toast_bg = pygame.Surface((toast_surf.get_width() + 20, toast_surf.get_height() + 10), pygame.SRCALPHA)
        toast_bg.fill(COLOR_TOAST_BG)
        toast_x = BTN_LEFT + (BTN_WIDTH - toast_bg.get_width()) // 2
        box_h = BTN_HEIGHT * 4 + BTN_GAP * 3 + BTN_BOX_PAD_Y * 2
        toast_y = btn_area_top + box_h + 4
        screen.blit(toast_bg, (toast_x, toast_y))
        screen.blit(toast_surf, (toast_x + 10, toast_y + 5))


def get_button_clicked(mouse_pos, game_over, move_count, btn_area_top):
    """检测按钮点击，返回按钮名称或 None"""
    btns = _get_button_rects(btn_area_top)
    for rect, name, _, _ in btns:
        if rect.collidepoint(mouse_pos):
            if name == "悔棋" and (move_count == 0 or game_over):
                return None
            return name
    return None


def draw_win_banner(screen, winner, anim_t, forbidden_reason=None):
    """绘制带动画效果的全屏宽度胜利横幅（无重影），包含禁手原因"""
    # 如果有禁手原因，横幅整体增高以容纳副标题
    has_reason = (forbidden_reason is not None and
                  FORBIDDEN_WIN_MESSAGES.get(forbidden_reason, ""))
    banner_h = 90 if has_reason else 70

    if winner == 'black':
        banner_bg = COLOR_BANNER_BLACK_BG
        text_color = COLOR_BANNER_BLACK_TEXT
        accent_color = COLOR_BANNER_BLACK_ACCENT
        text = "●  黑 棋 胜 利 ！"
    else:
        banner_bg = COLOR_BANNER_WHITE_BG
        text_color = COLOR_BANNER_WHITE_TEXT
        accent_color = COLOR_BANNER_WHITE_TEXT
        text = "○  白 棋 胜 利 ！"

    # 创建完整的横幅 surface，避免重影
    banner = pygame.Surface((WINDOW_WIDTH, banner_h), pygame.SRCALPHA)

    # 半透明背景
    banner.fill(banner_bg)

    # 装饰线
    for offset in [0, banner_h - 3]:
        pygame.draw.line(banner, accent_color, (0, offset), (WINDOW_WIDTH, offset), 3)

    # 左右装饰小菱形
    diamond_size = 5
    pulse = 1.0 + 0.08 * math.sin(anim_t * 3)
    d_s = max(3, int(diamond_size * pulse))
    for side_x in [60, WINDOW_WIDTH - 60]:
        cy = banner_h // 2
        pts = [(side_x, cy - d_s), (side_x + d_s, cy), (side_x, cy + d_s), (side_x - d_s, cy)]
        pygame.draw.polygon(banner, accent_color, pts)

    # 主体文字（固定字号 + 轻微脉冲缩放，绘制到 banner 上）
    text_pulse = 1.0 + 0.03 * math.sin(anim_t * 2.5)
    text_font_size = max(20, int(44 * text_pulse))
    try:
        text_font = pygame.font.SysFont("microsoftyahei", text_font_size, bold=True)
    except Exception:
        text_font = pygame.font.Font(None, text_font_size)

    text_surf = text_font.render(text, True, text_color)
    # 如果有原因，文字向上偏移以留出副标题空间
    text_y_offset = -6 if has_reason else 0
    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, banner_h // 2 + text_y_offset))
    banner.blit(text_surf, text_rect)

    # 副标题：禁手原因
    if has_reason:
        reason_text = FORBIDDEN_WIN_MESSAGES.get(forbidden_reason, "")
        try:
            sub_font = pygame.font.SysFont("microsoftyahei", 18, bold=False)
        except Exception:
            sub_font = pygame.font.Font(None, 22)
        sub_surf = sub_font.render(reason_text, True, text_color)
        sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, banner_h - 22))
        banner.blit(sub_surf, sub_rect)

    # 一次性 blit 到 screen
    screen.blit(banner, (0, 0))


# ==================== 模式选择界面 ====================

def draw_mode_select(screen):
    """绘制开始前的模式选择界面"""
    screen.fill(COLOR_BG)

    title_font, sub_font, body_font, small_font = _load_fonts()

    # 装饰棋盘图标（简化棋盘）
    icon_size = 120
    icon_x = WINDOW_WIDTH // 2 - icon_size // 2
    icon_y = 80
    icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
    icon_surf = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    icon_surf.fill(COLOR_ICON_BOARD)
    pygame.draw.rect(icon_surf, COLOR_ICON_BORDER, (0, 0, icon_size, icon_size), 3)
    # 简化的网格
    for i in range(5):
        y = icon_size // 5 + i * (icon_size // 5)
        pygame.draw.line(icon_surf, COLOR_ICON_GRID, (icon_size // 5, y),
                         (icon_size - icon_size // 5, y), 1)
        x = icon_size // 5 + i * (icon_size // 5)
        pygame.draw.line(icon_surf, COLOR_ICON_GRID, (x, icon_size // 5),
                         (x, icon_size - icon_size // 5), 1)
    # 小棋子
    pygame.draw.circle(icon_surf, COLOR_ICON_BLACK, (icon_size // 2 - 12, icon_size // 2), 6)
    pygame.draw.circle(icon_surf, COLOR_ICON_WHITE, (icon_size // 2 + 12, icon_size // 2 + 8), 6)
    screen.blit(icon_surf, (icon_x, icon_y))

    # 标题
    ts = title_font.render("优雅五子棋", True, COLOR_TEXT_TITLE)
    screen.blit(ts, (WINDOW_WIDTH // 2 - ts.get_width() // 2, 220))

    # 副标题
    ss = small_font.render("请选择对战模式", True, COLOR_TEXT_LIGHT)
    screen.blit(ss, (WINDOW_WIDTH // 2 - ss.get_width() // 2, 266))

    # 两个大按钮
    btn_w = 280
    btn_h = 76
    btn_gap = 24
    btn_y = 310

    btns = [
        ("双人对战", "两位玩家轮流落子", COLOR_BTN_RESTART, COLOR_BTN_RESTART_HOVER),
        ("人机对战", "玩家执黑 · AI 执白", COLOR_BTN_MODE, COLOR_BTN_MODE_HOVER),
    ]

    mouse_pos = pygame.mouse.get_pos()
    result = None

    for i, (title, desc, color, hover_color) in enumerate(btns):
        bx = WINDOW_WIDTH // 2 - btn_w // 2
        by = btn_y + i * (btn_h + btn_gap)

        rect = pygame.Rect(bx, by, btn_w, btn_h)
        mouse_on = rect.collidepoint(mouse_pos)

        # 按钮底色（带微弱阴影）
        if mouse_on:
            shadow = pygame.Rect(bx + 2, by + 2, btn_w, btn_h)
            pygame.draw.rect(screen, (0, 0, 0, 30), shadow, border_radius=14)

        fill = hover_color if mouse_on else color
        pygame.draw.rect(screen, fill, rect, border_radius=14)

        if mouse_on:
            lighter = tuple(min(c + 40, 255) for c in hover_color)
            pygame.draw.rect(screen, lighter, rect, 2, border_radius=14)

        # 标题文字
        t_surf = body_font.render(title, True, COLOR_BTN_TEXT)
        screen.blit(t_surf, (bx + btn_w // 2 - t_surf.get_width() // 2, by + 14))

        # 描述文字
        d_surf = small_font.render(desc, True, COLOR_BTN_TEXT)
        screen.blit(d_surf, (bx + btn_w // 2 - d_surf.get_width() // 2, by + btn_h - 28))

        if mouse_on:
            result = ('pvp' if title == "双人对战" else 'pve')

    # 禁手规则说明
    rule_note = small_font.render("规则说明：黑棋受禁手限制（三三 / 四四 / 长连），白棋无限制", True, COLOR_TEXT_LIGHT)
    screen.blit(rule_note, (WINDOW_WIDTH // 2 - rule_note.get_width() // 2, btn_y + 2 * (btn_h + btn_gap) + 4))

    # 底部提示
    tip = small_font.render("点击按钮选择模式开始游戏", True, COLOR_TEXT_LIGHT)
    screen.blit(tip, (WINDOW_WIDTH // 2 - tip.get_width() // 2, WINDOW_HEIGHT - 50))

    return result


def draw_difficulty_select(screen):
    """绘制难度选择界面，返回选中的难度或 None"""
    screen.fill(COLOR_BG)

    title_font, sub_font, body_font, small_font = _load_fonts()

    # 装饰棋盘图标（同模式选择）
    icon_size = 120
    icon_x = WINDOW_WIDTH // 2 - icon_size // 2
    icon_y = 80
    icon_surf = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    icon_surf.fill(COLOR_ICON_BOARD)
    pygame.draw.rect(icon_surf, COLOR_ICON_BORDER, (0, 0, icon_size, icon_size), 3)
    for i in range(5):
        y = icon_size // 5 + i * (icon_size // 5)
        pygame.draw.line(icon_surf, COLOR_ICON_GRID, (icon_size // 5, y),
                         (icon_size - icon_size // 5, y), 1)
        x = icon_size // 5 + i * (icon_size // 5)
        pygame.draw.line(icon_surf, COLOR_ICON_GRID, (x, icon_size // 5),
                         (x, icon_size - icon_size // 5), 1)
    pygame.draw.circle(icon_surf, COLOR_ICON_BLACK, (icon_size // 2 - 12, icon_size // 2), 6)
    pygame.draw.circle(icon_surf, COLOR_ICON_WHITE, (icon_size // 2 + 12, icon_size // 2 + 8), 6)
    screen.blit(icon_surf, (icon_x, icon_y))

    # 标题
    ts = title_font.render("优雅五子棋", True, COLOR_TEXT_TITLE)
    screen.blit(ts, (WINDOW_WIDTH // 2 - ts.get_width() // 2, 220))

    # 副标题
    ss = small_font.render("人机对战 · 选择电脑难度", True, COLOR_TEXT_LIGHT)
    screen.blit(ss, (WINDOW_WIDTH // 2 - ss.get_width() // 2, 266))

    # 三个难度按钮
    btn_w = 280
    btn_h = 70
    btn_gap = 16
    btn_y = 310

    difficulties = [
        ('easy',   "简单", "新手友好"),
        ('medium', "中等", "势均力敌"),
        ('hard',   "困难", "棋逢对手"),
    ]

    # 三个难度的按钮配色，从温和绿到深蓝，体现递进
    diff_colors = [
        ((135, 190, 130), (155, 215, 150)),   # 简单：柔和绿
        ((100, 145, 180), (120, 170, 205)),   # 中等：柔和蓝
        ((185, 120, 105), (215, 140, 125)),   # 困难：柔和红
    ]

    mouse_pos = pygame.mouse.get_pos()
    result = None

    for i, (diff_id, title, desc) in enumerate(difficulties):
        bx = WINDOW_WIDTH // 2 - btn_w // 2
        by = btn_y + i * (btn_h + btn_gap)
        color, hover_color = diff_colors[i]

        rect = pygame.Rect(bx, by, btn_w, btn_h)
        mouse_on = rect.collidepoint(mouse_pos)

        if mouse_on:
            shadow = pygame.Rect(bx + 2, by + 2, btn_w, btn_h)
            pygame.draw.rect(screen, (0, 0, 0, 30), shadow, border_radius=14)

        fill = hover_color if mouse_on else color
        pygame.draw.rect(screen, fill, rect, border_radius=14)

        if mouse_on:
            lighter = tuple(min(c + 40, 255) for c in hover_color)
            pygame.draw.rect(screen, lighter, rect, 2, border_radius=14)

        # 标题
        t_surf = body_font.render(title, True, COLOR_BTN_TEXT)
        screen.blit(t_surf, (bx + btn_w // 2 - t_surf.get_width() // 2 - 36, by + 12))

        # 描述
        d_surf = small_font.render(desc, True, COLOR_BTN_TEXT)
        screen.blit(d_surf, (bx + btn_w // 2 - t_surf.get_width() // 2 + 40, by + 16))

        # 难度等级圆点指示器
        dot_radius = 6
        dot_cx = bx + btn_w // 2 - t_surf.get_width() // 2 - 56
        dot_cy = by + btn_h // 2
        for j in range(3):
            dx = dot_cx - 16 + j * 16
            fill_dot = (255, 255, 255, 220) if j <= i else (255, 255, 255, 60)
            pygame.draw.circle(screen, fill_dot[:3],
                              (dx, dot_cy), dot_radius)
            if j <= i:
                # 实心
                pass
            else:
                # 空心
                pygame.draw.circle(screen, (255, 255, 255, 90),
                                  (dx, dot_cy), dot_radius, 1)

        if mouse_on:
            result = diff_id

    # 禁手规则说明
    rule_note = small_font.render("规则说明：黑棋受禁手限制（三三 / 四四 / 长连），白棋无限制", True, COLOR_TEXT_LIGHT)
    screen.blit(rule_note, (WINDOW_WIDTH // 2 - rule_note.get_width() // 2,
                             btn_y + 3 * (btn_h + btn_gap) + 4))

    # 返回按钮
    back_text = small_font.render("← 返回模式选择", True, COLOR_TEXT_LIGHT)
    back_rect = back_text.get_rect(topleft=(30, WINDOW_HEIGHT - 50))
    screen.blit(back_text, back_rect)

    # 底部提示
    tip = small_font.render("点击按钮选择难度开始游戏", True, COLOR_TEXT_LIGHT)
    screen.blit(tip, (WINDOW_WIDTH // 2 - tip.get_width() // 2, WINDOW_HEIGHT - 50))

    return result, back_rect


# ==================== 主循环 ====================

def _reset_game(ai_difficulty='medium'):
    """重置游戏状态，返回初始变量字典"""
    return {
        'board': [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)],
        'current_player': 'black',
        'game_over': False,
        'winner': None,
        'win_line': None,           # 胜利连线坐标 (sr, sc, er, ec)
        'hover_pos': None,
        'move_count': 0,
        'last_move': None,
        'move_history': [],
        'ai_thinking': False,
        'ai_schedule_time': 0,
        'forbidden_reason': None,   # 禁手判负原因
        'ai_difficulty': ai_difficulty,
        # 限时模式
        'time_mode_active': False,
        'black_time': TIME_LIMIT_SECONDS,
        'white_time': TIME_LIMIT_SECONDS,
        'last_frame_time': 0.0,
    }


def main():
    """游戏主循环 — 双人对战 / 人机对战"""
    screen = init_game()
    clock = pygame.time.Clock()

    # ========== 阶段一：模式选择界面 ==========
    game_mode = None
    while game_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_mode = draw_mode_select(screen)
                if game_mode is not None:
                    break

        if game_mode is None:
            draw_mode_select(screen)

        pygame.display.flip()
        clock.tick(60)

    # ========== 阶段二：难度选择（仅人机对战）==========
    ai_difficulty = 'medium'   # 默认中等
    if game_mode == 'pve':
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    diff_result, back_rect = draw_difficulty_select(screen)
                    if diff_result is not None:
                        ai_difficulty = diff_result
                        selecting = False
                        break
                    # 点击返回按钮
                    if back_rect.collidepoint(event.pos):
                        # 回到模式选择
                        game_mode = None
                        while game_mode is None:
                            for evt in pygame.event.get():
                                if evt.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                                    game_mode = draw_mode_select(screen)
                                    if game_mode is not None:
                                        break
                            if game_mode is None:
                                draw_mode_select(screen)
                            pygame.display.flip()
                            clock.tick(60)
                        if game_mode == 'pvp':
                            # 选了双人模式，跳过难度选择，直接开始
                            selecting = False
                            break
                        # 否则是 pve，继续难度选择循环

            if selecting:
                draw_difficulty_select(screen)
            pygame.display.flip()
            clock.tick(60)

    # ========== 阶段三：游戏开始 ==========
    state = _reset_game(ai_difficulty)
    btn_area_top = 0
    theme_rects = {}
    toggle_rect = pygame.Rect(0, 0, 0, 0)
    toast_msg = None
    toast_timer = 0
    anim_t = 0.0      # 动画时间（用于胜利横幅/呼吸效果）

    # 显示难度提示
    if game_mode == 'pve':
        diff_label = AI_DIFFICULTY_LABELS.get(ai_difficulty, "中等")
        diff_desc = AI_DIFFICULTY_DESCRIPTIONS.get(ai_difficulty, "势均力敌")
        toast_msg = f"当前难度：{diff_label}（{diff_desc}）"
        toast_timer = 120

    def do_player_move(row, col):
        """执行玩家落子，返回 True 表示落子成功"""
        player = state['current_player']
        if state['board'][row][col] is not None:
            return False
        state['board'][row][col] = player
        state['last_move'] = (row, col)
        state['move_history'].append((row, col, player))
        state['move_count'] += 1

        is_win, win_line = check_win(state['board'], row, col, player)

        # 禁手检测：仅对黑棋生效，且仅在非五连时判负
        if player == 'black' and not is_win:
            forbidden = detect_forbidden(state['board'], row, col)
            if forbidden is not None:
                # 禁手成立：落子保留在棋盘上，黑方判负，白方获胜
                state['game_over'] = True
                state['winner'] = 'white'
                state['forbidden_reason'] = forbidden
                return True

        # 五连获胜（含黑棋禁手点同时成五：五连优先，黑胜）
        if is_win:
            state['game_over'] = True
            state['winner'] = player
            state['win_line'] = win_line
            # 如果此手同时落在禁手点但成五连，记录原因以特别提示
            if player == 'black' and detect_forbidden(state['board'], row, col) is not None:
                state['forbidden_reason'] = 'five-override'
        else:
            # 切换回合
            next_player = 'white' if player == 'black' else 'black'
            state['current_player'] = next_player
            # 人机模式：调度 AI 落子
            if game_mode == 'pve' and next_player == 'white':
                state['ai_thinking'] = True
                state['ai_schedule_time'] = time.time() + 0.5
        return True

    def do_ai_move():
        """AI 落子，根据当前难度选择算法"""
        ai_color = state['current_player']
        difficulty = state.get('ai_difficulty', 'medium')
        row, col = ai_move(state['board'], ai_color, difficulty)
        if row is None:
            return

        state['board'][row][col] = ai_color
        state['last_move'] = (row, col)
        state['move_history'].append((row, col, ai_color))
        state['move_count'] += 1
        state['ai_thinking'] = False

        is_win, win_line = check_win(state['board'], row, col, ai_color)
        if is_win:
            state['game_over'] = True
            state['winner'] = ai_color
            state['win_line'] = win_line
        else:
            state['current_player'] = 'black' if ai_color == 'white' else 'white'

    while True:
        dt = clock.get_time() / 1000.0  # 帧间隔秒数
        anim_t += dt

        # ---- 限时模式计时 ----
        if (state['time_mode_active'] and not state['game_over']
                and not state['ai_thinking'] and state['current_player'] is not None):
            player = state['current_player']
            key = 'black_time' if player == 'black' else 'white_time'
            state[key] -= dt
            if state[key] <= 0.0:
                state[key] = 0.0
                state['game_over'] = True
                opponent = 'white' if player == 'black' else 'black'
                state['winner'] = opponent
                state['forbidden_reason'] = 'timeout_black' if player == 'black' else 'timeout_white'

        # ---- AI 定时落子 ----
        if state['ai_thinking'] and not state['game_over']:
            if time.time() >= state['ai_schedule_time']:
                do_ai_move()

        # ---- 事件处理 ----
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION and not state['game_over']:
                state['hover_pos'] = get_board_pos(*event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 限时模式 Toggle 开关
                if toggle_rect and toggle_rect.collidepoint(event.pos):
                    state['time_mode_active'] = not state.get('time_mode_active', False)
                    if state['time_mode_active']:
                        state['black_time'] = TIME_LIMIT_SECONDS
                        state['white_time'] = TIME_LIMIT_SECONDS
                    continue

                # 先检测主题切换点击
                theme_clicked = None
                if theme_rects:
                    for tname, trect in theme_rects.items():
                        if trect.collidepoint(event.pos):
                            theme_clicked = tname
                            break
                if theme_clicked and theme_clicked != get_current_theme():
                    apply_theme(theme_clicked)
                    label = THEME_LABELS.get(theme_clicked, theme_clicked)
                    toast_msg = f"已切换至「{label}」主题"
                    toast_timer = 90
                    continue

                # 检测按钮点击
                btn_name = get_button_clicked(event.pos, state['game_over'],
                                              state['move_count'], btn_area_top)

                if btn_name == "切换模式":
                    if game_mode == 'pvp':
                        game_mode = 'pve'
                    else:
                        # 从人机切换回双人：记住难度以便切回
                        game_mode = 'pvp'
                        ai_difficulty = state.get('ai_difficulty', 'medium')
                    state = _reset_game(ai_difficulty)
                    toast_msg = None
                    toast_timer = 0
                    anim_t = 0.0
                    continue

                elif btn_name == "再来一局":
                    state = _reset_game(ai_difficulty)
                    toast_msg = None
                    toast_timer = 0
                    anim_t = 0.0
                    continue

                elif btn_name == "悔棋":
                    if state['move_history']:
                        if game_mode == 'pve' and len(state['move_history']) >= 2:
                            r, c, p = state['move_history'].pop()
                            state['board'][r][c] = None
                            state['move_count'] -= 1
                            r, c, p = state['move_history'].pop()
                            state['board'][r][c] = None
                            state['move_count'] -= 1
                            state['current_player'] = 'black'
                            state['last_move'] = state['move_history'][-1][:2] if state['move_history'] else None
                            state['ai_thinking'] = False
                        else:
                            r, c, p = state['move_history'].pop()
                            state['board'][r][c] = None
                            state['move_count'] -= 1
                            state['current_player'] = p
                            state['last_move'] = state['move_history'][-1][:2] if state['move_history'] else None
                            state['ai_thinking'] = False
                        toast_msg = None
                        toast_timer = 0
                    else:
                        toast_msg = "当前没有棋子可悔"
                        toast_timer = 90
                    continue

                elif btn_name == "退出游戏":
                    pygame.quit()
                    sys.exit()

                # 棋盘落子
                if not state['game_over'] and not state['ai_thinking']:
                    # 人机模式下只允许玩家（黑棋）落子
                    if game_mode == 'pve' and state['current_player'] == 'white':
                        pass  # AI 回合，忽略玩家点击
                    else:
                        pos = get_board_pos(*event.pos)
                        if pos is not None:
                            row, col = pos
                            do_player_move(row, col)

        # ---- 绘制 ----
        draw_board(screen)

        # 棋子
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if state['board'][r][c] is not None:
                    draw_stone(screen, r, c, state['board'][r][c])

        # 最后一步标记（金色小圆环）
        if state['last_move'] is not None:
            lr, lc = state['last_move']
            lx = BOARD_ORIGIN_X + lc * CELL_SIZE
            ly = BOARD_ORIGIN_Y + lr * CELL_SIZE
            pygame.draw.circle(screen, COLOR_LAST_MOVE, (lx, ly), 5, 2)
            pygame.draw.circle(screen, COLOR_LAST_MOVE, (lx, ly), 2)

        # 胜利连线高亮
        if state['win_line'] is not None:
            sr, sc, er, ec = state['win_line']
            sx = BOARD_ORIGIN_X + sc * CELL_SIZE
            sy = BOARD_ORIGIN_Y + sr * CELL_SIZE
            ex = BOARD_ORIGIN_X + ec * CELL_SIZE
            ey = BOARD_ORIGIN_Y + er * CELL_SIZE
            # 粗金线底色
            pygame.draw.line(screen, COLOR_WIN_LINE_BASE, (sx, sy), (ex, ey), 6)
            # 细亮线内描
            pygame.draw.line(screen, COLOR_WIN_LINE_INNER, (sx, sy), (ex, ey), 3)
            # 脉冲光晕（随动画时间波动透明度）
            glow_alpha = int(120 + 40 * math.sin(anim_t * 4))
            glow_color = (*COLOR_WIN_LINE_GLOW[:3], glow_alpha)
            glow_surf = pygame.Surface((abs(ex - sx) + 14, abs(ey - sy) + 14), pygame.SRCALPHA)
            gx = (glow_surf.get_width() - abs(ex - sx)) // 2
            gy = (glow_surf.get_height() - abs(ey - sy)) // 2
            if abs(ex - sx) >= abs(ey - sy):
                pygame.draw.line(glow_surf, glow_color,
                                 (gx, gy), (gx + abs(ex - sx), gy + abs(ey - sy)), 10)
            else:
                pygame.draw.line(glow_surf, glow_color,
                                 (gx, gy), (gx + abs(ex - sx), gy + abs(ey - sy)), 10)
            screen.blit(glow_surf, (min(sx, ex) - 7, min(sy, ey) - 7))

        # 悬停预览
        if (state['hover_pos'] is not None and not state['game_over']
                and not state['ai_thinking']):
            row, col = state['hover_pos']
            if state['board'][row][col] is None:
                cx = BOARD_ORIGIN_X + col * CELL_SIZE
                cy = BOARD_ORIGIN_Y + row * CELL_SIZE
                preview_color = COLOR_HOVER_BLACK if state['current_player'] == 'black' else COLOR_HOVER_WHITE
                preview_alpha = COLOR_HOVER_BLACK_ALPHA if state['current_player'] == 'black' else COLOR_HOVER_WHITE_ALPHA
                preview = pygame.Surface((STONE_RADIUS * 2 + 4, STONE_RADIUS * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(preview, (*preview_color, preview_alpha),
                                   (STONE_RADIUS + 2, STONE_RADIUS + 2), STONE_RADIUS)
                screen.blit(preview, (cx - STONE_RADIUS - 2, cy - STONE_RADIUS - 2))

        # 胜利横幅
        if state['game_over'] and state['winner'] is not None:
            draw_win_banner(screen, state['winner'], anim_t, state.get('forbidden_reason'))

        # 右侧面板
        btn_area_top, theme_rects, toggle_rect = draw_panel(
            screen, state['current_player'], state['move_count'],
            state['game_over'], state['winner'],
            game_mode, state['ai_thinking'], anim_t,
            state.get('forbidden_reason'),
            state.get('ai_difficulty', 'medium'),
            black_time=state.get('black_time', TIME_LIMIT_SECONDS),
            white_time=state.get('white_time', TIME_LIMIT_SECONDS),
            time_mode_active=state.get('time_mode_active', False))

        # Toast 计时
        if toast_timer > 0:
            toast_timer -= 1
        else:
            toast_msg = None

        # 功能按钮（含 toast 提示）
        display_toast = toast_msg if toast_timer > 0 else None
        draw_buttons(screen, mouse_pos, state['game_over'], state['move_count'],
                     btn_area_top, display_toast)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
