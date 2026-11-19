"""One garden detail: the mature tree and the soil caught in its roots."""
from math import cos, pi, sin
from pathlib import Path
from random import Random

import numpy as np
from PIL import ImageDraw, ImageFont

from garden import garden, tree
from geometry import Model
from pitch_models import ORANGE, INK
from render_pitch import Camera, H, OUT, PAPER, W, draw_render

CUT = 2.26
CX = 2.55
DEPTH = 1.18


def sectioned_yard():
    """Slice the original yard on a vertical plane, keeping the deck behind it."""
    source = garden(0, yard_only=True)
    result = Model()
    for colour, (vertices, faces) in source.parts.items():
        for face in faces:
            tri = [vertices[i] for i in face]
            poly = []
            for a, b in zip(tri, tri[1:] + tri[:1]):
                if a[1] >= CUT:
                    poly.append(a)
                if (a[1] < CUT) != (b[1] < CUT):
                    t = (CUT - a[1]) / (b[1] - a[1])
                    poly.append(tuple(x + t * (y - x) for x, y in zip(a, b)))
            if len(poly) >= 3:
                result.mesh(colour, poly, [tuple(range(len(poly)))])
    # The vertical face is visible from the camera. Vary the stratum boundaries
    # together so adjacent layers meet along one continuous geological section.
    xs = np.linspace(-.06, 7.06, 24)
    rng = Random(29)
    roof = [.028] * len(xs)
    for base, noise, colour in [(-.075,.013,'85875c'),(-.32,.05,'806449'),
                                (-.77,.064,'a27e59'),(-DEPTH,0,'b1936e')]:
        floor = [base + rng.uniform(-noise,noise) for _ in xs]
        for i in range(len(xs)-1):
            result.mesh(colour,[(xs[i],CUT-.012,roof[i]),(xs[i+1],CUT-.012,roof[i+1]),
                                (xs[i+1],CUT-.012,floor[i+1]),(xs[i],CUT-.012,floor[i])],[(0,1,2,3)])
        roof=floor
    result.box(3.5,(CUT+5.655)/2,-DEPTH,7.12,5.655-CUT-.02,DEPTH-.03,'a68762')
    return result


def root_section(m):
    # A cut through the front half of the root ball. The light roots continue
    # beyond the proposed digging boundary into the undisturbed outer soil.
    y = CUT-.045
    ring = [(CX+.95*cos(t), y, -.025-.88*sin(t)) for t in np.linspace(0,pi,27)]
    m.mesh('614c3b',ring,[tuple(range(len(ring)))])
    for i in range(0,len(ring)-1,2):
        m.rod(ring[i],ring[i+1],.014,ORANGE,7)
    rng=Random(21)
    def root(points, radii, colour):
        nodes=[(CX+x,y-.043,z) for x,z in points]
        for i in range(len(nodes)-1):
            m.rod(nodes[i],nodes[i+1],radii[i],colour,9,radii[i+1])
    for sign in (-1,1):
        def branch(points,radii,c):
            root([(sign*x,z) for x,z in points],radii,c)
        branch([(0,.07),(.12,-.08),(.36,-.18),(.64,-.19),(.94,-.24),(1.24,-.21),(1.52,-.26),(1.91,-.32)],
               [.123,.087,.064,.048,.033,.027,.016,.004],'b18c5d')
        branch([(.18,-.11),(.32,-.29),(.46,-.41),(.69,-.49),(.94,-.53),(1.18,-.63)],
               [.064,.045,.036,.027,.015,.004],'bf9867')
        branch([(.03,-.04),(.08,-.30),(.20,-.48),(.31,-.60),(.34,-.76),(.44,-.87)],
               [.073,.054,.039,.025,.015,.005],'bf9567')
        for x,z in ((.41,-.16),(.58,-.18),(.87,-.23),(1.16,-.22),(1.49,-.26),(.71,-.49),(.32,-.60)):
            dx=rng.uniform(.11,.27);dz=rng.uniform(.07,.16)
            branch([(x,z),(x+.07,z-.08),(x+dx,z-dz),(x+dx+.12,z-dz-.06)],
                   [.025,.020,.012,.003],'c8a77b')
    for j in range(12):
        u=pi*j/12
        m.rod((CX+.95*cos(u),CUT+.95*sin(u),.051),
              (CX+.95*cos(u+.145),CUT+.95*sin(u+.145),.051),.015,ORANGE,7)


