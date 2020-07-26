import feedparser
import httpx
import pathlib
import re
import os
import requests
import git

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
    til_readme = "https://raw.githubusercontent.com/philovdy/til/master/README.md"
    r = requests.get(til_readme)
    #print(r)

    page = requests.get(til_readme)
    all_text = page.text
    search_re = re.findall( r'(\*+).(\[.*?\])(\(.*?\)).?-(.+)', all_text, re.M|re.I)
    dt_til = sorted(search_re, key=lambda search_re: search_re[3], reverse=True)[:5]
    
    til_md = ""
    
    for i in dt_til:
        til_md += "\n" + i[0] + ' ' + i[1] + i[2]         
       
    #print(til_md)
    
    return til_md

#     with open(all_text, "r") as ins:
#         line = ins.readline()
#         searchObj = re.search( r'(\*+).(\[.*?\])(\(.*?\)).?-(.+)', line, re.M|re.I)
#         print(line)

#     til_read = "https://github.com/philovdy/til/blob/master/README.md?raw=true"
    


    
    
#     with open(til_readme, "r") as ins:
#         line = ins.readline()
#         print(line)
    
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

    readme = root / "README.md"
    print('root is ', root)

    readme_contents = readme.open().read()
    
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    til_readme_contents = get_tils()
    rewritten = replace_chunk(rewritten, "tils", til_readme_contents)    
    
    readme.open("w").write(rewritten)
