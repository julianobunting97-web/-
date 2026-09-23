"""A vector-only, conceptual axonometric drawing for the portfolio cover."""
import math

from reportlab.lib.colors import HexColor


def draw_cover_axonometric(book):
    c = book.c
    paper = '#F5F3ED'
    edge = '#64736B'
    faint = '#CDD2C5'
    light = '#E8EBE1'
    sage = '#D5DDCE'
    scale = 24
    faces = []

    def project(p):
        u, v, z = p
        return 755 + (u-v)*math.sqrt(3)/2*scale, 265 + (u+v)*scale/2-z*scale

    def path(points, fill=None, stroke=edge, width=.7, close=False, dash=None):
        c.saveState()
        c.setLineWidth(width)
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setDash(dash or [])
        if fill:
            c.setFillColor(HexColor(fill))
        if stroke:
            c.setStrokeColor(HexColor(stroke))
        p = c.beginPath()
        for i, pt in enumerate(points):
            x, y = project(pt)
            if i == 0:
                p.moveTo(x, 720-y)
            else:
                p.lineTo(x, 720-y)
        if close:
            p.close()
        c.drawPath(p, fill=bool(fill), stroke=bool(stroke))
        c.restoreState()

    def face(points, fill, stroke=edge, width=.7):
        # Painter ordering uses distance along the axonometric viewing direction.
        depth = sum(u+v+z*1.2 for u, v, z in points)/len(points)
        faces.append((depth, points, fill, stroke, width))

    def flush():
        for _, points, fill, stroke, width in sorted(faces, key=lambda f: f[0]):
            path(points, fill, stroke, width, close=True)
        faces.clear()

    def block(u, v, w, d, base, height, top=paper, left=light, right='#E1E6DB', width=.65):
        z = base+height
        face([(u,v+d,base),(u+w,v+d,base),(u+w,v+d,z),(u,v+d,z)], left, width=width)
        face([(u+w,v,base),(u+w,v+d,base),(u+w,v+d,z),(u+w,v,z)], right, width=width)
        face([(u,v,z),(u+w,v,z),(u+w,v+d,z),(u,v+d,z)], top, width=width)

    def plane(u, v, w, d, z=0, fill=None, stroke=edge, width=.55):
        path([(u,v,z),(u+w,v,z),(u+w,v+d,z),(u,v+d,z)],
             fill, stroke, width, close=True)

    def arc(u, v, r, z, start=0, end=360, steps=80):
        return [(u+r*math.cos(math.radians(start+(end-start)*i/steps)),
                 v+r*math.sin(math.radians(start+(end-start)*i/steps)),z)
                for i in range(steps+1)]

    c.saveState()

    # Light construction lines extend past the built forms, without a surrounding frame.
    for u in [1, 7.6, 12, 17.5]:
        path([(u,-.6,0),(u,13.8,0)], stroke=faint, width=.35, dash=[2,4])
    for v in [1, 6.2, 12.4]:
        path([(-.6,v,0),(18.8,v,0)], stroke=faint, width=.35, dash=[2,4])

    outline = [(0,0),(15.5,0),(15.5,5.7),(18.5,5.7),
               (18.5,12.5),(10,12.5),(10,14),(0,14)]
    path([(u+.25,v+.3,-.28) for u,v in outline], '#E7E9DF', None, close=True)
    for i, (u,v) in enumerate(outline):
        a,b = outline[(i+1)%len(outline)]
        if a <= u and b >= v:
            path([(u,v,0),(a,b,0),(a,b,-.18),(u,v,-.18)], '#E2E7DC', faint, .5, True)
    path([(u,v,0) for u,v in outline], '#F0F1E9', edge, .85, True)

    # Ground plane: a quiet mineral forecourt and a planted inset.
    plane(.8,7.4,8.3,5.5,.01,paper,faint)
    plane(10.5,1.1,3.7,2.1,.01,sage,faint)
    for i in range(9):
        u = 10.7+i*.39
        path([(u,1.2,.02),(u,3.1,.02)], stroke='#B3BFAE', width=.35)
    for u in [1.3,2.7,4.1,5.5,6.9,8.3]:
        path([(u,7.4,.015),(u,12.9,.015)], stroke='#DEE2D6', width=.3)
    path([(1.8,13.35,.015),(8.4,13.35,.015)], stroke=faint, width=.45)
    plane(10.8,6.0,7.4,6.0,.05,'#E8EDE3',faint)

    # A stepped approach connects the open room to the courtyard.
    block(.7,.7,7.2,5.9,0,.44,top=paper)
    for i in range(5):
        block(3.0,6.6+i*.34,3.0,.34,0,.44-i*.075,top=paper,width=.5)
    block(10.7,5.8,7.6,6.4,0,.65,top='#F4F5EF')
    for i in range(4):
        block(8.9+i*.45,7.5,.45,3.4,0,.14+i*.16,top=paper,width=.5)
    flush()
    for v in [7,8.3,9.6,10.9]:
        path([(11,v,.665),(18.05,v,.665)], stroke=faint,width=.35)

    # Solid walls are offset to expose the interior instead of making closed boxes.
    block(1,1,6.6,.16,.44,3.15,top=paper,left='#E4E9DE',right=sage)
    block(1,1,.16,5.15,.44,3.15,top=paper,left='#EEF0E8',right=paper)
    block(7.44,1,.16,2.0,.44,3.15,top=paper,left=light,right='#DDE4D6')
    block(1,6.0,1.65,.15,.44,2.15,top=paper,left=paper,right=light)
    block(6.25,6.0,1.35,.15,.44,2.15,top=paper,left=paper,right=light)
    block(1.25,2.3,.52,2.5,.44,.42,top=sage)

    # A framed wall opening introduces a horizontal datum between the two volumes.
    block(8.65,2.8,4.5,.16,0,.7,top=paper,left=sage)
    block(8.65,2.8,.32,.16,.7,1.95,top=paper,left=sage)
    block(12.83,2.8,.32,.16,.7,1.95,top=paper,left=sage)
    block(8.65,2.8,4.5,.16,2.15,.5,top=paper,left=sage)
    flush()

    # Thin, repeated portal frames provide the dense end of the composition.
    for u in [11.1,12.5,13.9,15.3,16.7,18.1]:
        block(u,6.05,.10,.10,.65,2.9,top=paper,left=paper,right=light,width=.6)
        block(u,11.8,.10,.10,.65,2.9,top=paper,left=paper,right=light,width=.6)
        block(u,6.05,.10,5.85,3.55,.12,top=paper,left=light,width=.65)
    block(11.1,6.05,7.1,.10,3.4,.15,top=paper,left=light,width=.55)
    block(11.1,11.8,7.1,.10,3.4,.15,top=paper,left=light,width=.55)
    block(13.0,10.5,3.1,.6,.65,.4,top=sage,width=.55)
    flush()

    # A low crescent wall softens the orthogonal floor and frames a shared outdoor void.
    path(arc(5.0,10.6,2.1,.025),fill='#E4EADF',stroke='#B4C0B0',width=.6,close=True)
    path(arc(5.0,10.6,1.85,.03),stroke='#BEC9B8',width=.35)
    lower = arc(5.0,10.6,2.35,0,35,155,40)
    upper = arc(5.0,10.6,2.35,.83,35,155,40)
    path(lower+list(reversed(upper)),fill='#D9E1D2',stroke=edge,width=.6,close=True)
    inner = arc(5.0,10.6,2.15,.83,35,155,40)
    path(upper+list(reversed(inner)),fill=paper,stroke=edge,width=.5,close=True)
    block(7.85,10.4,.55,2.1,0,.4,top=sage,width=.55)
    flush()

    # An exploded canopy stays open and weightless; dashed ties identify its position.
    for u,v in [(2,2),(7.2,2),(7.2,5.65),(2,5.65)]:
        path([(u,v,3.6),(u,v,4.45)],stroke='#A9B5A5',width=.4,dash=[2,3])
    plane(2,2,5.2,3.65,4.45,None,'#99A890',.65)
    for u in [2.8,3.6,4.4,5.2,6.0,6.8]:
        path([(u,2,4.45),(u,5.65,4.45)],stroke='#B6C1AC',width=.35)
    path([(2,3.82,4.45),(7.2,3.82,4.45)],stroke='#B6C1AC',width=.35)

    c.restoreState()
    book.manifest[-1]['illustration'] = 'Original vector axonometric / abstract spatial composition'


