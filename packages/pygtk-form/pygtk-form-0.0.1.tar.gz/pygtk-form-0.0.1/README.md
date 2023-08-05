
# PYGTK FORM

Create forms very easily for your scripts with GTK !
Just call a function, with the data you want to recover, and a callback!

![pygtk_form examples](images/presentation.png)

Install the module with:

	pip install pygtk_form

## Example
![pygtk_form examples](images/cool_form.png)

And here is the (very simple code) !

	import pygtk_form

	def say_hello(data):
		if data:
			print("Hello " + data["pseudo"] + ", I know you are using " + data["distribution"] + "!")
		else:
			print("Ho no ... You canceled ...")

	pygtk_form.spawn_form({
		"title": "Cool form",
		"default_size": [400, 300],
		"theme": "windows_light",
		"resizable": True,
		"fields": [
			{
				"id": "pseudo",
				"type": "text",
				"text": "",
				"label": "Your username",
				"max_length": 255
			},
			{
				"id": "distribution",
				"type": "combobox",
				"label": "What distribution do you use ?",
				"default": "manjaro",
				"items": [
					{"id": "fedora", "name": "Fedora"},
					{"id": "ubuntu", "name": "Ubuntu"},
					{"id": "debian", "name": "Debian"},
					{"id": "manjaro", "name": "Manjaro"},
					{"id": "arch", "name": "Arch (BTW)"}
				]
			}
		]
	}, say_hello)
