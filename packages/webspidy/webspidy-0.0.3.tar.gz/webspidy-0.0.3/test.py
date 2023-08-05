import webspidy

# python setup.py sdist
# twine upload dist/*

soup = webspidy.get("https://google.com")
print(soup.images())
