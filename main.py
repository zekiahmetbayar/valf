import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)

        grid = Gtk.Grid()
        self.add(grid)

        listbox = Gtk.ListBox()
        self.add(listbox)
        array = ["Bu","Bir","Array"]
        for i in array:
            label = Gtk.Label(i)
            listbox.add(label)
        
        grid.add(listbox)
        #grid.attach(listbox, 10, 20, 20, 10)
 

window = MyWindow()
window.show_all()

Gtk.main()