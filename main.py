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
        listbox = Gtk.ListBox()
        self.add(table)
        self.add(listbox)

        two_d_array = {'Hello' : 'Hi', 'Example' : 'Merhaba'}
        for i in two_d_array.keys():
            items = Gtk.Label(i)
            listbox.add(items)

     

        table.attach(listbox,0,1,0,3)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label="Default Page!"))
        self.notebook.append_page(self.page1, Gtk.Label(label="Page1"))
        

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label(label="A page with an image for a Title."))
        self.notebook.append_page(self.page2, Gtk.Label(label="Page2"))

        table.attach(self.notebook,1,3,0,3)

    def on_button_clicked(listbox_widget): 
        windows= Gtk.Window() 
        windows.show()
 

window = MyWindow()
window.show_all()

Gtk.main()