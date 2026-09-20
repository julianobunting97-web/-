from __future__ import annotations

import hashlib
import html
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
OUTPUT = ROOT / "output" / "pdf" / "cao-shuo-portfolio.pdf"
CACHE = ROOT / "tmp" / "pdfs" / "cache"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 34

BG = colors.HexColor("#080708")
PANEL = colors.HexColor("#111114")
PANEL_2 = colors.HexColor("#17171b")
TEXT = colors.HexColor("#F4F0EA")
MUTED = colors.HexColor("#A39A95")
DIM = colors.HexColor("#6E6865")
ACCENT = colors.HexColor("#FF6A32")
ACCENT_2 = colors.HexColor("#FF9A61")
BLUE = colors.HexColor("#8EA7B7")
LINE = colors.HexColor("#2B292B")

FONT_REGULAR = "CN-Regular"
FONT_BOLD = "CN-Bold"

PORTRAIT = ROOT / "src" / "assets" / "portrait-cao-shuo.png"
ANURATI = PUBLIC / "fonts" / "Anurati-Regular.otf"


PROJECTS = [
    {
        "index": "01",
        "slug": "1532-park",
        "title": "潍坊市 1532 产业园改造项目",
        "category": "景观更新 / 实践项目",
        "period": "2026.05 - 2026.06",
        "description": "以潍坊世纪公园更新为背景，围绕公共空间、生态休闲与城市记忆展开改造设计，通过展板、效果图与短片呈现完整方案叙事。",
        "tags": ["公共空间", "生态休闲", "城市记忆", "短片表达"],
        "cover": "portfolio/1532-park-cover.jpg",
        "boards": [
            "portfolio/1532-park/boards/board-01.jpg",
            "portfolio/1532-park/boards/board-02.jpg",
        ],
        "renders": [f"portfolio/1532-park/renders/render-{i:02d}.{ext}" for i, ext in [
            (1, "jpeg"), (2, "png"), (3, "jpeg"), (5, "jpeg"), (8, "jpeg"), (11, "jpeg")
        ]],
        "video": "https://www.bilibili.com/video/BV1nRMh6LEZs?t=1.4",
    },
    {
        "index": "02",
        "slug": "1532-office",
        "title": "1532 办公空间设计",
        "category": "办公空间 / 室内设计",
        "period": "空间改造",
        "description": "围绕共享办公、会议交流、展览展示与休闲洽谈组织空间关系，在理性功能中加入更具温度的材质、灯光和开放式办公体验。",
        "tags": ["共享办公", "会议交流", "展览展示", "休闲洽谈"],
        "cover": "portfolio/1532-office-cover.png",
        "boards": [
            "portfolio/1532-office/boards/board-01.jpg",
            "portfolio/1532-office/boards/board-02.jpg",
        ],
        "renders": [f"portfolio/1532-office/renders/render-{i:02d}.{ext}" for i, ext in [
            (1, "jpeg"), (2, "png"), (3, "png"), (6, "jpeg"), (10, "png"), (14, "png")
        ]],
    },
    {
        "index": "03",
        "slug": "family-home",
        "title": "三口之家侘寂风住宅设计",
        "category": "住宅空间 / 室内设计",
        "period": "家居方案",
        "description": "以低饱和材质、自然肌理和柔和光线塑造安静克制的居住氛围，兼顾家庭成员的生活动线、休憩需求与空间情绪。",
        "tags": ["客厅", "餐厅", "直播间", "老人房"],
        "cover": "portfolio/family-home-cover.jpeg",
        "renders": [f"portfolio/family-home/renders/render-{i:02d}.{ext}" for i, ext in [
            (1, "jpeg"), (2, "jpeg"), (3, "png"), (4, "png"), (5, "png")
        ]],
    },
    {
        "index": "04",
        "slug": "single-apartment",
        "title": "单人公寓室内设计",
        "category": "小户型 / 室内设计",
        "period": "居住空间",
        "description": "针对单人生活方式重构紧凑空间的功能效率，强化厨房、休息、娱乐和收纳之间的连续性，让小空间具备完整生活场景。",
        "tags": ["厨房", "电竞房", "紧凑动线", "功能整合"],
        "cover": "portfolio/single-apartment-cover.png",
        "renders": [
            "portfolio/single-apartment/renders/render-01.png",
            "portfolio/single-apartment/renders/render-02.jpeg",
            "portfolio/single-apartment/renders/render-03.jpeg",
        ],
        "photos": [
            "portfolio/single-apartment/renders/photo-kitchen-01.png",
            "portfolio/single-apartment/renders/photo-living-01.png",
            "portfolio/single-apartment/renders/photo-living-02.png",
            "portfolio/single-apartment/renders/photo-living-03.png",
            "portfolio/single-apartment/renders/photo-living-04.png",
            "portfolio/single-apartment/renders/photo-gaming-01.png",
        ],
    },
    {
        "index": "05",
        "slug": "courtyard",
        "title": "庭院景观设计",
        "category": "庭院营造 / 景观设计",
        "period": "庭院方案",
        "description": "通过前院、后院、侧道和影壁墙组织归家路径与停留节点，结合夜景照明与植物层次，营造安静、有秩序的户外生活空间。",
        "tags": ["前院", "后院", "侧道夜景", "影壁墙"],
        "cover": "portfolio/courtyard-cover.jpeg",
        "renders": [f"portfolio/courtyard/renders/render-{i:02d}.jpeg" for i in range(1, 5)],
    },
    {
        "index": "06",
        "slug": "concept-space",
        "title": "海洋艺术与生态科技概念空间",
        "category": "概念空间 / AIGC 设计",
        "period": "概念展馆",
        "description": "以海洋艺术、生态科技与未来展陈为关键词，探索建筑体量、沉浸式空间和自然意象之间的关系，形成更具叙事感的概念场景。",
        "tags": ["概念建筑", "生态科技", "沉浸展陈", "AIGC"],
        "cover": "portfolio/concept-space-cover.jpg",
        "renders": [f"portfolio/concept-space/renders/render-{i:02d}.{ext}" for i, ext in [
            (1, "png"), (2, "png"), (3, "jpg"), (4, "png"), (7, "png"), (8, "png"), (10, "png"), (12, "png")
        ]],
        "video": "https://www.bilibili.com/video/BV1pXMh62EA9?t=37.1",
    },
]

