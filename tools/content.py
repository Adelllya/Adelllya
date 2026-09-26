"""All the words on the page. Change things here, then run tools/build.py."""

NAME_KANA = "アイラ"
NAME_LATIN = "AILACHU"
TAGLINE = "Backend developer. Python lover. Hyrule fan."
READOUT = "BACKEND · PYTHON · DJANGO/DRF · KBTU ALMATY"
STATUS = "OPEN TO FREELANCE · BACKEND · AUTOMATION"

# key, chapter tab, latin title, japanese twin, watermark kanji
CHAPTERS = [
    ("profile", "第一章", "PROFILE", "プロフィール", "勇"),
    ("arsenal", "第二章", "ARSENAL", "装備", "装"),
    ("quests", "第三章", "QUEST LOG", "冒険記録", "記"),
    ("slate", "第四章", "SLATE", "石板", "祠"),
    ("side", "第五章", "SIDE QUESTS", "寄り道", "寄"),
    ("requests", "第六章", "REQUESTS", "依頼", "依"),
    ("link", "第七章", "LINK", "連絡", "連"),
]

# Main stack, marked as equipped in the inventory.
EQUIPPED = {"PYTHON", "DJANGO", "DRF"}

# row label, then five cells of (icon file in tools/icons or a built-in name, label)
ARSENAL = [
    ("LANGUAGES", [("python", "PYTHON"), ("typescript", "TYPESCRIPT"), ("cplusplus", "C++"),
                   ("openjdk", "JAVA"), ("@sql", "SQL")]),
    ("BACKEND", [("django", "DJANGO"), ("@rest", "DRF"), ("postgresql", "POSTGRES / SQLITE"),
                 ("telegram", "AIOGRAM"), ("claude", "CLAUDE API")]),
    ("FRONTEND", [("angular", "ANGULAR"), ("react", "REACT"), ("vite", "VITE"),
                  ("tailwindcss", "TAILWIND"), ("html5", "HTML / CSS")]),
    ("TOOLS", [("git", "GIT / GITHUB"), ("selenium", "SELENIUM / CAMOUFOX"), ("postman", "POSTMAN"),
               ("unity", "UNITY"), ("visualstudiocode", "VS CODE / PYCHARM")]),
]

# status is one of: COMPLETE, IN PROGRESS, LOCKED, SIDE QUEST
# live adds a LIVE chip. caption is the vertical text on the left edge.
QUESTS = [
    dict(key="flavor-tree", num="01", title="FLAVOR TREE", status="IN PROGRESS", caption="味覚",
         pitch="Food and drink pairing for bars and restaurants in Kazakhstan: "
               "scan a QR, pick a dish, see what to pour and why.",
         stack="DJANGO · DRF · ANGULAR 18 · CLAUDE API",
         note="ONEIDEA CHAMPIONSHIP 2026 · TEAM OF TWO"),
    dict(key="petcare", num="02", title="PETCARE", status="COMPLETE", caption="保護",
         pitch="Pet shop and shelter adoption platform: pets, shelters, favourites, JWT auth.",
         stack="ANGULAR 19 · DJANGO 4.2 · DRF · SIMPLEJWT",
         note="KBTU WEB DEVELOPMENT FINAL · TEAM OF THREE"),
    dict(key="finance-bridge", num="03", title="FINANCE BRIDGE", status="COMPLETE", live=True, caption="会計",
         pitch="Landing kit for a private chief accountant: mobile prototype, "
               "three hero variants, copy per screen.",
         stack="REACT 19 · VITE 7 · TAILWIND 4 · TYPESCRIPT",
         note="FINANCE-BRIDGE-ONE.VERCEL.APP"),
    dict(key="shade", num="04", title="SHADE", status="COMPLETE", live=True, caption="創作",
         pitch="Website for SHADE, the creative people club at KBTU: drawing, art therapy, crafts.",
         stack="REACT · VITE · TYPESCRIPT",
         note="FIRST VERSION IN ANGULAR 19"),
    dict(key="coinq", num="05", title="COINQ", status="SIDE QUEST", caption="家計",
         pitch="Telegram expense tracker with step-by-step dialogs.",
         stack="AIOGRAM 3 · FSM · SQLITE",
         note="TELEGRAM BOT"),
    dict(key="heart-of-the-hero", num="06", title="HEART OF THE HERO", status="LOCKED", caption="封印",
         pitch="Pixel platformer. Not released yet.",
         stack="VANILLA JS · CANVAS · 320×180",
         note=""),
]

ARCHIVE = "ARCHIVES ▸ PP2_2025 (PYTHON LABS) · WEBDEV (HTML/CSS/JS LABS) · OOP FINAL (JAVA, TEAM OF FOUR)"

# Live sites shown as screenshots under the quest cards.
# The screenshot files live in tools/source (site-<key>.png), refresh them with tools/webshot.js.
# crop is left, top, right, bottom in pixels of the screenshot.
SHOWCASE = [
    dict(key="finance-bridge", title="FINANCE BRIDGE", url="finance-bridge-one.vercel.app", crop=(0, 262, 830, 760)),
    dict(key="shade", title="SHADE", url="shade-web-five.vercel.app", crop=(0, 0, 1280, 766)),
]

# What people can ask me for. title, icon, three lines, proof line.
REQUESTS = [
    ("BACKEND & APIs", "django",
     ["REST APIs on Django + DRF", "JWT auth, roles, admin panel", "PostgreSQL or SQLite models"],
     "BUILT ▸ PETCARE · FLAVOR TREE"),
    ("TELEGRAM BOTS", "telegram",
     ["aiogram 3, step-by-step dialogs", "Buttons, forms, admin alerts", "Data saved to SQLite"],
     "BUILT ▸ COINQ"),
    ("AUTOMATION", "selenium",
     ["Browser automation in Python", "Repetitive web tasks, data", "Selenium and Camoufox"],
     "TOOLS ▸ SELENIUM · CAMOUFOX"),
    ("LANDING PAGES", "react",
     ["React, Vite, Tailwind", "Mobile first, several languages", "Deployed on Vercel"],
     "BUILT ▸ FINANCE BRIDGE · SHADE"),
]

# Commands typed one after another in the closing terminal.
COMMANDS = ["python manage.py runserver", "python bot.py", "npm run build", "git push origin main"]

QUOTE = "It's dangerous to go alone. Take this."
QUOTE_JP = "ヒトリデハ キケンジャ コレヲ サズケヨウ"

# Part of the photo to use, as fractions: left, top, right, bottom.
# The bottom is trimmed to leave out the caption printed on the picture.
PHOTO_BOX = (0.0, 0.0, 1.0, 0.935)
# Where the face is inside that part, so the crop stays centred on it.
PHOTO_FOCUS = (0.5, 0.4)

# key, icon, label, handle
LINKS = [
    ("telegram", "telegram", "TELEGRAM", "@ailachu_dev"),
    ("gmail", "gmail", "GMAIL", "ailachu.echo"),
    ("tiktok", "tiktok", "TIKTOK", "@_ailachuchu_"),
    ("pinterest", "pinterest", "PINTEREST", "pin.it/75PPQTbym"),
]
