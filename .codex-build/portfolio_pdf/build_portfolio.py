from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(r"G:\文档\作品集网站")
PUBLIC = ROOT / "public"
BUILD = ROOT / ".codex-build" / "portfolio_pdf"
TMP = ROOT / "tmp" / "pdfs" / "portfolio_assets"
OUTPUT = ROOT / "output" / "pdf" / "曹硕_个人作品集_求职版.pdf"

W, H = 960, 540
M = 48

BG = HexColor("#08090A")
BG_SOFT = HexColor("#101214")
PANEL = HexColor("#14171A")
TEXT = HexColor("#F3F0EA")
MUTED = HexColor("#AAA39D")
DIM = HexColor("#6E6B68")
LINE = HexColor("#333638")
ORANGE = HexColor("#FF633E")
ORANGE_2 = HexColor("#FF8B55")
BLACK = HexColor("#000000")

FONT_REG = "DengXian-Regular"
FONT_LIGHT = "DengXian-Light"
FONT_BOLD = "DengXian-Bold"
FONT_SERIF = "FangSong"
FONT_DISPLAY = FONT_REG


def register_fonts() -> None:
    global FONT_DISPLAY
    font_files = {
        FONT_REG: Path(r"C:\Windows\Fonts\Deng.ttf"),
        FONT_LIGHT: Path(r"C:\Windows\Fonts\Dengl.ttf"),
        FONT_BOLD: Path(r"C:\Windows\Fonts\Dengb.ttf"),
        FONT_SERIF: Path(r"C:\Windows\Fonts\simfang.ttf"),
    }
    for name, path in font_files.items():
        pdfmetrics.registerFont(TTFont(name, str(path)))

    anurati = PUBLIC / "fonts" / "Anurati-Regular.otf"
    try:
        pdfmetrics.registerFont(TTFont("Anurati", str(anurati)))
        FONT_DISPLAY = "Anurati"
    except Exception:
        FONT_DISPLAY = FONT_LIGHT


def optimize_image(src: Path, key: str, max_side: int = 1600, quality: int = 78) -> Path:
    dst = TMP / f"{key}.jpg"
    image = ImageOps.exif_transpose(Image.open(src))
    if image.mode not in ("RGB", "L"):
        base = Image.new("RGB", image.size, (8, 9, 10))
        if "A" in image.getbands():
            base.paste(image, mask=image.getchannel("A"))
        else:
            base.paste(image.convert("RGB"))
        image = base
    else:
        image = image.convert("RGB")
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    image.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    return dst


def extract_hero_still() -> Path | None:
    dst = TMP / "hero-still.jpg"
    if dst.exists():
        return dst
    video = ROOT / "src" / "assets" / "hero-background.mp4"
    try:
        import cv2

        cap = cv2.VideoCapture(str(video))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(1, frames // 3))
        ok, frame = cap.read()
        cap.release()
        if not ok:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = ImageEnhance.Contrast(image).enhance(1.08)
        image.save(dst, "JPEG", quality=90, optimize=True)
        return dst
    except Exception:
        return None


def asset(path: str, key: str | None = None, max_side: int = 1600, quality: int = 78) -> Path:
    src = ROOT / path
    return optimize_image(src, key or src.stem, max_side=max_side, quality=quality)


def rgba(c: canvas.Canvas, fill, alpha: float = 1.0) -> None:
    c.setFillColor(fill)
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(alpha)


def reset_alpha(c: canvas.Canvas) -> None:
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(1)
    if hasattr(c, "setStrokeAlpha"):
        c.setStrokeAlpha(1)


def background(c: canvas.Canvas, warm: bool = False) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    rgba(c, ORANGE if warm else HexColor("#24323A"), 0.07)
    c.circle(W * 0.82, H * 0.72, 220, fill=1, stroke=0)
    rgba(c, ORANGE_2, 0.035)
    c.circle(W * 0.15, H * 0.18, 180, fill=1, stroke=0)
    reset_alpha(c)


def footer(c: canvas.Canvas, page: int, section: str = "PORTFOLIO") -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(M, 24, W - M, 24)
    c.setFillColor(DIM)
    c.setFont(FONT_REG, 7.5)
    c.drawString(M, 10, "CAO SHUO / 曹硕")
    c.drawCentredString(W / 2, 10, section)
    c.drawRightString(W - M, 10, f"{page:02d}")


def label(c: canvas.Canvas, text: str, x: float, y: float, color=ORANGE) -> None:
    c.setFillColor(color)
    c.setFont(FONT_BOLD, 8)
    c.drawString(x, y, text.upper())


def title(c: canvas.Canvas, cn: str, en: str, page: int, section: str, x=M, y=H - 78) -> None:
    label(c, f"{page:02d} / {section}", x, y + 24)
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 28)
    c.drawString(x, y - 4, cn)
    c.setFillColor(MUTED)
    c.setFont(FONT_LIGHT, 10)
    c.drawString(x, y - 24, en.upper())


