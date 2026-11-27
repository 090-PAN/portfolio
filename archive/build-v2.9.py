import base64, pathlib, re, sys

B = pathlib.Path(__file__).resolve().parent          # build/ 目录
OUT = B.parent / 'portfolio' / 'index.html'          # 产物：../portfolio/index.html

html = (B / 'template.html').read_text(encoding='utf-8')

def datauri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()

THREE_CANDIDATES = [B / 'three.min.js', B.parent / 'three.min.js']
three_path = next((p for p in THREE_CANDIDATES if p.exists()), None)
if three_path is None:
    print('three.min.js not found, put it next to build.py or in the parent folder'); sys.exit(1)
three = three_path.read_text(encoding='utf-8')
assert '</script' not in three.lower()

repl = {
    '__THREE__': three,
    '__PORTRAIT__': datauri(B / 'img/portrait.jpg', 'image/jpeg'),
    '__AVATAR__': datauri(B / 'img/avatar.jpg', 'image/jpeg'),
    '__IMG_CERT__': datauri(B / 'img/cert.webp', 'image/webp'),
    '__IMG_HONORS__': datauri(B / 'img/honors.webp', 'image/webp'),
    '__IMG_COURSE1__': datauri(B / 'img/course1.webp', 'image/webp'),
    '__IMG_COURSE2__': datauri(B / 'img/course2.webp', 'image/webp'),
    '__IMG_ROBOT__': datauri(B / 'img/robot.webp', 'image/webp'),
    '__IMG_TREND__': datauri(B / 'img/trend.webp', 'image/webp'),
    '__IMG_HIKE1__': datauri(B / 'img/hike1.webp', 'image/webp'),
    '__IMG_HIKE2__': datauri(B / 'img/hike2.webp', 'image/webp'),
    '__IMG_PAGODA__': datauri(B / 'img/pagoda.webp', 'image/webp'),
    '__IMG_SHOOTER__': datauri(B / 'img/shooter.webp', 'image/webp'),
    '__IMG_ORCHARD__': datauri(B / 'img/orchard.webp', 'image/webp'),
    '__IMG_CERT_RUANKAO__': datauri(B / 'img/cert_ruankao.webp', 'image/webp'),
    '__IMG_CERT_PATENT1__': datauri(B / 'img/cert_patent1.webp', 'image/webp'),
    '__IMG_CERT_PATENT2__': datauri(B / 'img/cert_patent2.webp', 'image/webp'),
    '__IMG_CERT_CAMP__': datauri(B / 'img/cert_camp.webp', 'image/webp'),
    '__IMG_CERT_AWARD__': datauri(B / 'img/cert_award.webp', 'image/webp'),
    '__IMG_CERT_NCRE__': datauri(B / 'img/cert_ncre.webp', 'image/webp'),
    '__IMG_CERT_CET6__': datauri(B / 'img/cert_cet6.webp', 'image/webp'),
}
for k, v in repl.items():
    if k not in html:
        print('skip (placeholder not used):', k)
        continue
    html = html.replace(k, v)

left = re.findall(r'__[A-Z_]+__', html)
if left:
    print('leftover placeholders:', set(left))

OUT.write_text(html, encoding='utf-8')
print('built', OUT, round(OUT.stat().st_size / 1024), 'KB')
