import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Vte
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GLib
from gi.repository import GObject
from pathlib import Path
from paramiko import SSHClient
from scp import SCPClient
import time
import paramiko

HOME = "HOME"
SHELLS = [ "/bin/bash" ]

ICONSIZE = Gtk.IconSize.MENU
get_icon = lambda name: Gtk.Image.new_from_icon_name(name, ICONSIZE)

class MyWindow(Gtk.Window):
    notebook = Gtk.Notebook()
    home = str(Path.home())
    baglantilar = dict() # Goal 1
    __gsignals__ = {
        "close-tab": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.set_title("Uzaktan Bağlantı Aracı")
        self.main()
        self.number_list = [1]
         
    def main(self):
        self.table = Gtk.Table(n_rows=10, n_columns=30, homogeneous=True)
        self.add(self.table)

        self.listbox = Gtk.ListBox()
        self.add(self.listbox)
        self.listbox_add_items()

        self.searchentry = Gtk.SearchEntry()
        self.searchentry.connect("activate",self.on_search_activated)
        self.add(self.searchentry)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        
        scrolled_window.add_with_viewport(self.listbox)
        self.add(scrolled_window)

        new_window_button = Gtk.Button("Add New Host")
        new_window_button.connect('clicked',self.add_newhost_window)

        self.table.attach(new_window_button,5,10,9,10)
        self.table.attach(scrolled_window,0,10,1,9)
        self.table.attach(self.searchentry,0,10,0,1)

        self.add(self.notebook)
        self.table.attach(self.notebook,10,30,0,10)

        self.notebook.show_all()
        self.listbox.show_all()
        self.searchentry.show_all()
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label = "İstediğiniz bağlantıya sol tıkladığınızda,\nbağlantı detaylarınız burada listelenecek."))
        self.notebook.append_page(self.page1, Gtk.Label("Ana Sayfa"))
        
    def read_config(self): # Conf dosyasını gezer, değerleri okur, dictionary'e atar.
        self.baglantilar.clear()
        with open(self.home+'/.ssh/config','r') as f:    
            for line in f: # Goal 2 
                if 'Host ' in line: # Goal 3
                    if line != '\n':
                        
                        (key,value) = line.split()
                        hostline = value
                        self.baglantilar[hostline] = dict() # Goal 3
                        self.baglantilar[hostline][key] = value # Goal 5

                    else:
                        continue
                    
                else: # Goal 4
                    if line != '\n':
                        (key,value) = line.split() 
                        self.baglantilar[hostline][key] = value
                
                    else:
                        continue

    def write_config(self): # RAM'de tutulan dictionary değerlerini dosyaya yazar.
        with open(self.home+'/.ssh/config','w') as f:
            for p_id, p_info in self.baglantilar.items():
                for key in p_info:
                    f.write(key+" "+p_info[key]+"\n")

                
    def context_menu(self): # Buton sağ tıkında açılan menü 
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("Create New Notebook")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_click_popup)

        menu_item_del = Gtk.MenuItem("Delete Host Configuration")
        menu.append(menu_item_del)
        menu_item_del.connect("activate",self.on_click_delete)

        menu_item_connect = Gtk.MenuItem("Connect Host")
        menu.append(menu_item_connect)
        menu_item_connect.connect("activate",self.on_click_connect)

        menu_item_scp = Gtk.MenuItem("Send File (Scp)")
        menu.append(menu_item_scp)
        menu_item_scp.connect("activate",self.scp_transfer)

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
                        
    def on_click_popup(self, action): ## Yeni sayfa oluştur
        
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
        baglantilar_index = list(self.baglantilar.keys()).index(self.labelmenu)
        self.listbox.remove(self.listbox.get_row_at_index(baglantilar_index))  
        self.listbox.show_all()

        self.baglantilar.pop(self.labelmenu)
        self.write_config()               

    def add_newhost_window(self,widget): ## Yeni açılan pencere
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
        self.submit_button.connect('clicked',self.on_click_add_newhost)

        self.table2.attach(self.host,0,1,0,1)
        self.table2.attach(self.host_name,0,1,2,3)
        self.table2.attach(self.user,0,1,4,5)
        self.table2.attach(self.submit_button,0,1,6,7)

        self.input_window.present()
        self.input_window.show_all()  
        
    def listbox_add_items(self): # Listbox'a host isimlerini ekleyen fonksiyon
        self.baglantilar.clear()
        self.read_config()
        keys = self.baglantilar.keys()
        for row in self.listbox.get_children():
            self.listbox.remove(row)
        for i in keys:
            ## label yerine buton oluşturduk
            buttons = Gtk.Button.new_with_label(i)
            buttons.connect("button-press-event",self.button_clicked)
            buttons.connect("button-press-event",self.button_left_click)
            self.listbox.add(buttons) 
        self.listbox.show_all()
    
    def on_click_add_newhost(self,widget): ## Açılır penceredeki gönder butonu fonksiyonu
        self.read_config()
        new_host = self.host.get_text()
        new_hostname = self.host_name.get_text()
        new_user = self.user.get_text()
        default_port = '22'

        self.baglantilar[new_host] = {'Host' : new_host, 'Hostname' : new_hostname , 'User' : new_user, 'Port' : default_port}
        self.write_config()

        self.listbox_add_items()
        self.listbox.show_all()
        self.input_window.hide()

    def _close_cb(self, button): # Kapatma butonu görevi.
        self.notebook.remove_page(self.number_list[-1])
        self.notebook.show_all()
       
    def close_button(self): # Close butonu
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
    
    def close_button_2(self):
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        self.label1 = Gtk.Label(label=self.get_host_before)

        self._close_btn = Gtk.Button()
        self._close_btn.get_style_context().add_class("titlebutton")
        self._close_btn.get_style_context().add_class("close")

        self._close_btn.add(get_icon("window-close-symbolic"))
        self._close_btn.connect("clicked", self._close_cb)
        
        self._close_btn.show_all()
        self.label1.show_all()
        
        self._button_box.pack_start(self.label1, False, False, 3)
        self._button_box.pack_start(self._close_btn, False, False, 3)
    
    def index_host(self,wanted_host):#indeksi istenilen hostun labelname atılmalı String
        self.read_config()
        self.wanted_host_index=int()
        
        baglanti_key=list(self.baglantilar.keys())
        for i in range(0,len(baglanti_key)):
            if(baglanti_key[i]==wanted_host):
                self.wanted_host_index=i

    def notebooks(self,labelname): # Attributes sayfası
        self.read_config()

        self.notebook.remove_page(0)
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.notebook.prepend_page(self.page1, Gtk.Label("Ana Sayfa"))
        self.notebook.set_current_page(0)
        self.get_host_before = labelname

        grid = Gtk.Grid()
        self.page1.add(grid)
        self.label_dict={}
        self.entries_dict={}
        grid_count=2
        grid_count_2=2
        self.header = Gtk.Label(labelname+" Attributes")
        grid.attach(self.header,1,1,1,1)

        for p_id, p_info in self.baglantilar.items():
                for key in p_info:
                    if(p_info['Host']==labelname):
                        self.labeltemp = "left_label_"+str(key)
                        self.oldlabel = self.labeltemp
                        self.labeltemp = Gtk.Label(key) 
                        self.label_dict[self.oldlabel] = self.labeltemp

                        grid.attach(self.labeltemp,1,grid_count,2,1)
                        grid_count += 1

                        self.temp = "right_entry_"+str(p_info[key])
                        self.oldname = self.temp
                        self.temp = Gtk.Entry()
                        self.entries_dict[self.oldname] = self.temp
                        self.temp.set_text(p_info[key])
                
                        grid.attach(self.temp,5,grid_count_2,2,1)
                        grid_count_2 += 1

        self.add_attribute_button = Gtk.Button("Add New Attribute")
        self.add_attribute_button.connect("clicked",self.add_attribute)

        self.notebook_change_button = Gtk.Button("Change Configuration")
        self.notebook_change_button.connect('clicked',self.on_click_change)

        self.start_sftp_button = Gtk.Button("Start File Transfer")
        self.start_sftp_button.connect("clicked",self.sftp_file_transfer)

        grid.attach(self.add_attribute_button,0,19,2,1)   # Add Attribute button
        grid.attach(self.notebook_change_button,0,20,2,1) # Change butonu 
        grid.attach(self.start_sftp_button,0,21,2,1)      # Start SFTP Button
          
        self.notebook.show_all()
        self.listbox.show_all()
    
    def button_left_click(self,listbox_widget,event): # Buton sol click fonksiyonu
        self.notebooks(listbox_widget.get_label())
        self.notebook.set_current_page(0)

    def on_click_change(self,listbox_widget): # Change attribute butonu görevi
        self.values_list = list(self.entries_dict.values())
        self.labels_list = list(self.label_dict.values())
        self.updated_list=dict()
        for i in range(0,len(self.values_list)):
            self.updated_list[self.labels_list[i].get_text()]=self.values_list[i].get_text()
            if self.values_list[i].get_text() == "":
                self.updated_list.pop(self.labels_list[i].get_text())

        self.index_host(self.get_host_before)
        self.baglantilar[self.get_host_before]=self.updated_list
        self.baglantilar[self.values_list[0].get_text()] = self.baglantilar[self.get_host_before]#index değişimi bakılmalı sona eklenen kendi indexsine eklenmeli normalde
        self.write_config()
        self.notebooks(self.values_list[0].get_text())
        self.listbox_add_items()
        self.notebook.set_current_page(0)

    def add_attribute(self,widget): # Yeni attribute penceresi
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

        self.notebook.set_current_page(0)

    def on_click_add_attribute(self,widget): # Yeni attribute ekleme butonu görevi
        self.add_attribute_window.hide()
        self.read_config()
        self.baglantilar[self.get_host_before][self.attribute_name.get_text()] = self.attribute_value.get_text()
        self.write_config()
        self.notebooks(self.get_host_before)
        self.notebook.set_current_page(0)

    def enter_password(self):
        self.connect_window = Gtk.Window()
        self.connect_window.set_title("Connect")
        self.connect_window.set_border_width(10)
        self.table4 = Gtk.Table(n_rows=2, n_columns=1, homogeneous=True)
        self.connect_window.add(self.table4)

        self.connect_password = Gtk.Entry()
        self.connect_button = Gtk.Button("Connect")

        self.connect_password.set_placeholder_text("password")
        self.connect_password.set_visibility(False)
        self.connect_window.add(self.connect_password)

        self.connect_window.add(self.connect_button)
        self.table4.attach(self.connect_password,0,1,0,1)
        self.table4.attach(self.connect_button,0,1,1,2)

        self.connect_window.present()
        self.connect_window.show_all()
        
    def on_click_connect(self,widget): # Sağ tık menüsündeki Connect Host seçeneği ile açılan pencere
        self.enter_password()
        self.connect_button.connect('clicked',self.send_password)

    def wrong_password_win(self): # Şifre yanlış olduğunda gösterilecek pencere
        self.wrong_pass_win = Gtk.Window()
        self.wrong_pass_win.set_title("Wrong")
        
        self.wrong_pass_label = Gtk.Label("Wrong pass ! Try Again.")
        self.table5 = Gtk.Table(n_rows=3, n_columns=3, homogeneous=True)
        self.wrong_pass_win.add(self.table5)

        self.table5.attach(self.wrong_pass_label,1,2,1,2)

        try_again_button = Gtk.Button("Try Again")
        try_again_button.connect("clicked",self.hide)

        self.table5.attach(try_again_button,1,2,2,3)
        self.wrong_pass_win.show_all()
    
    def hide(self,event):
        self.wrong_pass_win.hide()

    def send_password(self,event): # İlgili makineye login işlemi
        self.terminal2     = Vte.Terminal()
        self.terminal2.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ[HOME],
            SHELLS,
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,)

        self.new_page = Gtk.Box()
        self.new_page.set_border_width(10)

        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")

        self.close_button()
        self.new_page.add(self.terminal2)
        self.notebook.append_page(self.new_page, self._button_box)

        self.number = self.notebook.page_num(self.new_page)
        self.number_list.append(self.number)
        self.number_list.pop()

        self.aranan = self.baglantilar[self.labelmenu]['Hostname']
        
        self.fp_check = "ssh-keygen -H -F " + self.aranan + " 2>&1 | tee /tmp/control.txt\n"
        self.command = "ssh " + self.labelmenu + " 2>&1 | tee /tmp/control.txt\n"
        self.password = self.connect_password.get_text() + "\n" 

        self.terminal2.feed_child(self.fp_check.encode("utf-8"))
        time.sleep(0.5)
        with open('/tmp/control.txt','r') as t:
            t_list = list()
            t_list = t.readlines()
            length = len(t_list)

            if length > 0:
                self.terminal2.feed_child(self.command.encode("utf-8"))
                time.sleep(0.5) 

                self.terminal2.feed_child(self.password.encode("utf-8"))
                time.sleep(2) 

                self.is_correct()

                self.connect_window.hide()
            
            else:
                self.connect_window.hide()
                self.yes_no()

    def yes_no(self):
        self.yes_or_no_window = Gtk.Window()
        self.yes_or_no_window.set_title("yes or no")
        
        self.yes_or_no_entry = Gtk.Entry()
        self.table8 = Gtk.Table(n_rows=1, n_columns=3, homogeneous=True)
        self.yes_or_no_window.add(self.table8)

        self.table8.attach(self.yes_or_no_entry,1,2,1,2)

        yes_or_no_button = Gtk.Button("Send")
        yes_or_no_button.connect("clicked",self.yes_or_no)

        self.table8.attach(yes_or_no_button,1,2,2,3)
        self.yes_or_no_window.show_all()   
    
    def yes_or_no(self,event):
        self.ans = self.yes_or_no_entry.get_text()
        if self.ans == 'yes':
            self.terminal2.feed_child(self.command.encode("utf-8"))
            time.sleep(0.5) 

            self.answer = 'yes\n'

            self.terminal2.feed_child(self.answer.encode("utf-8"))
            time.sleep(0.5) 

            self.terminal2.feed_child(self.password.encode("utf-8"))
            time.sleep(2) 

            self.is_correct()

            self.connect_window.hide()

            self.yes_or_no_window.hide()
        
        else:
            self.connect_window.hide()
            self.yes_or_no_window.hide()

        

    def is_correct(self):
        with open('/tmp/control.txt','r') as correct_file:            
            correct_list = list()
            correct_list = correct_file.readlines()
            length = len(correct_list)
            
            if length > 3:
                
                self.directory = "cd .ssh 2>&1 | tee /tmp/control.txt\n"
                self.terminal2.feed_child(self.directory.encode("utf-8"))
                time.sleep(0.5)

                with open('/tmp/control.txt','r') as correct_file_:

                    correct_list_ = list()
                    string_file= correct_file_.read()
                    correct_list_ = string_file.split()
                    word = "-bash:"
                    self.notebook.set_current_page(-1)

                    if word in correct_list_:
                        self.create = "mkdir .ssh\n"+"touch .ssh/config\n"+ "touch .ssh/known_hosts\n"
                        self.terminal2.feed_child(self.create.encode("utf-8"))
                        time.sleep(0.5)
                        self.notebook.set_current_page(-1)
                        self.notebook.show_all()

                    else:
                        self.notebook.set_current_page(-1)
                        self.notebook.show_all()
                    
                    self.notebook.set_current_page(-1)
                    self.notebook.show_all()
                
            else:
                self.notebook.remove(self.new_page)
                self.wrong_password_win()
    
    def file_choose(self,event):
        name_list = []
        filechooserdialog = Gtk.FileChooserDialog(title="Select the file to send.",
             parent=None,
             action=Gtk.FileChooserAction.OPEN)
        filechooserdialog.add_buttons("_Open", Gtk.ResponseType.OK)
        filechooserdialog.add_buttons("_Close", Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)

        response = filechooserdialog.run()

        if response == Gtk.ResponseType.OK:
            print("File selected: %s" % filechooserdialog.get_filename())
            self.send_file_path = filechooserdialog.get_filename()
            name_list = self.send_file_path.split('/')
            self.file_name = name_list[-1]
        
        if response == Gtk.ResponseType.CANCEL:
            filechooserdialog.destroy()

        self.transfer()

        filechooserdialog.destroy()
        self.connect_window.hide()
        
    
    def send_file(self,event):
        ssh = SSHClient()
        ssh.load_system_host_keys()

        ip_adress = self.baglantilar[self.labelmenu]['Hostname']
        username = self.baglantilar[self.labelmenu]['User']
        password = self.connect_password.get_text()

        try:
            ssh.connect(ip_adress,username=username,password=password)
            self.connect_window.hide()
            self.choose_file_btn2()
            
        except paramiko.SSHException:
            print("Hata ! ")
            self.connect_window.hide()
            self.scp_transfer("clicked")
    
    def transfer(self):
        ssh = SSHClient()
        ssh.load_system_host_keys()

        ip_adress = self.baglantilar[self.labelmenu]['Hostname']
        username = self.baglantilar[self.labelmenu]['User']
        password = self.connect_password.get_text()

        ssh.connect(ip_adress,username=username,password=password)
        
        scp = SCPClient(ssh.get_transport())
        scp.put(self.send_file_path, self.file_name)

        scp.close()   
    
    def scp_transfer(self,event):
        self.enter_password()
        self.connect_button.connect('clicked',self.send_file)
        
    def choose_file_btn2(self):
        self.choose_file_winbtn = Gtk.Window()
        self.choose_file_winbtn.set_title("Choose File")
        self.choose_file_winbtn.set_default_size(200, 200)
        self.choose_file_winbtn.set_border_width(20)

        self.table6 = Gtk.Table(n_rows=1, n_columns=1, homogeneous=True)
        self.choose_file_winbtn.add(self.table6)
        
        choose_file_btn_ = Gtk.Button("Choose File")
        self.choose_file_winbtn.add(choose_file_btn_) 
        choose_file_btn_.connect("clicked",self.file_choose)      

        self.table6.attach(choose_file_btn_,0,1,0,1)
        self.choose_file_winbtn.show_all()
        self.connect_window.hide()
    
    def on_search_activated(self,searchentry):
        self.baglantilar.clear()
        self.read_config()
        search_text = searchentry.get_text()
        keys = self.baglantilar.keys()
        for row in self.listbox.get_children():
            self.listbox.remove(row)
        for i in keys:

            if search_text in i:
                deneme_button=Gtk.Button.new_with_label(i)
                deneme_button.connect("button-press-event",self.button_clicked)
                deneme_button.connect("button-press-event",self.button_left_click)
                self.listbox.add(deneme_button)
                
                self.listbox.show_all()
        
    def sftp_file_transfer(self,event):
        self.new_page = Gtk.Box()
        self.new_page.set_border_width(10)
        self.table7 = Gtk.Table(n_rows=1, n_columns=3, homogeneous=True)

        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")

        self.close_button_2()
        self.deneme_tree()
        self.table7.attach(self.view,0,1,0,1)
        self.table7.attach(self.view2,2,3,0,1)
        self.new_page.add(self.table7)
        
        self.notebook.append_page(self.new_page, self._button_box)

        self.number = self.notebook.page_num(self.new_page)
        self.number_list.append(self.number)
        self.number_list.pop()
        self.notebook.show_all()
        self.notebook.set_current_page(-1)
    
    def deneme_tree(self):
        books = [["/home", ["/Desktop",None], ["/Documents",None],["/Pictures",True]],
        
         ["/etc", ["/acpi",True], ["/cron.d",True], ["/ssh",True]],

         ["/tmp", ["is_correct.txt",True]]]

        self.store = Gtk.TreeStore(str, bool)

        for i in range(len(books)):
            piter = self.store.append(None, [books[i][0], False])
            j = 1
            while j < len(books[i]):
                self.store.append(piter, books[i][j])
                j += 1

        self.view = Gtk.TreeView()
        self.view.set_model(self.store)
        renderer_books = Gtk.CellRendererText()
        column_books = Gtk.TreeViewColumn("File System", renderer_books, text=0)
        self.view.append_column(column_books)
        self.add(self.view)

        self.view2 = Gtk.TreeView()
        self.view2.set_model(self.store)
        renderer_books = Gtk.CellRendererText()
        column_books = Gtk.TreeViewColumn("File System", renderer_books, text=0)
        self.view2.append_column(column_books)
        self.add(self.view2)

        
window = MyWindow()
window.show_all()
Gtk.main()