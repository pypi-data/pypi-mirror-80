import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ColorChooserField(Gtk.HBox):
    def __init__(self, field, parent, window):
        """
            "id": str,
            "type": str,
            "label": str,
            "button": str,
            "default": str ("hex" || "rgba" || "rgb")
        """
        
        self.field = field
        self.parent = parent
        self.window = window
        super(ColorChooserField, self).__init__()

        # hbox
        self.set_spacing(6)

        self.default_color=Gdk.RGBA()
        if "format" in self.field and self.field["format"] != "hex":
            self.default_color_hex = '#{:02x}{:02x}{:02x}'.format(*self.field["default"])
        else:
            self.default_color_hex = self.field["default"]
        self.default_color.parse(self.default_color_hex)

        self.return_color = self.field["default"]

        self.color_button = Gtk.Button.new_with_label(self.field["button"])
        self.color_button.connect("clicked", self.show_color_dialog)

        self.pack_start(self.color_button, False, True, 0)               

    def color_selected(self, colorchooserdialog):
        color = colorchooserdialog.get_rgba()

        red = int(color.red * 255)
        green = int(color.green * 255)
        blue = int(color.blue * 255)
        alpha = int(color.alpha * 255)

        self.color_button.modify_bg(0, colorchooserdialog.get_rgba().to_color())
        
        if "format" in self.field and self.field["format"] == "rgb":
            self.return_color = "(" + str(red) + "," + str(green) + "," + str(blue) + ")"
        elif "format" in self.field and self.field["format"] == "rgba":
            self.return_color = "(" + str(red) + "," + str(green) + "," + str(blue) + "," + str(alpha) + ")"
        else:
            self.return_color = '#%02x%02x%02x' % (red, green, blue)

    def show_color_dialog(self, event):
        colorchooserdialog = Gtk.ColorChooserDialog()
        colorchooserdialog.set_use_alpha(True)
        colorchooserdialog.set_rgba(self.default_color)

        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            self.color_selected(colorchooserdialog)

        colorchooserdialog.destroy()

    def pack(self):
        self.parent.pack_start(self, False, True, 0)

    def get_value(self):
        # return str
        return self.return_color