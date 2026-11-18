"""Project 08. One L-shaped kitchen; only the door and island depth change."""
from math import pi
from random import Random
from geometry import Model

OAK='b98153'
CREAM='e4d9ba'
STONE='efe8d8'
SAGE='637f70'
DARK='344345'


def kitchen(step):
    m=Model(); box=m.box; rod=m.rod
    rng=Random(808)
    box(3.3,2.25,-.24,6.78,4.68,.22,'a77954')
    for j in range(15):
        y=.15+.30*j
        bounds=[0,1.65,3.78,5.50,6.6] if j%2==0 else [0,.84,2.78,4.70,6.6]
        for a,b in zip(bounds,bounds[1:]):
            box((a+b)/2,y,-.025,b-a-.012,.292,.025,rng.choice(['dcb98f','e5c7a0','e9cda9','dfc19a']))
    box(-.06,2.25,0,.12,4.62,2.36,'e7dec9')
    box(3.3,4.56,0,6.84,.12,2.36,'eee6d4')
    # Tile courses, window glass, frame and opening lights.
    for j in range(2):
        for i in range(16):
            box(.206+i*.414,4.485,.96+j*.205,.405,.025,.197,'e2dfca' if (i+j)%3 else 'd5d9c8')
    box(3.9,4.43,1.38,2.08,.13,.88,OAK)
    for x in [3.40,4.40]:
        box(x,4.35,1.44,.93,.045,.75,'bed7d3')
    box(3.9,4.32,1.78,1.96,.045,.047,'f6f0dc')
    box(3.9,4.35,1.33,2.20,.28,.08,STONE)
    # Rear run. Carcass, recessed plinth, panelled fronts, pulls.
    rear_front=3.72
    box(3.3,4.12,.035,6.5,.65,.12,DARK)
    box(3.3,4.09,.15,6.50,.72,.70,SAGE)
    for i in range(8):
        x=.50+i*.80
        if i==4: continue
        box(x,3.715,.16,.775,.045,.68,SAGE)
        box(x,3.682,.20,.68,.024,.58,'758e7c')
        box(x,3.651,.71,.18,.033,.026,'c6a169')
    box(3.3,4.105,.85,6.61,.79,.075,STONE)
    # Sink and bridge tap.
    box(4.42,4.04,.926,.78,.48,.018,'9aaba6')
    box(4.42,4.04,.945,.64,.35,.008,'586d6a')
    rod((4.66,4.31,.93),(4.66,4.31,1.23),.022,DARK)
    rod((4.66,4.31,1.23),(4.66,4.12,1.23),.022,DARK)
    rod((4.66,4.12,1.23),(4.66,4.12,1.17),.022,DARK)
    # Dishwasher hinge fixed to the same front in every scene.
    x=3.70
    if step==0:
        box(x,3.695,.15,.77,.052,.69,'9ba8a6')
        box(x,3.655,.73,.54,.03,.046,DARK)
    else:
        box(x,3.694,.17,.76,.05,.65,'394b4a')
        box(x,3.65,.19,.68,.04,.49,'647471')
        box(x,rear_front-.31,.14,.77,.62,.065,'a8b4ad')
        for i in range(9):
            xx=x-.28+i*.07
            rod((xx,3.17,.22),(xx,3.64,.22),.008,'5b6b67',6)
        for i in range(4):
            xx=x-.19+i*.113
            rod((xx,3.45,.32),(xx+.019,3.45,.32),.112,'fff5d7',16)
    # Side run and hob.
    box(.36,1.92,.06,.61,3.65,.79,'688072')
    for j in range(4):
        yy=.53+j*.87
        box(.68,yy,.17,.052,.84,.64,'819583')
        box(.718,yy,.72,.034,.23,.027,'c6a169')
    box(.36,1.92,.85,.76,3.68,.075,STONE)
    box(.37,2.60,.928,.62,.86,.02,'374342')
    for xx in (.22,.52):
        for yy in (2.40,2.79):
            rod((xx,yy,.95),(xx,yy,.961),.106,'71807c',16)
            rod((xx,yy,.962),(xx,yy,.967),.078,DARK,16)
    rod((.29,2.78,.965),(.29,2.78,1.04),.138,'69716b',20,.159)
    rod((.29,2.78,1.042),(.29,2.78,1.047),.135,'3e4844',20)
    rod((.35,2.66,1.02),(.43,2.39,1.035),.024,'a47f54',8)
    box(.20,2.6,1.69,.49,.96,.12,'a5b1a2')
    box(.11,2.6,1.81,.24,.55,.55,'cccfbd')
    # Floating oak shelf, jars, board and herb pot.
    box(1.52,4.34,1.58,2.02,.33,.065,OAK)
    for i in range(4):
        xx=.93+i*.34; ht=.16+i%2*.08
        rod((xx,4.27,1.645),(xx,4.27,1.645+ht),.102,('d2c09d','b88c69','9aaf95','e9dfc3')[i])
        rod((xx,4.27,1.645+ht),(xx,4.27,1.67+ht),.106,OAK)
    box(1.30,4.19,.927,.59,.32,.027,OAK,.12)
    rod((5.74,4.15,.93),(5.74,4.15,1.15),.105,'ac7255',12,.14)
    for _ in range(10):
        m.blob(5.74+rng.uniform(-.13,.13),4.15+rng.uniform(-.12,.12),1.24+rng.uniform(-.05,.1),.10,.09,.12,rng.choice(['607f50','85955b','516e4b']),rng,6)
    # The front edge is fixed at y=1.32. Clearances refer to the worktop edge.
    end=2.78 if step<2 else 2.23
    depth=end-1.32; mid=(end+1.32)/2
    box(3.52,mid,.025,2.40,depth-.19,.13,'60584b')
    box(3.52,mid,.155,2.48,depth-.17,.68,OAK)
    for j in range(23):
        box(2.34+j*.108,1.394,.16,.065,.031,.65,'d2a477')
    box(3.52,mid,.835,2.67,depth,.10,STONE)
    box(4.14,mid,.935,.54,.31,.027,'aa7653',-.15)
    for ix in (2.9,4.12):
        rod((ix,1.05,.64),(ix,1.05,.71),.205,'bd8a5b',16)
        for dx,dy in ((-.12,-.10),(.12,-.10),(0,.14)):
            rod((ix+dx*1.3,1.05+dy*1.3,.02),(ix+dx,1.05+dy,.65),.03,DARK,8)
    for j in range(3):
        m.blob(3.00+j*.135,mid+rng.uniform(-.035,.035),1.01,.085,.08,.08,'d3a044' if j%2 else 'ac6c39',rng)
    # A floor ruler spans the remaining gap at the open door.
    if step:
        tone='b95743' if step==1 else '478773'
        gap_end=rear_front-.62
        box(3.89,(end+gap_end)/2,.012,.032,gap_end-end,.013,tone)
        for y in (end,gap_end): box(3.89,y,.014,.19,.032,.013,tone)
    return m
