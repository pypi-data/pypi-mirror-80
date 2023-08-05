import webspidy as spidy

# python setup.py sdist
# twine upload dist/*


soup = spidy.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_audio_all")
print(soup.audios())
