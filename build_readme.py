import feedparser
import httpx
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_blog_entries():
    entries = feedparser.parse("https://philovdy.github.io/github-pages-with-jekyll/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"

#     rewritten = replace_chunk(rewritten, "tils", tils_md)

    readme_contents = readme.open().read()
    
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)
