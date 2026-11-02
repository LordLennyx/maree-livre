"""Chaîne d'édition : couverture (SVG vectorisé + PDF imprimeur), intérieur PDF, EPUB 3.
python src/build.py <dossier-polices>"""
import os, sys, json, math, random, subprocess, zipfile, html, io
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POL = sys.argv[1]
OUT = os.path.join(ICI, "fichiers"); os.makedirs(OUT, exist_ok=True)
L = json.loads(subprocess.run(["node", "-e", "console.log(JSON.stringify(require('./texte.js')))"], cwd=ICI, capture_output=True, text=True, encoding="utf-8").stdout)

# ——— Format (pouces) : 5,5 × 8,5, 132 pages, papier crème KDP ———
U = 100                       # unités SVG par pouce
TW, TH, BLEED, PAGES = 5.5, 8.5, 0.125, 132
SPINE = round(PAGES * 0.0025, 4)   # épaisseur papier crème : 0,0025 po / page
COL = {"nuit": "#0f3b47", "abysse": "#0a2a33", "corail": "#e8765c", "sable": "#f2e3c9", "ecume": "#cfe0dc", "verre": "#3f7a5a"}

DISPLAY = TTFont(os.path.join(POL, "Caslon.ttf"))
SANS = instantiateVariableFont(TTFont(os.path.join(POL, "Karla.ttf")), {"wght": 600})
SANS_R = instantiateVariableFont(TTFont(os.path.join(POL, "Karla.ttf")), {"wght": 400})
SERIF = instantiateVariableFont(TTFont(os.path.join(POL, "CaslonText.ttf")), {"wght": 400})


def mesure(font, s, size, track=0.0):
    cmap, hm, k = font.getBestCmap(), font["hmtx"], size / font["head"].unitsPerEm
    return sum(hm[cmap.get(ord(c), cmap[32])][0] * k + track * size for c in s) - (track * size if s else 0)


def texte(font, s, size, x, y, track=0.0, anchor="start", fill="#000", extra=""):
    gs, cmap, k = font.getGlyphSet(), font.getBestCmap(), size / font["head"].unitsPerEm
    hm = font["hmtx"]; w = mesure(font, s, size, track)
    cx = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    d = []
    for c in s:
        g = cmap.get(ord(c), cmap[32]); pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y))); d.append(pen.getCommands())
        cx += hm[g][0] * k + track * size
    return f'<path d="{" ".join(d)}" fill="{fill}" {extra}/>'


def paragraphe(font, s, size, x, y, largeur, interligne, fill):
    mots, lignes, cur = s.split(), [], ""
    for m in mots:
        t = (cur + " " + m).strip()
        if mesure(font, t, size) > largeur and cur: lignes.append(cur); cur = m
        else: cur = t
    lignes.append(cur)
    return "".join(texte(font, l, size, x, y + i * interligne, fill=fill) for i, l in enumerate(lignes)), len(lignes)


