import requests

def download(url):
	get_responce = requests.get(url)
	filename = url.split('/')
	new_filename = filename[-1]
	with open(new_filename,"wb") as file:
		file.write(get_responce.content)
		file.close()


url = "https://wallpaperaccess.com/full/187161.jpg"

download(url)