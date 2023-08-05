import webspidy


soup = webspidy.get("https://google.com")
print(soup.images())
