import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from gi.repository import GObject
from pathlib import Path
import re

ICONSIZE = Gtk.IconSize.MENU
get_icon = lambda name: Gtk.Image.new_from_icon_name(name, ICONSIZE)

class MyWindow(Gtk.Window):
    notebook = Gtk.Notebook()
    home = str(Path.home())

    __gsignals__ = {
        "close-tab": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.list_view()
        self.number_list = [1]
        
        
    def list_view(self):

        self.table = Gtk.Table(n_rows=10, n_columns=30, homogeneous=True)
        self.add(self.table)
        self.listbox = Gtk.ListBox()
        self.add(self.listbox)

        self.listbox_add_items()

        new_window_button = Gtk.Button("Yeni Bağlantı Ekle")
        new_window_button.connect('clicked',self.insert_config_file)
        self.table.attach(new_window_button,5,10,9,10)

        self.table.attach(self.listbox,0,10,0,9)

        self.add(self.notebook)
        self.table.attach(self.notebook,10,30,0,10)

        self.notebook.show_all()
        self.listbox.show_all()
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label = "Host Attributes : "))
        self.notebook.append_page(self.page1, Gtk.Label("İlk Sayfa"))

    def context_menu(self):
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("Create New Notebook")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_click_popup)

        menu_item_del = Gtk.MenuItem("Delete Host Configuration")
        menu.append(menu_item_del)
        menu_item_del.connect("activate",self.on_click_delete)

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
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        self.close_button()
        self.new_page.add(Gtk.Label(label=self.labelmenu))
        self.notebook.append_page(self.new_page, self._button_box)
        self.number = self.notebook.page_num(self.new_page)
        self.number_list.append(self.number)
        self.number_list.pop()
        self.notebook.show_all()
    
    def on_click_delete(self,action): # # Seçilen bağlantıyı silme fonksiyonu        
        with open(self.home + '/.ssh/config','r') as f:
            lines = f.readlines()
        
            for line in lines:
                host_index = lines.index("Host " + self.labelmenu+"\n")
            
            for i in range(0,5):
                lines.pop(host_index)
            
            with open(self.home + '/.ssh/config','w') as f2:
                for last_lines in lines:
                    f2.write(last_lines)
        self.listbox.show_all() 
        
    def open_config_file(self): ## config dosyasındaki itemlar'ı return eden fonksiyon
        y = list()
        with open(self.home + '/.ssh/config') as myFile:
            for num, line in enumerate(myFile, 1):
                if 'Host ' in line:
                    x = line.split()
                    y.append(x[1])
                        
        return y 
    
    def new_item_config(self): ## Yeni eklenen itemı return eden fonksiyon
        y = list()
        with open(self.home + '/.ssh/config') as myFile:
            for num, line in enumerate(myFile, 1):
                if 'Host ' in line:
                    x = line.split()
                    y.append(x[1])
                        
        return y[-1]
    
    def insert_config_file(self,widget): ## Yeni açılan pencere

        self.input_window = Gtk.Window()
        self.input_window.set_title("New Window")
        self.input_window.set_border_width(10)
        self.table2 = Gtk.Table(n_rows=10, n_columns=0, homogeneous=True)
        self.input_window.add(self.table2)

        self.host = Gtk.Entry()
        self.host_name = Gtk.Entry()
        self.user = Gtk.Entry()
        self.port = Gtk.Entry()
        self.submit_button = Gtk.Button("Gönder")
  
        self.host.set_placeholder_text("Host")
        self.host_name.set_placeholder_text("HostName")
        self.user.set_placeholder_text("User")

        self.input_window.add(self.host)
        self.input_window.add(self.host_name)
        self.input_window.add(self.user)
        self.input_window.add(self.port)
        self.input_window.add(self.submit_button)
        self.submit_button.connect('clicked',self.on_click_submit)

        self.table2.attach(self.host,0,1,0,1)
        self.table2.attach(self.host_name,0,1,2,3)
        self.table2.attach(self.user,0,1,4,5)

        self.table2.attach(self.submit_button,0,1,8,9)

        self.input_window.present()
        self.input_window.show_all()  
        
    def listbox_add_items(self):
        
        self.two_d_array = dict()
        self.hosts = self.open_config_file() # Config dosyasındaki host isimleri
        for i in range(0,len(self.hosts)):
            self.two_d_array[self.hosts[i]] = "dddd" # Host isimlerinin two_d_array dizisine aktarılması
        
        for i in self.two_d_array.keys():
            ## label yerine buton oluşturduk
            buttons = Gtk.Button.new_with_label(i)
            buttons.connect("button-press-event",self.button_clicked)
            buttons.connect("button-press-event",self.button_left_click)
            self.listbox.add(buttons)
        
        self.listbox.show_all()
    
    def listbox_add_last_item(self,last): ## Son item'ın listbox'a eklenmesi
        self.last_item_button = Gtk.Button.new_with_label(last)
        self.last_item_button.connect("button-press-event",self.button_clicked)
        self.listbox.add(self.last_item_button)

        self.listbox.show_all()
    
    def on_click_submit(self,widget): ## Açılır penceredeki gönder butonu fonksiyonu
        
        with open(self.home + '/.ssh/config','a') as myFile:
            myFile.write("\nHost {}\n\tHostName {}\n\tUser {}\n\tPort {}\n\n".format(self.host.get_text() ,self.host_name.get_text(),self.user.get_text(),22))

        last_value = self.new_item_config()
        self.listbox_add_last_item(last_value)    
    
    def _close_cb(self, button): # Kapatma butonu görevi.
        self.notebook.remove_page(self.number_list[-1])
        self.notebook.show_all()
       
    def close_button(self):
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        self.label1 = Gtk.Label(label=self.labelmenu)
        self._close_btn = Gtk.Button()
        self._close_btn.get_style_context().add_class("titlebutton")
        self._close_btn.get_style_context().add_class("close")
        self._close_btn.add(get_icon("window-close-symbolic"))
        self._close_btn.connect("clicked", self._close_cb)
        self._close_btn.show_all()
        self.label1.show_all()
        self._button_box.pack_start(self.label1, False, False, 3)
        self._button_box.pack_start(self._close_btn, False, False, 3)
    
        
    def button_left_click(self,listbox_widget,event):
            
            with open('/home/zeki/.ssh/config','r') as f:
                self.notebook.remove_page(0)
                self.page1 = Gtk.Box()
                self.page1.set_border_width(10)
                self.notebook.prepend_page(self.page1, Gtk.Label(listbox_widget.get_label()+" Attributes"))
                self.notebook.set_current_page(0)
                
                self.lines = f.readlines()
                for line in self.lines:
                    self.host_index = self.lines.index("Host "+listbox_widget.get_label()+"\n")

                self.host_attributes= list()
                for i in range(0,5):
                    count = 0
                    self.host_attributes.append(self.lines.pop(self.host_index+count))
                    count += 1
                
                self.host_attributes_label = ""
                for z in self.host_attributes:
                    self.host_attributes_label += z

                self.page1.add(Gtk.Label(label = self.host_attributes_label))
                #self.page1.add(Gtk.Label(label=self.host_attributes_label))
                self.notebook.show_all()
                self.listbox.show_all()

                

    

    
window = MyWindow()
window.show_all()

Gtk.main()


