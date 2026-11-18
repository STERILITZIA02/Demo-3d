"""Render the title-free Canva inserts at 1920 x 1080 with world-space annotations."""
from datetime import datetime
from math import radians, cos, sin, dist
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo
import argparse
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from astral import Observer
from astral.sun import azimuth,elevation
from render import mi,T,diffuse
from pitch_models import kitchen,yard,A,B,PIT,FENCE,BIN_WIDTH,FRONT,FAR,PROJECTION,TAP,BED,hose

W,H=1920,1080
NAMES=['K1-measured','K2-wide-open','K3-narrow-open','G1-yard','G2-table','G3-fence']
PAPER='#f8f7f1';INK='#303735';ACC='#bc412d'
OUT=Path(__file__).resolve().parents[1]/'pitch-778'
SITE=Observer(-36.85,174.76)
TIME=datetime(2027,1,15,18,tzinfo=ZoneInfo('Pacific/Auckland'))
AZ,ALT=map(radians,(azimuth(SITE,TIME),elevation(SITE,TIME,with_refraction=False)))
SUN=np.array([sin(AZ)*cos(ALT),cos(AZ)*cos(ALT),sin(ALT)])


class Camera:
    def __init__(self,k):
        self.target=np.array((4.15,2.27,.50) if k else (3.46,2.79,.85))
        self.look=np.array((3.4,-8.,21.) if k else (.65,-8.,16.5))
        self.radius=6.52 if k else 7.13
        self.right=np.cross([0,0,1],self.look);self.right/=np.linalg.norm(self.right)
        self.up=np.cross(self.look,self.right);self.up/=np.linalg.norm(self.up)
    def screen(self,p):
        q=np.array(p)-self.target
        return np.array([W/2+q@self.right*W/(2*self.radius),H/2-q@self.up*W/(2*self.radius)])
    def transform(self):
        return T.look_at(origin=(self.target+self.look).tolist(),target=self.target.tolist(),up=[0,0,1]) @ T.scale([self.radius]*2+[1])


def draw_render(m,cam,k,spp,width):
    # A direction in Mitsuba points from the source towards the scene.
    sun=np.array([-.4,-.35,.85]) if k else SUN
    scene={'type':'scene','integrator':{'type':'path','max_depth':4},
           'sensor':{'type':'orthographic','to_world':cam.transform(),
                     'film':{'type':'hdrfilm','width':width,'height':round(width*H/W),'rfilter':{'type':'tent'}},
                     'sampler':{'type':'independent','sample_count':spp}},
           'ground':{'type':'rectangle','to_world':T.translate([0,0,-.267 if not k else -.225]) @ T.scale(150),'bsdf':diffuse('ede9df')},
           'sky':{'type':'constant','radiance':{'type':'rgb','value':[.48,.49,.50]}},
           'sun':{'type':'directional','direction':(-sun).tolist(),'irradiance':{'type':'rgb','value':[2.65,2.53,2.32]}}}
    with TemporaryDirectory() as tmp:
        for c,p in m.ply(Path(tmp)):
            scene['m'+c]={'type':'ply','filename':str(p),'face_normals':True,'bsdf':{'type':'twosided','bsdf':diffuse(c)}}
        out=mi.render(mi.load_dict(scene),seed=21)
        bitmap=mi.Bitmap(out).convert(mi.Bitmap.PixelFormat.RGB,mi.Struct.Type.UInt8,True)
        return Image.fromarray(np.array(bitmap)).filter(ImageFilter.MedianFilter(3)).resize((W,H),Image.Resampling.LANCZOS)