def draw_closing_axonometric(book):
    """An original Pei-inspired museum study, not a depiction of a built project."""
    c = book.c
    paper = '#F5F3ED'
    edge = '#64736B'
    faint = '#CDD2C5'
    faces = []

    def project(point):
        u, v, z = point
        return 1095+(u-v)*math.sqrt(3)/2*26, 458+(u+v)*13-z*26

    def path(points, fill=None, stroke=edge, width=.65, close=False, dash=None):
        c.saveState()
        c.setLineWidth(width)
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setDash(dash or [])
        if fill:
            c.setFillColor(HexColor(fill))
        if stroke:
            c.setStrokeColor(HexColor(stroke))
        p = c.beginPath()
        for i, point in enumerate(points):
            x, y = project(point)
            if i == 0:
                p.moveTo(x, 720-y)
            else:
                p.lineTo(x, 720-y)
        if close:
            p.close()
        c.drawPath(p, fill=bool(fill), stroke=bool(stroke))
        c.restoreState()

    def face(points, fill, lines=(), stroke=edge, width=.65):
        depth = sum(a+b+h for a,b,h in points)/len(points)
        faces.append((depth,points,fill,lines,stroke,width))

    def block(u, v, w, d, base, height, front='#E8EBE1', side='#D5DDCE'):
        z = base+height
        planes = [
            ([(u,v+d,base),(u+w,v+d,base),(u+w,v+d,z),(u,v+d,z)],front),
            ([(u+w,v,base),(u+w,v+d,base),(u+w,v+d,z),(u+w,v,z)],side),
            ([(u,v,z),(u+w,v,z),(u+w,v+d,z),(u,v+d,z)],paper),
        ]
        for points, fill in planes:
            face(points,fill)

    def flush():
        for _, points, fill, lines, stroke, width in sorted(faces, key=lambda face: face[0]):
            path(points,fill,stroke,width,close=True)
            for line in lines:
                path(line,stroke='#ABB7AA',width=.3)
        faces.clear()

    def lerp(a, b, t):
        return tuple(x+(y-x)*t for x,y in zip(a,b))

    def glass_triangle(a, b, apex, fill):
        grid = []
        for i in range(1,7):
            t = i/7
            grid.extend([
                [lerp(a,apex,t),lerp(b,apex,t)],
                [lerp(a,b,t),lerp(apex,b,t)],
                [lerp(b,a,t),lerp(apex,a,t)],
            ])
        face([a,b,apex],fill,grid,stroke='#7E9285',width=.75)

    # The terrace and water court stay grounded; only the skylight is exploded.
    for u in [.6,5.4]:
        path([(u,-.8,0),(u,7.2,0)],stroke=faint,width=.35,dash=[2,4])
    path([(-.5,3.6,0),(6.2,3.6,0)],stroke=faint,width=.35,dash=[2,4])
    path([(.12,.16,-.16),(6.02,.16,-.16),(6.02,6.96,-.16),(.12,6.96,-.16)],
         fill='#E7E9DF',stroke=None,close=True)
    block(0,0,5.9,6.8,-.12,.12,front='#E7EADF',side='#E1E6DB')
    flush()

    block(.45,.55,5,4.4,0,.54)
    for i in range(4):
        block(1.5,4.95+i*.35,2.5,.35,0,.432-i*.108)
    flush()
    path([(4.35,5.1,.02),(5.48,5.1,.02),(5.48,6.37,.02),(4.35,6.37,.02)],
         fill='#DDE7DF',stroke='#9DAE9E',width=.5,close=True)
    for v in [5.35,5.65,5.95]:
        path([(4.47,v,.025),(5.36,v,.025)],stroke='#BDCEBF',width=.3)
    for u in [1.5,2.75,4.0]:
        path([(u,.7,.55),(u,4.8,.55)],stroke=faint,width=.3)
    for v in [2.0,3.3,4.65]:
        path([(.6,v,.55),(5.3,v,.55)],stroke=faint,width=.3)

    # A triangular stone wing establishes a strong diagonal beside the open atrium.
    stone_top = [(.6,.7,6.85),(4.8,.7,6.85),(.6,2.55,6.85)]
    face(stone_top,paper)
    stone_front = [(4.8,.7,.54),(.6,2.55,.54),(.6,2.55,6.85),(4.8,.7,6.85)]
    joints = [[(4.8,.7,z),(.6,2.55,z)] for z in [1.65,2.85,4.05,5.25]]
    for t in [.25,.5,.75]:
        a = lerp(stone_front[0],stone_front[1],t)
        joints.append([a,(a[0],a[1],6.85)])
    face(stone_front,'#E8EADF',joints)

    # Split side masses and a low bridge imply a gallery rather than a sealed cube.
    block(.6,2.55,.5,1.9,.54,4.6,front='#E6EADD',side='#DDE4D6')
    block(4.55,1.6,.62,2.85,.54,4.95,front=paper,side='#DFE5D9')
    block(.6,4.2,1.0,.26,.54,2.35,front=paper)
    block(3.75,4.2,1.42,.26,.54,2.35,front=paper)
    block(1.6,4.2,2.15,.26,2.55,.34,front=paper)
    block(1.4,2.9,2.35,.42,.54,.38,front='#D5DDCE')
    flush()

    # The raised triangulated roof makes light and geometry the focus of the closing.
    corners = [(.48,.55,8.15),(5.3,.55,8.15),(5.3,4.7,8.15),(.48,4.7,8.15)]
    for u,v,z in corners:
        base = 6.85 if v < 1 else 3.05
        path([(u,v,base),(u,v,z)],stroke='#A6B5A2',width=.4,dash=[2,4])
    apex = (2.65,2.35,11.7)
    # Rear edges remain only as faint construction; the two visible glass faces are solid.
    path([corners[0],corners[1]],stroke=faint,width=.35)
    path([corners[0],corners[3]],stroke=faint,width=.35)
    path([corners[0],apex],stroke=faint,width=.35,dash=[2,3])
    glass_triangle(corners[1],corners[2],apex,'#E0E9E0')
    glass_triangle(corners[2],corners[3],apex,'#EDF0E8')
    flush()
    book.manifest[-1]['illustration'] = 'Original vector axonometric / Pei-inspired geometric light court'
