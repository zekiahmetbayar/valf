from gi.repository import Gdk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    notebook = Gtk.Notebook()

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.list_view()
        
    def list_view(self):
        self.table = Gtk.Table(n_rows=3, n_columns=3, homogeneous=True)
        listbox = Gtk.ListBox()
        self.add(self.table)
        self.add(listbox)

        self.two_d_array = dict()
        hosts = self.open_config_file() # Config dosyasındaki host isimleri
        for i in range(0,len(hosts)):
            self.two_d_array[hosts[i]] = "new" # Host isimlerinin two_d_array dizisine aktarılması
        
        for i in self.two_d_array.keys():
            ## label yerine buton oluşturduk
            items = Gtk.Button.new_with_label(i)
            items.connect("button-press-event",self.button_clicked)
            listbox.add(items)
        self.table.attach(listbox,0,1,0,3)
        
        self.add(self.notebook)
        self.table.attach(self.notebook,1,3,0,3)

        self.notebook.show_all()
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label="Merhaba bu ilk sayfa."))
        self.notebook.append_page(self.page1, Gtk.Label(label="Default Page"))

    def context_menu(self):
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("New Page")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_click_popup)
        menu.show_all()

        return menu

    ##  Buton sağ click ise context menu açtı
    def button_clicked(self,listbox_widget,event): 
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            menu = self.context_menu()
            ## Tıklanan objenin labelini print ediyor
            print(listbox_widget.get_label())
            self.labelmenu = listbox_widget.get_label()
            menu.popup( None, None, None,None, event.button, event.get_time()) 
            return True

    def on_pop_menu(self, widget, event):
        if event.button == 3:
            widget.popup(None, None, None, None, event.button, event.time)
        
    def on_click_popup(self, action):   
        ## Yeni sayfa oluştur
        
        self.new_page = Gtk.Box()
        self.new_page.set_border_width(10)
        self.new_page.add(Gtk.Label(label=self.two_d_array[self.labelmenu]))

        #header = Gtk.HBox()
        #image = Gtk.Image()
        #image.set_from_stock(Gtk.STOCK_CLOSE,Gtk.ICON_SIZE_MENU)
        #close_button = Gtk.Button()
        #close_button.set_image(image)
        #close_button.set_relief(Gtk.RELIEF_NONE)
        #self.connect(close_button, 'clicked', self.close_cb)
        #header.pack_start(new_page,
        #                  expand=True, fill=True, padding=0)
        #header.pack_end(close_button,
        #                expand=False, fill=False, padding=0)
        #header.show_all()
        

        self.notebook.append_page(self.new_page, Gtk.Label(label="New Page"))
        self.notebook.set_tab_reorderable(self.new_page, True)
        window.connect('delete-event', Gtk.main_quit)
        self.notebook.show_all()
    
    def open_config_file(self):
        y = list()
        with open('/home/zeki/.ssh/config') as myFile:
            for num, line in enumerate(myFile, 1):
                if 'Host ' in line:
                    x = line.split()
                    y.append(x[1])
                        
        return y



        
        
window = MyWindow()
window.show_all()

Gtk.main()