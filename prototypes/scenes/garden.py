"""Project 09. Relocate one tree, then compare its crown at the same site."""
from math import pi, cos, sin
from random import Random
from geometry import Model


def tree(m,x,y,mature):
    rng=Random(918); s=1.0 if mature else .51
    def loc(a,b,h):return (x+a*s,y+b*s,.06+h*s)
    m.rod(loc(0,0,0),loc(.06,.02,1.83),.135*s,'826749',9,.079*s)
    colours=['718948','91a25a','a9b56b','69864c','8eaa5f','889948']
    for i in range(7):
        a=2*pi*i/7+.27
        dx=cos(a)*.66;dy=sin(a)*.63; dz=2.08+.18*(i%3)
        m.rod(loc(.03,.01,1.05+(i%2)*.25),loc(dx,dy,dz),.062*s,'816648',8,.032*s)
        m.blob(*loc(dx,dy,dz+.26),.73*s,.67*s,.66*s,colours[i%6],rng)
    m.blob(*loc(.06,.01,2.96),.83*s,.74*s,.63*s,'9bac57',rng,9)


def garden(step, *, yard_only=False):
    m=Model(); box=m.box; rod=m.rod;rng=Random(909)
    box(3.5,2.8,-.26,7.12,5.71,.16,'a48761')
    box(3.5,2.8,-.10,7.08,5.66,.13,'a6b878')
    # Continuous paving along the right fence, up to the side gate.
    for i in range(14):
        box(6.44,.20+.40*i,.032,.91,.375,.042,('ddcdb1','d7c7a9')[i%2])
    # Back and left boundary; low front edges leave the plot readable.
    for i in range(38):
        h=1.15+.025*(i%3)
        box(-.025,.08+i*.148,.025,.065,.135,h,'bf966c' if i%3 else 'c99f73')
    for i in range(47):
        if 5.93<i*.15<6.93:continue
        box(.075+i*.15,5.57,.025,.14,.072,1.18,'c79b6d')
    for y in (.18,1.85,3.65,5.52):box(.04,y,0,.11,.12,1.23,'9e794f')
    for x in (5.9,6.99):box(x,5.48,.04,.13,.13,1.23,'8a6d49')
    for i in range(7):box(6.02+.139*i,5.47,.08,.123,.065,.99,'7b8f77')
    rod((5.98,5.40,.20),(6.90,5.40,.97),.035,'536c5b',6)
    box(6.79,5.415,.72,.11,.04,.03,'39473c')
    # Small rear house face, sliding doors and a pitched metal roof.
    box(3.54,5.21,.03,3.78,.66,1.80,'ded4b8')
    for j in range(12):
        box(3.54,4.870,.16+.138*j,3.75,.022,.012,'c5b89b')
    for x in (2.45,3.18):
        box(x,4.842,.24,.75,.08,1.31,'575f50')
        box(x,4.794,.32,.66,.02,1.16,'b1ccc0')
    box(4.67,4.84,.88,.87,.07,.63,'606e62')
    box(4.67,4.79,.94,.74,.03,.51,'adcbc3')
    m.mesh('59675f',[(1.53,4.77,1.84),(5.54,4.77,1.84),(5.54,5.7,2.15),(1.53,5.7,2.15)],[(0,1,2,3)])
    box(3.54,4.78,1.76,4.00,.095,.095,'4e6056')
    for i in range(23):
        x=1.55+i*.18
        rod((x,4.78,1.85),(x,5.70,2.16),.012,'879185',6)
    # Terrace with planks, an outdoor table and slatted chairs.
    for j in range(12):
        box(4.04,3.13+j*.15,.035,3.30,.142,.11,'cdab80' if j%4 else 'bd986d')
    rod((4.03,3.88,.145),(4.03,3.88,.81),.085,'967653',10)
    rod((4.03,3.88,.79),(4.03,3.88,.87),.48,'d6b784',24)
    for a in (-.4,1.95,3.72):
        x=4.03+.76*cos(a);y=3.88+.76*sin(a)
        tx,ty=-sin(a),cos(a)
        for k in (-1,0,1):
            box(x+tx*k*.131,y+ty*k*.131,.51,.31,.116,.04,'c09b66',a)
        for side in (-1,1):
            for end in (-1,1):
                dx=.11*end*cos(a)+side*.15*tx;dy=.11*end*sin(a)+side*.15*ty
                rod((x+dx*1.35,y+dy*1.35,.149),(x+dx,y+dy,.53),.028,'957a55',7)
            rod((x+.14*cos(a)+side*.15*tx,y+.14*sin(a)+side*.15*ty,.52),(x+.21*cos(a)+side*.15*tx,y+.21*sin(a)+side*.15*ty,.91),.025,'a48458',7)
        for k in (0,1):
            box(x+.19*cos(a),y+.19*sin(a),.71+k*.105,.057,.40,.075,'c6a06a',a)
    # Strawberries in a raised bed. Visible red fruit distinguishes the crop.
    box(1.18,1.03,.035,1.77,1.20,.22,'ad845b')
    box(1.18,1.03,.245,1.66,1.08,.03,'725b43')
    for j in range(3):
        for i in range(5):
            x=.54+i*.30;y=.69+j*.31
            for k in range(3):
                a=k*2*pi/3
                m.blob(x+.076*cos(a),y+.076*sin(a),.36,.122,.095,.10,'6b8d51',rng,6)
            m.blob(x+.10,y-.08,.363,.05,.048,.061,'be5544',rng,6)
    # Stepping stones keep a clear approach to the terrace.
    for i,(x,y) in enumerate(((4.75,.33),(4.61,.91),(4.47,1.49),(4.35,2.08),(4.23,2.68))):
        box(x,y,.032,.78,.45,.044,'dbd4bf',.05*(i-2))
    # Layered boundary planting with short foliage and upright flower spikes.
    for x,y in ([(.26,.24+i*.29) for i in range(18)]+[(.58+i*.37,5.18) for i in range(3)]+[(5.65,.31+i*.33) for i in range(8)]):
        for j in range(3):
            rx=x+rng.uniform(-.15,.15);ry=y+rng.uniform(-.15,.15)
            m.blob(rx,ry,.18+rng.random()*.09,.20,.17,.18,rng.choice(['72965c','8d9d61','547858']),rng,6)
        if rng.random()<.65:
            for j in range(4):
                xx=x+rng.uniform(-.14,.14);yy=y+rng.uniform(-.13,.13);h=rng.uniform(.38,.69)
                rod((xx,yy,.14),(xx+.02,yy,h),.012,'637b43',5)
                m.blob(xx+.02,yy,h,.045,.045,.10,rng.choice(['ae8fab','c59d9a','dbca86']),rng,6)
    # Rosettes of folded leaves break up the straight edge of the planting.
    for x,y in ((.56,2.03),(.48,3.31),(.79,4.59),(1.17,5.08),(5.62,.34),(5.50,1.46),(5.57,2.65)):
        for i in range(12):
            a=i*2.40; reach=rng.uniform(.18,.36); h=rng.uniform(.35,.59)
            dx,dy=cos(a),sin(a); width=.048
            m.mesh(rng.choice(['86924b','78914e','a4ad5d']),[(x,y,.05),
                (x+.49*reach*dx-width*dy,y+.49*reach*dy+width*dx,h*.72),
                (x+.45*reach*dx,y+.45*reach*dy,h*.83),
                (x+.49*reach*dx+width*dy,y+.49*reach*dy-width*dx,h*.72),
                (x+reach*dx,y+reach*dy,h)],[(0,1,2),(2,1,4),(0,2,3),(3,2,4)])
    if yard_only:
        return m
    old=(1.43,2.42); new=(2.91,2.63);p=old if step==0 else new
    # Native model marks for the planting socket, original site and drag direction.
    def ring(cx,cy,r,colour):
        for j in range(18):
            a=2*pi*j/18;b=a+.21
            rod((cx+r*cos(a),cy+r*sin(a),.061),(cx+r*cos(b),cy+r*sin(b),.061),.016,colour,5)
    if step==1:
        ring(*old,.38,'eee2bc')
        dx=new[0]-old[0];dy=new[1]-old[1]
        for j in range(4,9):
            t=j/11
            rod((old[0]+dx*t,old[1]+dy*t,.063),(old[0]+dx*(t+.055),old[1]+dy*(t+.055),.063),.025,'558b77',6)
        for side in (-1,1):
            rod((new[0]-.43,new[1]-.05+side*.13,.064),(new[0]-.26,new[1]-.04,.064),.024,'558b77',6)
    if step<2:ring(*p,.32,'587f67')
    tree(m,*p,step==2)
    return m
