import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from gi.repository import GObject
from pathlib import Path

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

        new_window_button = Gtk.Button("Add New Host")
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
        two_d_array_index = list(self.two_d_array.keys()).index(self.labelmenu)
        self.listbox.remove(self.listbox.get_row_at_index(two_d_array_index))  
        self.listbox.show_all()
                 
        with open(self.home + '/.ssh/config','r') as f:
            lines = f.readlines()
        
            for line in lines:
                host_index = lines.index("Host " + self.labelmenu+" \n")
            
            for i in range(0,5):
                lines.pop(host_index)
            
            with open(self.home + '/.ssh/config','w') as f2:
                for last_lines in lines:
                    f2.write(last_lines)
        
        self.refresh()
        
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
        self.table2 = Gtk.Table(n_rows=7, n_columns=0, homogeneous=True)
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
        self.table2.attach(self.submit_button,0,1,6,7)

        self.input_window.present()
        self.input_window.show_all()  
        
    def listbox_add_items(self):
        
        self.refresh()
        
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
        self.last_item_button.connect("button-press-event",self.button_left_click)

        self.listbox.add(self.last_item_button)
        self.listbox.show_all()
    
    def on_click_submit(self,widget): ## Açılır penceredeki gönder butonu fonksiyonu
        with open(self.home + '/.ssh/config','a') as myFile:
            myFile.write("Host {} \n\tHostName {} \n\tUser {} \n\tPort {} \n".format(self.host.get_text() ,self.host_name.get_text(),self.user.get_text(),22))
        self.input_window.hide()

        last_value = self.new_item_config()
        self.listbox_add_last_item(last_value)   

        self.refresh()
    
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

    def change_notebook(self,labelname):
        self.refresh()
        self.notebook_change_button = Gtk.Button("Change Configuration")
        self.notebook_change_button.connect('clicked',self.on_click_change)
            
        with open(self.home + '/.ssh/config','r') as f:
            self.notebook.remove_page(0)
            self.page1 = Gtk.Box()
            self.page1.set_border_width(10)
            self.notebook.prepend_page(self.page1, Gtk.Label(labelname+" Attributes"))
            self.numm = self.notebook.page_num(self.page1)
            self.notebook.set_current_page(0)

            grid = Gtk.Grid()
            self.page1.add(grid)

            self.refresh()
            self.lines_list = list()
            self.lines = f.read()
            self.lines_list.append(self.lines.split())
            self.host_index = self.lines_list[0].index(labelname)
            self.get_host_before = labelname

            if labelname in self.lines:
                seek_index = self.lines.index("Host " + labelname)
            
            f.seek(seek_index,0)
            self.array_index = list(self.two_d_array.keys()).index(labelname)

            self.next_word_index = self.array_index + 1    
            if list(self.two_d_array.keys())[self.array_index] == list(self.two_d_array.keys())[-1]:
                self.next_word_index = self.array_index

            self.next_item = list(self.two_d_array.keys())[self.next_word_index]          
            if list(self.two_d_array.keys())[self.array_index] == list(self.two_d_array.keys())[-1]:
                self.next_item = None
            self.dictionary = {} ### Conf file dict -- Attribute : Att -- ###

            for line in f:
                if line != '\n':

                    (key, val) = line.split()
                    self.dictionary[key] = val
                    if val == self.next_item:
                        self.dictionary['Host'] = labelname
                        break
                else:
                    continue   
            self.label_dict = {}
            grid_count = 2
            for i in list(self.dictionary.keys()):
                self.labeltemp = "left_label_"+str(i)
                self.oldlabel = self.labeltemp
                self.labeltemp = Gtk.Label(i) 
                self.label_dict[self.oldlabel] = self.labeltemp
                grid.attach(self.labeltemp,0,grid_count,2,1)
                grid_count += 1

            self.entries_dict = {}
            grid_count_2 = 2
            count = 0
            for j in list(self.dictionary.values()):
                self.temp = "right_entry_"+str(j)
                self.oldname = self.temp
                self.temp = Gtk.Entry()
                self.entries_dict[self.oldname] = self.temp
                self.temp.set_text(j)
                

                grid.attach(self.temp,5,grid_count_2,2,1)
                grid_count_2 += 1
                count += 1
                

            self.add_attribute_button = Gtk.Button("Add New Attribute")
            self.add_attribute_button.connect("clicked",self.add_attribute)
            grid.attach(self.notebook_change_button,0,20,2,1) # Change butonu    
            grid.attach(self.add_attribute_button,0,19,2,1)     
            self.notebook.show_all()
            self.listbox.show_all()
    
    def button_left_click(self,listbox_widget,event):
        self.refresh()
        self.open_config_file()
        self.change_notebook(listbox_widget.get_label())

    def on_click_change(self,listbox_widget):
        self.values_list = list(self.entries_dict.values())
        self.labels_list = list(self.label_dict.values())
        self.values_dict = dict()

        for i in range(0,len(self.values_list)):
            self.values_dict[self.labels_list[i].get_label()] = self.values_list[i].get_text()
        self.list1 = list()
        self.list2 = list()
        self.set1 = self.dictionary.items()
        self.set2 = self.values_dict.items()
        self.set3 = self.set2 - self.set1
        self.set4 = self.set1 - self.set2
        for i in self.set3:
            self.list1.append(i)
        for i in self.set4:
            self.list2.append(i)

        with open(self.home + '/.ssh/config','r') as f:
            lines = f.readlines()

        with open(self.home + '/.ssh/config','w') as f:
            index = lines.index(self.list2[0][0] + " " + self.list2[0][1] + '\n')
            lines.pop(index)
            lines.insert(index,self.list1[0][0] + " " + self.list1[0][1]+ '\n')

            for i in lines:
                f.write(i)
            
                
                

        
        


        
                

        
            

    def add_attribute(self,widget):
        self.add_attribute_window = Gtk.Window()
        self.add_attribute_window.set_title("Add Attribute")
        self.add_attribute_window.set_border_width(10)
        self.table3 = Gtk.Table(n_rows=5, n_columns=30, homogeneous=True)
        self.add_attribute_window.add(self.table3)

        self.attribute_name = Gtk.Entry()
        self.attribute_value = Gtk.Entry()
        self.add_attribute_submit_button = Gtk.Button("Add")
  
        self.attribute_name.set_placeholder_text("Attribute Name")
        self.attribute_value.set_placeholder_text("Value")

        self.add_attribute_window.add(self.attribute_name)
        self.add_attribute_window.add(self.attribute_value)

        self.add_attribute_window.add(self.add_attribute_submit_button)
        self.add_attribute_submit_button.connect('clicked',self.on_click_add_attribute)

        self.table3.attach(self.attribute_name,0,14,0,1)
        self.table3.attach(self.attribute_value,16,30,0,1)

        self.table3.attach(self.add_attribute_submit_button,10,20,2,3)

        self.add_attribute_window.present()
        self.add_attribute_window.show_all() 

    def on_click_add_attribute(self,widget):
        with open(self.home + '/.ssh/config','r') as myFile:
            self.array_index_attribute = list(self.two_d_array.keys()).index(self.get_host_before)

            self.next_word_index_attribute = self.array_index_attribute + 1    
            if list(self.two_d_array.keys())[self.array_index_attribute] == list(self.two_d_array.keys())[-1]:
                self.next_word_index_attribute = self.array_index_attribute

            self.next_item_attribute = list(self.two_d_array.keys())[self.next_word_index_attribute]          
            if list(self.two_d_array.keys())[self.array_index_attribute] == list(self.two_d_array.keys())[-1]:
                self.next_item_attribute = None


            self.lines_att = myFile.read()
            if self.get_host_before in self.lines_att:
                seek_index = self.lines.index("Host " + self.next_item_attribute)

        with open(self.home + '/.ssh/config','r+') as myFile:
            myFile.seek(seek_index,0)
            remainder = myFile.read()                    
            myFile.seek(seek_index,0)  
            myFile.write("\t{} {}".format(self.attribute_name.get_text(),self.attribute_value.get_text())+"\n" + remainder)
            self.add_attribute_window.hide()

        self.change_notebook(self.get_host_before)

        
        

        self.refresh() 

    def refresh(self):
        self.hosts = self.open_config_file() # Config dosyasındaki host isimleri
        self.two_d_array = dict()
        for i in range(0,len(self.hosts)):
            self.two_d_array[self.hosts[i]] = "dddd" 

            
window = MyWindow()
window.show_all()

Gtk.main()