def gardener(m):
    """A figure leaning on a garden spade beside the cut line."""
    rng=Random(78)
    def rod(a,b,r,c,tip=None):m.rod(a,b,r,c,9,tip)
    x,y=CX+1.42,CUT+.29
    def at(dx,dy,z):return (x+dx,y+dy,z)
    for xx,yy in ((-.13,-.045),(.15,.14)):
        m.box(*at(xx-.045,yy,.04),.27,.14,.115,INK,-.06)
        rod(at(xx,yy,.14),at(xx-.04,yy,.47),.074,'57615c',.085)
        rod(at(xx-.04,yy,.47),at(xx*.65,.06,.82),.088,'616960',.10)
    rod(at(0,.06,.75),at(-.15,.05,1.24),.175,'839088',.205)
    rod(at(-.15,.05,1.22),at(-.20,.045,1.37),.075,'ac9175')
    m.blob(*at(-.20,.045,1.45),.135,.12,.16,'c5a98a',rng)
    m.blob(*at(-.19,.055,1.54),.144,.128,.08,'555c55',rng)
    # Blade, socket, shaft and a hollow D grip.
    bx,by=x-.70,y-.13
    m.mesh('515e5c',[(bx-.118,by,.20),(bx+.115,by,.21),(bx+.10,by-.025,.023),
                     (bx,by-.035,-.037),(bx-.094,by-.025,.03),(bx,by-.045,.13)],
           [(0,1,5),(1,2,5),(2,3,5),(3,4,5),(4,0,5)])
    lo=(bx+.003,by,.16);hi=at(-.46,-.095,1.03)
    rod(lo,hi,.023,'a98159')
    rod(lo,(bx+.028,by,.29),.032,'65706b')
    for side in (-1,1):
        rod(hi,at(-.44,-.095+side*.085,1.155),.017,INK)
    rod(at(-.44,-.18,1.155),at(-.44,-.01,1.155),.021,'ad855e')
    for yy,z,dx in ((-.125,1.16,-.44),(.148,.83,-.51)):
        elbow=at(-.30,yy,.99); hand=at(dx,-.083,z)
        rod(at(-.14,yy,1.20),elbow,.06,'839088')
        rod(elbow,hand,.046,'c5a98a',.033)
    for i in range(10):
        m.blob(bx+rng.uniform(-.19,.02),by+rng.uniform(-.08,.17),.062,
               rng.uniform(.055,.10),rng.uniform(.04,.08),rng.uniform(.034,.076),'896e52',rng,6)


def main():
    m=sectioned_yard()
    tree(m,CX,CUT+.015,True)
    root_section(m)
    gardener(m)
    cam=Camera(False)
    cam.target=np.array([3.36,3.16,1.08])
    cam.look=np.array([2.8,-15.,5.6])
    cam.radius=4.92
    # Camera axes follow this lower, section-facing angle.
    cam.right=np.cross([0,0,1],cam.look);cam.right/=np.linalg.norm(cam.right)
    cam.up=np.cross(cam.look,cam.right);cam.up/=np.linalg.norm(cam.up)
    img=draw_render(m,cam,False,72,W,ground_z=-DEPTH-.006)
    d=ImageDraw.Draw(img)
    try:
        f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',28)
    except OSError:
        f=ImageFont.load_default(size=28)
    def note(target,text,pos):
        hit=cam.screen(target);x,y=pos;w=d.textlength(text,font=f)
        end=x+w+10 if x<hit[0] else x-10
        d.line([tuple(hit),(end,y)],fill='#ac4633',width=3)
        d.ellipse((hit[0]-4,hit[1]-4,hit[0]+4,hit[1]+4),fill='#ac4633')
        d.rounded_rectangle((x-10,y-21,x+w+10,y+21),radius=5,fill=PAPER)
        d.text((x,y),text,fill='#343b37',font=f,anchor='lm')
    note((CX+.60,CUT-.06,-.66),'Root ball to lift',(950,979))
    note((CX-1.27,CUT-.09,-.23),'Roots beyond the cut',(85,871))
    assert img.size==(W,H)
    OUT.mkdir(exist_ok=True)
    img.save(OUT/'G4-established-roots.png',optimize=True)


if __name__=='__main__':
    main()
