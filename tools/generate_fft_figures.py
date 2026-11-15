"""Generate original explanatory SVG diagrams; no third-party dependencies."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parents[1]/'docs/06-procesamiento/figures'
NAVY='#142d4e';BLUE='#176db0';TEAL='#057d80';GRAY='#52657a';LIGHT='#edf4fa';RED='#ae3547'

def start(title,subtitle,height=760):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{height}" viewBox="0 0 1400 {height}" role="img"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc>',
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#52657a"/></marker></defs>',
    '<rect width="100%" height="100%" fill="white"/>',
    f'<style>text{{font-family:Segoe UI,Arial,sans-serif;fill:{NAVY}}}.mono{{font-family:Consolas,monospace}}.small{{font-size:18px}}.label{{font-size:22px}}</style>',
    text(48,55,title,32,weight='700'),text(48,91,subtitle,20,color=GRAY)]

def text(x,y,s,size=22,color=NAVY,weight='400',anchor='start',mono=False):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" style="fill:{color}" font-weight="{weight}" text-anchor="{anchor}"'+(' class="mono"' if mono else '')+f'>{escape(s)}</text>'

def rect(x,y,w,h,fill=LIGHT,stroke='#c9d8e6',radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def arrow(x1,y1,x2,y2,color=GRAY):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>'

def line(x1,y1,x2,y2,color=GRAY,dash=False):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"'+(' stroke-dasharray="6 5"' if dash else '')+'/>'

def box(x,y,w,h,lines,fill=LIGHT):
    out=[rect(x,y,w,h,fill)]
    for i,s in enumerate(lines):out.append(text(x+w/2,y+32+29*i,s,21,anchor='middle',weight='600' if i==0 else '400'))
    return ''.join(out)

def footer(parts,label,y=718):parts.extend([line(48,y-28,1352,y-28,'#dce5ed'),text(48,y,label,18,color=GRAY)])
def save(name,parts):
    data='\n'.join(parts+['</svg>'])+'\n';ET.fromstring(data);(OUT/name).write_text(data,encoding='utf-8',newline='\n')

def formats():
    a=start('01 / Punto fijo: el entero y su escala','Propuesta didáctica · cada componente I o Q usa su propia palabra signed de 16 bits')
    a.extend([text(50,148,'Q1.15   |   W = 16, F = 15   |   valor = código / 32768',26,weight='600')])
    for j in range(16):
        x=50+j*80;is_sign=j==0
        a.extend([rect(x,180,74,65,'#fcebed' if is_sign else '#e7f2fb'),text(x+37,220,'0' if j!=1 else '1',28,anchor='middle',mono=True),text(x+37,273,f'b{15-j}',18,anchor='middle'),text(x+37,305,'−1' if is_sign else f'2^−{j}',18,anchor='middle')])
    a.extend([line(127,172,127,252,RED),text(50,352,'Ejemplo: 0100 0000 0000 0000 → entero 16384 → 0,5',26,mono=True)])
    a.extend([box(50,398,405,150,['Rango de una componente','−1 ≤ valor ≤ 0,9999694824','Paso: 1 / 32768']),box(485,398,405,150,['El signo cuenta en Qm.n','m incluye el bit de signo','Q1.15 suma 16 bits']),box(920,398,405,150,['Twiddle propuesto: Q2.16','W = 18, F = 16','+1 y −1 sí son exactos'])])
    a.append(text(50,607,'I y Q pueden caber por separado y aun así tener |I + jQ| > 1.',25,weight='600'))
    a.append(text(50,645,'Ejemplo: 0,9 + j0,9 tiene módulo ≈ 1,273. Hay que definir margen de entrada.',23))
    footer(a,'Esquema explicativo. No fija todavía el formato óptimo ni demuestra ausencia de overflow.');save('fft-formatos.svg',a)

def butterfly():
    a=start('02 / Mariposa radix-2 con aritmética fija','T = B·W; U = (A + T)/2; V = (A − T)/2 · misma regla aplicada a real e imaginario')
    a.extend([text(48,181,'A',30,weight='700'),text(48,387,'B',30,weight='700'),arrow(85,170,680,170),arrow(85,375,240,375)])
    a.append(box(240,335,185,88,['× W','producto complejo']))
    a.append(arrow(425,375,455,375));a.append(box(455,335,185,88,['Roundshift 16','F31 → F15']))
    a.extend([arrow(640,375,690,375),line(650,170,690,375,BLUE),line(650,375,690,170,TEAL)])
    for y,s in [(170,'+'),(375,'−')]:
        a.append(f'<circle cx="720" cy="{y}" r="30" fill="#edf4fa" stroke="#176db0" stroke-width="2"/>');a.append(text(720,y+9,s,32,anchor='middle'))
        a.extend([arrow(750,y,815,y),box(815,y-44,200,88,['Roundshift 1','escala /2']),arrow(1015,y,1050,y),box(1050,y-44,230,88,['Saturar a 16 bits','registrar overflow']),arrow(1280,y,1340,y)])
    a.extend([text(1345,179,'U',25,weight='700'),text(1345,384,'V',25,weight='700'),text(245,480,'W = cos(θ) − j·sin(θ)',23,mono=True),arrow(332,455,332,425),text(50,540,'A = 0,5 + j0,25; B = 0,25 − j0,125; W = −j',25,weight='600'),text(50,585,'T = −0,125 − j0,25     U = 0,1875     V = 0,3125 + j0,25',25,mono=True),text(50,632,'Cruces sin punto no conectan señales. El esquema no especifica ciclos ni pipeline.',21,color=GRAY)])
    footer(a,'Ejemplo teórico exacto. Redondeo propuesto: al más cercano, empates alejándose de cero.');save('fft-mariposa.svg',a)

def stages():
    a=start('03 / Ocho puntos: tres etapas de mariposas','DIT iterativa · entrada en orden de bits invertidos · salida en orden natural, escalada por 1/8',820)
    xs=[185,520,855,1190];ys=[180+i*61 for i in range(8)]
    perm=[0,4,2,6,1,5,3,7]
    for i,y in enumerate(ys):
        a.extend([text(65,y+7,f'x[{perm[i]}]',23,mono=True),line(145,y,xs[0],y),text(1250,y+7,f'X[{i}]/8',22,mono=True),line(xs[-1],y,1230,y)])
    for stage in range(3):
        left,right=xs[stage],xs[stage+1];L=2**(stage+1);half=L//2
        a.append(text((left+right)/2,140,f'Etapa {stage+1}: L={L}',24,weight='600',anchor='middle'))
        for base in range(0,8,L):
            for j in range(half):
                u,v=base+j,base+j+half
                a.extend([line(left,ys[u],right,ys[u],BLUE),line(left,ys[v],right,ys[v],BLUE),line(left,ys[u],right,ys[v],TEAL),line(left,ys[v],right,ys[u],TEAL)])
        a.append(text((left+right)/2,675,'W = exp(−i·2π·r/L)',19,anchor='middle',mono=True))
        a.append(text((left+right)/2,710,'4 mariposas · escala /2',20,anchor='middle'))
    for x in xs:
        for y in ys:a.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{NAVY}"/>')
    footer(a,'Cada par aplica la mariposa de la figura 2; el coeficiente gira la entrada inferior antes de combinar. Cruces sin punto: sin conexión.',785)
    save('fft-etapas.svg',a)

def scaling():
    a=start('04 / Anchos intermedios y escala acumulada','Contrato propuesto para N=512 · 9 etapas · mantener precisión antes de redondear y almacenar',820)
    cells=[(50,170,220,['Datos I/Q','W16 · F15']), (320,170,220,['Twiddle','W18 · F16']), (590,170,220,['Producto real','W34 · F31']), (860,170,220,['Producto complejo','W35 · F31'])]
    for x,y,w,ls in cells:a.append(box(x,y,w,90,ls))
    a.extend([arrow(270,215,310,215),text(288,202,'×',24,anchor='middle'),arrow(540,215,580,215),arrow(810,215,850,215),text(1110,202,'Conservar',22),text(1110,234,'bit de guarda',22)])
    lower=[(50,['Roundshift 16','W19 · F15']),(365,['A ± T','W20 · F15']),(680,['Roundshift 1','escala /2']),(995,['Saturar y registrar','W16 · F15'])]
    for x,ls in lower:a.append(box(x,330,270,90,ls))
    for x in [320,635,950]:a.append(arrow(x,375,x+35,375))
    a.append(f'<path d="M970,260 L970,295 L185,295 L185,325" stroke="{GRAY}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>')
    a.append(text(50,480,'Nueve divisiones por dos → escala total 1/512',28,weight='600'))
    a.append(text(50,523,'Comparar con fft(x_cuantizado)/512, no directamente con fft(x).',24))
    a.extend([box(50,566,600,140,['Margen de entrada','La división por dos no garantiza seguridad','para todas las entradas I/Q a escala completa.'],'#fff5e7'),box(680,566,650,140,['Aritmética ≠ arquitectura física','Estos anchos no determinan DSP, BRAM ni latencia.','Hacen falta simulación bit-exact y síntesis.'])])
    footer(a,'Diseño propuesto. W indica bits totales con signo; F indica bits fraccionarios. No es un esquema RTL sintetizado.',785);save('fft-escalado.svg',a)

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    formats();butterfly();stages();scaling()
    print('Generated and XML-validated four original SVG figures.')
