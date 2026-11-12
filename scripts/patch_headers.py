import pathlib, re

SKIP = {"index.html", "en/index.html", "pl/index.html"}

CSS_SHARED = """
.tbj-top{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border-bottom:1px solid #dce3f0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.tbj-top-inner{max-width:1100px;margin:0 auto;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.tbj-top a.tbj-logo{font-weight:700;font-size:1.1rem;text-decoration:none;color:#312e81}
.tbj-top a.tbj-logo span{color:#0e9bb8}
.tbj-top nav.tbj-desk{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.tbj-top nav.tbj-desk a{color:#0f172a;text-decoration:none;font-size:.9rem;font-weight:500}
.tbj-top nav.tbj-desk a:hover{color:#312e81}
.tbj-lang{display:flex;gap:6px;font-size:.8rem}
.tbj-lang a{color:#5c6578;text-decoration:none;padding:4px 8px;border-radius:6px;border:1px solid transparent}
.tbj-lang a:hover,.tbj-lang a.active{color:#312e81;border-color:#dce3f0;background:#f3f5fb;font-weight:700}
.tbj-ham{display:none;width:44px;height:44px;border:1px solid #dce3f0;border-radius:10px;background:#fff;cursor:pointer;align-items:center;justify-content:center;padding:0}
.tbj-ham span,.tbj-ham span:before,.tbj-ham span:after{display:block;width:18px;height:2px;background:#0f172a;border-radius:1px;position:relative;transition:.2s}
.tbj-ham span:before,.tbj-ham span:after{content:"";position:absolute;left:0}
.tbj-ham span:before{top:-6px}.tbj-ham span:after{top:6px}
.tbj-ham[aria-expanded="true"] span{background:transparent}
.tbj-ham[aria-expanded="true"] span:before{top:0;transform:rotate(45deg)}
.tbj-ham[aria-expanded="true"] span:after{top:0;transform:rotate(-45deg)}
.tbj-mm{display:none;width:100%;flex-direction:column;gap:2px;padding:8px 16px 12px;border-top:1px solid #dce3f0}
.tbj-mm.open{display:flex}
.tbj-mm a{text-decoration:none;color:#0f172a;font-weight:500;padding:12px 4px;border-radius:8px;font-size:.95rem}
.tbj-mm a:hover{color:#312e81;background:#f3f5fb}
@media(max-width:720px){
  .tbj-top nav.tbj-desk{display:none}
  .tbj-ham{display:inline-flex}
}
"""

def lang_of(path):
    if path.startswith("en/"):
        return "en"
    if path.startswith("pl/"):
        return "pl"
    return "it"

def header_html(lang):
    if lang == "en":
        home = "https://thebestjob.org/en/"
        links = [("https://thebestjob.org/en/", "Home"), ("https://thebestjob.org/en/poland-startup/", "Poland startup"), ("https://thebestjob.org/en/digital-ai/", "Digital & AI"), ("https://thebestjob.org/en/contact/", "Contact")]
        li, lp, le = "", "", " active"
    elif lang == "pl":
        home = "https://thebestjob.org/pl/"
        links = [("https://thebestjob.org/pl/", "Start"), ("https://thebestjob.org/pl/startup-polska/", "Startup Polska"), ("https://thebestjob.org/pl/cyfryzacja-ai/", "Cyfryzacja i AI"), ("https://thebestjob.org/pl/kontakt/", "Kontakt")]
        li, lp, le = "", " active", ""
    else:
        home = "https://thebestjob.org/"
        links = [("https://thebestjob.org/", "Home"), ("https://thebestjob.org/startup-polonia/", "Startup Polonia"), ("https://thebestjob.org/digitale-ai/", "Digitale & AI"), ("https://thebestjob.org/contatti/", "Contatti")]
        li, lp, le = " active", "", ""
    desk = "\n".join('      <a href="%s">%s</a>' % (h, t) for h, t in links)
    mob = "\n".join('    <a href="%s" onclick="tbjCloseMM()">%s</a>' % (h, t) for h, t in links)
    return """<div class="tbj-top" id="tbj-top">
  <div class="tbj-top-inner">
    <a class="tbj-logo" href="%s">The Best <span>Job</span></a>
    <nav class="tbj-desk" aria-label="Menu">
%s
    </nav>
    <div style="display:flex;align-items:center;gap:8px;margin-left:auto">
      <div class="tbj-lang" aria-label="Language">
        <a href="/contatti/" hreflang="it" class="%s">IT</a>
        <a href="/pl/kontakt/" hreflang="pl" class="%s">PL</a>
        <a href="/en/contact/" hreflang="en" class="%s">EN</a>
      </div>
      <button type="button" class="tbj-ham" id="tbj-ham" aria-label="Menu" aria-expanded="false" aria-controls="tbj-mm" onclick="tbjToggleMM()"><span></span></button>
    </div>
  </div>
  <nav class="tbj-mm" id="tbj-mm" hidden>
%s
  </nav>
</div>
<script>
function tbjToggleMM(){var m=document.getElementById("tbj-mm");var h=document.getElementById("tbj-ham");var open=m.classList.toggle("open");h.setAttribute("aria-expanded",open?"true":"false");m.hidden=!open;}
function tbjCloseMM(){var m=document.getElementById("tbj-mm");var h=document.getElementById("tbj-ham");if(!m)return;m.classList.remove("open");m.hidden=true;if(h)h.setAttribute("aria-expanded","false");}
</script>
""" % (home, desk, li.strip(), lp.strip(), le.strip(), mob)

changed = []
for path in pathlib.Path(".").rglob("*.html"):
    rel = path.as_posix()
    if rel in SKIP or rel.startswith(".github"):
        continue
    if rel in ("contatti/index.html", "en/contact/index.html", "pl/kontakt/index.html"):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "tbj-top" in text:
        continue
    if "position:sticky" in text and ("class=\"ham\"" in text or "mobile-menu" in text):
        continue
    if "</head>" not in text:
        continue
    lang = lang_of(rel)
    if "tbj-top-css" not in text:
        text = text.replace("</head>", '<style id="tbj-top-css">' + CSS_SHARED + '</style>\n</head>', 1)
    m = re.search(r"<body[^>]*>", text, flags=re.I)
    if not m:
        continue
    if 'id="tbj-top"' in text:
        continue
    hdr = header_html(lang)
    text = text[:m.end()] + "\n" + hdr + text[m.end():]
    path.write_text(text, encoding="utf-8")
    changed.append(rel)
print("Patched", len(changed), "pages")
for c in sorted(changed):
    print(" ", c)
