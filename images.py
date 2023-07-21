def _yieldPossibleImg(soup):
	possibles = [
		soup.find_all("div", class_="js-delayed-image-load"),
		soup.find_all("figure"),
		soup.find_all("img"),
	]
	for l in possibles:
		for x in l:
			yield x