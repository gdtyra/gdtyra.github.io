import markdown2
import time

html = markdown2.markdown_path('index.md', extras={'wiki-tables': None, 'toc': {'depth': 2}})

timestamp = time.time()

document = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css?v={timestamp}" />
</head>
<body>
<div id="main">
<div id ="nav" class="column">
{html.toc_html}
</div>
<div class="column">
<div id="content">
{html}
</div>
</div>
</div>
<script src="script.js"></script>
</body>
</html>
"""

with open('index.html', 'wt') as f:
    f.write(document)