

from gi.repository import Gdk

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
            ## label yerine buton oluşturduk
            items = Gtk.Button.new_with_label(i)
            items.connect("button-press-event",self.button_clicked)
            listbox.add(items)


        menu = Gtk.Menu()
        acts = two_d_array.values()
        for i in acts:
            menuitem = Gtk.MenuItem(i)
            menu.append(menuitem)
            menuitem.show()
        
        

        # listbox.connect_object('button-press-event', self.on_pop_menu, menu)
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
    

    def context_menu(self):
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("New")
        menu.append(menu_item)
        menu.show_all()
        return menu

    ##  Buton sağ click ise context menu açtı
    def button_clicked(self,listbox_widget,event): 
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            menu = self.context_menu()
            ## Tıklanan objenin labelini print ediyor
            print(listbox_widget.get_label())
            menu.popup( None, None, None,None, event.button, event.get_time()) 
            return True

    def on_pop_menu(self, widget, event):
        if event.button == 3:
            widget.popup(None, None, None, None, event.button, event.time)
        

    def on_button_clicked(self,listbox_widget): 
        windows= Gtk.Window() 
        windows.show()
 

window = MyWindow()
window.show_all()

Gtk.main()