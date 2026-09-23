"""Validate the PDF and make visual review sheets without altering source assets."""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'tmp/pdfs/light-edition'
PDF = ROOT / 'output/pdf/曹硕_环境艺术设计作品集_16比9_浅色求职版_含展板.pdf'
reader = PdfReader(PDF)
assert len(reader.pages) == 29
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
assert any('Anurati' in name for name in font_states)
assert 'PORTFOLIO' in texts[0]
assert '曹硕' not in texts[0]
assert '曹硕' in texts[1]
assert '潍坊学院' not in texts[0]
assert '环境设计本科' not in texts[0]
assert '潍坊学院' in texts[1]
assert '环境设计本科在读' in texts[1]
assert '世纪绿洲' not in texts[0]
assert '1532' not in texts[0]
assert not any(ref.get_object().get('/Subtype') == '/Image'
               for ref in reader.pages[0]['/Resources'].get('/XObject', {}).values())
assert not any(ref.get_object().get('/Subtype') == '/Image'
               for ref in reader.pages[-1]['/Resources'].get('/XObject', {}).values())
assert 'LET\'S CREATE' in texts[-1]
assert 'mailto:fengfan3812@gmail.com' in uris
assert 'tel:13361444417' in uris
assert any('BV1nRMh6LEZs' in u for u in uris)
assert any('BV1pXMh62EA9' in u for u in uris)
assert 'julianobunting97' not in all_text
manifest = json.loads((WORK/'page-manifest.json').read_text(encoding='utf-8'))
assert len(manifest) == len(reader.pages)
assert manifest[0]['images'] == []
assert 'vector axonometric' in manifest[0]['illustration']
assert manifest[-1]['images'] == []
assert 'vector axonometric / Pei-inspired geometric light court' in manifest[-1]['illustration']
assert Path(manifest[7]['images'][0]).as_posix() == 'output/pdf/source-assets/1532-park-detail-07.jpg'
prepared_image = ROOT/'output/pdf/source-assets/1532-park-detail-07.jpg'
assert prepared_image.stat().st_size < 1024*1024
assert any(ref.get_object().get('/Subtype') == '/Image'
           and ref.get_object().get('/Width') == 2048
           and ref.get_object().get('/Height') == 1152
           and ref.get_object().get_data() == prepared_image.read_bytes()
           for ref in reader.pages[7]['/Resources']['/XObject'].values())
board_pages = [page for page in manifest if page.get('full_boards')]
assert [page['page'] for page in board_pages] == [9, 10, 16]
assert sum(len(page['full_boards']) for page in board_pages) == 6
boxes = json.loads((WORK/'text-boxes.json').read_text(encoding='utf-8'))
profile_labels = ['曹硕', 'CAO SHUO', '环境设计本科在读', '潍坊学院', '预计 2027 年毕业']
profile_boxes = [box for box in boxes if box[0] == 2 and box[1] in profile_labels and box[3] > 100]
assert len(profile_boxes) == len(profile_labels)
assert all(abs((box[2]+box[4])/2 - 149) < 0.01 for box in profile_boxes)
for page in board_pages:
    assert not any(box[0] == page['page'] and box[1] in ['01', '02']
                   and box[2] < 320 and box[3] > 60 for box in boxes)
    assert any(box[0] == page['page'] and box[2] == 52 and box[3] == 100
               for box in boxes)
    images = reader.pages[page['page']-1]['/Resources']['/XObject'].values()
    images = [ref.get_object() for ref in images if ref.get_object().get('/Subtype') == '/Image']
    assert len(images) == 2
    assert all(im['/Height'] >= 4900 for im in images), page['page']
for text, start in [('04 - 10',4),('11 - 16',11),('17 - 20',17),('21 - 22',21),('23 - 25',23),('26 - 27',26)]:
    assert text in texts[2]
    assert manifest[start-1]['chapter'].split(' / ')[0] in ['01','02','03','04','05','06']

font = ImageFont.truetype('C:/Windows/Fonts/calibri.ttf', 18)
pngs = sorted((WORK/'rendered').glob('page-*.png'))
assert len(pngs) == len(reader.pages)
if len(pngs) == len(reader.pages):
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
          'links':uris,'rendered_pages':len(pngs),'full_board_pages':[p['page'] for p in board_pages],
          'complete_boards':6,'text_and_links':'passed'}
(WORK/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
