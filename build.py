import bs4
import markdown2
import time
import glob

def _html_from_markdown_path(md_path):
    return markdown2.markdown_path(md_path, extras={'wiki-tables': None, 'toc': {'depth': 2}, 'fenced-code-blocks': None})

def _page_title_from_html_content(content):
    soup = bs4.BeautifulSoup(content)
    return soup.find(name='h1').text

files = [f for f in glob.glob('*.md') if not f.startswith("_")]
html_files = [f.replace('.md', '.html') for f in files]
html_file_content = [_html_from_markdown_path(f) for f in files]
page_titles = [_page_title_from_html_content(content) for content in html_file_content]

timestamp = time.time()

files_html = (
    "<ul>" +
    "".join(f"<li><a href=\"{path}\">{title}</a></li>" for path, title in zip(html_files, page_titles)) +
    "</ul>"
)

for path, html, title in zip(html_files, html_file_content, page_titles):
    document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="style.css?v={timestamp}" />
        <link rel="stylesheet" href="vim.css?v={timestamp}" />
        <title>gdtyra :: {title}</title>
    </head>
    <body>
    <div id="main">
    <div id ="nav" class="column">
    <nav>
    <h1>Table of Contents</h1>
    {html.toc_html}
    <h1>Other Pages</h2>
    {files_html}
    </nav>
    </div>
    <div class="column">
    <div id="content">
    <article>
    {html}
    <footer>
    <p class="generated_date">Generated on {time.strftime('%B %d %Y')}</p>
    </footer>
    </article>
    </div>
    </div>
    </div>
    <script src="script.js"></script>
    </body>
    </html>
    """

    with open(path, 'wt') as f:
        f.write(document)

document = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css?v={timestamp}" />
    <title>gdtyra :: Index</title>
</head>
<body>
<div id="main">
<div class="column">
<div id="content">
<article>
{files_html}
<footer>
<p class="generated_date">Generated on {time.strftime('%B %d %Y')}</p>
</footer>
</article>
</div>
</div>
</div>
<script src="script.js"></script>
</body>
</html>
"""

with open("index.html", 'wt') as f:
    f.write(document)