"""Matched prototype states for the six media slots in pitch 778. Metres; Y north."""
from math import cos, sin, pi, dist
from random import Random
from geometry import Model
from garden import garden, tree

INK='374042'
ORANGE='ca4931'
STONE='e1dacb'
WOOD='c9b18c'
SHALE='6e7975'
MILK='eee9dc'
FRONT=3.72
FAR=1.62
PROJECTION=.60
A=(1.53,3.58)
B=(5.91,2.33)
PIT=.46
FENCE=7.00
BIN_WIDTH=.54
TAP=(2.07,4.75)
BED=(1.38,1.78)
BIN_ROUTE=[(6.66,.48),(6.66,2.35),(6.66,5.48)]


def path(m,points,c,r=.022,dashed=False,z=.066):
    for a,b in zip(points,points[1:]):
        length=dist(a,b)
        def loc(t):return (a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]),z)
        if dashed:
            n=max(1,round(length/.18))
            for i in range(n):m.rod(loc(i/n),loc((i+.62)/n),r,c,6)
        else:m.rod(loc(0),loc(1),r,c,8)


def mannequin(m,x,y,a,plates,shirt):
    # z-up figures with jointed arms and separate dishes held in each hand.
    def at(u,v,h):return (x+u*cos(a)-v*sin(a),y+u*sin(a)+v*cos(a),h)
    for k in (-1,1):
        m.rod(at(k*.10,0,.08),at(k*.09,0,.80),.075,'575d60',9,.09)
        m.box(*at(k*.10,.034,.013),.17,.28,.09,'4b514e',a)
    m.rod(at(0,0,.73),at(0,0,1.26),.193,shirt,9,.218)
    m.rod(at(0,0,1.27),at(0,0,1.40),.071,'b79a80',10)
    m.blob(*at(0,0,1.48),.137,.13,.165,'c6ab90',Random(89))
    m.blob(*at(0,-.024,1.575),.138,.126,.10,'655b52',Random(17))
    for k in (-1,1):
        elbow=at(.246*k,.025,1.00);hand=at(k*.203,.30,1.04)
        m.rod(at(k*.164,0,1.23),elbow,.071,shirt,9,.06)
        m.rod(elbow,hand,.048,'c6ab90',9,.04)
        if plates or k==1:
            m.rod((hand[0],hand[1],1.069),(hand[0],hand[1],1.087),.136,MILK,20,.156)


def kitchen(s):
    m=Model(); bx=m.box;rod=m.rod
    bx(4.2,2.20,-.22,8.48,4.48,.21,'bcae97')
    for j in range(12):
        for i in range(6):
            bx(.7+i*1.4,.183+j*.366,-.010,1.395,.361,.017,'e4dac5' if (i+j)%3 else 'dfd4be')
    bx(-.045,2.20,.008,.09,4.48,1.19,STONE)
    bx(4.20,4.445,.008,8.48,.09,1.2,STONE)
    # Dining is reached through the single opening beside the rear counter.
    bx(5.65,1.04,.01,.09,2.08,.66,STONE)
    bx(5.65,4.18,.01,.09,.44,.66,STONE)
    bx(2.75,4.10,.05,5.40,.63,.75,SHALE)
    bx(2.75,4.06,.80,5.48,.68,.075,MILK)
    for i in range(7):
        cx=.47+i*.76
        if i==4:continue
        bx(cx,3.752,.13,.73,.048,.62,'b4b9ac')
        bx(cx,3.72,.66,.19,.025,.019,INK)
    # Black hob and the heavy pot on the adjacent landing space.
    bx(.90,4.06,.876,.81,.53,.025,INK)
    for x in (.69,1.10):
        for y in (3.94,4.18):rod((x,y,.90),(x,y,.912),.092,'76807a',16)
    rod((1.57,4.08,.875),(1.57,4.08,1.13),.165,'4d5656',16,.19)
    bx(1.57,4.08,1.08,.53,.05,.035,INK)
    bx(4.48,4.07,.876,.74,.45,.013,'909c98')
    bx(4.48,4.07,.89,.62,.34,.012,'566864')
    for a,b in [((4.70,4.32,.88),(4.70,4.32,1.15)),((4.70,4.32,1.15),(4.70,4.10,1.15)),((4.70,4.10,1.15),(4.70,4.10,1.10))]:
        rod(a,b,.022,INK,10)
    x=3.51
    if not s:
        bx(x,FRONT+.018,.09,.72,.036,.69,'788584')
        bx(x,FRONT-.012,.67,.43,.029,.033,INK)
    else:
        bx(x,FRONT+.016,.12,.71,.032,.65,'434f4e')
        bx(x,FRONT-.30,.135,.72,PROJECTION,.055,'87938f')
        # The pulled rack reaches the same outer edge as the horizontal door.
        for k in range(7):
            xx=x-.31+k*.103
            rod((xx,3.15,.22),(xx,3.67,.22),.009,INK,6)
        for yy in (3.14,3.38,3.65):
            rod((x-.34,yy,.235),(x+.34,yy,.235),.014,INK,8)
        for xx in (x-.34,x+.34):
            rod((xx,3.14,.31),(xx,3.66,.31),.015,INK,8)
        for j in range(5):
            xx=x-.23+j*.10
            rod((xx,3.40,.315),(xx+.027,3.40,.315),.143,'f2ecd9',20)
    depth=.75 if s==2 else 1.05;near=FAR+depth
    bx(3.02,FAR+.375,.03,2.94,.66,.12,'76786e')
    bx(3.02,FAR+.375,.15,2.96,.73,.67,WOOD)
    bx(3.02,FAR+depth/2,.82,3.04,depth,.078,'eee4d1')
    if s<2:
        bx(3.02,FAR+.89,.15,2.96,.285,.67,'c3ab8a')
        # Removable shallow drawer bank, including its visible right end panel.
        bx(4.507,FAR+.895,.15,.038,.285,.68,ORANGE)
        for k in range(3):
            bx(3.02,near-.012,.16+k*.213,2.94,.04,.194,ORANGE)
            bx(3.02,near-.017,.30+k*.213,.60,.025,.018,INK)
        bx(3.02,near-.08,.901,3.04,.16,.012,ORANGE)
    if not s:
        for yy in (FAR,near):bx(3.02,yy,.907,3.04,.025,.01,ORANGE)
        for xx in (1.51,4.53):bx(xx,FAR+depth/2,.907,.025,depth,.01,ORANGE)
    if s==2:
        path(m,[(1.50,2.67),(4.54,2.67)],ORANGE,.015,True,.901)
    # Dining table, legs and chairs.
    bx(7.23,2.76,.74,1.32,1.02,.078,WOOD)
    for xx in (6.70,7.76):
        for yy in (2.36,3.16):bx(xx,yy,.013,.07,.07,.74,INK)
    for yy,sign in ((1.98,-1),(3.54,1)):
        bx(7.23,yy,.42,.45,.43,.055,'969f90')
        bx(7.23,yy+sign*.185,.46,.45,.06,.36,'969f90')
        for dx in (-.17,.17):
            for dy in (-.15,.15):bx(7.23+dx,yy+dy,.011,.045,.045,.41,INK)
    for xx in (6.95,7.52):rod((xx,2.76,.818),(xx,2.76,.837),.149,MILK,20)
    if s:
        # Same poses; only the path and island change in K3.
        mannequin(m,2.04,3.16,-pi/2,True,'697b76')
        mannequin(m,4.20,3.16,pi/2,False,'a09686')
        path(m,[(1.15,3.18),(1.43,3.08),(2.87,3.04)],ORANGE,.030,True,.045)
        if s==2:path(m,[(2.87,3.04),(3.08,2.80),(4.85,2.80),(5.67,2.91),(6.38,2.74)],ORANGE,.027,True,.045)
    else:
        for xx,yy in ((1.23,3.28),(4.2,3.24)):
            rod((xx,yy,.014),(xx,yy,.044),.095,ORANGE,20)
    return m


