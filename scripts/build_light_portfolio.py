"""Create the light 16:9 recruitment edition from original website assets."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab import rl_config
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from cover_axonometric import draw_cover_axonometric, draw_closing_axonometric

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public' / 'portfolio'
WORK = ROOT / 'tmp' / 'pdfs' / 'light-edition'
OUT = ROOT / 'output' / 'pdf' / '曹硕_环境艺术设计作品集_16比9_浅色求职版_含展板.pdf'
W, H = 1280, 720
BG = '#F5F3ED'
INK = '#252D29'
MUTED = '#69716A'
ACCENT = '#526853'
RULE = '#C8CBBE'
PANEL = '#E7E9DF'
WHITE = '#FFFFFF'
EMAIL = 'fengfan3812@gmail.com'
PHONE = '133 6144 4417'
VIDEO_PARK = 'https://www.bilibili.com/video/BV1nRMh6LEZs?t=1.4'
VIDEO_OCEAN = 'https://www.bilibili.com/video/BV1pXMh62EA9?t=37.1'
Image.MAX_IMAGE_PIXELS = 200_000_000
# Keep JPEG streams binary; ASCII85 adds size without improving image fidelity.
rl_config.useA85 = False


def asset(slug, number):
    return next((PUBLIC / slug / 'renders').glob(f'render-{number:02d}.*'))


def audit_assets():
    WORK.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype('C:/Windows/Fonts/calibri.ttf', 20)
    for slug in ['1532-park', '1532-office', 'concept-space', 'family-home', 'single-apartment', 'courtyard']:
        paths = sorted((PUBLIC / slug).rglob('*'))
        paths = [p for p in paths if p.suffix.lower() in ('.jpg', '.jpeg', '.png')]
        sheet = Image.new('RGB', (1320, math.ceil(len(paths) / 3) * 278), BG)
        d = ImageDraw.Draw(sheet)
        for i, p in enumerate(paths):
            with Image.open(p) as original:
                original.draft('RGB', (800, 800))
                im = ImageOps.exif_transpose(original).convert('RGB')
                im.thumbnail((416, 238))
            x, y = (i % 3) * 440 + 12, (i // 3) * 278
            sheet.paste(im, (x + (416 - im.width) // 2, y + (238 - im.height) // 2))
            d.text((x, y + 242), str(p.relative_to(PUBLIC / slug)), fill=INK, font=font)
        sheet.save(WORK / f'assets-{slug}.jpg', quality=90)
    print('Asset contact sheets ready', flush=True)


def anurati_pdf_font():
    source = ROOT / 'public/fonts/Anurati-Regular.otf'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    target = ROOT / '.codex-build/pdf-fonts' / f'Anurati-{digest}.ttf'
    if target.exists():
        return target

    # ReportLab needs quadratic outlines; retain the site's glyphs and font metadata.
    sys.path.insert(0, str(ROOT / '.codex-build/pdf-python'))
    from fontTools.ttLib import TTFont as SourceFont
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    with SourceFont(source) as font:
        order = font.getGlyphOrder()
        glyph_set = font.getGlyphSet()
        glyphs = {}
        for name in order:
            pen = TTGlyphPen(glyph_set)
            glyph_set[name].draw(Cu2QuPen(pen, max_err=1, reverse_direction=True))
            glyphs[name] = pen.glyph()
        builder = FontBuilder(font['head'].unitsPerEm, isTTF=True)
        builder.setupGlyphOrder(order)
        builder.setupCharacterMap(font.getBestCmap())
        builder.setupGlyf(glyphs)
        builder.setupHorizontalMetrics(font['hmtx'].metrics)
        builder.setupHorizontalHeader(ascent=font['hhea'].ascent,
                                      descent=font['hhea'].descent,
                                      lineGap=font['hhea'].lineGap)
        builder.font['name'] = font['name']
        os2 = font['OS/2']
        builder.setupOS2(sTypoAscender=os2.sTypoAscender, sTypoDescender=os2.sTypoDescender,
                         sTypoLineGap=os2.sTypoLineGap, usWinAscent=os2.usWinAscent,
                         usWinDescent=os2.usWinDescent, fsType=os2.fsType,
                         usWeightClass=os2.usWeightClass, usWidthClass=os2.usWidthClass)
        builder.setupPost()
        target.parent.mkdir(parents=True, exist_ok=True)
        builder.save(target)
    return target


def register_fonts():
    for name, filename in [('Sans', 'msyh.ttc'), ('Bold', 'msyhbd.ttc'),
                           ('Serif', 'NotoSerifSC-VF.ttf'), ('Latin', 'calibri.ttf'),
                           ('LatinLight', 'calibril.ttf')]:
        pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/' + filename))
    pdfmetrics.registerFont(TTFont('Anurati', str(anurati_pdf_font())))


class Book:
    def __init__(self):
        OUT.parent.mkdir(parents=True, exist_ok=True)
        WORK.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
        self.c.setTitle('曹硕 | 环境艺术设计作品集')
        self.c.setAuthor('曹硕 CAO SHUO')
        self.c.setSubject('环境设计 / 公共空间 / 室内设计 / AIGC | 2026 求职作品集')
        self.c.setViewerPreference('DisplayDocTitle', 'true')
        self.page = 0
        self.manifest = []
        self.boxes = []

    def rect(self, x, y, w, h, color=BG):
        self.c.setFillColor(HexColor(color))
        self.c.rect(x, H-y-h, w, h, stroke=0, fill=1)

    def line(self, x, y, end, color=RULE, width=.65):
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(width)
        self.c.line(x, H-y, end, H-y)

    def text(self, value, x, y, size=16, font='Sans', color=INK, align='left', tracking=0):
        length = pdfmetrics.stringWidth(value, font, size) + max(0, len(value)-1)*tracking
        if align == 'right':
            x -= length
        elif align == 'center':
            x -= length/2
        if x < -1 or x+length > W+1:
            raise ValueError(f'Page {self.page}: text wider than page: {value}')
        self.c.setFillColor(HexColor(color))
        ob = self.c.beginText(x, H-y-size*.94)
        ob.setFont(font, size)
        ob.setCharSpace(tracking)
        ob.textLine(value)
        self.c.drawText(ob)
        self.boxes.append((self.page, value[:36], x, y, x+length, y+size*1.2))

    def para(self, value, x, y, width, size=16, leading=27, color=INK, font='Sans', maxh=None):
        style = ParagraphStyle('body', fontName=font, fontSize=size, leading=leading,
                               textColor=HexColor(color), wordWrap='CJK', splitLongWords=False)
        p = Paragraph(value, style)
        _, height = p.wrap(width, 1500)
        if maxh is not None and height > maxh+.1:
            raise ValueError(f'Page {self.page}: paragraph overflow {height} > {maxh}: {value}')
        if y+height > 671:
            raise ValueError(f'Page {self.page}: paragraph enters footer')
        p.drawOn(self.c, x, H-y-height)
        self.boxes.append((self.page, value[:36], x, y, x+width, y+height))
        return height

    def image(self, path, x, y, w, h, mode='cover', crop=None, anchor=(.5, .5), pixel_ratio=2.25):
        path = Path(path)
        spec = f'{path}|{path.stat().st_mtime}|{w}|{h}|{mode}|{crop}|{anchor}'
        if pixel_ratio != 2.25:
            spec += f'|{pixel_ratio}|q91'
        dest = WORK / ('img-' + hashlib.sha1(spec.encode()).hexdigest()[:18] + '.jpg')
        if not dest.exists():
            with Image.open(path) as original:
                original.draft('RGB', (4200, 4200))
                im = ImageOps.exif_transpose(original)
                if im.mode == 'RGBA':
                    base = Image.new('RGBA', im.size, BG)
                    base.alpha_composite(im)
                    im = base.convert('RGB')
                else:
                    im = im.convert('RGB')
                if crop:
                    a,b,c,d = crop
                    im = im.crop((int(a*im.width), int(b*im.height), int(c*im.width), int(d*im.height)))
                target = (max(1, int(w*pixel_ratio)), max(1, int(h*pixel_ratio)))
                if mode == 'cover':
                    im = ImageOps.fit(im, target, Image.Resampling.LANCZOS, centering=anchor)
                else:
                    im.thumbnail(target, Image.Resampling.LANCZOS)
                im.save(dest, 'JPEG', quality=91, optimize=True)
        with Image.open(dest) as im:
            iw, ih = im.size
        if mode == 'contain':
            ratio = min(w/iw, h/ih)
            dw, dh = iw*ratio, ih*ratio
            x, y, w, h = x+(w-dw)/2, y+(h-dh)/2, dw, dh
        self.c.drawImage(str(dest), x, H-y-h, w, h)
        self.manifest[-1]['images'].append(str(path.relative_to(ROOT)))

    def compressed_image(self, path, x, y, w, h):
        path = Path(path)
        with Image.open(path) as im:
            if im.format != 'JPEG' or abs(im.width/im.height-w/h) > .001:
                raise ValueError('Precompressed image must be a JPEG matching the layout ratio')
        # Embed the optimized JPEG stream directly, without another lossy encode.
        self.c.drawImage(str(path), x, H-y-h, w, h)
        self.manifest[-1]['images'].append(str(path.relative_to(ROOT)))

    def boards(self, number, title, description, items, key):
        self.begin(f'{number} / Original Presentation Boards')
        self.c.bookmarkPage(key)
        self.c.addOutlineEntry(title, key, level=1)
        self.text(title, 52, 100, 34, 'Serif')
        self.para(description, 52, 166, 252, 15, 27, MUTED, maxh=120)
        self.line(52, 316, 292)
        for i, (_, label, detail) in enumerate(items):
            top = 346+i*90
            self.text(label, 52, top, 17, 'Serif')
            self.text(detail, 52, top+30, 12, 'Sans', MUTED)
        self.text('完整展板 / 放大阅读细节', 52, 625, 11, 'Sans', MUTED)
        for i, (path, label, _) in enumerate(items):
            x = 350+i*450
            self.image(path, x, 83, 428, 570, mode='contain', pixel_ratio=10)
        self.manifest[-1]['full_boards'] = [str(item[0].relative_to(ROOT)) for item in items]

    def begin(self, chapter, title=None, subtitle=None, key=None):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.manifest.append({'page':self.page, 'chapter':chapter, 'title':title, 'images':[]})
        self.rect(0, 0, W, H)
        self.line(52, 60, 1228)
        self.text('CAO SHUO', 52, 30, 12, 'Latin', tracking=2.2)
        self.text(chapter.upper(), 1228, 32, 10, 'Latin', MUTED, 'right', 1.2)
        self.line(52, 677, 1228)
        self.text('环境艺术设计作品集', 52, 689, 10, 'Sans', MUTED)
        self.text('SELECTED WORKS  /  2026', 640, 689, 10, 'Latin', MUTED, 'center', .8)
        self.text(f'{self.page:02d}', 1228, 686, 16, 'Latin', INK, 'right')
        if title:
            self.text(title, 52, 83, 35, 'Serif')
        if subtitle:
            self.text(subtitle, 52, 133, 12, 'Sans', MUTED)
        if key:
            self.c.bookmarkPage(key)
            self.c.addOutlineEntry(title or chapter, key, level=0)

    def cap(self, label, x, y, detail=None, width=560):
        self.text(label, x, y, 13, 'Sans', INK)
        if detail:
            self.para(detail, x, y+24, width, 12, 20, MUTED, maxh=42)

    def note(self, number, title, body, x, y, width):
        self.text(number, x, y, 12, 'Latin', ACCENT, tracking=1)
        self.text(title, x+33, y-4, 20, 'Serif')
        self.para(body, x+33, y+31, width-33, 14, 24, MUTED)

    def opener(self, num, titlelines, en, category, brief, image, caption, key, period=None):
        self.begin(f'{num} / {en}', key=key)
        self.text(num, 52, 99, 88, 'LatinLight', ACCENT)
        top = 221
        for t in titlelines:
            self.text(t, 52, top, 37, 'Serif')
            top += 53
        self.text(category, 52, top+9, 13, 'Sans', MUTED)
        self.line(52, top+51, 326)
        self.para(brief, 52, top+71, 304, 15, 27, maxh=145)
        if period:
            self.text(period, 52, 614, 12, 'Latin', MUTED)
        self.image(image, 408, 112, 820, 462)
        self.cap(caption, 408, 595)
        self.text(en, 1228, 625, 11, 'Latin', ACCENT, 'right', 2)

    def link(self, label, url, x, y, size=14):
        self.text(label, x, y, size, 'Sans', ACCENT)
        length = pdfmetrics.stringWidth(label, 'Sans', size)
        self.line(x, y+size+5, x+length, ACCENT)
        self.c.linkURL(url, (x, H-y-size-8, x+length, H-y+3), relative=0, thickness=0)

    def qr(self, url, x, y, size=86):
        q = QrCodeWidget(url, barFillColor=HexColor(INK), barBorder=2)
        a,b,c,d = q.getBounds()
        drawing = Drawing(size, size, transform=[size/(c-a),0,0,size/(d-b),0,0])
        drawing.add(q)
        self.rect(x, y, size, size, WHITE)
        renderPDF.draw(drawing, self.c, x, H-y-size)
        self.c.linkURL(url, (x,H-y-size,x+size,H-y), relative=0, thickness=0)

    def save(self):
        self.c.save()
        (WORK / 'page-manifest.json').write_text(json.dumps(self.manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        (WORK / 'text-boxes.json').write_text(json.dumps(self.boxes,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'Created {self.page} pages; {OUT.stat().st_size/1024/1024:.1f} MB', flush=True)


def build():
    register_fonts()
    b = Book()
    park = lambda n: asset('1532-park', n)
    office = lambda n: asset('1532-office', n)
    ocean = lambda n: asset('concept-space', n)
    family = lambda n: asset('family-home', n)
    apartment = lambda n: asset('single-apartment', n)
    court = lambda n: asset('courtyard', n)
    pb1 = PUBLIC / '1532-park/boards/board-01.jpg'
    pb2 = PUBLIC / '1532-park/boards/board-02.jpg'
    pb3 = ROOT / 'output/pdf/source-assets/1532-park-board-03.jpg'
    poster = PUBLIC / '1532-park-cover.jpg'
    ob1 = PUBLIC / '1532-office/boards/board-01.jpg'
    ob2 = PUBLIC / '1532-office/boards/board-02.jpg'

    # 01 / Cover: abstract vector architecture rather than a single project image.
    b.begin('Environmental Art & Spatial Design', key='cover')
    b.text('PORTFOLIO', 48, 78, 110, 'Anurati', INK, tracking=15.4)
    b.text('2026', 1228, 121, 34, 'LatinLight', ACCENT, 'right')
    b.text('空间之间', 52, 231, 47, 'Serif')
    b.text('环境艺术设计作品集', 55, 303, 18, 'Sans', MUTED)
    b.line(54, 358, 335)
    b.para('公共空间<br/>室内设计<br/>AIGC', 55, 389, 280, 21, 36, INK)
    b.para('以空间为媒介，<br/>连接逻辑与感知。', 55, 560, 280, 15, 27, ACCENT)
    draw_cover_axonometric(b)

    # 02 / Profile. Award follows the website verbatim; no project attribution inferred.
    b.begin('Profile / Education & Recognition', '以空间为媒介，连接设计与创作。', key='profile')
    b.image(ROOT/'src/assets/portrait-cao-shuo.png', 52, 154, 194, 259, mode='contain')
    b.text('曹硕', 149, 430, 32, 'Serif', align='center')
    b.text('CAO SHUO', 149, 480, 15, 'Latin', MUTED, align='center', tracking=1.6)
    for i, line in enumerate(['环境设计本科在读', '潍坊学院', '预计 2027 年毕业']):
        b.text(line, 149, 519+i*27, 14, 'Sans', MUTED, align='center')
    b.text('设计表达 / 方案执行 / AI 辅助创作', 284, 158, 17, 'Bold')
    b.para('系统学习室内设计、景观规划、建筑设计与施工工艺，关注从前期分析、概念推演到视觉呈现与方案深化的完整过程。',
           284, 205, 440, 16, 28)
    b.para('希望在公共空间设计及 AIGC 设计相关实习中，将空间判断、视觉表达与协作执行结合，完成清晰、完整的设计成果。',
           284, 307, 440, 15, 27, MUTED)
    b.line(284, 419, 730)
    for x,val,label in [(284,'3.86','GPA / 4.0'),(450,'3 / 80','学年成绩排名'),(606,'7 / 80','学年综测排名')]:
        b.text(val,x,440,31,'LatinLight',ACCENT)
        b.text(label,x,486,12,'Sans',MUTED)
    b.text('工具与表达',284,539,15,'Bold')
    b.para('AutoCAD / 3DMax / Photoshop<br/>GPT / Codex / Gemini / ComfyUI',284,571,450,14,26,MUTED)
    b.rect(782,154,446,235,PANEL)
    b.text('荣誉与认可',805,174,13,'Sans',MUTED)
    b.text('一等奖',805,207,37,'Serif',ACCENT)
    b.para('第十二届“广联达杯”BIM毕业设计创新大赛<br/>B模块建筑设计AI+BIM应用与创新项目大赛',
           805,270,397,15,26,maxh=90)
    b.para('2024-2025  潍坊学院二等奖学金、优秀学生<br/>2023-2024  潍坊学院三等奖学金<br/>2024  暑期“三下乡”社会实践优秀个人<br/>普通话二级甲等',
           791,411,424,13,29,MUTED)
    b.line(791,552,1228)
    b.text(PHONE,791,574,18,'Latin')
    b.link(EMAIL,'mailto:'+EMAIL,791,610,14)

    # 03 / Contents with in-document navigation.
    b.begin('Index / Selected Projects','精选项目','从场地更新到居住日常，再到 AIGC 概念表达。',key='contents')
    contents = [
        ('01','世纪绿洲','潍坊市 1532 产业园改造','景观更新','04 - 10',park(11),'park'),
        ('02','LUMEN','1532 办公空间设计','室内改造','11 - 16',office(7),'office'),
        ('03','海洋艺术与生态科技','概念展馆与沉浸式空间','AIGC 概念','17 - 20',ocean(8),'ocean'),
        ('04','柔和的居住秩序','三口之家侘寂风住宅','住宅设计','21 - 22',family(1),'family'),
        ('05','一人居所','单人公寓室内设计','小户型设计','23 - 25',apartment(1),'apartment'),
        ('06','庭院有境','庭院景观设计','庭院营造','26 - 27',court(1),'courtyard'),
    ]
    for i,(num,title,sub,cat,pages,img,key) in enumerate(contents):
        x,y = 52+(i%3)*400, 177+(i//3)*234
        b.image(img,x,y,376,119)
        b.text(num,x,y+138,25,'LatinLight',ACCENT)
        b.text(title,x+49,y+138,19,'Serif')
        b.text(sub,x+49,y+171,12,'Sans',MUTED)
        b.text(pages,x+376,y+201,10,'Latin',MUTED,'right')
        b.text(cat,x,y+201,10,'Sans',MUTED)
        b.c.linkRect('',key,(x,H-y-220,x+376,H-y),relative=0,thickness=0)

    # 04-10 / Public landscape: setting, systems and complete boards.
    b.opener('01',['世纪绿洲','重塑时间的维度'],'URBAN LANDSCAPE',
             '潍坊市 1532 产业园改造项目',
             '以工业记忆、时间叙事、社区共生与生态疗愈为线索，将存量场地转化为可停留、可感知的公共空间。',
             park(1),'入口日晷广场 · 景观效果表达','park','2026.05 - 2026.06')

    b.begin('01 / Context & Strategy','从工业记忆，到社区日常',
            '场地分析与设计回应  /  潍坊世纪公园时空叙事与生态疗愈景观设计')
    b.image(pb1,52,178,760,257,mode='contain',crop=(.013,.611,.99,.793))
    b.cap('区位与城市肌理分析',52,448,'原方案展板局部：联系周边居住、文化与公共服务界面。',width=748)
    b.line(52,520,804)
    for x,t,s in [(52,'工业记忆','保留历史肌理'),(304,'时间叙事','日晷成为记忆锚点'),(556,'社区共生','建立休闲与交流场景')]:
        b.text(t,x,543,24,'Serif')
        b.text(s,x,586,14,'Sans',MUTED)
    b.note('01','场地联系','关注城市界面与场地入口，让公共活动与周边日常生活建立联系。',858,181,350)
    b.note('02','记忆转译','以日晷、旧砖墙与场地构筑物组织时间线索，形成可识别的空间节点。',858,333,350)
    b.note('03','生态体验','用植物、水景和地形丰富游览节奏，将生态策略转化为可感知的场景。',858,485,350)

    b.begin('01 / Landscape Systems','让生态策略进入空间剖面',
            '原方案剖面与系统示意：地形、水景、植物与雨水收集共同组织场地。')
    b.image(pb2,52,175,1176,438,mode='contain',crop=(0,.055,1,.350))
    b.text('入口水景',52,635,14,'Serif',ACCENT)
    b.text('雨水收集与净化',334,635,14,'Serif',ACCENT)
    b.text('种植层与地形',668,635,14,'Serif',ACCENT)
    b.text('公共活动与感官体验',962,635,14,'Serif',ACCENT)

    b.begin('01 / Place & Detail','入口，是进入场所的第一段叙事',
            '以日晷雕塑建立识别，以跌水和台阶延伸抵达、停留与观看的过程。')
    b.image(park(2),52,177,762,427)
    b.cap('跌水台阶与停留边界',52,626)
    b.image(park(3),838,177,390,218)
    b.cap('日晷雕塑与环形铺装',838,410)
    b.image(park(4),838,449,390,184)
    b.cap('时间刻度与铺装细节',838,642)

    b.begin('01 / Social Landscape','从白昼到夜晚，延续公共生活',
            '社区休憩、生态草地与夜间照明共同构成场地的生活场景。')
    b.compressed_image(ROOT/'output/pdf/source-assets/1532-park-detail-07.jpg',52,177,768,432)
    b.cap('林下交流空间与建筑界面',52,628)
    b.image(park(8),844,177,384,215)
    b.cap('B612 草地节点',844,402)
    b.image(park(5),844,437,384,189)
    b.cap('夜间休闲场景',844,640)

    b.boards('01', '项目全貌', '潍坊市 1532 产业园改造<br/>从整体视觉到场地分析，呈现公共空间更新的设计线索。',
             [(poster, '海报', '项目视觉与设计主题'),
              (pb1, '展板 01', '场地分析与设计策略')], 'park-boards-01')
    b.boards('01', '策略与场景', '世纪绿洲 / 生态疗愈景观<br/>将生态系统、节点设计与场景表达联结为完整方案。',
             [(pb2, '展板 02', '系统分析与景观节点'),
              (pb3, '展板 03', '效果展示与场景细节')], 'park-boards-02')

    # 11-16 / Office: context, plan, materials/light and complete boards.
    b.opener('02',['LUMEN','1532 办公空间'],'WORKPLACE DESIGN',
             '旧厂房改造 / AI 工作室',
             '以展示、交流与创作为线索，在工业肌理中引入温暖材质、自然光和灵活协作场景，组织开放与私密之间的层次。',
             office(7),'入口接待与品牌展示空间','office')

    b.begin('02 / Plan & Programme','用空间关系，回应不同的工作状态',
            '原方案图纸局部：平面布局、功能分区与流线组织。')
    b.rect(52,178,713,404,'#F0E4CE')
    b.image(ob1,52,178,713,404,mode='contain',crop=(.057,.857,.394,.971))
    b.cap('平面布局',52,598,'以共享区域联结办公、洽谈、展示与休闲节点。',width=713)
    with Image.open(ob1) as board:
        board_w, board_h = board.size
    for y, label, crop in [
        (178, '功能分区', (.425,.846,.611,.934)),
        (428, '流线组织', (.619,.844,.802,.934)),
    ]:
        a, top, right, bottom = crop
        crop_w = int(right*board_w)-int(a*board_w)
        crop_h = int(bottom*board_h)-int(top*board_h)
        height = 300*crop_h/crop_w
        b.image(ob1,863,y,300,height,mode='contain',crop=crop)
        b.cap(label,863,y+height+14,width=300)

    b.begin('02 / Open Collaboration','协作，从开放的公共界面开始',
            '从共享工位到休闲吧台，以材质连续性组织公共交流。')
    b.image(office(10),52,177,742,430)
    b.image(office(2),818,177,410,270,mode='contain')
    b.cap('共享办公 / 自然光与工作界面',52,627)
    b.text('非正式交流',818,472,24,'Serif')
    b.para('吧台、木质格栅与软性座位构成更轻松的交流界面，让讨论从正式会议延伸到日常互动。',
           818,522,399,15,28,MUTED,maxh=113)

    b.begin('02 / Day & Night','光线，让同一空间拥有不同节奏',
            '同一办公场景的日夜表达：自然采光、线性灯光与展示界面。')
    b.image(office(3),52,186,576,290)
    b.image(office(4),652,186,576,290)
    b.cap('01 / 日间',52,499,'利用窗面与室外景观建立视觉联系，强调材料的自然质感。',width=560)
    b.cap('02 / 夜间',652,499,'以重点照明和线性光勾勒空间层次，强化工作区与展示面的关系。',width=560)
    b.line(52,601,1228)
    b.text('DAYLIGHT',52,622,15,'Latin',ACCENT,tracking=2)
    b.text('ARTIFICIAL LIGHT',652,622,15,'Latin',ACCENT,tracking=2)

    b.begin('02 / Work, Talk & Pause','不同尺度的交流，与专注并存',
            '会议协作、景观休闲与展览展示构成复合工作场景。')
    b.image(office(6),52,178,730,409)
    b.cap('创意会议室',52,609,'以围合布局、共享界面和中部绿植组织团队交流。',width=710)
    b.image(office(12),806,178,422,226)
    b.cap('景观休闲区',806,416)
    b.image(office(14),806,454,422,174)
    b.cap('展览展示空间',806,640)

    b.boards('02', '完整方案', 'LUMEN / 1532 办公空间<br/>从前期分析、功能布局到空间效果与材料表达，展示旧厂房的办公转译。',
             [(ob1, '展板 01', '前期分析与空间组织'),
              (ob2, '展板 02', '场景效果与材料表达')], 'office-boards')

    # 17-20 / AIGC concept: distinguish concept exploration from built work.
    b.opener('03',['海洋艺术','与生态科技'],'AIGC CONCEPT SPACE',
             '概念展馆 / 沉浸式空间探索',
             '以海洋意象、生态科技与未来展陈为关键词，探索流动体量、自然界面和沉浸体验之间的关系。',
             ocean(8),'概念场景表达 · 滨水公共界面','ocean')

    b.begin('03 / Form & Nature','让自然意象，成为空间语言',
            '概念体量研究  /  曲面、水体、植物与多层公共界面的组合。')
    b.image(ocean(5),52,177,451,451,mode='contain')
    b.cap('概念俯视 / 体量与水体关系',52,642)
    b.image(ocean(6),529,177,699,314)
    b.text('流动形态与垂直绿意',529,518,28,'Serif')
    b.para('将波浪般的表皮、水景和立体绿化结合，形成建筑与环境之间的连续界面；从整体轮廓到局部肌理保持视觉叙事的一致性。',
           529,569,686,15,27,MUTED,maxh=84)

    b.begin('03 / Immersive Interior','以光、水与曲面，组织沉浸式观看',
            '展馆内部概念效果：从一层展示场景延伸到二层环廊与共享中庭。')
    b.image(ocean(3),52,184,576,322)
    b.image(ocean(4),652,184,576,322)
    b.cap('一层 / 展示与探索',52,530,'水体与展示单元结合，围绕行进路径形成连续的观看节点。',width=560)
    b.cap('二层 / 环廊与中庭',652,530,'曲面顶棚、自然采光与中庭视线形成上下层空间的联系。',width=560)
    b.text('概念设计表达',52,640,11,'Sans',MUTED)

    b.begin('03 / Material & Atmosphere','从建筑尺度，走近材料与感知',
            '以局部画面检验整体视觉语言：水的运动、表皮光影与自然细节。')
    b.image(ocean(7),52,177,340,453,mode='contain')
    b.cap('水景与外立面',52,640)
    b.image(ocean(11),416,177,494,217)
    b.image(ocean(12),416,417,494,232)
    b.text('视觉深化',944,188,29,'Serif')
    b.para('整体轮廓确立后，继续检查局部材质、光线与环境氛围，使概念不只停留在单张“主视觉”中。',
           944,251,275,15,28,MUTED,maxh=169)
    b.line(944,436,1228)
    b.para('AIGC 的价值，是拓展方案推演与表达的可能；设计判断仍决定画面的取舍与空间逻辑。',
           944,462,275,15,28,ACCENT,maxh=169)

    # 21-22 / Family home.
    b.opener('04',['柔和的','居住秩序'],'FAMILY HOME',
             '三口之家侘寂风住宅设计',
             '以低饱和材质、自然肌理与柔和光线塑造安静的居住氛围，兼顾共同生活、独处与休憩的不同需求。',
             family(1),'客厅效果表达 · 自然光与柔和界面','family')

    b.begin('04 / Everyday Living','让日常功能，拥有统一的温度',
            '餐厨、休憩与工作空间，延续克制的色彩和柔和的材质语言。')
    b.image(family(2),52,178,721,405)
    b.cap('餐厨空间',52,606,'以开放的操作与交流界面，联结家庭共同生活。',width=701)
    b.image(family(4),798,178,430,242)
    b.cap('老人房 / 休憩空间',798,429)
    b.image(family(3),798,468,430,158)
    b.cap('直播与居家工作空间',798,640)

    # 23-25 / Compact living. Photo-style assets are not labelled as completed construction.
    b.opener('05',['一人居所','完整的生活场景'],'COMPACT APARTMENT',
             '单人公寓室内设计',
             '围绕单人生活方式整合厨房、休息、娱乐与收纳，让有限面积下的空间保持功能连续与视觉秩序。',
             apartment(1),'客厅效果表达 · 紧凑空间中的日常生活','apartment')

    b.begin('05 / Function & Rhythm','把生活功能，组织成连续的空间',
            '从餐厨操作到兴趣娱乐，以收纳、光线与活动界面形成场景区分。')
    b.image(apartment(2),52,177,475,417,mode='contain')
    b.cap('厨房 / 操作与收纳',52,614)
    b.image(apartment(3),552,177,676,377)
    b.cap('电竞房 / 专注与兴趣',552,576,'将工作台、展示与设备纳入完整的空间表达。',width=665)

    b.begin('05 / Lived Atmosphere','让人物尺度，回到空间之中',
            '生活场景表达：通过日常动作、采光与视点补充空间的情绪与尺度。')
    shots = [('photo-kitchen-01.png','餐厨日常'),('photo-living-02.png','客厅停留'),
             ('photo-living-04.png','窗边休憩'),('photo-gaming-01.png','兴趣与夜间氛围')]
    for i,(name,caption) in enumerate(shots):
        x = 52+i*300
        b.image(PUBLIC/'single-apartment/renders'/name,x,183,276,414,mode='contain')
        b.cap(caption,x,617,width=276)

    # 26-27 / Garden sequence.
    b.opener('06',['庭院有境','归家的另一段路'],'COURTYARD LANDSCAPE',
             '庭院营造 / 景观设计',
             '以前院、后院、侧道与影壁组织归家与停留，将植物层次、水景、材料与夜间照明转化为安静的户外生活体验。',
             court(2),'后院休憩空间 · 庭院效果表达','courtyard')

    b.begin('06 / Arrival & Pause','在行走与停留之间，建立庭院层次',
            '由前院迎接、侧道过渡到影壁收景，形成连续的空间序列。')
    b.image(court(1),52,178,588,439,mode='contain')
    b.cap('前院 / 水景与休憩',52,635)
    b.image(court(3),664,178,359,268)
    b.cap('侧道 / 夜景与引导',664,460)
    b.para('沿墙照明与地面材质强调行进方向，植物、水景与影壁共同定义归家过程中的视线与节奏。',
           664,513,346,15,27,MUTED,maxh=137)
    b.image(court(4),1047,178,181,325,mode='contain')
    b.cap('影壁 / 材料界面',1047,519,width=181)

    # 28 / Personal methodology and working video links.
    b.begin('Practice / Design & AIGC','以设计判断，连接工具与成果',
            '个人方法与实践  /  把 AI 辅助创作纳入清晰的设计表达过程。',key='practice')
    steps = [('01','分析','场地、使用者与功能需求'),('02','推演','概念方向与方案比较'),
             ('03','表达','模型、图像与视觉叙事'),('04','校核','尺度、材料与成果一致性')]
    for i,(n,t,s) in enumerate(steps):
        x=52+i*300
        b.line(x,186,x+276)
        b.text(n,x,209,16,'Latin',ACCENT)
        b.text(t,x+41,201,30,'Serif')
        b.text(s,x,264,13,'Sans',MUTED)
    b.rect(52,324,554,299,PANEL)
    b.text('AIGC 理解',77,348,25,'Serif')
    b.para('AI 不只用于生成图片，也用于辅助资料整理、概念推演、变量比较与视觉深化。通过筛选与迭代，让工具服务于空间逻辑和设计判断。',
           77,395,501,16,28,maxh=120)
    b.line(77,511,579)
    b.para('校园文化墙实践：完成资料分析、主题提炼、提示词优化与视觉控制，将项目周期压缩至原来的一半。',
           77,534,501,14,26,MUTED,maxh=80)
    b.text('项目影像',658,330,25,'Serif')
    b.qr(VIDEO_PARK,658,387,92)
    b.text('1532 产业园改造',778,393,19,'Serif')
    b.link('观看方案短片',VIDEO_PARK,778,436,13)
    b.qr(VIDEO_OCEAN,658,526,92)
    b.text('海洋艺术与生态科技',778,530,19,'Serif')
    b.link('观看概念短片',VIDEO_OCEAN,778,573,13)

    # 29 / Closing spread: contact details remain selectable and clickable.
    b.begin('Contact / Available for Internship',key='contact')
    b.text('LET\'S CREATE',52,104,66,'LatinLight',ACCENT,tracking=2)
    b.text('让空间设计与 AIGC 协同工作。',52,225,43,'Serif')
    b.text('把创意转化为清晰、完整的设计成果。',52,293,36,'Serif')
    b.para('寻找公共空间设计及 AIGC 设计相关实习机会。<br/>期待在真实项目中发挥设计表达、方案执行与 AI 辅助创作能力。',
           55,395,795,16,29,MUTED,maxh=96)
    b.line(52,518,909)
    b.text('曹硕 / CAO SHUO',52,546,25,'Serif')
    b.text('潍坊学院 · 环境设计本科 · 2027 届',52,592,14,'Sans',MUTED)
    b.link(EMAIL,'mailto:'+EMAIL,491,551,18)
    b.link(PHONE,'tel:13361444417',491,598,16)
    draw_closing_axonometric(b)
    b.save()


if __name__ == '__main__':
    if '--audit' in sys.argv:
        audit_assets()
    else:
        build()