def paragraph_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if char == "\n":
            lines.append(current)
            current = ""
        elif pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def draw_paragraph(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    size: float = 11,
    leading: float | None = None,
    color=MUTED,
    font: str = FONT_REG,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.65
    lines = paragraph_lines(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFillColor(color)
    c.setFont(font, size)
    yy = y
    for line in lines:
        c.drawString(x, yy, line)
        yy -= leading
    return yy


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.width, im.height


def image_cover(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float, darken: float = 0) -> None:
    iw, ih = image_size(path)
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), dx, dy, dw, dh, mask="auto")
    if darken:
        rgba(c, BLACK, darken)
        c.rect(x, y, w, h, fill=1, stroke=0)
        reset_alpha(c)
    c.restoreState()


def image_contain(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float, bg=PANEL) -> None:
    c.setFillColor(bg)
    c.rect(x, y, w, h, fill=1, stroke=0)
    iw, ih = image_size(path)
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def image_frame(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float, mode="cover", caption: str | None = None) -> None:
    c.saveState()
    c.setStrokeColor(HexColor("#3A3D3F"))
    c.setLineWidth(0.7)
    c.rect(x, y, w, h, fill=0, stroke=1)
    if mode == "contain":
        image_contain(c, path, x + 1, y + 1, w - 2, h - 2)
    else:
        image_cover(c, path, x + 1, y + 1, w - 2, h - 2)
    c.restoreState()
    if caption:
        rgba(c, BG, 0.82)
        c.rect(x + 10, y + 10, min(w - 20, 180), 24, fill=1, stroke=0)
        reset_alpha(c)
        c.setFillColor(TEXT)
        c.setFont(FONT_REG, 8)
        c.drawString(x + 18, y + 18, caption)


def line_accent(c: canvas.Canvas, x: float, y: float, w: float = 42) -> None:
    c.setStrokeColor(ORANGE)
    c.setLineWidth(3)
    c.line(x, y, x + w, y)


def metric(c: canvas.Canvas, value: str, caption: str, x: float, y: float) -> None:
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 22)
    c.drawString(x, y, value)
    c.setFillColor(DIM)
    c.setFont(FONT_REG, 8)
    c.drawString(x, y - 18, caption)


def add_video_link(c: canvas.Canvas, x: float, y: float, url: str, text: str = "观看项目短片") -> None:
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 9)
    c.drawString(x, y, text)
    width = pdfmetrics.stringWidth(text, FONT_BOLD, 9)
    c.linkURL(url, (x, y - 3, x + width, y + 11), relative=0)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(0.6)
    c.line(x, y - 4, x + width, y - 4)


def new_page(c: canvas.Canvas, page: int, section: str, warm: bool = False) -> None:
    if page > 1:
        c.showPage()
    background(c, warm=warm)
    footer(c, page, section)


