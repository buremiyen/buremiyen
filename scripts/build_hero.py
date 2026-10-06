"""Self-contained SVG profile art. The supplied mascot is embedded unchanged."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
STYLE = '''text{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}
.sans{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.enter{animation:enter .7s ease-out both}.d1{animation-delay:.15s}.d2{animation-delay:.3s}.d3{animation-delay:.45s}.d4{animation-delay:.6s}
.cursor{animation:blink 1.3s step-end 4}
@keyframes enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{50%{opacity:0}}
@media(prefers-reduced-motion:reduce){.enter,.cursor{animation:none}}'''


def svg(height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc><style>{STYLE}</style>{body}</svg>\n'''


def main():
    portrait = base64.b64encode((ASSETS / 'mascot.png').read_bytes()).decode('ascii')
    body = f'''
<defs>
<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#14121e"/><stop offset="1" stop-color="#0b0d12"/></linearGradient>
<clipPath id="portrait"><rect x="36" y="98" width="308" height="308" rx="22"/></clipPath>
</defs>
<rect x="1" y="1" width="998" height="498" rx="20" fill="url(#bg)" stroke="#302b40"/>
<path d="M1 58H999" stroke="#302b40"/>
<circle cx="30" cy="30" r="5" fill="#fd8a8a"/><circle cx="49" cy="30" r="5" fill="#f4c66d"/><circle cx="68" cy="30" r="5" fill="#6ee7c7"/>
<text x="93" y="36" fill="#a7a0b8" font-size="14">bey@creative-studio: ~</text>
<text x="966" y="36" text-anchor="end" fill="#6ee7c7" font-size="13">● CREATE / PLAY</text>
<g class="enter d1">
<image x="36" y="98" width="308" height="308" clip-path="url(#portrait)" xlink:href="data:image/png;base64,{portrait}"/>
<rect x="36" y="98" width="308" height="308" rx="22" fill="none" stroke="#9d6af1"/>
<rect x="55" y="380" width="124" height="28" rx="7" fill="#17131f" stroke="#a78bfa"/>
<text x="117" y="399" text-anchor="middle" fill="#ddd2fc" font-size="13">BEY / avatar</text>
</g>
<g class="enter d2">
<text x="384" y="112" fill="#a78bfa" font-size="15">DESIGN × 3D × CREATIVE TECH</text>
<text class="sans" x="380" y="198" fill="#f5f2ff" font-weight="800" font-size="86" letter-spacing="-5">BEY<tspan class="cursor" fill="#a78bfa">_</tspan></text>
<text class="sans" x="384" y="240" fill="#e8e3f3" font-weight="600" font-size="29">Burhan Emin Yenier</text>
<text class="sans" x="384" y="278" fill="#aba4ba" font-size="20">Graphic Designer · 3D Artist · Game Developer</text>
</g>
<g class="enter d3">
<text x="384" y="323" fill="#6ee7c7" font-size="17">~ $ whoami</text>
<text x="384" y="353" fill="#d2cbdc" font-size="17">Graphic Design student @ Selçuk University.</text>
<text x="384" y="380" fill="#d2cbdc" font-size="17">Designing visuals. Building worlds.</text>
<text x="384" y="407" fill="#d2cbdc" font-size="17">Turning ideas into playable experiences.</text>
</g>
<g class="enter d4">
<path d="M36 438H964" stroke="#302b40"/>
<rect x="36" y="458" width="4" height="15" rx="2" fill="#a78bfa"/>
<text x="52" y="471" fill="#e4ddef" font-size="16">Design it. Build it. Make it fun.</text>
<text x="964" y="471" text-anchor="end" fill="#82798f" font-size="13">burhan / emin / yenier</text>
</g>'''
    (ASSETS / 'hero.svg').write_text(svg(500, 'BEY — Burhan Emin Yenier', 'User-supplied BEY mascot. Graphic Designer, 3D Artist and Game Developer. Graphic Design student at Selçuk University. Designing visuals, building worlds and turning ideas into playable experiences.', body), encoding='utf-8')
    body = '''
<rect x="1" y="1" width="998" height="208" rx="18" fill="#101117" stroke="#302b40"/>
<text x="32" y="38" fill="#6ee7c7" font-size="16">~ $ toolkit --creative</text>
<text x="966" y="38" text-anchor="end" fill="#82798f" font-size="13">IDEA → FORM → INTERACTION</text>
<path d="M32 57H968" stroke="#282534"/><path d="M350 79V178M681 79V178" stroke="#282534"/>
<g class="enter d1">
<text x="32" y="90" fill="#a78bfa" font-size="13">01 / VISUAL DESIGN</text>
<text class="sans" x="32" y="122" fill="#ece7f4" font-size="24" font-weight="600">Shape the idea.</text>
<text x="32" y="151" fill="#ada5ba" font-size="15">Photoshop · Illustrator</text>
<text x="32" y="176" fill="#ada5ba" font-size="15">After Effects · Figma</text>
</g><g class="enter d2">
<text x="378" y="90" fill="#a78bfa" font-size="13">02 / 3D &amp; GAMES</text>
<text class="sans" x="378" y="122" fill="#ece7f4" font-size="24" font-weight="600">Build the world.</text>
<text x="378" y="151" fill="#ada5ba" font-size="15">Blender · Unity · C#</text>
<text x="378" y="176" fill="#ada5ba" font-size="15">3D modeling · Game development</text>
</g><g class="enter d3">
<text x="709" y="90" fill="#a78bfa" font-size="13">03 / CREATIVE TECH</text>
<text class="sans" x="709" y="122" fill="#ece7f4" font-size="24" font-weight="600">Make it work.</text>
<text x="709" y="151" fill="#ada5ba" font-size="15">Git · GitHub · UI/UX</text>
<text x="709" y="176" fill="#ada5ba" font-size="15">AR · Creative AI</text>
</g>'''
    (ASSETS / 'toolkit.svg').write_text(svg(210, 'BEY creative toolkit', 'Visual design: Photoshop, Illustrator, After Effects, Figma. 3D and games: Blender, Unity, C#. Creative technology: Git, GitHub, UI/UX, AR, Creative AI.', body), encoding='utf-8')


if __name__ == '__main__':
    main()
