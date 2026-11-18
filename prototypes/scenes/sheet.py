"""Compose a presentation plate with a matching plan and a single operation."""
from math import cos,sin,pi
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PAPER='#faf8f2'
INK='#27352f'
MUTED='#59675f'
RULE='#cdd0bd'

TEXT={
 'kitchen':[
 ('Lay out the kitchen','Layout','Island depth','1.46 m','Sink, hob and dishwasher stay in place.','Check where the island sits between them.'),
 ('Open the dishwasher','Open door','Gap at open door','0.32 m','The open door reaches into the aisle.','Only 32 cm remains at the island edge.'),
 ('Try a slimmer island','Resize island','Gap at open door','0.87 m','Pull the rear edge of the island in by 55 cm.','Keep the door open to compare the gap.')],
 'garden':[
 ('Lay out the garden','Layout','Planting site','A','Place the sapling beside the strawberry bed.','The paved strip leads to the side gate.'),
 ('Move the tree','Move tree','Planting site','B','Move the sapling towards the dining deck.','The dashed ring marks its original site.'),
 ('Preview the canopy','Grow canopy','Crown span','~2.8 m','Keep site B and preview a mature crown.','Compare shade on the deck with the gate route.')]}
def font(size,serif=False):
    options=(['/System/Library/Fonts/Supplemental/Georgia.ttf','DejaVuSerif.ttf'] if serif else
             ['/System/Library/Fonts/Helvetica.ttc','DejaVuSans.ttf'])
    for p in options:
        try:return ImageFont.truetype(p,size)
        except OSError:pass
    return ImageFont.load_default(size=size)


def plan(draw,theme,step):
    scale=40; left=1302; base=549
    def pt(x,y):return (round(left+x*scale),round(base-y*scale))
    def rect(x,y,w,h,colour,edge=None):
        draw.rectangle([pt(x,y+h),pt(x+w,y)],fill=colour,outline=edge,width=2)
    def circ(x,y,r,fill,outline=None):
        draw.ellipse([pt(x-r,y+r),pt(x+r,y-r)],fill=fill,outline=outline,width=2)
    def line(a,b,c,w=2):draw.line([pt(*a),pt(*b)],fill=c,width=w)
    if theme=='kitchen':
        rect(0,0,6.60,4.5,'#ead9ba',INK)
        rect(.03,.08,.67,3.65,'#a7b2a0')
        rect(.03,3.72,6.54,.76,'#a7b2a0')
        rect(.08,2.17,.55,.86,'#596661')
        rect(4.0,3.87,.76,.45,'#637b75')
        end=2.78 if step<2 else 2.23
        rect(2.185,1.32,2.67,end-1.32,'#c39b68',INK)
        for x in [2.90,4.12]:circ(x,1.03,.19,'#a5825d')
        if step:
            rect(3.315,3.10,.77,.62,'#a3aaa3',INK)
            c='#b6604b' if step==1 else '#448573'
            rect(3.315,end,.77,3.1-end,c)
            line((4.18,end),(4.18,3.1),c)
        else:rect(3.315,3.72,.77,.045,INK)
    else:
        rect(0,0,7,5.6,'#cad5ae',INK)
        rect(5.98,.04,.92,5.51,'#e6dbc7')
        rect(2.40,3.05,3.30,1.80,'#d6b587')
        rect(1.65,4.89,3.78,.66,'#79877b')
        rect(.29,.43,1.77,1.20,'#79915f')
        for i in range(5):rect(4.36+(4-i)*.10-.33,.14+i*.59,.65,.4,'#e6dbc7')
        circ(4.03,3.88,.48,'#f2e1bd',INK)
        x,y=(1.43,2.42) if step==0 else (2.91,2.63)
        if step==1:
            for i in range(10):
                a=i*2*pi/10
                line((1.43+.65*cos(a),2.42+.65*sin(a)),(1.43+.65*cos(a+.31),2.42+.65*sin(a+.31)),MUTED)
            line((1.43,2.42),(x,y),'#477d69')
        circ(x,y,.67 if step<2 else 1.36,'#95ae73','#567d56')
        circ(x,y,.085,INK)
        line((5.96,5.51),(6.94,5.51),INK,4)


def compose(theme,step,render):
    page=Image.new('RGB',(1700,1050),PAPER);d=ImageDraw.Draw(page)
    title,action,key,value,first,second=TEXT[theme][step]
    ident='08   /   KITCHEN' if theme=='kitchen' else '09   /   GARDEN'
    d.text((49,28),'luxluane    /    Spatial studies',font=font(22),fill=MUTED)
    d.text((1650,28),ident,font=font(22),fill=MUTED,anchor='ra')
    d.line((49,71,1650,71),fill=RULE,width=2)
    d.text((48,86),title,font=font(64,True),fill=INK)
    render=render.resize((1230,813),Image.Resampling.LANCZOS)
    page.paste(render,(42,184))
    d.line((1272,184,1272,997),fill=RULE,width=2)
    d.text((1302,202),'PLAN VIEW',font=font(18),fill=MUTED)
    plan(d,theme,step)
    d.line((1302,591,1649,591),fill=RULE,width=2)
    d.text((1302,616),key,font=font(25),fill=MUTED)
    d.text((1300,654),value,font=font(59,True),fill=INK)
    for i,para in enumerate((first,second)):
        words=para.split();line='';f=font(22);y=763+i*81
        for word in words:
            trial=(line+' '+word).strip()
            if d.textlength(trial,font=f)>347 and line:
                d.text((1302,y),line,font=f,fill=INK);line=word;y+=30
            else:line=trial
        d.text((1302,y),line,font=f,fill=INK)
    d.text((1302,959),f'0{step+1} / 03     {action}',font=font(21),fill=MUTED)
    return page
