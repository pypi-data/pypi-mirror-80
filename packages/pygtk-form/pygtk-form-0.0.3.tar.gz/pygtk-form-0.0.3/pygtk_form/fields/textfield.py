import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class TextField(Gtk.Entry):
    def __init__(self, field, parent):
        """
            "id": str,
            "type": str,
            "label": str,
            "text": str,
            "max_length": int
        """

        self.field = field
        self.parent = parent
        super(TextField, self).__init__()

        if "text" in self.field:
            self.set_text(self.field["text"])

        if "max_length" in self.field:
            if isinstance(self.field["max_length"], int):
                self.set_max_length(self.field["max_length"])
            else:
                print('The "max_length" property of the "text" field "' + self.field["id"] + '" which must be an int.')

    def pack(self):
        self.parent.pack_start(self, False, True, 0)

    def get_value(self):
        # return str
        return self.get_text()