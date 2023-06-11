import markdown2

html = markdown2.markdown_path('index.md')

document = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css" />
</head>
<body>
{html}
</body>
</html>
"""

with open('index.html', 'wt') as f:
    f.write(document)