from .images import _yieldPossibleImg

def _replaceOfftopicLink(soup, args = {}):
	for link in soup.find_all("a"):
		img = next(_yieldPossibleImg(link), None)
		if img:
			link.replace_with(img)
			continue
		if link.text and link.text.strip():
			link.replace_with(link.text)
			continue
		link.decompose()
	return soup