"""
@jorjun 
"""
import math
import string



def polarToCartesian(x, y, radius, rad):
    return {
        "x": x + (radius * math.cos(rad)),
        "y": y + (radius * math.sin(rad))
    }


class _SVG(object):
    id = 1

    def __init__(self, parent, tag=None, **attrs):
        if not tag:
            raise Exception(f"Bad parent: {parent}")
        self.parent = parent
        self.tag = tag
        self.style = {}
        self.attrs = {}
        for k, v in attrs.items():
            self.addAttr(k, v)
        self.content = ''
        self.id = f"el-{_SVG.id}"
        _SVG.id += 1

    def describeArc(self, x, y, radius, startRad, endRad):
        args = (x, y, radius)
        (start, end) = polarToCartesian(*args, startRad), polarToCartesian(*args, endRad)
        largeArcFlag = "0" if (abs(endRad - startRad) <= math.pi) else "1"
    
        return f'M {start["x"]:.1f},{start["y"]:.1f} A{radius},{radius} 0 {largeArcFlag} 1 {end["x"]:.1f},{end["y"]:.1f}'

    def addAttr(self, name, value):
        name = name.replace("_", "-")
        if name in ("x", "y"):
            value = f"{value:.2f}"
        self.attrs[name] = value
        return self

    def setContent(self, content):
        self.content = content
        return self

    def addContent(self, content):
        self.content += content
        return self

    @property
    def p_attrs(self):
        return " ".join(f'{name}="{self.attrs[name]}"' for name in self.attrs)

    @property
    def svg(self):
        if "stroke" not in self.attrs:
            self.addAttr("stroke", "black")
        return f'<{self.tag} id="{self.id}" {self.p_attrs}> {self.content} </{self.tag }>\n'

    def getId(self):
        return self.id


class TextArc(_SVG):
    def __init__(self, parent, x, y, radius, rad, txt, **attrs):
        _SVG.__init__(self, parent, "text", **attrs)
        textPath = _SVG(parent, "textPath")
        arc = Arc(parent, x, y, radius, rad[0], rad[1])
        textPath.addAttr("href", f"#{arc.id}")
        for _ in ("textLength", "text_anchor", "startOffset"):
            if _ in attrs:            
                textPath.addAttr(_, attrs[_])
            
        textPath.setContent(txt)
        parent.add_def(arc)
        for _ in ("font_size", "font_family"):
            if _ in attrs:
                self.addAttr(_, attrs[_])

        self.setContent(textPath.svg)


class Text(_SVG):
    def __init__(self, parent, x=None, y=None, txt="Hello", **attrs):
        _SVG.__init__(self, parent, "text", **attrs)
        if x is not None and y is not None:
            self.addAttr("x", x).addAttr("y", y).setContent(txt)


class Circle(_SVG):
    def __init__(self, parent, **attrs):
        _SVG.__init__(self, parent, 'circle', **attrs)


class Group(_SVG):
    def __init__(self, **attrs):
        _SVG.__init__(self,"g")


class Symbol(_SVG):
    def __init__(self, parent, x, y, scale, size, deg=0, **attrs):
        _SVG.__init__(self, parent, "path", **attrs)
        #x -= size / 2
        #y -= size / 2
        self.addAttr("transform", f"translate({x},{y}) scale({scale}) rotate ({deg+10},0,0)")


class Fan(_SVG):
    def __init__(self, parent, x=0, y=0, rad=0, length=50, num=3, extend=0, **attrs):
        _SVG.__init__(self, parent, 'g', **attrs)

        for _ix in range(num):
            dx = math.cos(rad) * extend
            dy = math.sin(rad) * extend
            self.addContent(Spoke(parent=parent, x1=x + dx, y1=y + dy, rad=rad, length=length + extend, **attrs).svg)
            rad += 2 * math.pi / num


class Spoke(_SVG):
    def __init__(self, parent, length=100, rad=0, **attrs):
        _SVG.__init__(self, parent, "line", **attrs)
        x2 = math.cos(rad) * length
        y2 = math.sin(rad) * length
        self.addAttr("x2", x2).addAttr("y2", y2)

class Arc(_SVG):
    def __init__(self, parent, x, y, radius, startRad, endRad, **attrs):
        _SVG.__init__(self, parent, "path", **attrs)
        self.addAttr("d", self.describeArc(x, y, radius, startRad, endRad))


class Rect(_SVG):
    def __init__(self, parent, x=None, y=None, width=100, height=100, **attrs):
        _SVG.__init__(self, parent, "rect", **attrs)
        if x is None:
            x = -width / 2
        if y is None:
            y = -height / 2
        self.addAttr("x", x).addAttr("y", y).addAttr("width", width).addAttr("height", height)
        