STRENGTHS = [
    ("01", "跨领域空间视角", "在室内、景观与建筑尺度下组织空间逻辑，把场地、功能与体验连接起来。"),
    ("02", "AIGC 设计思维", "通过控制变量、筛选结果与持续迭代，让 AI 服务于空间逻辑和设计判断。"),
    ("03", "视觉表达与方案叙事", "将空间概念转化为效果图、展板、短片与网页，让项目亮点被清晰看见。"),
    ("04", "细节意识与协作能力", "关注材料、尺度、灯光与节点细节，在反馈与协作中推动方案完整呈现。"),
]

HONORS = [
    "普通话二级甲等",
    "2024 学年暑期“三下乡”社会实践优秀个人",
    "2023-2024 学年潍坊学院三等奖学金",
    "2024-2025 学年潍坊学院优秀学生",
    "2024-2025 学年潍坊学院二等奖学金",
]


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, r"C:\Windows\Fonts\msyh.ttc"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\msyhbd.ttc"))


def source_path(relative: str) -> Path:
    return PUBLIC / relative


def hex_with_alpha(color: colors.Color, alpha: float) -> colors.Color:
    return colors.Color(color.red, color.green, color.blue, alpha=alpha)


def prepared_image(path: Path, width_pt: float, height_pt: float, mode: str = "cover") -> Path:
    key = f"{path.resolve()}|{round(width_pt, 2)}|{round(height_pt, 2)}|{mode}".encode("utf-8")
    output = CACHE / f"{hashlib.sha1(key).hexdigest()}.jpg"
    if output.exists() and output.stat().st_mtime >= path.stat().st_mtime:
        return output

    CACHE.mkdir(parents=True, exist_ok=True)
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        target_w = max(320, min(2400, int(width_pt * 2.5)))
        target_h = max(240, min(1800, int(height_pt * 2.5)))
        if mode.startswith("cover"):
            image = ImageOps.fit(image, (target_w, target_h), method=Image.Resampling.LANCZOS)
        else:
            image.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
            background = Image.new("RGB", (target_w, target_h), (17, 17, 20))
            offset = ((target_w - image.width) // 2, (target_h - image.height) // 2)
            background.paste(image, offset)
            image = background
        if mode == "cover-dark":
            image = ImageEnhance.Brightness(image).enhance(0.42)
        image.save(output, "JPEG", quality=86, optimize=True, progressive=True)
    return output


def draw_image(c: canvas.Canvas, path: Path, x: float, y: float, width: float, height: float,
               mode: str = "cover", radius: float = 0) -> None:
    image = prepared_image(path, width, height, mode)
    c.saveState()
    if radius:
        clip = c.beginPath()
        clip.roundRect(x, y, width, height, radius)
        c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(str(image), x, y, width, height, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def draw_background(c: canvas.Canvas, accent: bool = True) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    if accent:
        c.setFillColor(colors.HexColor("#2A130F"))
        c.circle(PAGE_W - 35, PAGE_H - 35, 130, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#111A20"))
        c.circle(80, 30, 160, stroke=0, fill=1)


def draw_footer(c: canvas.Canvas, page_no: int, chapter: str = "PORTFOLIO") -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN, 24, PAGE_W - MARGIN, 24)
    c.setFont("Helvetica", 7)
    c.setFillColor(DIM)
    c.drawString(MARGIN, 11, f"CAO SHUO / {chapter}")
    c.drawRightString(PAGE_W - MARGIN, 11, f"{page_no:02d}")


def draw_label(c: canvas.Canvas, text: str, x: float, y: float, color=ACCENT) -> None:
    c.setFillColor(color)
    c.roundRect(x, y - 4, 7, 7, 2, stroke=0, fill=1)
    c.setFont("Helvetica", 7.6)
    c.setFillColor(MUTED)
    c.drawString(x + 14, y - 2, text.upper())


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float,
              font: str = FONT_REGULAR, color=TEXT) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def draw_paragraph(c: canvas.Canvas, text: str, x: float, top: float, width: float,
                   size: float = 10, leading: float | None = None, color=MUTED,
                   font: str = FONT_REGULAR, max_height: float = 300) -> float:
    style = ParagraphStyle(
        "body",
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.7,
        textColor=color,
        alignment=TA_LEFT,
        wordWrap="CJK",
        spaceAfter=0,
    )
    paragraph = Paragraph(html.escape(text), style)
    _, height = paragraph.wrap(width, max_height)
    paragraph.drawOn(c, x, top - height)
    return top - height


def draw_tags(c: canvas.Canvas, tags: list[str], x: float, y: float, max_width: float) -> float:
    cursor_x = x
    cursor_y = y
    for tag in tags:
        width = max(48, pdfmetrics.stringWidth(tag, FONT_REGULAR, 8) + 22)
        if cursor_x + width > x + max_width:
            cursor_x = x
            cursor_y -= 28
        c.setFillColor(PANEL_2)
        c.roundRect(cursor_x, cursor_y, width, 20, 10, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.roundRect(cursor_x, cursor_y, width, 20, 10, stroke=1, fill=0)
        c.setFillColor(MUTED)
        c.setFont(FONT_REGULAR, 7.5)
        c.drawCentredString(cursor_x + width / 2, cursor_y + 6.2, tag)
        cursor_x += width + 7
    return cursor_y


def render_anurati_title(text: str) -> Path:
    output = CACHE / "cover-title.png"
    if output.exists():
        return output
    CACHE.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(str(ANURATI), 150)
    tracking = 11
    widths = [font.getlength(char) for char in text]
    total = int(sum(widths) + tracking * (len(text) - 1) + 24)
    image = Image.new("RGBA", (total, 190), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    x = 12
    for char, width in zip(text, widths):
        draw.text((x, 10), char, font=font, fill=(255, 122, 49, 255))
        x += width + tracking
    image.save(output)
    return output


def cover_page(c: canvas.Canvas) -> None:
    cover = source_path("portfolio/concept-space/renders/render-02.png")
    draw_image(c, cover, 0, 0, PAGE_W, PAGE_H, "cover-dark")
    c.setFillColor(colors.HexColor("#090809"))
    c.rect(0, 0, 470, PAGE_H, stroke=0, fill=1)

    draw_label(c, "INTERIOR / AIGC / LANDSCAPE", 50, PAGE_H - 54)
    title = render_anurati_title("PORTFOLIO")
    c.drawImage(str(title), 48, 280, 510, 112, mask="auto", preserveAspectRatio=True)
    draw_text(c, "曹硕", 52, 244, 30, FONT_BOLD)
    draw_text(c, "环境设计 · 空间表达 · AIGC 创作", 52, 215, 12, FONT_REGULAR, MUTED)
    c.setFillColor(ACCENT)
    c.rect(52, 185, 92, 3, stroke=0, fill=1)

    metrics = [("3.86", "GPA"), ("2 / 40", "学年成绩排名"), ("2027", "毕业时间")]
    for idx, (value, label) in enumerate(metrics):
        x = 52 + idx * 135
        draw_text(c, value, x, 112, 17, FONT_BOLD)
        draw_text(c, label, x, 92, 7.5, FONT_REGULAR, MUTED)

    draw_text(c, "SELECTED WORKS 2023-2026", 52, 45, 7.5, "Helvetica", MUTED)
    c.setTitle("曹硕个人作品集")
    c.setAuthor("曹硕")
    c.setSubject("环境设计 / 室内设计 / 景观规划 / AIGC 设计")
    c.bookmarkPage("cover")
    c.addOutlineEntry("封面", "cover", level=0, closed=False)
    c.showPage()


def about_page(c: canvas.Canvas, page_no: int) -> None:
    draw_background(c)
    draw_label(c, "01 / PROFILE", MARGIN, PAGE_H - 46)
    draw_text(c, "个人经历", MARGIN, PAGE_H - 82, 27, FONT_BOLD)

    draw_image(c, PORTRAIT, MARGIN, 54, 258, 430, "contain", 18)
    c.saveState()
    c.setFillAlpha(0.72)
    c.setFillColor(colors.black)
    c.rect(MARGIN, 54, 258, 76, stroke=0, fill=1)
    c.restoreState()
    draw_text(c, "曹硕", MARGIN + 18, 95, 20, FONT_BOLD)
    draw_text(c, "AIGC DESIGNER", MARGIN + 18, 76, 7.5, "Helvetica", MUTED)

    right_x = 322
    draw_text(c, "以空间为媒介，", right_x, 470, 23, FONT_BOLD)
    draw_text(c, "连接设计逻辑、视觉表达与 AIGC 创作。", right_x, 437, 23, FONT_BOLD)
    bottom = draw_paragraph(
        c,
        "我就读于潍坊学院环境设计专业，系统学习室内设计、景观规划、建筑设计与施工工艺，熟练掌握 AutoCAD、3DMax、Photoshop 及 AIGC 工具，能够完成二维制图、三维效果呈现、图像后期、方案排版与视频演示。",
        right_x,
        396,
        468,
        9.5,
        16,
    )
    draw_paragraph(
        c,
        "我关注空间从前期分析、概念推演到视觉呈现与方案落地的完整过程，也将 AIGC 作为辅助设计判断和提升效率的方法。曾在校园文化墙项目中完成资料分析、主题提炼、提示词优化与视觉控制，将项目周期压缩至原来的一半。",
        right_x,
        bottom - 18,
        468,
        9.5,
        16,
    )

    stats = [("3.86 / 4.0", "GPA"), ("2 / 40", "学年成绩排名"), ("7 / 40", "学年综测排名"), ("10+", "设计与 AI 工具")]
    for idx, (value, label) in enumerate(stats):
        x = right_x + (idx % 2) * 235
        y = 155 - (idx // 2) * 78
        c.setFillColor(PANEL)
        c.roundRect(x, y, 220, 60, 13, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.roundRect(x, y, 220, 60, 13, stroke=1, fill=0)
        draw_text(c, value, x + 15, y + 29, 16, FONT_BOLD)
        draw_text(c, label, x + 15, y + 12, 7.2, FONT_REGULAR, MUTED)

    draw_footer(c, page_no, "PROFILE")
    c.bookmarkPage("profile")
    c.addOutlineEntry("个人经历", "profile", level=0, closed=False)
    c.showPage()


def contents_page(c: canvas.Canvas, page_no: int) -> None:
    draw_background(c)
    draw_label(c, "02 / INDEX & METHOD", MARGIN, PAGE_H - 46)
    draw_text(c, "项目目录 / 设计方法", MARGIN, PAGE_H - 82, 27, FONT_BOLD)

    left_w = 430
    y = 445
    for project in PROJECTS:
        c.setStrokeColor(LINE)
        c.line(MARGIN, y - 11, MARGIN + left_w, y - 11)
        draw_text(c, project["index"], MARGIN, y + 8, 8, "Helvetica", ACCENT)
        draw_text(c, project["title"], MARGIN + 44, y + 3, 12, FONT_BOLD)
        draw_text(c, project["category"], MARGIN + 44, y - 15, 7.5, FONT_REGULAR, MUTED)
        y -= 66

    right_x = 510
    for idx, (number, title, body) in enumerate(STRENGTHS):
        y = 415 - idx * 104
        c.setFillColor(PANEL)
        c.roundRect(right_x, y, 295, 86, 14, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.roundRect(right_x, y, 295, 86, 14, stroke=1, fill=0)
        draw_text(c, number, right_x + 16, y + 60, 8, "Helvetica", ACCENT)
        draw_text(c, title, right_x + 52, y + 56, 11, FONT_BOLD)
        draw_paragraph(c, body, right_x + 52, y + 39, 225, 7.2, 12, MUTED, max_height=42)

    draw_footer(c, page_no, "INDEX")
    c.bookmarkPage("index")
    c.addOutlineEntry("项目目录与个人优势", "index", level=0, closed=False)
    c.showPage()


def project_intro_page(c: canvas.Canvas, project: dict, page_no: int) -> None:
    draw_background(c)
    image_x, image_y, image_w, image_h = MARGIN, 48, 510, 500
    draw_image(c, source_path(project["cover"]), image_x, image_y, image_w, image_h, "cover", 18)

    right_x = 575
    draw_text(c, project["index"], right_x, 515, 50, "Helvetica-Bold", hex_with_alpha(ACCENT, 0.9))
    draw_text(c, project["category"], right_x, 475, 8, FONT_REGULAR, ACCENT_2)
    title_bottom = draw_paragraph(c, project["title"], right_x, 448, 230, 20, 27, TEXT, FONT_BOLD, 100)
    draw_text(c, project["period"], right_x, title_bottom - 24, 8, FONT_REGULAR, MUTED)
    description_bottom = draw_paragraph(c, project["description"], right_x, title_bottom - 54, 230, 9, 16, MUTED, max_height=150)
    draw_tags(c, project["tags"], right_x, description_bottom - 38, 230)

    if project.get("video"):
        link_y = 64
        c.setFillColor(ACCENT)
        c.roundRect(right_x, link_y, 180, 31, 15.5, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 8)
        c.drawCentredString(right_x + 90, link_y + 10, "观看项目短片  ↗")
        c.linkURL(project["video"], (right_x, link_y, right_x + 180, link_y + 31), relative=0)

    draw_footer(c, page_no, project["slug"].upper())
    anchor = f"project-{project['slug']}"
    c.bookmarkPage(anchor)
    c.addOutlineEntry(project["title"], anchor, level=0, closed=False)
    c.showPage()


def board_page(c: canvas.Canvas, project: dict, board: str, board_index: int, page_no: int) -> None:
    draw_background(c, accent=False)
    draw_label(c, f"{project['index']} / PRESENTATION BOARD", MARGIN, PAGE_H - 42)
    draw_text(c, f"展板 {board_index:02d}", MARGIN, PAGE_H - 76, 20, FONT_BOLD)
    draw_text(c, project["title"], MARGIN, PAGE_H - 98, 8, FONT_REGULAR, MUTED)

    board_w = 354
    board_h = 501
    board_x = (PAGE_W - board_w) / 2
    board_y = 42
    c.setFillColor(PANEL)
    c.roundRect(board_x - 8, board_y - 8, board_w + 16, board_h + 16, 8, stroke=0, fill=1)
    draw_image(c, source_path(board), board_x, board_y, board_w, board_h, "contain", 3)

    draw_text(c, "FULL BOARD", MARGIN, 74, 7, "Helvetica", ACCENT)
    draw_paragraph(c, "展板保留完整原始比例，可在 PDF 中放大查看图纸、分析与设计说明。", MARGIN, 60, 150, 7.5, 13, MUTED)
    draw_text(c, f"{board_index:02d} / {len(project['boards']):02d}", PAGE_W - 132, 72, 18, "Helvetica-Bold", DIM)
    draw_footer(c, page_no, project["slug"].upper())
    c.showPage()


def gallery_page(c: canvas.Canvas, project: dict, images: list[str], page_no: int, label: str = "SELECTED VIEWS") -> None:
    draw_background(c, accent=False)
    draw_label(c, f"{project['index']} / {label}", MARGIN, PAGE_H - 42)
    draw_text(c, project["title"], MARGIN, PAGE_H - 75, 20, FONT_BOLD)

    gap = 10
    grid_top = PAGE_H - 105
    columns = 2 if len(images) == 4 else 3
    card_w = (PAGE_W - 2 * MARGIN - (columns - 1) * gap) / columns
    card_h = 205
    for idx, image in enumerate(images[:6]):
        col = idx % columns
        row = idx // columns
        x = MARGIN + col * (card_w + gap)
        y = grid_top - (row + 1) * card_h - row * gap
        draw_image(c, source_path(image), x, y, card_w, card_h, "cover", 10)
        c.saveState()
        c.setFillAlpha(0.6)
        c.setFillColor(colors.black)
        c.rect(x, y, card_w, 28, stroke=0, fill=1)
        c.restoreState()
        draw_text(c, f"{idx + 1:02d}", x + 10, y + 10, 7, "Helvetica-Bold", ACCENT)
        draw_text(c, "VIEW", x + 31, y + 10, 6.5, "Helvetica", TEXT)

    draw_footer(c, page_no, project["slug"].upper())
    c.showPage()


def feature_collage_page(c: canvas.Canvas, project: dict, page_no: int) -> None:
    draw_background(c, accent=False)
    draw_label(c, f"{project['index']} / SELECTED PROJECT", MARGIN, PAGE_H - 42)
    draw_text(c, project["title"], MARGIN, PAGE_H - 75, 20, FONT_BOLD)

    renders = project["renders"]
    x0, y0 = MARGIN, 48
    main_w, main_h = 520, 440
    draw_image(c, source_path(renders[0]), x0, y0, main_w, main_h, "cover", 13)
    small_x = x0 + main_w + 12
    small_w = PAGE_W - MARGIN - small_x
    small_h = (main_h - 18) / 3
    for idx, image in enumerate(renders[1:4]):
        y = y0 + main_h - (idx + 1) * small_h - idx * 9
        draw_image(c, source_path(image), small_x, y, small_w, small_h, "cover", 10)

    c.saveState()
    c.setFillAlpha(0.78)
    c.setFillColor(colors.black)
    c.roundRect(x0 + 18, y0 + 18, 310, 78, 12, stroke=0, fill=1)
    c.restoreState()
    draw_text(c, project["category"], x0 + 34, y0 + 69, 7.5, FONT_REGULAR, ACCENT_2)
    draw_paragraph(c, project["description"], x0 + 34, y0 + 55, 278, 7.4, 12, TEXT, max_height=45)

    draw_footer(c, page_no, project["slug"].upper())
    anchor = f"project-{project['slug']}"
    c.bookmarkPage(anchor)
    c.addOutlineEntry(project["title"], anchor, level=0, closed=False)
    c.showPage()


def single_render_page(c: canvas.Canvas, project: dict, page_no: int) -> None:
    draw_background(c, accent=False)
    draw_label(c, f"{project['index']} / DESIGN RENDERS", MARGIN, PAGE_H - 42)
    draw_text(c, project["title"], MARGIN, PAGE_H - 75, 20, FONT_BOLD)
    images = project["renders"]
    draw_image(c, source_path(images[0]), MARGIN, 48, 490, 440, "cover", 13)
    draw_image(c, source_path(images[1]), 536, 273, 271, 215, "cover", 11)
    draw_image(c, source_path(images[2]), 536, 48, 271, 215, "cover", 11)
    draw_footer(c, page_no, project["slug"].upper())
    anchor = f"project-{project['slug']}"
    c.bookmarkPage(anchor)
    c.addOutlineEntry(project["title"], anchor, level=0, closed=False)
    c.showPage()


def concept_overview_page(c: canvas.Canvas, project: dict, page_no: int) -> None:
    draw_background(c, accent=False)
    hero = source_path(project["renders"][1])
    draw_image(c, hero, 0, 0, PAGE_W, PAGE_H, "cover-dark")
    c.setFillColor(BG)
    c.roundRect(42, 52, 352, 490, 22, stroke=0, fill=1)
    draw_label(c, "06 / AIGC CONCEPT SPACE", 68, 510)
    draw_text(c, "海洋艺术与", 68, 448, 30, FONT_BOLD)
    draw_text(c, "生态科技概念空间", 68, 407, 30, FONT_BOLD)
    draw_paragraph(c, project["description"], 68, 360, 280, 9.3, 17, MUTED)
    draw_tags(c, project["tags"], 68, 245, 280)
    c.setFillColor(ACCENT)
    c.roundRect(68, 98, 188, 34, 17, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 8.5)
    c.drawCentredString(162, 109, "观看项目短片  ↗")
    c.linkURL(project["video"], (68, 98, 256, 132), relative=0)
    draw_text(c, "AIGC / ARCHITECTURE / EXHIBITION", 68, 72, 6.8, "Helvetica", MUTED)
    draw_footer(c, page_no, project["slug"].upper())
    anchor = f"project-{project['slug']}"
    c.bookmarkPage(anchor)
    c.addOutlineEntry(project["title"], anchor, level=0, closed=False)
    c.showPage()


def closing_page(c: canvas.Canvas, page_no: int) -> None:
    draw_background(c)
    draw_label(c, "CONTACT / OPPORTUNITY", MARGIN, PAGE_H - 48)
    draw_text(c, "让空间设计与 AIGC 协同工作，", MARGIN, 442, 27, FONT_BOLD)
    draw_text(c, "把创意转化为清晰、完整的设计成果。", MARGIN, 404, 27, FONT_BOLD)
    draw_paragraph(
        c,
        "目前正在寻找公共空间设计以及 AIGC 设计相关实习机会，期待在真实项目中发挥设计表达、方案执行与 AI 辅助创作能力。",
        MARGIN,
        360,
        520,
        10,
        18,
        MUTED,
    )

    c.setFillColor(PANEL)
    c.roundRect(MARGIN, 108, 500, 168, 20, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.roundRect(MARGIN, 108, 500, 168, 20, stroke=1, fill=0)
    draw_text(c, "PHONE", MARGIN + 24, 232, 7, "Helvetica", DIM)
    draw_text(c, "133 6144 4417", MARGIN + 140, 228, 13, FONT_BOLD)
    c.setStrokeColor(LINE)
    c.line(MARGIN + 24, 204, MARGIN + 476, 204)
    draw_text(c, "EMAIL", MARGIN + 24, 168, 7, "Helvetica", DIM)
    draw_text(c, "julianobunting97@gmail.com", MARGIN + 140, 164, 12, "Helvetica-Bold")
    c.linkURL("mailto:julianobunting97@gmail.com", (MARGIN + 130, 150, MARGIN + 465, 185), relative=0)
    c.setFillColor(ACCENT)
    c.roundRect(MARGIN + 24, 124, 452, 26, 13, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 7.5)
    c.drawCentredString(MARGIN + 250, 133, "发送邮件")
    c.linkURL("mailto:julianobunting97@gmail.com", (MARGIN + 24, 124, MARGIN + 476, 150), relative=0)

    x = 574
    draw_text(c, "荣誉与认可", x, 295, 12, FONT_BOLD)
    y = 261
    for honor in HONORS:
        c.setFillColor(ACCENT)
        c.circle(x + 3, y + 4, 2.2, stroke=0, fill=1)
        draw_paragraph(c, honor, x + 17, y + 11, 220, 7.6, 12, MUTED, max_height=30)
        y -= 38

    draw_text(c, "THANK YOU", PAGE_W - 255, 70, 30, "Helvetica-Bold", LINE)
    draw_footer(c, page_no, "CONTACT")
    c.bookmarkPage("contact")
    c.addOutlineEntry("联系我", "contact", level=0, closed=False)
    c.showPage()


def build_pdf() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    cover_page(c)
    page = 2
    about_page(c, page)
    page += 1
    contents_page(c, page)
    page += 1

    park = PROJECTS[0]
    project_intro_page(c, park, page)
    page += 1
    for idx, board in enumerate(park["boards"], start=1):
        board_page(c, park, board, idx, page)
        page += 1
    gallery_page(c, park, park["renders"], page)
    page += 1

    office = PROJECTS[1]
    project_intro_page(c, office, page)
    page += 1
    for idx, board in enumerate(office["boards"], start=1):
        board_page(c, office, board, idx, page)
        page += 1
    gallery_page(c, office, office["renders"], page)
    page += 1

    feature_collage_page(c, PROJECTS[2], page)
    page += 1
    single_render_page(c, PROJECTS[3], page)
    page += 1
    gallery_page(c, PROJECTS[3], PROJECTS[3]["photos"], page, "REAL PHOTOGRAPHY")
    page += 1
    gallery_page(c, PROJECTS[4], PROJECTS[4]["renders"], page)
    page += 1
    concept_overview_page(c, PROJECTS[5], page)
    page += 1
    gallery_page(c, PROJECTS[5], PROJECTS[5]["renders"], page)
    page += 1
    closing_page(c, page)

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
