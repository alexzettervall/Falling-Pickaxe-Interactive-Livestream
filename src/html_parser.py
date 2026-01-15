import bs4

file = open("example_html.txt", "r", encoding="UTF-8")
html = file.read()
soup = bs4.BeautifulSoup(html, 'html.parser')
for link in soup.find_all('a'):
    print(soup.get_text())
file.close()