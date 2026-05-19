import bs4
import markdown2
import time
import glob

def _html_from_markdown_path(md_path):
    return markdown2.markdown_path(md_path, extras={'wiki-tables': None, 'toc': {'depth': 2}, 'fenced-code-blocks': None})

def _page_title_from_html_content(content):
    soup = bs4.BeautifulSoup(content, features="html.parser")
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
    print(f"Processing {path}")
    document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style.css?v={timestamp}" />
        <link rel="stylesheet" href="vim.css?v={timestamp}" />
        <link rel="shortcut icon" href="favicon.ico?v={timestamp}" />
        <title>gdtyra :: {title}</title>
    </head>
    <body>
    <header>
        <h1>gdtyra</h1>
    </header>
    <!-- Toggle Button -->
    <button class="menu-btn" onclick="toggleNav()">Menu</button>

    <!-- Side Navigation Drawer -->
    <nav id="nav-drawer">
        <h3>Table of Contents</h3>
        {html.toc_html}
        <h3>Other Pages</h3>
        {files_html}
    </nav>
    <main class="container">
    {html}
    </main>
    <footer>
    <p class="generated_date">Generated on {time.strftime('%B %d %Y')}</p>
    </footer>
    <script src="script.js?v={timestamp}"></script>
    </body>
    </html>
    """

    with open(path, 'wt') as f:
        f.write(document)

document = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css?v={timestamp}" />
    <link rel="stylesheet" href="vim.css?v={timestamp}" />
    <link rel="shortcut icon" href="favicon.ico?v={timestamp}" />
    <title>gdtyra :: Index</title>
</head>
<body>
<header>
    <h1>gdtyra</h1>
</header>
<main class="container">
{files_html}
</main>
<footer>
<p class="generated_date">Generated on {time.strftime('%B %d %Y')}</p>
</footer>
<script src="script.js?v={timestamp}"></script>
</body>
</html>
"""

with open("index.html", 'wt') as f:
    f.write(document)