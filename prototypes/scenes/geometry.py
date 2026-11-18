"""Small flat-shaded meshes in metres, with Z up."""
from collections import defaultdict
from math import cos, sin, pi
import struct
import numpy as np


class Model:
    def __init__(self):
        self.parts = defaultdict(lambda: ([], []))

    def mesh(self, colour, vertices, faces):
        vs, fs = self.parts[colour]
        base = len(vs)
        vs.extend(vertices)
        for face in faces:
            for i in range(1, len(face)-1):
                fs.append((base+face[0], base+face[i], base+face[i+1]))

    def box(self, x, y, z, w, d, h, colour, turn=0):
        # Centre in plan; z is the bottom.
        pts = [(x+a*cos(turn)-b*sin(turn), y+a*sin(turn)+b*cos(turn), z+c)
               for c in (0,h) for a,b in ((-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2))]
        self.mesh(colour, pts, [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])

    def rod(self, a, b, rad, colour, n=12, tip=None):
        a,b = np.array(a),np.array(b)
        axis=b-a
        axis=axis/np.linalg.norm(axis)
        u=np.cross(axis, (1,0,0) if abs(axis[0])<.85 else (0,1,0))
        u=u/np.linalg.norm(u)
        v=np.cross(axis,u)
        rim=[u*cos(2*pi*i/n)+v*sin(2*pi*i/n) for i in range(n)]
        vs=[a+rad*t for t in rim]+[b+(rad if tip is None else tip)*t for t in rim]
        faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
        faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
        self.mesh(colour,vs,faces)

    def blob(self,x,y,z,rx,ry,rz,colour,rng,n=8):
        vs=[(x,y,z-rz)]
        for ring,(height,radius) in enumerate(((-.52,.84),(.13,1),(.67,.73))):
            for i in range(n):
                a=2*pi*(i+.36*ring)/n
                r=radius*rng.uniform(.89,1.08)
                vs.append((x+rx*cos(a)*r,y+ry*sin(a)*r,z+rz*(height+rng.uniform(-.09,.09))))
        vs.append((x+.08*rx,y,z+rz))
        faces=[]
        for i in range(n):
            j=(i+1)%n
            faces.extend([(0,1+j,1+i),(1+2*n+i,1+2*n+j,len(vs)-1)])
            for k in range(2):
                t=1+k*n
                faces.extend([(t+i,t+j,t+n+i),(t+j,t+n+j,t+n+i)])
        self.mesh(colour,vs,faces)

    def ply(self, folder):
        for i,(colour,(vs,fs)) in enumerate(self.parts.items()):
            path=folder/f'mesh-{i}.ply'
            header=f'ply\nformat binary_little_endian 1.0\nelement vertex {len(vs)}\nproperty float x\nproperty float y\nproperty float z\nelement face {len(fs)}\nproperty list uchar int vertex_indices\nend_header\n'
            with path.open('wb') as out:
                out.write(header.encode());out.write(np.asarray(vs,dtype='<f4').tobytes())
                for f in fs: out.write(struct.pack('<Biii',3,*f))
            yield colour,path
