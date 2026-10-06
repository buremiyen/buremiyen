"""Build a typing ASCII portrait from the original mascot and local app logos."""
from html import escape
import hashlib
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
PORTRAIT_COLS = 120
PORTRAIT_ROWS = 84
PORTRAIT_SIZE = 308
PORTRAIT_DURATION = 6.24
STYLE = '''text{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}
.sans{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.enter{animation:enter .7s ease-out both}.d1{animation-delay:.15s}.d2{animation-delay:1.2s}.d3{animation-delay:2.1s}.d4{animation-delay:7s}
.window{animation:window .55s ease-out both}
.cursor{animation:blink 1.1s step-end 7}
.row-mask{animation:type-row .13s steps(80,end) both}
.row-cursor{animation:travel .13s steps(80,end) both,cursor-row .13s linear both}
.type-mask{animation:type-line .75s steps(46,end) both}
.toolkit{animation:enter .6s ease-out 7.2s both}
.logo{animation:enter .45s ease-out both}
@keyframes window{from{opacity:0;transform:translateY(10px) scaleY(.96)}to{opacity:1;transform:translateY(0) scaleY(1)}}
@keyframes type-row{from{width:0}98%,100%{width:308px}}
@keyframes type-line{from{width:0}98%,100%{width:580px}}
@keyframes travel{from{transform:translateX(0)}98%,100%{transform:translateX(308px)}}
@keyframes cursor-row{0%,99%,100%{opacity:0}1%,97%{opacity:1}}
@keyframes enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{50%{opacity:0}}
@media(prefers-reduced-motion:reduce){.enter,.cursor,.window,.row-mask,.type-mask,.toolkit,.logo{animation:none}.row-cursor{display:none}}'''


def ascii_mascot():
    # Sample the provided source into SVG text, without changing the PNG.
    # Ignore its purple backdrop; preserve the face, hair, and white outline.
    with Image.open(ASSETS / 'mascot.png') as image:
        source = image.convert('RGB')
        # Locate the source silhouette so empty purple margins no longer spend
        # most of the character budget. This only samples the original PNG.
        def background(rgb):
            r, g, b = rgb
            return b > r * 1.25 and r > 55 and g < r * .8

        silhouette = Image.new('L', source.size)
        silhouette.putdata([0 if background(pixel) else 255 for pixel in source.get_flattened_data()])
        bounds = silhouette.getbbox()
        if bounds is None:
            raise ValueError('No mascot silhouette found')
        left, top, right, bottom = bounds
        side = min(round(max(right-left, bottom-top)*1.07), *source.size)
        left = max(0, min(round((left+right-side)/2), source.width-side))
        top = max(0, min(round((top+bottom-side)/2), source.height-side))
        sampled = source.crop((left, top, left+side, top+side)).resize(
            (PORTRAIT_COLS, PORTRAIT_ROWS), Image.Resampling.LANCZOS)
        rows = []
        ramp = '.:-=+*#%@'
        for y in range(PORTRAIT_ROWS):
            row = ''
            for x in range(PORTRAIT_COLS):
                r, g, b = sampled.getpixel((x, y))
                brightness = .2126 * r + .7152 * g + .0722 * b
                row += ' ' if background((r, g, b)) else ramp[round(brightness / 255 * (len(ramp)-1))]
            rows.append(row)
    # One left-to-right character sweep per row, then keep the completed art.
    masks, lines, cursors = [], [], []
    row_height = PORTRAIT_SIZE / PORTRAIT_ROWS
    row_time = PORTRAIT_DURATION / PORTRAIT_ROWS
    for index, row in enumerate(rows):
        y = index * row_height
        delay = .65 + index * row_time
        masks.append(f'<clipPath id="row-{index}"><rect class="row-mask" x="0" y="{y:.3f}" width="308" height="{row_height:.4f}" style="animation-delay:{delay:.4f}s;animation-duration:{row_time:.6f}s;animation-timing-function:steps({PORTRAIT_COLS},end)"/></clipPath>')
        lines.append(f'<text clip-path="url(#row-{index})" x="0" y="{y+row_height*.88:.3f}" fill="#e4d8fa" font-size="{row_height*1.08:.3f}" textLength="308" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(row)}</text>')
        cursors.append(f'<rect class="row-cursor" x="0" y="{y:.3f}" width="{PORTRAIT_SIZE/PORTRAIT_COLS:.4f}" height="{row_height:.4f}" fill="#6ee7c7" style="animation-delay:{delay:.4f}s,{delay:.4f}s;animation-duration:{row_time:.6f}s,{row_time:.6f}s;animation-timing-function:steps({PORTRAIT_COLS},end),linear"/>')
    return '<defs>'+''.join(masks)+'</defs>'+''.join(lines+cursors)


def typed(text, x, y, delay, color='#d2cbdc', size=17, key='line'):
    return f'''<defs><clipPath id="{key}"><rect class="type-mask" x="{x}" y="{y-size-3}" width="580" height="{size+8}" style="animation-delay:{delay}s"/></clipPath></defs>
<text x="{x}" y="{y}" fill="{color}" font-size="{size}" clip-path="url(#{key})">{escape(text)}</text>'''


def icon(name, x, y, label, index):
    # Nested local SVGs keep the toolkit independent of an image service.
    source = (ASSETS / 'icons' / name).read_text(encoding='utf-8')
    source = re.sub(r'<svg\b[^>]*>', f'<svg x="{x}" y="{y}" width="52" height="52" viewBox="0 0 256 256">', source, count=1)
    # Prefix IDs so Adobe and other logos cannot collide in one SVG document.
    source = re.sub(r'id="([^"]+)"', lambda m:f'id="icon{index}-{m[1]}"', source)
    source = re.sub(r'url\(#([^)]+)\)', lambda m:f'url(#icon{index}-{m[1]})', source)
    return f'<g class="logo" style="animation-delay:{7.4+index*.12:.2f}s">{source}<text x="{x+26}" y="{y+73}" text-anchor="middle" fill="#c5bdcf" font-size="13">{escape(label)}</text></g>'