def illustration(w, h, seed=7):
    """Face avant : ciel nocturne, lune, mer gravée en lignes, bouteille verte."""
    r = random.Random(seed); o = []
    o.append(f'<defs><linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{COL["abysse"]}"/><stop offset=".55" stop-color="{COL["nuit"]}"/><stop offset="1" stop-color="#14505c"/></linearGradient>'
             f'<radialGradient id="halo"><stop offset="0" stop-color="{COL["sable"]}" stop-opacity=".35"/><stop offset="1" stop-color="{COL["sable"]}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="vb" x1="0" x2="1"><stop offset="0" stop-color="#245a42"/><stop offset=".4" stop-color="{COL["verre"]}"/><stop offset=".55" stop-color="#6aa585"/><stop offset="1" stop-color="#1d4734"/></linearGradient></defs>')
    o.append(f'<rect width="{w}" height="{h}" fill="url(#ciel)"/>')
    for _ in range(70):
        o.append(f'<circle cx="{r.random()*w:.1f}" cy="{r.random()*h*.5:.1f}" r="{r.random()*1.3+.3:.2f}" fill="{COL["sable"]}" opacity="{r.random()*.6+.2:.2f}"/>')
    mx, my = w * .72, h * .36
    o.append(f'<circle cx="{mx}" cy="{my}" r="{w*.42}" fill="url(#halo)"/><circle cx="{mx}" cy="{my}" r="{w*.17}" fill="{COL["sable"]}"/>')
    horizon = h * .58
    # reflet de lune
    for i in range(26):
        y = horizon + 8 + i * 9; lw = (w * .2) * (1 - i / 30) * (0.6 + r.random() * .6)
        o.append(f'<rect x="{mx - lw/2:.1f}" y="{y:.1f}" width="{lw:.1f}" height="2" rx="1" fill="{COL["sable"]}" opacity="{.5 - i/60:.2f}"/>')
    # mer gravée
    for i in range(46):
        y0 = horizon + i * (h - horizon) / 44; amp = 1.5 + i * .18; f = .018 + r.random() * .01; ph = r.random() * 6
        pts = " ".join(f"{x},{y0 + math.sin(x*f+ph)*amp + math.sin(x*f*2.7+ph)*amp*.4:.1f}" for x in range(-10, int(w) + 12, 8))
        col = COL["corail"] if i % 7 == 3 else COL["ecume"]
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{.7 + i*.03:.2f}" opacity="{.25 + i/90:.2f}"/>')
    # bouteille
    bx, by = w * .44, horizon + 36
    o.append(f'<g transform="translate({bx} {by}) rotate(-24)">'
             f'<ellipse cx="0" cy="62" rx="56" ry="7" fill="{COL["abysse"]}" opacity=".55"/>'
             f'<path d="M-24 60 V-40 C-24 -62 -9 -70 -8 -90 V-120 H8 V-90 C9 -70 24 -62 24 -40 V60 Q24 66 18 66 H-18 Q-24 66 -24 60Z" fill="url(#vb)"/>'
             f'<rect x="-10" y="-136" width="20" height="18" rx="3" fill="#5a3b25"/><rect x="-11" y="-124" width="22" height="6" fill="{COL["corail"]}"/>'
             f'<rect x="-12" y="-38" width="24" height="70" rx="4" fill="{COL["sable"]}" opacity=".9"/>'
             f'<path d="M-12 -20 H12 M-12 -6 H12 M-12 8 H8" stroke="#b9a37f" stroke-width="1.2"/>'
             f'<path d="M-15 -36 V54" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/></g>')
    # vagues devant la bouteille
    for i in range(6):
        y0 = by + 30 + i * 7
        pts = " ".join(f"{x},{y0 + math.sin(x*.05+i)*2.4:.1f}" for x in range(int(bx-90), int(bx+90), 6))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{COL["ecume"]}" stroke-width="1.1" opacity=".7"/>')
    return "".join(o)


def face(w, h):
    s = illustration(w, h)
    s += texte(SANS, "ROMAN", 11, 44, 66, track=.4, fill=COL["corail"])
    s += texte(DISPLAY, "Ce que la", 52, 42, 128, fill=COL["sable"])
    s += texte(DISPLAY, "marée", 96, 38, 214, fill=COL["sable"])
    s += texte(DISPLAY, "rapporte", 52, 42, 268, fill=COL["sable"])
    s += texte(SANS, L["auteur"].upper(), 15, w / 2, h - 46, track=.36, anchor="middle", fill=COL["sable"])
    return s


def dos(w, h):
    s = f'<rect width="{w}" height="{h}" fill="{COL["nuit"]}"/>'
    s += texte(DISPLAY, "« Une première fiction d'une justesse rare.", 19, 50, 92, fill=COL["sable"])
    s += texte(DISPLAY, "On referme le livre avec du sel sur les lèvres. »", 19, 50, 118, fill=COL["sable"])
    s += texte(SANS, "LE COURRIER DU LITTORAL", 9, 50, 142, track=.3, fill=COL["corail"])
    resume = ("Après vingt ans à Douala, Awa revient à Londji, le village de pêcheurs où elle a grandi, pour vider la maison de sa grand-mère. "
              "Un matin, la mer dépose à ses pieds une bouteille verte. À l'intérieur, une lettre écrite le jour de son départ, adressée à la personne qui la trouverait. "
              "Vingt-quatre bouteilles ont été jetées. Une seule est revenue.")
    p, n = paragraphe(SERIF, resume, 12.5, 50, 196, w - 100, 19, COL["ecume"])
    s += p
    y = 196 + n * 19 + 22
    p2, _ = paragraphe(SERIF, "Un roman lumineux sur l'exil intérieur, la transmission, et la patience obstinée de ceux qui nous aiment.", 12.5, 50, y, w - 100, 19, COL["ecume"])
    s += p2
    r0 = random.Random(11)
    for i in range(16):
        y0 = 470 + i * 9; ph = r0.random() * 6
        pts = " ".join(f"{x},{y0 + math.sin(x*.03+ph)*(2+i*.2):.1f}" for x in range(40, int(w) - 36, 8))
        s += f'<polyline points="{pts}" fill="none" stroke="{COL["corail"] if i % 6 == 2 else COL["ecume"]}" stroke-width=".8" opacity="{.15 + i/40:.2f}"/>'
    # code-barres (gabarit) et prix
    bx, byy = w - 50 - 190, h - 170
    s += f'<rect x="{bx}" y="{byy}" width="190" height="110" fill="#fff"/>'
    r = random.Random(3); x = bx + 14
    while x < bx + 176:
        bw = r.choice([1, 1, 2, 3]); s += f'<rect x="{x}" y="{byy+14}" width="{bw}" height="66" fill="#111"/>'; x += bw + r.choice([1, 2, 2, 3])
    s += texte(SANS_R, "ISBN 978-2-0000-0000-0", 9, bx + 95, byy + 96, anchor="middle", fill="#111")
    s += texte(SANS, "14,90 € · 9 500 FCFA", 10, 50, h - 70, track=.12, fill=COL["sable"])
    s += texte(SANS, L["editeur"].upper(), 9, 50, h - 52, track=.3, fill=COL["corail"])
    return s