def build() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    register_fonts()

    # Optimized working copies keep the PDF sharp while remaining practical to send.
    hero = asset("public/portfolio/1532-park/renders/render-15.jpeg", "cover-landscape-night", 1800, 80)
    portrait = asset("src/assets/portrait-cao-shuo.png", "portrait", 1400, 80)
    park_cover = asset("public/portfolio/1532-park-cover.jpg", "park-cover", 2000, 80)
    park_board1 = asset("public/portfolio/1532-park/boards/board-01.jpg", "park-board-1", 2000, 80)
    park_board2 = asset("public/portfolio/1532-park/boards/board-02.jpg", "park-board-2", 2000, 80)
    office_board1 = asset("public/portfolio/1532-office/boards/board-01.jpg", "office-board-1", 2000, 80)
    office_board2 = asset("public/portfolio/1532-office/boards/board-02.jpg", "office-board-2", 2000, 80)

    def imgs(folder: str, numbers: list[str], prefix: str) -> list[Path]:
        base = ROOT / folder
        result = []
        for number in numbers:
            matches = sorted(base.glob(f"render-{number}.*"))
            if not matches:
                matches = sorted(base.glob(f"photo-{number}.*"))
            if not matches:
                raise FileNotFoundError(f"Missing image {folder} / {number}")
            result.append(optimize_image(matches[0], f"{prefix}-{number}"))
        return result

    park = imgs("public/portfolio/1532-park/renders", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], "park")
    office = imgs("public/portfolio/1532-office/renders", ["01", "02", "03", "06", "07", "08", "09", "10", "11", "12", "13", "14"], "office")
    concept = imgs("public/portfolio/concept-space/renders", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], "concept")
    family = imgs("public/portfolio/family-home/renders", ["01", "02", "03", "04", "05"], "family")
    courtyard = imgs("public/portfolio/courtyard/renders", ["01", "02", "03", "04"], "courtyard")
    apartment = imgs("public/portfolio/single-apartment/renders", ["01", "02", "03"], "apartment")
    apartment_photos = [
        optimize_image(ROOT / "public/portfolio/single-apartment/renders/photo-kitchen-01.png", "apartment-photo-kitchen"),
        optimize_image(ROOT / "public/portfolio/single-apartment/renders/photo-living-02.png", "apartment-photo-living"),
        optimize_image(ROOT / "public/portfolio/single-apartment/renders/photo-gaming-01.png", "apartment-photo-gaming"),
    ]

    c = canvas.Canvas(str(OUTPUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("曹硕个人作品集 - 求职版")
    c.setAuthor("曹硕")
    c.setSubject("环境设计 / 室内设计 / AIGC设计 / 景观规划")

    # 01 Cover
    image_cover(c, hero, 0, 0, W, H, darken=0.58)
    rgba(c, ORANGE, 0.8)
    c.rect(0, 0, 9, H, fill=1, stroke=0)
    reset_alpha(c)
    label(c, "INTERIOR / AIGC / LANDSCAPE", M, H - 64)
    c.setFillColor(TEXT)
    c.setFont(FONT_DISPLAY, 53 if FONT_DISPLAY == "Anurati" else 48)
    c.drawString(M, H - 148, "PORTFOLIO")
    c.setFont(FONT_BOLD, 20)
    c.drawString(M + 2, H - 186, "曹硕  CAO SHUO")
    c.setFillColor(MUTED)
    c.setFont(FONT_LIGHT, 11)
    c.drawString(M + 2, H - 214, "环境设计本科在读 / 室内设计 / AIGC设计 / 景观规划")
    line_accent(c, M + 2, 84, 64)
    c.setFillColor(TEXT)
    c.setFont(FONT_REG, 10)
    c.drawString(M + 2, 62, "SELECTED WORKS 2023-2026")

    # 02 Profile
    new_page(c, 2, "PROFILE", warm=True)
    title(c, "个人简介", "PROFILE", 2, "PROFILE")
    image_frame(c, portrait, M, 70, 300, 345, "contain")
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 24)
    c.drawString(386, 410, "曹硕")
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 11)
    c.drawString(386, 386, "环境设计 / AIGC设计")
    draw_paragraph(c, "我就读于潍坊学院环境设计专业，系统学习室内设计、景观规划、建筑设计与施工工艺，能够完成二维制图、三维效果呈现、图像后期、方案排版与视频演示。", 386, 350, 500, 11.2, 19)
    draw_paragraph(c, "我关注空间从前期分析、概念推演到视觉呈现的完整过程，并将 AIGC 用于方案比较、视觉控制和效率提升。", 386, 272, 500, 11.2, 19)
    metric(c, "3.86 / 4.0", "GPA", 386, 188)
    metric(c, "2 / 40", "学年成绩排名", 548, 188)
    metric(c, "7 / 40", "学年综测排名", 680, 188)
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 9)
    c.drawString(386, 118, "核心荣誉")
    draw_paragraph(c, "第十二届“广联达杯”BIM毕业设计创新大赛 B模块建筑设计AI+BIM应用与创新项目大赛一等奖", 386, 96, 500, 10.5, 17, TEXT, FONT_BOLD, 3)

    # 03 Contents
    new_page(c, 3, "CONTENTS")
    title(c, "作品目录", "SELECTED WORKS", 3, "CONTENTS")
    entries = [
        ("01", "潍坊市1532产业园改造", "景观更新 / 实践项目"),
        ("02", "1532办公空间设计", "办公空间 / 室内设计"),
        ("03", "海洋艺术与生态科技概念空间", "AIGC / 概念展馆"),
        ("04", "居住空间与庭院设计", "住宅 / 景观"),
        ("05", "单人公寓室内设计", "小户型 / 实景验证"),
    ]
    yy = 376
    for idx, name, typ in entries:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(M, yy - 20, W - M, yy - 20)
        c.setFillColor(ORANGE)
        c.setFont(FONT_BOLD, 11)
        c.drawString(M, yy, idx)
        c.setFillColor(TEXT)
        c.setFont(FONT_BOLD, 17)
        c.drawString(110, yy - 2, name)
        c.setFillColor(MUTED)
        c.setFont(FONT_REG, 9.5)
        c.drawRightString(W - M, yy, typ)
        yy -= 68

    # 04 Project 01 cover
    new_page(c, 4, "PROJECT 01")
    image_contain(c, park_cover, 535, 48, 350, 444, BG_SOFT)
    label(c, "PROJECT 01 / LANDSCAPE RENEWAL", M, 444)
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 30)
    c.drawString(M, 390, "潍坊市1532")
    c.drawString(M, 350, "产业园改造项目")
    line_accent(c, M, 318, 58)
    draw_paragraph(c, "以潍坊世纪公园更新为背景，围绕公共空间、生态休闲与城市记忆展开改造设计。项目以展板、效果图和短片形成完整的空间叙事。", M, 278, 410, 11.3, 19)
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 9)
    c.drawString(M, 160, "项目时间  2026.05 - 2026.06")
    c.drawString(M, 140, "项目类型  景观更新 / 实践项目")
    add_video_link(c, M, 102, "https://www.bilibili.com/video/BV1nRMh6LEZs?t=1.4")

    # 05 Boards
    new_page(c, 5, "PROJECT 01")
    title(c, "方案展板", "MASTER BOARDS", 5, "PROJECT 01")
    image_frame(c, park_board1, M, 50, 405, 382, "contain", "总体策略与空间系统")
    image_frame(c, park_board2, 507, 50, 405, 382, "contain", "节点设计与场景表达")

    # 06 Strategy
    new_page(c, 6, "PROJECT 01")
    title(c, "场地更新策略", "SITE RENEWAL STRATEGY", 6, "PROJECT 01")
    image_frame(c, park[0], M, 58, 554, 360, "cover", "生态休闲节点")
    image_frame(c, park[2], 626, 232, 286, 186, "cover", "公共空间视角")
    image_frame(c, park[3], 626, 58, 286, 152, "cover", "景观动线")

    # 07 Atmosphere
    new_page(c, 7, "PROJECT 01")
    title(c, "空间氛围与公共体验", "ATMOSPHERE AND PUBLIC EXPERIENCE", 7, "PROJECT 01")
    image_frame(c, park[6], M, 140, 864, 278, "cover")
    image_frame(c, park[7], M, 52, 272, 70, "cover")
    image_frame(c, park[9], 344, 52, 272, 70, "cover")
    image_frame(c, park[10], 640, 52, 272, 70, "cover")

    # 08 Nodes
    new_page(c, 8, "PROJECT 01")
    title(c, "节点深化", "DETAILS AND NODES", 8, "PROJECT 01")
    image_frame(c, park[1], M, 240, 416, 178, "cover", "场地细节")
    image_frame(c, park[4], 496, 240, 416, 178, "cover", "节点氛围")
    image_frame(c, park[5], M, 52, 268, 166, "cover")
    image_frame(c, park[8], 346, 52, 268, 166, "cover")
    image_frame(c, park[11], 644, 52, 268, 166, "cover")

    # 09 Project 02 boards
    new_page(c, 9, "PROJECT 02")
    label(c, "PROJECT 02 / INTERIOR DESIGN", M, 465)
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 27)
    c.drawString(M, 424, "1532办公空间设计")
    draw_paragraph(c, "围绕共享办公、会议交流、展览展示与休闲洽谈组织空间关系，在理性功能中加入更具温度的材质和灯光。", M, 390, 400, 10.5, 17)
    image_frame(c, office_board1, M, 56, 404, 300, "contain", "展板 01")
    image_frame(c, office_board2, 508, 56, 404, 408, "contain", "展板 02")

    # 10 Office overview
    new_page(c, 10, "PROJECT 02")
    title(c, "开放办公与公共界面", "OPEN OFFICE AND SHARED SPACE", 10, "PROJECT 02")
    image_frame(c, office[2], M, 58, 558, 360, "cover", "办公区白天")
    image_frame(c, office[4], 630, 240, 282, 178, "cover", "大厅空间")
    image_frame(c, office[7], 630, 58, 282, 160, "cover", "公共办公区域")

    # 11 Office functions
    new_page(c, 11, "PROJECT 02")
    title(c, "功能空间", "WORKPLACE PROGRAM", 11, "PROJECT 02")
    image_frame(c, office[0], M, 240, 416, 178, "cover", "会议桌细节")
    image_frame(c, office[1], 496, 240, 416, 178, "cover", "吧台空间")
    image_frame(c, office[3], M, 52, 416, 166, "cover", "创意会议室")
    image_frame(c, office[5], 496, 52, 416, 166, "cover", "隔音舱")

    # 12 Office details
    new_page(c, 12, "PROJECT 02")
    title(c, "材质、灯光与交流场景", "MATERIAL, LIGHT AND COMMUNICATION", 12, "PROJECT 02")
    image_frame(c, office[6], M, 238, 416, 180, "cover", "夜间办公")
    image_frame(c, office[8], 496, 238, 416, 180, "cover", "机房空间")
    image_frame(c, office[9], M, 52, 268, 164, "cover", "景观休闲区")
    image_frame(c, office[10], 346, 52, 268, 164, "cover", "私密洽谈室")
    image_frame(c, office[11], 644, 52, 268, 164, "cover", "展览空间")

    # 13 Project 03 cover
    new_page(c, 13, "PROJECT 03", warm=True)
    image_cover(c, concept[7], 0, 0, W, H, darken=0.52)
    rgba(c, BLACK, 0.3)
    c.rect(0, 0, 500, H, fill=1, stroke=0)
    reset_alpha(c)
    label(c, "PROJECT 03 / AIGC CONCEPT SPACE", M, 448)
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 31)
    c.drawString(M, 392, "海洋艺术与生态科技")
    c.drawString(M, 350, "概念空间")
    line_accent(c, M, 316, 58)
    draw_paragraph(c, "以海洋艺术、生态科技与未来展陈为关键词，探索建筑体量、沉浸空间和自然意象之间的关系。", M, 276, 390, 11, 19, TEXT)
    add_video_link(c, M, 108, "https://www.bilibili.com/video/BV1pXMh62EA9?t=37.1", "观看海洋艺术展馆短片")

    # 14 Concept exterior
    new_page(c, 14, "PROJECT 03")
    title(c, "建筑形态与场景叙事", "FORM AND SCENARIO", 14, "PROJECT 03")
    image_frame(c, concept[0], M, 230, 416, 188, "cover", "建筑全貌")
    image_frame(c, concept[1], 496, 230, 416, 188, "cover", "建筑特写")
    image_frame(c, concept[8], M, 52, 416, 156, "cover", "室外摆拍")
    image_frame(c, concept[11], 496, 52, 416, 156, "cover", "蝴蝶意象")

    # 15 Concept interior
    new_page(c, 15, "PROJECT 03")
    title(c, "沉浸式展陈空间", "IMMERSIVE EXHIBITION", 15, "PROJECT 03")
    image_frame(c, concept[2], M, 238, 416, 180, "cover", "一层空间")
    image_frame(c, concept[3], 496, 238, 416, 180, "cover", "二层空间")
    image_frame(c, concept[4], M, 52, 268, 164, "cover", "俯视关系")
    image_frame(c, concept[5], 346, 52, 268, 164, "cover", "侧向界面")
    image_frame(c, concept[6], 644, 52, 268, 164, "cover", "室外瀑布")

    # 16 Concept details
    new_page(c, 16, "PROJECT 03")
    title(c, "AIGC视觉深化", "AIGC VISUAL DEVELOPMENT", 16, "PROJECT 03")
    image_frame(c, concept[9], M, 58, 560, 360, "cover", "人物与空间尺度")
    image_frame(c, concept[10], 634, 236, 278, 182, "cover", "细节摄影")
    draw_paragraph(c, "通过多轮变量控制和结果筛选，将海洋意象转译为体量、材质与空间氛围。AIGC用于快速比较方案方向，最终结果仍以空间逻辑和使用体验为判断标准。", 634, 192, 278, 10.2, 17)

    # 17 Residential
    new_page(c, 17, "PROJECT 04")
    title(c, "居住空间与庭院", "RESIDENTIAL AND COURTYARD", 17, "PROJECT 04")
    image_frame(c, family[0], M, 212, 560, 206, "cover", "三口之家侘寂风住宅")
    image_frame(c, courtyard[0], 634, 212, 278, 206, "cover", "庭院景观设计")
    draw_paragraph(c, "住宅以低饱和材质、自然肌理和柔和光线塑造安静的居住氛围；庭院通过归家路径、停留节点和夜景照明组织户外生活。", M, 164, 864, 11, 19)
    c.setFillColor(DIM)
    c.setFont(FONT_REG, 9)
    c.drawString(M, 84, "设计关注：家庭动线 / 材质触感 / 植物层次 / 夜间体验")

    # 18 Residential details
    new_page(c, 18, "PROJECT 04")
    title(c, "室内细节与庭院节点", "DETAILS AND LANDSCAPE NODES", 18, "PROJECT 04")
    image_frame(c, family[1], M, 260, 268, 158, "cover", "餐厅")
    image_frame(c, family[2], 346, 260, 268, 158, "cover", "直播间")
    image_frame(c, family[3], 644, 260, 268, 158, "cover", "老人房")
    image_frame(c, courtyard[1], M, 52, 268, 186, "cover", "后院")
    image_frame(c, courtyard[2], 346, 52, 268, 186, "cover", "侧道夜景")
    image_frame(c, courtyard[3], 644, 52, 268, 186, "cover", "影壁墙")

    # 19 Apartment
    new_page(c, 19, "PROJECT 05")
    title(c, "单人公寓：方案与实景", "SINGLE APARTMENT / DESIGN TO REALITY", 19, "PROJECT 05")
    image_frame(c, apartment[0], M, 264, 268, 154, "cover", "方案主视角")
    image_frame(c, apartment[1], 346, 264, 268, 154, "cover", "厨房方案")
    image_frame(c, apartment[2], 644, 264, 268, 154, "cover", "电竞房方案")
    image_frame(c, apartment_photos[0], M, 52, 268, 190, "cover", "厨房实景")
    image_frame(c, apartment_photos[1], 346, 52, 268, 190, "cover", "客厅实景")
    image_frame(c, apartment_photos[2], 644, 52, 268, 190, "cover", "电竞房实景")

    # 20 Capability and contact
    new_page(c, 20, "PROFILE", warm=True)
    label(c, "CAPABILITY / HONORS / CONTACT", M, 464)
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 30)
    c.drawString(M, 420, "空间设计与AIGC协同")
    skills = [
        ("01", "跨领域空间视角", "在室内、景观与建筑尺度之间组织空间逻辑。"),
        ("02", "AIGC设计思维", "通过变量控制、筛选和迭代辅助方案判断。"),
        ("03", "视觉表达与叙事", "将概念转化为效果图、展板、短片和网页。"),
        ("04", "执行与协作", "整理需求、回应反馈并持续推进方案。"),
    ]
    sy = 350
    for idx, name, desc in skills:
        c.setFillColor(ORANGE)
        c.setFont(FONT_BOLD, 9)
        c.drawString(M, sy, idx)
        c.setFillColor(TEXT)
        c.setFont(FONT_BOLD, 12)
        c.drawString(82, sy, name)
        c.setFillColor(MUTED)
        c.setFont(FONT_REG, 9.2)
        c.drawString(248, sy, desc)
        sy -= 44
    c.setStrokeColor(LINE)
    c.line(M, 150, W - M, 150)
    c.setFillColor(TEXT)
    c.setFont(FONT_BOLD, 18)
    c.drawString(M, 112, "曹硕  CAO SHUO")
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 10)
    c.drawString(M, 86, "潍坊学院 环境设计本科 / 预计2027年毕业")
    c.drawString(490, 112, "133 6144 4417")
    c.drawString(490, 86, "fengfan3812@gmail.com")
    c.linkURL("mailto:fengfan3812@gmail.com", (490, 80, 700, 102), relative=0)
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 9)
    c.drawRightString(W - M, 112, "求职方向")
    c.setFillColor(TEXT)
    c.setFont(FONT_REG, 10)
    c.drawRightString(W - M, 86, "公共空间设计 / 室内设计 / AIGC设计")

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
