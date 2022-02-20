import chompjs

with open("scriptjson.html") as file:
	data = chompjs.parse_js_object(file.read())