def tranche(w, h):
    s = f'<rect width="{w}" height="{h}" fill="{COL["abysse"]}"/>'
    g = (texte(DISPLAY, L["titre"], 15, 0, 0, fill=COL["sable"]) +
         texte(SANS, L["auteur"].upper(), 9, 0, 0, track=.3, fill=COL["corail"], extra=f'transform="translate({mesure(DISPLAY, L["titre"], 15) + 26} -2)"'))
    s += f'<g transform="translate({w/2 + 5} 52) rotate(90)">{g}</g>'
    s += f'<circle cx="{w/2}" cy="{h-44}" r="9" fill="{COL["corail"]}"/><path d="M{w/2-5} {h-43} q5 -6 10 0" stroke="{COL["abysse"]}" stroke-width="1.6" fill="none"/>'
    return s


def svg(w, h, corps):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w/U:.4f}in" height="{h/U:.4f}in">{corps}</svg>'


fw, fh = TW * U, TH * U
open(os.path.join(OUT, "couverture-face.svg"), "w", encoding="utf-8").write(svg(fw, fh, face(fw, fh)))

b, sp = BLEED * U, SPINE * U
W, H = 2 * fw + sp + 2 * b, fh + 2 * b
plein = (f'<g transform="translate(0 0)"><svg width="{fw+b}" height="{H}" viewBox="{-b} {-b} {fw+b} {H}">{dos(fw, fh)}<rect x="{-b}" y="{-b}" width="{b}" height="{H}" fill="{COL["nuit"]}"/><rect x="0" y="{-b}" width="{fw}" height="{b}" fill="{COL["nuit"]}"/><rect x="0" y="{fh}" width="{fw}" height="{b}" fill="{COL["nuit"]}"/></svg></g>'
         f'<g transform="translate({b+fw} {b})">{tranche(sp, fh)}</g><rect x="{b+fw}" y="0" width="{sp}" height="{b}" fill="{COL["abysse"]}"/><rect x="{b+fw}" y="{H-b}" width="{sp}" height="{b}" fill="{COL["abysse"]}"/>'
         f'<g transform="translate({b+fw+sp} 0)"><svg width="{fw+b}" height="{H}" viewBox="0 0 {fw+b} {H}" preserveAspectRatio="none">{illustration(fw+b, fh+b*2)}</svg></g>')
# Face avant : l'illustration déborde dans le fond perdu, les textes restent dans la zone de sécurité
fr = face(fw, fh)
plein += f'<g transform="translate({b+fw+sp} {b})">{fr[fr.find(chr(60) + "path d=" + chr(34) + "M", fr.rfind("</g>")):]}</g>'
open(os.path.join(OUT, "couverture-complete.svg"), "w", encoding="utf-8").write(svg(W, H, plein))
rep = (f'<g fill="none" stroke="#ff2d55" stroke-width=".8" stroke-dasharray="4 3"><rect x="{b}" y="{b}" width="{W-2*b}" height="{fh}"/>'
       f'<path d="M{b+fw} 0V{H}M{b+fw+sp} 0V{H}"/><rect x="{b+12.5}" y="{b+12.5}" width="{fw-25}" height="{fh-25}" stroke="#00b3ff"/><rect x="{b+fw+sp+12.5}" y="{b+12.5}" width="{fw-25}" height="{fh-25}" stroke="#00b3ff"/></g>')
