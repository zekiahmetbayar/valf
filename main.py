import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.list_view()
        

    def list_view(self):
        table = Gtk.Table(n_rows=3, n_columns=3, homogeneous=True)
        self.add(table)
        listbox = Gtk.ListBox()
        self.add(listbox)
        array = ["Bu","Bir","Array","Merhaba"]

        for i in array:
            items = Gtk.Label(i)
            listbox.add(items)

        table.attach(listbox,0,1,0,3)
 

 

window = MyWindow()
window.show_all()

Gtk.main()