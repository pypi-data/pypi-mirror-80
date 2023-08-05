import gi
import pathlib
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

# import fields
from pygtk_form.fields.textfield import TextField
from pygtk_form.fields.togglefield import ToggleField
from pygtk_form.fields.filechooserfield import FileChooserField
from pygtk_form.fields.colorchooserfield import ColorChooserField
from pygtk_form.fields.comboboxfield import ComboboxField

class Form(Gtk.Window):
    def __init__(self, props, _callback):
        super(Form, self).__init__()

        self.props = props
        self._callback = _callback

        self.connect("destroy", Gtk.main_quit)

        # default size
        if "default_size" in self.props and isinstance(self.props["default_size"], list) and len(self.props["default_size"]) >= 2:
            self.set_default_size(self.props["default_size"][0], self.props["default_size"][1])
        else:
            self.set_default_size(400, 600)

        # resizable
        if "resizable" in self.props and isinstance(self.props["resizable"], bool):
            self.set_resizable(props["resizable"])
        else:
            self.set_resizable(True)

        # Set default style
        cssFile = str(pathlib.Path(__file__).parent.absolute()) + '/res/css/' + self.props["theme"] + '.css'
        style_provider = Gtk.CssProvider()

        if os.path.exists(cssFile):
            self.get_style_context().add_class("pygtk_form_" + self.props["theme"])
            style_provider.load_from_path(cssFile)
        else:
            self.get_style_context().add_class("pygtk_form_default")
            style_provider.load_from_path(str(pathlib.Path(__file__).parent.absolute()) + '/res/css/default.css')

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # root
        vbox_root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # scrollable
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC,
                                    Gtk.PolicyType.AUTOMATIC)
        vbox_root.pack_start(scrolled_window, True, True, 0)

        # fields
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.get_style_context().add_class("container")
        scrolled_window.add(vbox)

        # title
        if "title" in self.props and isinstance(self.props["title"], str):
            self.set_title(self.props["title"])

            title_label = Gtk.Label()
            title_label.set_text(props["title"])
            title_label.get_style_context().add_class("form_title")
            title_label.set_halign(0)
            vbox.pack_start(title_label, False, True, 0)
        
        self.gtkFields = {}
        self.addedFields = {}

        for field in self.props["fields"]:
            # ID verification
            if "id" in field:
                if field["id"] not in self.gtkFields:
                    self.addedFields[field["id"]] = field

                    # label
                    if "label" in field:
                        label = Gtk.Label()
                        label.set_text(field["label"])
                        label.set_halign(1)
                        vbox.pack_start(label, False, True, 0)

                    # TEXT
                    if field["type"].lower() == "text":
                        self.gtkFields[field["id"]] = TextField(field, vbox)
                        self.gtkFields[field["id"]].pack()
                    # TOGGLE
                    elif field["type"].lower() == "toggle":
                        self.gtkFields[field["id"]] = ToggleField(field, vbox)
                        self.gtkFields[field["id"]].pack()
                    # FILE CHOOSER
                    elif field["type"].lower() == "filechooser":
                        self.gtkFields[field["id"]] = FileChooserField(field, vbox, self)
                        self.gtkFields[field["id"]].pack()
                    # COLOR CHOOSER
                    elif field["type"].lower() == "colorchooser":
                        self.gtkFields[field["id"]] = ColorChooserField(field, vbox, self)
                        self.gtkFields[field["id"]].pack()
                    # COMBOBOX
                    elif field["type"].lower() == "combobox":
                        self.gtkFields[field["id"]] = ComboboxField(field, vbox, self)
                        self.gtkFields[field["id"]].pack()
                else:
                    print('Each field must have a unique "id", "' + field["id"] + '" already exists')
            else:
                print('An "id" is required for each field.')

        # validation button

        # hbox
        validation_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        validation_hbox.get_style_context().add_class("validation_container")

        # spacer
        spacer = Gtk.Box()
        validation_hbox.pack_start(spacer, True, True, 0)

        cancel_button = Gtk.Button.new_with_label("CANCEL")
        cancel_button.connect("clicked", self.cancel)
        validation_hbox.pack_start(cancel_button, False, True, 0)

        validation_button = Gtk.Button.new_with_label("VALIDATE")
        validation_button.get_style_context().add_class("accent")
        validation_button.connect("clicked", self.validate)
        validation_hbox.pack_start(validation_button, False, True, 0)    

        vbox_root.pack_start(validation_hbox, False, True, 0)

        self.add(vbox_root)
        self.show_all()

    def validate(self, event):
        toReturn = {}
        for field in self.addedFields:
            toReturn[self.addedFields[field]["id"]] = self.gtkFields[self.addedFields[field]["id"]].get_value()

        self.destroy()

        if self._callback:
            self._callback(toReturn)

    def cancel(self, event):

        self.destroy()

        if self._callback:
            self._callback(False)

def spawn_form(props, _callback):
    Form(props, _callback)
    Gtk.main()

def spawn_test():
    form_props = {
        "title": "Test form",
        "default_size": [400, 600],
        "theme": "none",
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
                "id": "toggle",
                "type": "toggle",
                "label": "Votre titre",
                "value": "choisir ?",
                "default": True
            },
            {
                "id": "profilepicture",
                "type": "filechooser",
                "label": "Choose a profile picture",
                "button": "Choose",
                "filters": [
                    {
                        "name": "Images",
                        "type": ["png", "jpg", "svg", "gif"]
                    }
                ]
            },
            {
                "id": "favouritecolor",
                "type": "colorchooser",
                "label": "Select your favorite color",
                "button": "Select",
                "format": "hex",
                "default": "#00b4c4"
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
                    {"id": "manjaro", "name": "Manjaro"}
                ]
            }
        ]
    }

    def _callback(props):
        print(props)

    def start_with_theme(theme):
        new_props = form_props
        new_props["theme"] = theme
        Form(new_props, _callback)

    start_with_theme("none")
    start_with_theme("windows_light")
    start_with_theme("windows_dark")

    Gtk.main()