open(os.path.join(OUT, "couverture-reperes.svg"), "w", encoding="utf-8").write(svg(W, H, plein + rep))
print(f"couverture : {W/U:.3f} × {H/U:.3f} po, tranche {SPINE} po ({PAGES} p.)")
json.dump({"largeur_po": round(W / U, 4), "hauteur_po": round(H / U, 4), "tranche_po": SPINE, "pages": PAGES, "fond_perdu_po": BLEED},
          open(os.path.join(OUT, "gabarit.json"), "w"), indent=1)

# ——— EPUB 3 ———
def xhtml(titre, corps):
    return f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="fr" xml:lang="fr"><head><meta charset="utf-8"/><title>{html.escape(titre)}</title><link rel="stylesheet" href="style.css"/></head><body>{corps}</body></html>'

css = ("body{font-family:serif;line-height:1.55;margin:0 5%} h1{font-weight:normal;text-align:center;margin:3em 0 1.5em;font-size:1.6em}"
       " .num{text-align:center;letter-spacing:.3em;font-size:.75em;margin-top:4em;color:#b4563f} p{text-indent:1.4em;margin:0;text-align:justify}"
       " p.premier{text-indent:0} p.premier::first-letter{font-size:3.2em;float:left;line-height:.9;margin:.05em .08em 0 0;color:#0f3b47}"
       " .titre{text-align:center;margin-top:30%} .titre h1{font-size:2.2em;margin:0} .ded{text-align:center;font-style:italic;margin-top:40%}")
ep = os.path.join(OUT, "ce-que-la-maree-rapporte.epub")
with zipfile.ZipFile(ep, "w") as z:
    z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/style.css", css, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/couverture.svg", open(os.path.join(OUT, "couverture-face.svg"), encoding="utf-8").read(), compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/cover.xhtml", xhtml("Couverture", '<div style="text-align:center"><img src="couverture.svg" alt="Couverture" style="max-height:100%;max-width:100%"/></div>'), compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/titre.xhtml", xhtml(L["titre"], f'<div class="titre"><p style="text-indent:0;text-align:center;letter-spacing:.2em">{L["auteur"].upper()}</p><h1>{L["titre"]}</h1><p style="text-indent:0;text-align:center">roman — extrait</p></div><p class="ded">{L["dedicace"]}</p>'), compress_type=zipfile.ZIP_DEFLATED)
    items, spine, nav = [], [], []
    for i, c in enumerate(L["chapitres"], 1):
        corps = f'<p class="num">{["UN","DEUX","TROIS","QUATRE","CINQ"][i-1]}</p><h1>{html.escape(c["titre"])}</h1>' + "".join(f'<p{" class=\"premier\"" if j == 0 else ""}>{html.escape(p)}</p>' for j, p in enumerate(c["paras"]))
        z.writestr(f"OEBPS/ch{i}.xhtml", xhtml(c["titre"], corps), compress_type=zipfile.ZIP_DEFLATED)
        items.append(f'<item id="ch{i}" href="ch{i}.xhtml" media-type="application/xhtml+xml"/>'); spine.append(f'<itemref idref="ch{i}"/>')
        nav.append(f'<li><a href="ch{i}.xhtml">{html.escape(c["titre"])}</a></li>')
    z.writestr("OEBPS/nav.xhtml", xhtml("Sommaire", f'<nav epub:type="toc" id="toc"><h1>Sommaire</h1><ol>{"".join(nav)}</ol></nav>'), compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/content.opf", f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="fr"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">urn:uuid:5f1c2a7e-6c1b-4f0e-9d1a-maree2026</dc:identifier><dc:title>{L["titre"]}</dc:title><dc:creator>{L["auteur"]}</dc:creator><dc:publisher>{L["editeur"]}</dc:publisher><dc:language>fr</dc:language><meta property="dcterms:modified">2026-11-02T00:00:00Z</meta><meta name="cover" content="cov"/></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/><item id="cov" href="couverture.svg" media-type="image/svg+xml" properties="cover-image"/><item id="coverpage" href="cover.xhtml" media-type="application/xhtml+xml" properties="svg"/><item id="titre" href="titre.xhtml" media-type="application/xhtml+xml"/>{"".join(items)}</manifest>
<spine><itemref idref="coverpage"/><itemref idref="titre"/><itemref idref="nav"/>{"".join(spine)}</spine></package>''', compress_type=zipfile.ZIP_DEFLATED)
print("EPUB :", os.path.getsize(ep) // 1024, "Ko")
