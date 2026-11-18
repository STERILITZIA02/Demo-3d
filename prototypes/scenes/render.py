"""Render matched orthographic studies. Run from any directory."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
import mitsuba as mi
import numpy as np
from PIL import Image, ImageFilter
from kitchen import kitchen
from garden import garden
from sheet import compose

mi.set_variant('scalar_rgb')
T=mi.ScalarTransform4f
VIEWS=Path(__file__).resolve().parents[1]/'views'


def diffuse(colour):
    rgb=np.array([int(colour[i:i+2],16)/255 for i in (0,2,4)])
    linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    return {'type':'diffuse','reflectance':{'type':'rgb','value':linear.tolist()}}


def render(theme, step, samples, width):
    scene_model = kitchen(step) if theme=='kitchen' else garden(step)
    target=np.array((3.23,2.24,1.02) if theme=='kitchen' else (3.48,2.70,.92))
    eye=target+np.array((12,-9,16.5) if theme=='kitchen' else (7.4,-13.9,11.9))
    # The frame, light and camera stay fixed for every state within a brief.
    scale=6.24 if theme=='kitchen' else 5.55
    height=round(width*820/1240)
    scene={'type':'scene','integrator':{'type':'path','max_depth':5},
           'sensor':{'type':'orthographic','to_world':T.look_at(origin=eye.tolist(),target=target.tolist(),up=[0,0,1]) @ T.scale([scale,scale,1]),
                     'film':{'type':'hdrfilm','width':width,'height':height,'rfilter':{'type':'tent'}},
                     'sampler':{'type':'independent','sample_count':samples}},
           'floor':{'type':'rectangle','to_world':T.translate([0,0,-.267]) @ T.scale(150),'bsdf':diffuse('eee7d9')},
           'sky':{'type':'constant','radiance':{'type':'rgb','value':[.54,.55,.57]}},
           'windowlight':{'type':'rectangle','to_world':T.look_at(origin=[-5,-9,14],target=[3.5,2.5,0],up=[0,0,1]) @ T.scale([2.2,2.2,1]),
                          'emitter':{'type':'area','radiance':{'type':'rgb','value':[42,40,36]}}}}
    with TemporaryDirectory() as tmp:
        for colour,mesh in scene_model.ply(Path(tmp)):
            material=diffuse(colour)
            if colour in ('86924b','78914e','a4ad5d'):
                material={'type':'twosided','bsdf':material}
            scene['m'+colour]={'type':'ply','filename':str(mesh),'face_normals':True,'bsdf':material}
        img=mi.render(mi.load_dict(scene),seed=13)
        bitmap=mi.Bitmap(img).convert(mi.Bitmap.PixelFormat.RGB,mi.Struct.Type.UInt8,True)
        return Image.fromarray(np.array(bitmap)).filter(ImageFilter.MedianFilter(3))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--theme',choices=['kitchen','garden','both'],default='both')
    parser.add_argument('--step',choices=[1,2,3],type=int,nargs='+',default=[1,2,3])
    parser.add_argument('--samples',type=int,default=48)
    parser.add_argument('--width',type=int,default=1488)
    args=parser.parse_args()
    VIEWS.mkdir(exist_ok=True)
    for theme in (['kitchen','garden'] if args.theme=='both' else [args.theme]):
        for number in args.step:
            out=VIEWS/f'{theme}-{number:02}.png'
            compose(theme,number-1,render(theme,number-1,args.samples,args.width)).save(out,optimize=True)
            print(out,flush=True)
