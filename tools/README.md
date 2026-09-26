# How this profile is built

Every picture on the profile is an SVG in `/assets`, in a dark and a light version.
They are generated, not drawn by hand in an editor, so changing a text never means redrawing.

```
python3 -m pip install fonttools pillow
python3 tools/build.py      # rebuilds /assets
python3 tools/readme.py     # rewrites README.md
python3 tools/preview.py    # local preview in tools/.preview (open the html files)
```

Fonts are downloaded into `tools/.fonts` on the first run and are not committed.

## When a quest changes

Open `tools/content.py` and edit the entry in `QUESTS`:

- `status` is one of `COMPLETE`, `IN PROGRESS`, `SIDE QUEST`, `LOCKED`.
- `live=True` adds the LIVE chip.
- A `LOCKED` quest is drawn dark, with the lock and the hearts. Change the status and it becomes a normal card.
- To make a card clickable, add its repo to `QUEST_LINKS` in `tools/readme.py`.

Then run `build.py` and `readme.py` again.

## Refreshed by itself

`.github/workflows/refresh.yml` rebuilds the slate readout (repos, languages, last push) every Monday
and commits it. It can also be started by hand from the Actions tab.

## Live site screenshots

The two browser windows under the quest cards come from `tools/source/site-<key>.png`.
To refresh one (needs Node 22 and Chrome):

```
node tools/webshot.js https://shade-web-five.vercel.app tools/source/site-shade.png
python3 tools/build.py site-shade
```

The crop of each screenshot is `SHOWCASE` in `content.py`.

## Pictures

- `tools/source/kyoka.jpg` is the art on the Kyoka card. Replace the file to change it.
- `tools/source/photo.jpg` (or .png) is the portrait. When the file exists, a photo card is built,
  recoloured into the palette, and shown next to the profile lines. Delete the file to remove the card.

## Files

- `photo.py` crops and recolours the pictures
- `ghdata.py` public GitHub numbers, cached in `data/github.json`
- `webshot.js` screenshots of live sites

- `content.py` all the words: name, tagline, skills, quests, links
- `panels.py` layout of every panel
- `art.py` illustrations: Kyoka, the cat, the sword, the tower
- `kit.py` palette, text to outlines, shared shapes
- `icons/` single-colour tech icons from Simple Icons (CC0)

Fonts: Chakra Petch, JetBrains Mono, Noto Sans JP (all under the SIL Open Font License).
