# translate_po.py
from pathlib import Path
import re
import codecs
import polib
from deep_translator import GoogleTranslator

ROOT = Path(__file__).parent
PO_FILES = list((ROOT / "locale").rglob("LC_MESSAGES/*.po"))

# --- glossary for deterministic UI terms ---
GLOSSARY = {
    "ar": {
        "All Products": "جميع المنتجات",
        "Home": "الصفحة الرئيسية",
        "Shop Now": "تسوق الآن",
        "Search our site": "ابحث في الموقع",
        "My Account": "حسابي",
        "My Profile": "ملفي الشخصي",
        "Logout": "تسجيل الخروج",
        "Login": "تسجيل الدخول",
        "Register": "تسجيل",
        "Product Management": "إدارة المنتجات",
        "Start shopping here": "ابدأ التسوق من هنا",
        "Profile updated successfully": "تم تحديث الملف الشخصي بنجاح",
    },
    "de": {
        "All Products": "Alle Produkte",
        "Home": "Startseite",
        "Shop Now": "Jetzt einkaufen",
        "Search our site": "Unsere Seite durchsuchen",
        "My Account": "Mein Konto",
        "My Profile": "Mein Profil",
        "Logout": "Abmelden",
        "Login": "Anmelden",
        "Register": "Registrieren",
        "Product Management": "Produktmanagement",
        "Start shopping here": "Beginnen Sie hier mit dem Einkaufen",
        "Profile updated successfully": "Profil erfolgreich aktualisiert",
    },
}

# --- placeholder patterns (Python %-format and {...}) ---
PH_RE = re.compile(
    r"""
    %\([^)]+\)[#0\- +]?\d*(?:\.\d+)?[sdifuxXeEgGcr] |  # %(name)s / %(count)d
    %\d*\$?[#0\- +]?\d*(?:\.\d+)?[sdifuxXeEgGcr]   |  # %s %d %1$s ...
    \{[^}]+\}                                         # {user}
    """,
    re.VERBOSE,
)

def extract_placeholders(s: str):
    return [(m.start(), m.end(), m.group(0)) for m in PH_RE.finditer(s or "")]

def translate_chunk(text: str, lang: str) -> str:
    if not text or text.isspace():
        return text or ""
    # glossary first
    g = GLOSSARY.get(lang, {})
    if text in g:
        return g[text]
    try:
        out = GoogleTranslator(source="en", target=lang).translate(text)
        return out if isinstance(out, str) and out else text
    except Exception:
        return text

def segment_translate(s: str, lang: str) -> str:
    if not s:
        return ""
    phs = extract_placeholders(s)
    if not phs:
        return translate_chunk(s, lang)
    parts = []
    last = 0
    for start, end, ph in phs:
        if start > last:
            parts.append(translate_chunk(s[last:start], lang))
        parts.append(ph)
        last = end
    if last < len(s):
        parts.append(translate_chunk(s[last:], lang))
    return "".join(p if isinstance(p, str) else "" for p in parts)

def validate_placeholders(src: str, dst: str) -> str:
    from collections import Counter
    src_ph = [t for *_, t in extract_placeholders(src)]
    dst_ph = [t for *_, t in extract_placeholders(dst)]
    need, have = Counter(src_ph), Counter(dst_ph)
    missing = []
    for k, cnt in need.items():
        if have[k] < cnt:
            missing.extend([k] * (cnt - have[k]))
    if missing:
        dst = (dst.rstrip() + " " + " ".join(missing)).strip()
    return dst

def ensure_headers(po: polib.POFile, lang_code: str):
    po.metadata["Language"] = lang_code
    po.metadata["MIME-Version"] = "1.0"
    po.metadata["Content-Type"] = "text/plain; charset=UTF-8"
    po.metadata["Content-Transfer-Encoding"] = "8bit"
    if lang_code == "ar":
        po.metadata["Plural-Forms"] = (
            "nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : "
            "n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5;"
        )
    elif lang_code == "de":
        po.metadata["Plural-Forms"] = "nplurals=2; plural=(n != 1);"

def strip_bom_inplace(path: Path):
    text = codecs.open(path, "r", "utf-8-sig").read()
    path.write_text(text, encoding="utf-8")

def fill_po_file(po_path: Path):
    lang_code = po_path.parent.parent.name  # ar or de
    po = polib.pofile(str(po_path), encoding="utf-8-sig")
    ensure_headers(po, lang_code)

    changed = 0
    total = 0

    for e in po:
        if e.obsolete:
            continue
        total += 1

        # clear fuzzy if we will set a translation
        def clear_fuzzy(entry):
            if "fuzzy" in entry.flags:
                entry.flags = [f for f in entry.flags if f != "fuzzy"]

        if e.msgid_plural:
            # plural
            if not e.msgstr:
                s_tr = segment_translate(e.msgid, lang_code)
                s_tr = validate_placeholders(e.msgid, s_tr)
                e.msgstr = s_tr
                clear_fuzzy(e)
                changed += 1
            plural_tr = segment_translate(e.msgid_plural, lang_code)
            plural_tr = validate_placeholders(e.msgid_plural, plural_tr)
            plural_count = 6 if lang_code == "ar" else 2
            if not e.msgstr_plural:
                e.msgstr_plural = {}
            for i in range(plural_count):
                if not e.msgstr_plural.get(i):
                    e.msgstr_plural[i] = plural_tr
                    clear_fuzzy(e)
                    changed += 1
        else:
            # singular
            if not e.msgstr:
                tr = segment_translate(e.msgid, lang_code)
                tr = validate_placeholders(e.msgid, tr)
                if tr and tr != e.msgid:
                    e.msgstr = tr
                else:
                    # If API failed, at least use glossary if present
                    g = GLOSSARY.get(lang_code, {})
                    if e.msgid in g:
                        e.msgstr = g[e.msgid]
                if e.msgstr:
                    clear_fuzzy(e)
                    changed += 1

    po.save(str(po_path))
    strip_bom_inplace(po_path)
    return changed, total

if __name__ == "__main__":
    if not PO_FILES:
        print("No .po files found under locale/**/LC_MESSAGES/")
    for p in PO_FILES:
        ch, tot = fill_po_file(p)
        print(f"[{p}] translated {ch}/{tot} entries")
    print("Now run: python manage.py compilemessages -l ar -l de")


# fix_newline_parity.py
from pathlib import Path
import polib

def fix_file(path):
    po = polib.pofile(str(path), encoding="utf-8")
    changed = 0
    for e in po:
        if e.obsolete:
            continue
        id_starts_nl = e.msgid.startswith("\n")
        # singular
        if e.msgstr:
            tr = e.msgstr
            tr_starts_nl = tr.startswith("\n")
            if id_starts_nl and not tr_starts_nl:
                e.msgstr = "\n" + tr
                changed += 1
            if not id_starts_nl and tr_starts_nl:
                e.msgstr = tr.lstrip("\n")
                changed += 1
        # plural
        if e.msgid_plural and e.msgstr_plural:
            for k, v in list(e.msgstr_plural.items()):
                tr_starts_nl = v.startswith("\n")
                if id_starts_nl and not tr_starts_nl:
                    e.msgstr_plural[int(k)] = "\n" + v
                    changed += 1
                if not id_starts_nl and tr_starts_nl:
                    e.msgstr_plural[int(k)] = v.lstrip("\n")
                    changed += 1
    po.save(str(path))
    print(f"fixed {changed} entries in {path}")

fix_file(Path("locale/de/LC_MESSAGES/django.po"))
fix_file(Path("locale/ar/LC_MESSAGES/django.po"))