def hose(p):
    via=[TAP,(2.08,3.21),BED]
    if p==A:return via+[(1.06,2.15),(1.06,3.30),(A[0]-.15,A[1])]
    if p==B:return via+[(2.10,1.68),(5.22,1.68),(B[0]-.16,B[1])]
    return via


def yard(s):
    m=garden(0,yard_only=True)
    # Desaturate the garden palette before adding the moving parts.
    from collections import defaultdict
    remap=defaultdict(lambda:([],[]))
    for colour,(vs,fs) in m.parts.items():
        rgb=[int(colour[i:i+2],16) for i in (0,2,4)]
        lum=sum(x*w for x,w in zip(rgb,(.21,.72,.07)))
        key=''.join(f'{round(.36*c+.45*lum+.19*231):02x}' for c in rgb)
        pts,tris=remap[key];k=len(pts);pts.extend(vs);tris.extend((a+k,b+k,c+k) for a,b,c in fs)
    m.parts=remap;bx=m.box;rod=m.rod
    # Right boundary and the bin that must fit through the side gate.
    bx(7.027,2.78,.025,.055,5.56,.28,'aca994')
    bx(6.66,.49,.13,BIN_WIDTH,.55,.72,'666e68')
    bx(6.66,.49,.85,BIN_WIDTH,.57,.060,INK)
    for xx in (6.45,6.86):rod((xx-.025,.64,.15),(xx+.025,.64,.15),.11,INK,12)
    rod((2.07,4.77,.75),(2.07,4.56,.75),.037,INK)
    rod((2.07,4.56,.75),(2.07,4.56,.64),.033,INK)
    bx(2.07,4.65,.785,.16,.035,.035,'9d795d')
    path(m,BIN_ROUTE,'545e5b',.026,True,.10)
    p=[None,A,B][s]
    route=hose(p)
    path(m,route,'576f73',.027,False,.087)
    if not s:
        for xx,yy in (A,B):
            bx(xx,yy,.04,.075,.075,.49,WOOD);bx(xx,yy,.43,.09,.09,.075,ORANGE)
        tp=(3.58,1.15)
        rod((*tp,.045),(*tp,.37),.19,ORANGE,12,.27)
        tree(m,*tp,False)
    else:
        rod((*p,.04),(*p,.09),PIT,'96704f',36)
        for j in range(32):
            a=j*pi/16;b=(j+1)*pi/16
            rod((p[0]+PIT*cos(a),p[1]+PIT*sin(a),.094),(p[0]+PIT*cos(b),p[1]+PIT*sin(b),.094),.023,ORANGE,7)
        tree(m,*p,True)
    return m
