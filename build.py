import markdown2
import time
import glob

files = [f for f in glob.glob('*.md') if not f.startswith("_")]
timestamp = time.time()

files_html = "<ul>" + "".join(f"<li><a href=\"{f.replace('.md', '.html')}\">{f.replace('.md', '').replace('_', ' ').capitalize()}</a></li>" for f in files) + "</ul>"

for path in files:
    html = markdown2.markdown_path(path, extras={'wiki-tables': None, 'toc': {'depth': 2}})

    document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="style.css?v={timestamp}" />
        <title>gdtyra :: {path.replace('.md', '').replace('_', ' ').capitalize()}</title>
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

    with open(path.replace('.md', '.html'), 'wt') as f:
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