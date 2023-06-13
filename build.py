import markdown2

html = markdown2.markdown_path('index.md', extras={'toc': {'depth': 2}})

document = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css" />
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