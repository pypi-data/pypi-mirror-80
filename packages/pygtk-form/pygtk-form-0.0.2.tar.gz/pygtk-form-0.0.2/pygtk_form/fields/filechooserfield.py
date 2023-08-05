import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class FileChooserField(Gtk.HBox):
    def __init__(self, field, parent, window):
        """
            "id": str,
            "type": str,
            "label": str,
            "button": str
            "filters": [
                {
                    "name": str,
                    "ext": [str]
                }
            ] 
        """
        
        self.field = field
        self.parent = parent
        self.window = window
        super(FileChooserField, self).__init__()

        # hbox
        self.set_spacing(6)

        # filename entry
        self.filename_entry = Gtk.Entry()
        self.filename_entry.set_text("")
        self.pack_start(self.filename_entry, True, True, 0)

        # open button
        self.open_button = Gtk.Button.new_with_label(field["button"])
        self.open_button.connect("clicked", self.open_dialog)
        self.pack_start(self.open_button, False, True, 0)                      

    def open_dialog(self, event):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a image",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        # filters
        print(self.field)
        for filt in self.field["filters"]:
            n_filter = Gtk.FileFilter()
            n_filter.set_name(filt["name"])
            for ext in filt["type"]:
                n_filter.add_pattern("*."+ext)
            dialog.add_filter(n_filter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename_entry.set_text(dialog.get_filename())

        dialog.destroy()

    def pack(self):
        self.parent.pack_start(self, False, True, 0)

    def get_value(self):
        # return str
        return self.filename_entry.get_text()