class Polygon(_SVG):
    def __init__(self, parent, points, *attrs):
        _SVG.__init__(self, parent, "path")
        cvt_points = " ".join([f'{x:.2f},{y:.2f}' for x, y in points])
        self.addAttr("d", f'M {cvt_points} Z')


class SVGDoc:
    def __init__(self, width, height, rotate_deg=0):
        self.object_list, self.def_list, self.rotate_deg = [], [], rotate_deg
        self.width, self.height = width, height

    def add(self, obj): self.object_list.append(obj)
    def add_def(self, obj): self.def_list.append(obj)

    def render(self):
        obj_list = "".join([_.svg for _ in self.object_list])
        def_list = "".join([_.svg for _ in self.def_list])
        CSS = """
            <style type="text/css">
        <![CDATA[
        @font-face \{
         font-family: 'Roboto';
         font-style: normal;
         font-weight: 400;
         src: local('Roboto'), local('Roboto-Regular'),
         url(https://fonts.gstatic.com/s/roboto/v20/KFOmCnqEu92Fr1Mu4mxKKTU1Kg.woff2) format('woff2');
       \}
       ]]>
    </style>
        """
        return f"""\
<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg"
    version="1.1" preserveAspectRatio="xMinYMin slice" viewbox="0 0 {self.width} {self.height}"
    width="{self.width}" height="{self.height}" >

    <defs>
    { CSS }
    
    <clipPath id="clip1">
        <rect x="-200" y="-210" width="436" height="214" >  </rect>
    </clipPath>
    
    <g id="suit-c">
      <path d="M21.106,70.1 L35.551,70.1" fill-opacity="0" stroke="#000000" stroke-width="3"/>
      <g>
        <path d="M14.183,9.5 C14.183,24.166 20.35,36.056 27.956,36.056 M41.73,9.5 C41.73,24.166 35.563,36.056 27.956,36.056 M13.5,9.5 L42.315,9.5" fill-opacity="0" stroke="#000000" stroke-width="3"/>
        <path d="M35.551,69.903 C31.668,69.903 28.52,55.092 28.52,36.822 M21.489,69.903 C25.372,69.903 28.52,55.092 28.52,36.822" fill-opacity="0" stroke="#000000" stroke-width="3"/>
      </g>
    </g>

    <path  id="suit-d" d="M30.5,51.5 C18.902,51.5 9.5,42.098 9.5,30.5 C9.5,18.902 18.902,9.5 30.5,9.5 C42.098,9.5 51.5,18.902 51.5,30.5 C51.5,42.098 42.098,51.5 30.5,51.5 z M30.5,51.5 L30.5,9.5 M52.686,30.5 L9.5,30.5" fill-opacity="0" stroke="#000000" stroke-width="3"/>

    <path id="suit-s"  d="M23.534,32.976 L28.683,70.975 L33.832,32.976 z M38.237,31.693 L28.593,17.112 L18.949,31.693 z M36.309,10.375 L28.914,27.312 L21.52,10.375 z" fill-opacity="0" stroke="#000000" stroke-width="3"/>

    <g id="suit-w">
      <path d="M29.296,17.7 L28.867,61.9" fill-opacity="0" stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-miterlimit="5"/>
      <path d="M29.296,17.7 L32.872,20.134 L29.365,10.5 L25.672,20.065 z" fill="#000000" fill-opacity="1" stroke="#000000" stroke-width="2" stroke-opacity="1"/>
      <path d="M28.867,61.9 L25.291,59.466 L28.798,69.1 L32.491,59.535 z" fill="#000000" fill-opacity="1" stroke="#000000" stroke-width="2" stroke-opacity="1"/>
    </g>
       {def_list}
    </defs>
        

    <g transform="translate({self.width/2}, {self.height/2+440}) scale(3.2)" clip-path='url(#clip1)'>

        <g transform="rotate({self.rotate_deg})">
           {obj_list}
        </g>
    </g>

    <g transform="translate({self.width/2 -4}, 3) scale(2)" id="indicator">
      <path d="M8,-0 L6,8 L4,16 L2,8 L-0,0 L4,0 z" fill="#333333"/>
      <path d="M8,-0 L6,8 L4,16 L2,8 L-0,0 L4,0 z" fill-opacity="0" stroke="#333333" stroke-width="1"/>
    </g>

    
</svg>"""

    def write(self, fil):
        with open(fil, "w") as _fil:
            _fil.writelines(self.render())
            
