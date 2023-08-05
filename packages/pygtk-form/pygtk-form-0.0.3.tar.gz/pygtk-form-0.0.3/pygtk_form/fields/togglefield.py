import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ToggleField(Gtk.HBox):
    def __init__(self, field, parent):
        """
            "id": str,
            "type": str,
            "label": str,
            "value": str,
            "default": int
        """
        
        self.field = field
        self.parent = parent
        super(ToggleField, self).__init__()

        # hbox
        self.set_spacing(6)

        self.toggle_button = Gtk.ToggleButton(label=self.field["value"])

        if "default" in self.field and self.field["default"]:
            self.toggle_button.set_active(True)

        self.pack_start(self.toggle_button, False, False, 0)

    def pack(self):
        self.parent.pack_start(self, False, True, 0)

    def get_value(self):
        # return bool
        return self.toggle_button.get_active()