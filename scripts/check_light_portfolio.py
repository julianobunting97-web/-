"""Validate the PDF and make visual review sheets without altering source assets."""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'tmp/pdfs/light-edition'
PDF = ROOT / 'output/pdf/曹硕_环境艺术设计作品集_16比9_浅色求职版_更新.pdf'
reader = PdfReader(PDF)
assert len(reader.pages) == 26
texts = []
uris = []
font_states = {}
for i, page in enumerate(reader.pages, 1):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    assert abs(w/h - 16/9) < 0.0001, (i,w,h)
    text = page.extract_text()
    assert len(text) > 50, i
    assert '\ufffd' not in text, i
    texts.append(text)
    for ref in page.get('/Annots', []):
        annotation = ref.get_object()
        if '/A' in annotation:
            action = annotation['/A']
            if action.get('/S') == '/URI':
                uris.append(action['/URI'])
    for ref in page['/Resources'].get('/Font', {}).values():
        font = ref.get_object()
        descriptor = font.get('/FontDescriptor')
        if descriptor:
            desc = descriptor.get_object()
            font_states[str(font['/BaseFont'])] = any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3'])
all_text = '\n'.join(texts)
for required in ['fengfan3812@gmail.com','ComfyUI','广联达杯','一等奖','3.86','3 / 80','7 / 80']:
    assert required in all_text, required
for outdated in ['2 / 40', '7 / 40', '2/40', '7/40']:
    assert outdated not in all_text, outdated
assert all(font_states.values())
assert any('BV1nRMh6LEZs' in u for u in uris)
assert any('BV1pXMh62EA9' in u for u in uris)
assert 'julianobunting97' not in all_text

font = ImageFont.truetype('C:/Windows/Fonts/calibri.ttf', 18)
pngs = sorted((WORK/'rendered').glob('page-*.png'))
if len(pngs) == 26:
    for start in range(0,len(pngs),8):
        subset = pngs[start:start+8]
        sheet = Image.new('RGB',(1320,((len(subset)+1)//2)*400),'#DDE0D7')
        d = ImageDraw.Draw(sheet)
        for j,png in enumerate(subset):
            with Image.open(png) as image:
                image.thumbnail((640,360))
                x,y = (j%2)*660+10,(j//2)*400+28
                sheet.paste(image,(x,y))
            d.text((x,y-25),f'PAGE {start+j+1:02d}',font=font,fill='#252D29')
        sheet.save(WORK/f'review-{start+1:02d}-{start+len(subset):02d}.jpg',quality=94)

report = {'pages':len(reader.pages),'page_size':[1280,720],'ratio':'16:9',
          'size_mb':round(PDF.stat().st_size/1024/1024,2),'embedded_fonts':font_states,
          'links':uris,'rendered_pages':len(pngs),'text_and_links':'passed'}
(WORK/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