def annotate(img,cam,index):
    d=ImageDraw.Draw(img);proj=cam.screen
    def font(size):
        for p in ('/System/Library/Fonts/Helvetica.ttc','DejaVuSans.ttf'):
            try:return ImageFont.truetype(p,size)
            except OSError:pass
        return ImageFont.load_default(size=size)
    def chip(msg,x,y,c=INK):
        f=font(27);x=int(x);y=int(y);w=d.textlength(msg,font=f)
        d.rounded_rectangle((x-11,y-19,x+w+11,y+19),radius=6,fill=PAPER)
        d.text((x,y),msg,fill=c,font=f,anchor='lm')
    def note(p,msg,x,y,c=INK):
        px,py=proj(p); end=x-10 if x>px else x+d.textlength(msg,font=font(27))+10
        d.line([(px,py),(end,y)],fill=c,width=2)
        d.ellipse((px-4,py-4,px+4,py+4),fill=c)
        chip(msg,x,y,c)
    def measure(a,b,msg,x,y):
        a,b=proj(a),proj(b);v=b-a;normal=np.array([-v[1],v[0]])/np.linalg.norm(v)*9
        d.line([tuple(a),tuple(b)],fill=ACC,width=5)
        for p in (a,b):d.line([tuple(p-normal),tuple(p+normal)],fill=ACC,width=4)
        p=(a+b)/2
        end=x-8 if x>p[0] else x+d.textlength(msg,font=font(27))+9
        d.line([tuple(p),(end,y)],fill=ACC,width=2)
        chip(msg,x,y,ACC)
    if index==0:
        measure((0,4.4,1.21),(8.4,4.4,1.21),'8 400 mm · model wall',1270,91)
        note((1.23,3.28,.05),'Ella · plates',66,373)
        note((4.2,3.24,.05),'Ben · rack',1130,186)
        note((3.0,1.62,.91),'Island · selected',187,811,ACC)
    elif index in (1,2):
        depth=1.05 if index==1 else .75;near=FAR+depth
        g=round((FRONT-PROJECTION-near)*1000)
        measure((3.70,near,.90),(3.70,FRONT-PROJECTION,.90),f'{g} mm clear',1058,167)
        # Dashed witness lines drop from the raised dimension onto the physical edges.
        top=proj((3.70,FRONT-PROJECTION,.90));bottom=proj((3.70,FRONT-PROJECTION,.215))
        for j in range(0,10,2):
            d.line([tuple(top+(bottom-top)*j/10),tuple(top+(bottom-top)*(j+1)/10)],fill=ACC,width=2)
        note((4.51,2.49,.65) if index==1 else (4.46,2.67,.04),
             'Drawer bank retained' if index==1 else 'Drawer bank removed',1150,907,ACC)
        measure((2.45,FAR,.91),(2.45,near,.91),f'{round(depth*1000):,} mm island',250,851)
        if index==1:note((2.04,3.16,1.25),'Ella waits',170,570)
    else:
        # One plan orientation and one lighting condition throughout.
        north=proj((0,1,0))-proj((0,0,0));north=north/np.linalg.norm(north)
        start=np.array([1755.,147.]);end=start+north*70;perp=np.array([-north[1],north[0]])
        d.line([tuple(start),tuple(end)],fill=INK,width=4)
        d.polygon([tuple(end),tuple(end-16*north+6*perp),tuple(end-16*north-6*perp)],fill=INK)
        chip('N',end[0]+12,end[1]-1)
        if index==3:
            note((*A,.52),'A · table',175,212,ACC)
            note((*B,.52),'B · fence',1493,646,ACC)
            note((*TAP,.75),'Tap',474,111)
            note((*BED,.10),'Watering route',101,714)
            note((6.66,1.60,.10),'Bin route',1511,838)
            note((6.46,5.49,.95),'Gate',1472,291)
        else:
            p=A if index==4 else B
            note((*p,2.47),'Illustrative mature canopy',103,125)
            note((4.03,3.88,.88),'Dining table',1350,213)
            note((1.13,1.03,.32),'Strawberries',103,786)
            route=hose(p);length=sum(dist(a,b) for a,b in zip(route,route[1:]))
            chip(f'Hose via bed  {length:.1f} m',83,959)
            chip('15 Jan 2027   /   18:00 NZDT',1455,959)
            if index==5:
                measure((p[0]+PIT,p[1],.32),(FENCE,p[1],.32),'630 mm gap · 540 mm bin',1455,729)
            else:note((*A,.11),'Site A',185,502,ACC)
    return img


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--samples',type=int,default=40)
    parser.add_argument('--width',type=int,default=W)
    parser.add_argument('--only',nargs='+',choices=NAMES,default=NAMES)
    args=parser.parse_args();OUT.mkdir(exist_ok=True)
    for name in args.only:
        i=NAMES.index(name);k=i<3;cam=Camera(k)
        model=kitchen(i) if k else yard(i-3)
        img=draw_render(model,cam,k,args.samples,args.width)
        annotate(img,cam,i).save(OUT/(name+'.png'),optimize=True)
        print(name,flush=True)
