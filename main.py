import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from pathlib import Path


class MyWindow(Gtk.Window):
    notebook = Gtk.Notebook()
    home = str(Path.home())

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.list_view()
        
    def list_view(self):
        self.table = Gtk.Table(n_rows=3, n_columns=3, homogeneous=True)
        self.add(self.table)
        self.listbox = Gtk.ListBox()
        self.add(self.listbox)

        self.listbox_add_items()
        new_window_button = Gtk.Button("Yeni Bağlantı Ekle")
        new_window_button.connect('clicked',self.insert_config_file)
        self.listbox.add(new_window_button)
        self.table.attach(self.listbox,0,1,0,3)
        
        self.add(self.notebook)
        self.table.attach(self.notebook,1,3,0,3)

        self.notebook.show_all()
        self.listbox.show_all()
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label="Merhaba bu ilk sayfa."))
        self.notebook.append_page(self.page1, Gtk.Label(label="Default Page"))

    def context_menu(self):
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("New")
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
        
    def on_click_popup(self, action):   
        ## Yeni sayfa oluştur
        
        self.new_page = Gtk.Box()
        self.new_page.set_border_width(10)
        self.new_page.add(Gtk.Label(label=self.two_d_array[self.labelmenu]))
        self.notebook.append_page(self.new_page, Gtk.Label(label="New Page"))
        self.notebook.show_all()

    
    def open_config_file(self): ## config dosyasındaki itemlar'ı return eden fonksiyon
        y = list()
        with open(self.home + '/.ssh/config') as myFile:
            for num, line in enumerate(myFile, 1):
                if 'Host ' in line:
                    x = line.split()
                    y.append(x[1])
                        
        return y 
    
    def new_item_config(self): ## Yeni eklenen itemi return eden fonksiyon
        y = list()
        with open(self.home + '/.ssh/config') as myFile:
            for num, line in enumerate(myFile, 1):
                if 'Host ' in line:
                    x = line.split()
                    y.append(x[1])
                        
        return y[-1]
    
    def insert_config_file(self,widget): ## Yeni açılan pencere tasarımı
        
        input_window = Gtk.Window()
        input_window.set_title("New Window")
        input_window.set_border_width(10)
        self.table2 = Gtk.Table(n_rows=10, n_columns=0, homogeneous=True)
        input_window.add(self.table2)

        self.host = Gtk.Entry()
        self.host_name = Gtk.Entry()
        self.user = Gtk.Entry()
        self.port = Gtk.Entry()
        self.submit_button = Gtk.Button("Gönder")
  
        self.host.set_placeholder_text("Host")
        self.host_name.set_placeholder_text("HostName")
        self.user.set_placeholder_text("User")
        self.port.set_placeholder_text("Port")

        input_window.add(self.host)
        input_window.add(self.host_name)
        input_window.add(self.user)
        input_window.add(self.port)
        input_window.add(self.submit_button)
        self.submit_button.connect('clicked',self.on_click_submit)

        self.table2.attach(self.host,0,1,0,1)
        self.table2.attach(self.host_name,0,1,2,3)
        self.table2.attach(self.user,0,1,4,5)
        self.table2.attach(self.port,0,1,6,7)
        self.table2.attach(self.submit_button,0,1,8,9)

        input_window.present()
        input_window.show_all()  
        
    def listbox_add_items(self):
        
        self.two_d_array = dict()
        self.hosts = self.open_config_file() # Config dosyasındaki host isimleri
        for i in range(0,len(self.hosts)):
            self.two_d_array[self.hosts[i]] = "dddd" # Host isimlerinin two_d_array dizisine aktarılması
        
        for i in self.two_d_array.keys():
            ## label yerine buton oluşturduk
            buttons = Gtk.Button.new_with_label(i)
            buttons.connect("button-press-event",self.button_clicked)
            self.listbox.add(buttons)
        
        self.listbox.show_all()
    
    def listbox_add_last_item(self,last): ## Son item'ın listbox'a eklenmesi
        self.last_item_button = Gtk.Button.new_with_label(last)
        self.last_item_button.connect("button-press-event",self.button_clicked)
        self.listbox.add(self.last_item_button)

        self.listbox.show_all()
    
    def on_click_submit(self,widget): ## Gönder butonu fonksiyonu
        
        with open(self.home + '/.ssh/config','a') as myFile:
            myFile.write("\nHost {}\n\tHostName {}\n\tUser {}\n\tPort {}\n\n".format(self.host.get_text() ,self.host_name.get_text(),self.user.get_text(),self.port.get_text()))

        last_value = self.new_item_config()
        self.listbox_add_last_item(last_value)    


window = MyWindow()
window.show_all()

Gtk.main()


