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

def get_tils():
    # til_readme = "https://github.com/philovdy/til/blob/master/README.md"
    til_readme = "https://raw.githubusercontent.com/philovdy/til/master/README.md"
    print('til_file', til_readme)
    
    with open(til_readme, "r") as ins:
        line = ins.readline()
        print(line)
    
#     for filepath in root.glob("*/*.md"):
#         fp = filepath.open()
#         title = fp.readline().lstrip("#").strip()
#         body = fp.read().strip()
#         path = str(filepath.relative_to(root))    
    
#     with open(til_file, "r") as ins:  
#         for line in ins:
#             print(line_test)

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
    
#     rewritten = replace_chunk(rewritten, "tils", tils_md)

    til_readme_contents = get_tils()

    readme = root / "README.md"
    print('root is ', root)

    readme_contents = readme.open().read()
    
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)