def svg(height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc><style>{STYLE}</style>{body}</svg>\n'''


def publish_art(stem, content):
    # A new design gets a new URL. Browsers can otherwise keep the old raw/main
    # image even after GitHub has rendered the latest README around it.
    digest = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
    filename = f'{stem}-{digest}.svg'
    (ASSETS / filename).write_text(content, encoding='utf-8')
    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8')
    pattern = rf'\./assets/{stem}(?:-[0-9a-f]{{12}})?\.svg'
    text, replacements = re.subn(pattern, f'./assets/{filename}', text)
    if replacements != 1:
        raise ValueError(f'Expected one {stem} image in README; found {replacements}')
    readme.write_text(text, encoding='utf-8')
    for old in ASSETS.glob(f'{stem}*.svg'):
        if old.name != filename and re.fullmatch(rf'{stem}(?:-[0-9a-f]{{12}})?\.svg', old.name):
            old.unlink()
    print(f'Published {filename}')


def main():
    portrait = ascii_mascot()
    body = f'''
<defs>
<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#14121e"/><stop offset="1" stop-color="#0b0d12"/></linearGradient>
</defs>
<g class="window">
<rect x="1" y="1" width="998" height="498" rx="20" fill="url(#bg)" stroke="#302b40"/>
<path d="M1 58H999" stroke="#302b40"/>
<circle cx="30" cy="30" r="5" fill="#fd8a8a"/><circle cx="49" cy="30" r="5" fill="#f4c66d"/><circle cx="68" cy="30" r="5" fill="#6ee7c7"/>
<text x="93" y="36" fill="#a7a0b8" font-size="14">bey@creative-studio: ~</text>
<text x="966" y="36" text-anchor="end" fill="#6ee7c7" font-size="13">● CREATE / PLAY</text>
<g class="enter d1">
<rect x="36" y="98" width="308" height="308" rx="12" fill="#111019" stroke="#302b40"/>
<g transform="translate(36 98)">{portrait}</g>
<text x="36" y="88" fill="#a78bfa" font-size="11">~ $ render mascot --ascii</text>
</g>
<g class="enter d2">
<text x="384" y="112" fill="#a78bfa" font-size="15">DESIGN × 3D × CREATIVE TECH</text>
<text class="sans" x="380" y="198" fill="#f5f2ff" font-weight="800" font-size="86" letter-spacing="-5">BEY<tspan class="cursor" fill="#a78bfa">_</tspan></text>
{typed('Burhan Emin Yenier',384,240,1.55,'#e8e3f3',28,'name')}
{typed('Graphic Designer · 3D Artist · Game Developer',384,278,2.1,'#aba4ba',19,'roles')}
</g>
<g class="enter d3">
{typed('~ $ whoami',384,323,2.9,'#6ee7c7',17,'prompt')}
{typed('Graphic Design student @ Selçuk University.',384,353,3.55,key='study')}
{typed('Designing visuals. Building worlds.',384,380,4.3,key='design')}
{typed('Turning ideas into playable experiences.',384,407,5.05,key='play')}
</g>
<g class="enter d4">
<path d="M36 438H964" stroke="#302b40"/>
<rect x="36" y="458" width="4" height="15" rx="2" fill="#a78bfa"/>
<text x="52" y="471" fill="#e4ddef" font-size="16">Design it. Build it. Make it fun.</text>
<text x="964" y="471" text-anchor="end" fill="#82798f" font-size="13">burhan / emin / yenier</text>
</g></g>'''
    publish_art('hero', svg(500, 'BEY — Burhan Emin Yenier', 'The original BEY mascot types itself in ASCII, left to right, row by row. Graphic Designer, 3D Artist and Game Developer. Graphic Design student at Selçuk University. Designing visuals, building worlds and turning ideas into playable experiences.', body))
    body = '''<g class="toolkit">
<rect x="1" y="1" width="998" height="248" rx="18" fill="#101117" stroke="#302b40"/>
<text x="32" y="38" fill="#6ee7c7" font-size="16">~ $ toolkit --creative</text>
<text x="966" y="38" text-anchor="end" fill="#82798f" font-size="13">IDEA → FORM → INTERACTION</text>
<path d="M32 57H968" stroke="#282534"/>
<text x="32" y="222" fill="#a78bfa" font-size="13">VISUAL DESIGN</text>
<text x="276" y="222" fill="#aba4ba" font-size="13">3D MODELING</text>
<text x="508" y="222" fill="#aba4ba" font-size="13">GAME DEVELOPMENT</text>
<text x="788" y="222" fill="#aba4ba" font-size="13">UI/UX · CREATIVE AI</text>
'''
    apps = [('Photoshop.svg','Photoshop'),('Illustrator.svg','Illustrator'),('AfterEffects.svg','After Effects'),('Figma-Dark.svg','Figma'),('Blender-Dark.svg','Blender'),('Unity-Dark.svg','Unity'),('CS.svg','C#'),('Git.svg','Git'),('Github-Dark.svg','GitHub')]
    for index, (filename, label) in enumerate(apps):
        body += icon(filename, 58+index*104, 98, label, index)
    body += '</g>'
    publish_art('toolkit', svg(250, 'BEY creative toolkit — application logos', 'Photoshop, Illustrator, After Effects, Figma, Blender, Unity, C#, Git and GitHub logos. Focus: visual design, 3D modeling, game development, UI/UX and Creative AI.', body))


if __name__ == '__main__':
    main()
