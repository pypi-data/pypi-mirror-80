import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ComboboxField(Gtk.HBox):
    def __init__(self, field, parent, window):
        """
            "id": str,
            "type": str,
            "label": str,
            "items": [
                { id: str | int, name: str }
            ],
            "default": str | int
        """
        
        self.field = field
        self.parent = parent
        self.window = window
        super(ComboboxField, self).__init__()

        # hbox
        self.set_spacing(6)

        default_index = 0

        liststore = Gtk.ListStore(str, str)
        for i in range(len(self.field["items"])):
            item = self.field["items"][i]

            if item["id"] == self.field["default"]:
                default_index = i

            liststore.append([item["id"], item["name"]])

        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(liststore)
        self.combobox.set_active(default_index)

        cellrenderertext = Gtk.CellRendererText()
        self.combobox.pack_start(cellrenderertext, True)
        self.combobox.add_attribute(cellrenderertext, "text", 1)

        self.pack_start(self.combobox, False, True, 0)               

    def pack(self):
        self.parent.pack_start(self, False, True, 0)

    def get_value(self):
        # return str
        tree_iter = self.combobox.get_active_iter()
        if tree_iter is not None:
            item_id = self.combobox.get_model()[tree_iter][:1][0]
            return item_id
        else:
            return ""