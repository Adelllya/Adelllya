"""Public numbers for the slate readout, fetched from the GitHub API.

The result is cached in tools/data/github.json, so a build without network still works.
Set GITHUB_TOKEN to avoid the anonymous rate limit (the refresh workflow does this).
"""
import datetime
import json
import os
import urllib.request

USER = "Adelllya"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "data", "github.json")

# Repos that are not code of hers, or are this profile itself.
SKIP_REPOS = {USER}
# Generated or incidental languages that would drown out the real ones.
SKIP_LANGS = {"Jupyter Notebook", "Batchfile", "PowerShell", "Procfile", "Shell", "Dockerfile", "Makefile"}


def _get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-build"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch():
    user = _get("https://api.github.com/users/%s" % USER)
    repos = [r for r in _get("https://api.github.com/users/%s/repos?per_page=100" % USER)
             if not r["fork"] and r["name"] not in SKIP_REPOS]
    langs = {}
    for r in repos:
        for lang, size in _get(r["languages_url"]).items():
            if lang not in SKIP_LANGS:
                langs[lang] = langs.get(lang, 0) + size
    last_push = max(r["pushed_at"] for r in repos) if repos else None
    return {
        "fetched": datetime.date.today().isoformat(),
        "public_repos": len(repos),
        "stars": sum(r["stargazers_count"] for r in repos),
        "followers": user["followers"],
        "since": user["created_at"][:4],
        "last_push": last_push[:10] if last_push else None,
        "languages": sorted(langs.items(), key=lambda kv: -kv[1]),
    }


def load(refresh=True):
    data = None
    if refresh:
        try:
            data = fetch()
            os.makedirs(os.path.dirname(CACHE), exist_ok=True)
            with open(CACHE, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=1)
        except Exception as exc:  # offline or rate limited: fall back to the cache
            print("github fetch failed (%s), using cache" % exc)
    if data is None:
        with open(CACHE, encoding="utf-8") as fh:
            data = json.load(fh)
    return data


if __name__ == "__main__":
    print(json.dumps(load(), indent=1))
