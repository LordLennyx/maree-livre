"""PDF imprimeur : couverture à plat (taille exacte avec fond perdu) et intérieur 5,5 × 8,5 po."""
import json, pathlib
from playwright.sync_api import sync_playwright
ICI = pathlib.Path(__file__).resolve().parent.parent; F = ICI / "fichiers"
g = json.loads((F / "gabarit.json").read_text())
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    svg = (F / "couverture-complete.svg").read_text(encoding="utf-8")
    pg.set_content(f'<style>@page{{size:{g["largeur_po"]}in {g["hauteur_po"]}in;margin:0}}body{{margin:0}}svg{{display:block;width:{g["largeur_po"]}in;height:{g["hauteur_po"]}in}}</style>{svg}')
    pg.pdf(path=str(F / "couverture-imprimeur.pdf"), prefer_css_page_size=True, print_background=True)
    pg.goto((ICI / "interieur.html").as_uri(), wait_until="networkidle"); pg.evaluate("document.fonts.ready.then(()=>1)")
    pg.emulate_media(media="print")
    pg.pdf(path=str(F / "interieur.pdf"), prefer_css_page_size=True, print_background=True)
    b.close()
import fitz
for n in ("couverture-imprimeur.pdf", "interieur.pdf"):
    d = fitz.open(F / n); r = d[0].rect; print(n, d.page_count, "p.", round(r.width / 72, 3), "x", round(r.height / 72, 3), "po")
d = fitz.open(F / "interieur.pdf"); (ICI / "_work").mkdir(exist_ok=True)
for i in (4, 5): d[i].get_pixmap(dpi=70).save(ICI / "_work" / f"int{i}.png")
