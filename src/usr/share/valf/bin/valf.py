#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi
import os
import getpass
from stat import S_ISDIR, S_ISREG
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GLib
gi.require_version('Vte', '2.91')
from gi.repository import Vte

from gi.repository import GObject
from pathlib import Path
from paramiko import SSHClient
from scp import SCPClient
import time
import paramiko
from subprocess import run, PIPE
import glob
from file_transfer import onRowCollapsed,onRowExpanded,populateFileSystemTreeStore,on_tree_selection_changed 
from ssh_file_transfer import onRowCollapsed2,onRowExpanded2,populateFileSystemTreeStore2,on_tree_selection_changed2,ssh_connect
from gi.repository.GdkPixbuf import Pixbuf
import pexpect
import subprocess
import signal

HOME = "HOME"
SHELLS = [ "/bin/bash" ]
DRAG_ACTION = Gdk.DragAction.COPY
ICONSIZE = Gtk.IconSize.MENU
get_icon = lambda name: Gtk.Image.new_from_icon_name(name, ICONSIZE)

TARGETS = [('MY_TREE_MODEL_ROW', Gtk.TargetFlags(2) , 0),
('text/plain', 0, 1),
('TEXT', 0, 2),('STRING', 0, 3),]

class MyWindow(Gtk.Window):

    notebook = Gtk.Notebook()
    home = str(Path.home())
    baglantilar = dict() # Goal 1
    __gsignals__ = {
        "close-tab": (GObject.SignalFlags.RUN_LAST, GObject.TYPE_NONE, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.set_title("VALF")
        self.main()
        self.number_list = [1]
         
    def main(self):
        table = Gtk.Table(n_rows=10, n_columns=30, homogeneous=True) # Main table tanımlanması
        self.add(table)
        self.listbox = Gtk.ListBox() # Bağlantıların listelendiği listbox tanımlanması
        self.listbox_add_items()
        self.set_icon_from_file('/usr/share/icons/valf/icon.png')

        searchentry = Gtk.SearchEntry() # Searchbox tanımlanması
        searchentry.connect("activate",self.on_search_activated)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(5)
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        scrolled_window.add(self.listbox) # Bağlantı listbox'ına scrollview eklenmesi

        new_window_button = Gtk.Button(label ="Yeni Bağlantı")
        new_window_button.connect('clicked',self.add_new_host_window)
        self.toolbar()
        
        table.attach(self.box,0,10,0,1)
        table.attach(new_window_button,5,10,9,10)
        table.attach(scrolled_window,0,10,2,9)
        table.attach(searchentry,0,10,1,2)
        table.attach(self.notebook,10,30,0,10)
        
        self.notebook.show_all()
        self.listbox.show_all()
        searchentry.show_all()

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label = "İstediğiniz bağlantıya sol tıkladığınızda,\nbağlantı detaylarınız burada listelenecek."))
        self.notebook.append_page(self.page1, Gtk.Label(label = "Ana Sayfa"))
    
    ########################## Config Dosyası İşlemleri #####################################

    def read_config(self): # Conf dosyasını gezer, değerleri okur, dictionary'e atar.
        try : 
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
        
        except:
            ssh_path = self.home + '/.ssh'
            os.mkdir(ssh_path)

            files_list = ['/config','/known_hosts','/authorized_keys']
            for i in files_list:

                Path(ssh_path+ i).touch()

    def write_config(self): # RAM'de tutulan dictionary değerlerini dosyaya yazar.
        with open(self.home+'/.ssh/config','w') as f:
            for p_id, p_info in self.baglantilar.items():
                for key in p_info:
                    f.write(key+" "+p_info[key]+"\n")
    
    ########################## Listbox İşlemleri #####################################
                
    def context_menu(self): # Buton sağ tıkında açılan menü 
        menu = Gtk.Menu()

        menu_item_del = Gtk.MenuItem(label = "Bağlantıyı Sil")
        menu.append(menu_item_del)
        menu_item_del.connect("activate",self.on_click_delete)

        menu_item_connect = Gtk.MenuItem(label = "Bağlan")
        menu.append(menu_item_connect)
        menu_item_connect.connect("activate",self.on_click_connect)

        menu_item_scp = Gtk.MenuItem(label = "Scp ile Dosya Gönder")
        menu.append(menu_item_scp)
        menu_item_scp.connect("activate",self.scp_transfer)

        menu_item_scp = Gtk.MenuItem(label = "Tanımlı Sertifikayı Sil")
        menu.append(menu_item_scp)
        menu_item_scp.connect("activate",self.delete_defined_certificate)

        menu.show_all()

        return menu

    def on_click_connect(self,widget): # Sağ tık menüsündeki Connect Host seçeneği ile açılan pencere
        try:
            sshProcess = subprocess.Popen(['ssh', '-T',self.labelmenu],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = sshProcess.communicate(timeout=0.5)

            key_word = b'Linux'

            if key_word in out:
                self.terminal     = Vte.Terminal()
                self.terminal.spawn_sync(
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
                self.new_page.add(self.terminal)
                self.notebook.append_page(self.new_page, self._button_box)

                self.number = self.notebook.page_num(self.new_page)
                self.number_list.append(self.number)
                self.number_list.pop()

                self.notebook.show_all()
                self.notebook.set_current_page(-1)

                com = 'ssh ' + self.labelmenu + '\n'

                self.terminal.feed_child(com.encode("utf-8"))
                time.sleep(0.5) 
            
            else:
                self.enter_password()
                self.connect_button.connect('clicked',self.send_password)
            
        except:
            sshProcess.send_signal(signal.SIGINT)
            self.enter_password()
            self.connect_button.connect('clicked',self.send_password)

    def button_left_click(self,listbox_widget,event): # Buton sol click fonksiyonu
        self.notebooks(listbox_widget.get_label())
        self.notebook.set_current_page(0)
        self.toolbar()

    def button_clicked(self,listbox_widget,event):  # Buton sağ click fonksiyonu
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

    def add_new_host_window(self,event): # Yeni host ekleme penceresi
        self.input_window = Gtk.Window()
        self.input_window.set_title("Yeni Bağlantı Ekle")
        self.input_window.set_border_width(10)
        table2 = Gtk.Table(n_rows=7, n_columns=0, homogeneous=True)
        self.input_window.add(table2)

        self.host = Gtk.Entry()
        self.host_name = Gtk.Entry()
        self.user = Gtk.Entry()
        self.port = Gtk.Entry()
        self.submit_button = Gtk.Button(label ="Gönder")
        self.submit_button.connect('clicked',self.on_click_add_new_host)
  
        self.host.set_placeholder_text("Host")
        self.host_name.set_placeholder_text("HostName")
        self.user.set_placeholder_text("User")

        table2.attach(self.host,0,1,0,1)
        table2.attach(self.host_name,0,1,2,3)
        table2.attach(self.user,0,1,4,5)
        table2.attach(self.submit_button,0,1,6,7)

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
    
    def on_click_add_new_host(self,widget): ## Açılır penceredeki gönder butonu fonksiyonu
        if self.host.get_text() == '':
            self.blank_entry_from_new_host()
        
        elif self.host_name.get_text() == '':
            self.blank_entry_from_new_host()
        
        elif self.user.get_text() == '':
            self.blank_entry_from_new_host()

        elif self.host.get_text() == self.user.get_text():
            self.same_name_from_new_host()

        else:
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
    
    def same_name_from_new_host(self):
        self.same_name_from_new_host_window= Gtk.Window()
        self.same_name_from_new_host_window.set_title("Yeni Bağlantı Ekle")
        self.same_name_from_new_host_window.set_border_width(10)
        table15 = Gtk.Table(n_rows=2, n_columns=3, homogeneous=True)
        self.same_name_from_new_host_window.add(table15)
        self.same_name_from_new_host_window.set_size_request(200,100)

        same_name_from_new_host_label = Gtk.Label(label = 'Host ve User değişkenleri aynı isme sahip olamaz !')
        same_name_from_new_host_button = Gtk.Button(label = 'Tamam')

        table15.attach(same_name_from_new_host_label,0,3,0,1)
        table15.attach(same_name_from_new_host_button,2,3,1,2)

        same_name_from_new_host_button.connect('clicked',self.same_name_hide)

        self.same_name_from_new_host_window.present()
        self.same_name_from_new_host_window.show_all()

    def same_name_hide(self,clicked):
        self.same_name_from_new_host_window.hide()

    def blank_entry_from_new_host(self):
        self.blank_entry_from_new_host_window= Gtk.Window()
        self.blank_entry_from_new_host_window.set_title("Yeni Bağlantı Ekle")
        self.blank_entry_from_new_host_window.set_border_width(10)
        table16 = Gtk.Table(n_rows=2, n_columns=0, homogeneous=True)
        self.blank_entry_from_new_host_window.add(table16)
        self.blank_entry_from_new_host_window.set_size_request(200,100)

        blank_entry_from_new_host_label = Gtk.Label(label = 'Boş değer bırakılamaz !')
        blank_entry_from_new_host_button = Gtk.Button(label = 'Tamam')

        table16.attach(blank_entry_from_new_host_label,0,2,0,1)
        table16.attach(blank_entry_from_new_host_button,1,2,1,2)

        blank_entry_from_new_host_button.connect('clicked',self.blank_entry_hide)

        self.blank_entry_from_new_host_window.present()
        self.blank_entry_from_new_host_window.show_all()
    
    def blank_entry_hide(self,clicked):
        self.blank_entry_from_new_host_window.hide()

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

    ########################## Toolbar Menu #####################################
    
    def ui_info(self):
        self.UI_INFO = """
    <ui>
    <menubar name='MenuBar'>
        <menu action='FileMenu'>
        <menuitem action='FileNew' />
        <menuitem action='FileNewNew' />
        </menu>
    </menubar>
    </ui>
    """      

    def toolbar(self): # Sertifikaların yer aldığı toolbar

        action_group = Gtk.ActionGroup(name="my_actions")
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        self.add_file_menu_actions(action_group)
        menubar = uimanager.get_widget("/MenuBar")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(menubar, False, False, 0)

        eventbox = Gtk.EventBox()
        self.box.pack_start(eventbox, True, True, 0)
        
    def add_file_menu_actions(self, action_group): # Menü itemların tanımlanması ve görevleri
        
        action_filemenu = Gtk.Action(name="FileMenu", label="Sertifikalar")
        action_group.add_action(action_filemenu)

        action_filenewmenu = Gtk.Action(name="FileNew", label = "Sertifikalarım")
        action_group.add_action(action_filenewmenu)
        action_filenewmenu.connect("activate", self.list_certificates)

        action_filenewnewmenu = Gtk.Action(name="FileNewNew", label = "Sertifika Oluştur")
        action_filenewnewmenu.connect("activate", self.create_new_certificate)
        action_group.add_action(action_filenewnewmenu)
    
    def create_ui_manager(self): 
        uimanager = Gtk.UIManager()
        self.ui_info()
        uimanager.add_ui_from_string(self.UI_INFO)
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager           

    ########################## Sertifika İşlemleri #####################################
    
    def read_local_certificates(self): # Var olan sertifikaları okuyan fonksiyon
        self.certificates =  glob.glob(self.home+"/.ssh/*.pub")
    
    def list_certificates(self,event): # Sertifikaların listelendiği fonksiyon
        self.read_local_certificates()

        page = Gtk.ScrolledWindow()
        page.set_border_width(10)
        self.cert_listbox = Gtk.ListBox()
        self.notebook.remove_page(0)
        self.notebook.set_current_page(0)
        self.notebook.prepend_page(page, Gtk.Label(label = "Ana Sayfa"))
        self.toolbar()
        
        for i in self.certificates:
            ## label yerine buton oluşturduk
            buttons = Gtk.Button.new_with_label(i)
            buttons.connect("button-press-event",self.button_right_clicked_cert)
            buttons.connect("button-press-event",self.on_cert_left_clicked)
            self.cert_listbox.add(buttons) 
        
        page.add(self.cert_listbox)
        self.cert_listbox.show_all()
        self.notebook.show_all()
        self.notebook.set_current_page(0)
    
    def context_menu_cert(self): # Sertifika butonuna sağ tıklanınca açılan menü
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem(label = "Sertifikayı Sil")
        menu.append(menu_item)
        menu_item.connect("activate", self.delete_cert)

        menu_item = Gtk.MenuItem(label ="Sertifikayı Gönder")
        menu.append(menu_item)
        menu_item.connect("activate", self.send_cert)
        menu.show_all()

        return menu
    
    def delete_cert(self,action): # Sertifika silme görevi 
        self.read_local_certificates()
        cert_index = self.certificates.index(self.labelmenu_cert)
        self.cert_listbox.remove(self.cert_listbox.get_row_at_index(cert_index))
        self.cert_listbox.show_all()
        priv  = self.labelmenu_cert.rstrip('.pub')
        os.remove(self.labelmenu_cert)   
        os.remove(priv)   

    def send_cert(self,action):
        self.send_cert_window = Gtk.Window()
        self.send_cert_window.set_title("Sertifikayı Gönder")

        self.send_cert_window.set_border_width(10)
        table12 = Gtk.Table(n_rows=2, n_columns=1, homogeneous=True)
        self.send_cert_window.add(table12)

        certificate_combo = Gtk.ComboBoxText()
        certificate_combo.set_entry_text_column(0)
        certificate_combo.connect("changed", self.on_combo_changed)
        for currency in self.baglantilar.keys():
            certificate_combo.append_text(currency)

        send_cert_button = Gtk.Button(label = "Gönder")
        send_cert_button.connect('clicked',self.on_click_send_cert)
        table12.attach(certificate_combo,0,1,0,1)
        table12.attach(send_cert_button,0,1,1,2)

        self.send_cert_window.present()
        self.send_cert_window.show_all()
    
    def on_combo_changed(self, combo):
        self.text = combo.get_active_text()
    
    def on_click_send_cert(self,action):
        self.send_cert_window.hide()
        self.enter_password()
        self.connect_button.connect('clicked',self.send_cert_action)
    
    def send_cert_action(self,event):
        try:
            self.read_local_certificates()
            send_pass = self.connect_password.get_text() + '\n'
            send_cert = 'ssh-copy-id -i ' + self.labelmenu_cert + ' ' + self.text

            child = pexpect.spawn(send_cert,encoding='utf-8')
            child.expect('password:')
            child.sendline(send_pass)
            time.sleep(2)
            self.connect_window.hide()
            self.send_cert_window.hide()
        
        except:
            self.fail_cert()
            self.connect_window.hide()
            self.send_cert_window.hide()
    
    def fail_cert(self):
        self.fail_cert_window = Gtk.Window()
        self.fail_cert_window.set_title("Hata Mesajı")

        self.fail_cert_window.set_border_width(10)
        table14 = Gtk.Table(n_rows=3, n_columns=1, homogeneous=True)
        self.fail_cert_window.add(table14)

        fail_cert_label = Gtk.Label(label = "Sunucu şifrenizi yanlış girmiş olabilirsiniz veya sertifika göndermek istediğiniz sunucuda\nzaten bir sertifikanız kayıtlı olabilir.Devam etmek için önceki sertifikanızı silmeniz\ngerekmektedir.")
        fail_cert_button = Gtk.Button(label = "Tamam")
        fail_cert_button.connect('clicked',self.fail_cert_hide)
        table14.attach(fail_cert_label,0,1,0,2)
        table14.attach(fail_cert_button,0,1,2,3)

        self.fail_cert_window.present()
        self.fail_cert_window.show_all()
    
    def fail_cert_hide(self,clicked):
        self.fail_cert_window.hide()
    
    
    def on_cert_left_clicked(self,listbox_widget,event): # Sertifikalara sol tıklanma görevi
        desc = ""
        cert_path = listbox_widget.get_label().rstrip('\n')
        cert_name = os.path.basename(cert_path)

        with open(cert_path, 'r') as description:
            desc = description.read()
        dialog = Gtk.Dialog(transient_for=self, flags=0,title=cert_name)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dialog.set_default_size(750, 120)
        label = Gtk.Label(label=desc)
        label.set_line_wrap(True)
        label.set_selectable(True)
        scrollableWindow = Gtk.ScrolledWindow()
        scrollableWindow.add(label)
        scrollableWindow.set_min_content_width(750)
        scrollableWindow.set_min_content_height(100)
        content = dialog.get_content_area()
        content.add(scrollableWindow)
        dialog.show_all()

        response = dialog.run()

        dialog.destroy() 

    def button_right_clicked_cert(self,listbox_widget,event): # Sertifikalara sağ tıklandığında  
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            menu = self.context_menu_cert()
            self.labelmenu_cert = listbox_widget.get_label()
            menu.popup( None, None, None,None, event.button, event.get_time()) 
            return True

    def create_new_certificate(self,event):
        self.cert_name_win = Gtk.Window()
        self.cert_name_win.set_title("Yeni Sertifika")

        self.cert_name_win.set_border_width(10)
        table11 = Gtk.Table(n_rows=2, n_columns=1, homogeneous=True)
        self.cert_name_win.add(table11)

        self.cert_name_entry = Gtk.Entry()
        self.cert_pass_entry = Gtk.Entry()
        self.cert_pass_entry.set_visibility(False)
        cert_name_button = Gtk.Button(label = "Gönder")
        cert_name_button.connect("clicked",self.create_certificate)

        self.cert_name_entry.set_placeholder_text("Sertifika Adı (İsteğe Bağlı)")

        table11.attach(self.cert_name_entry,0,1,0,1)
        table11.attach(cert_name_button,0,1,1,2)

        self.cert_name_win.present()
        self.cert_name_win.show_all()

    def create_certificate(self,event): # Sertifika oluşturma görevi
        self.read_local_certificates()
        cert_input = self.home + '/.ssh/' + self.cert_name_entry.get_text() + '\n'

        if self.cert_name_entry.get_text() == '':
            if self.home + '/.ssh/id_rsa.pub' in self.certificates:
                self.write_on_certificate()
                time.sleep(0.5)
            else:
                no_name_cert_input = '\n' + self.cert_pass_entry.get_text() + '\n'
                create_cert = run('ssh-keygen', stdout=PIPE, input=no_name_cert_input, encoding='utf-8')
        else:
            create_cert = run('ssh-keygen', stdout=PIPE, input=cert_input, encoding='utf-8')

        self.list_certificates('clicked')
        self.cert_name_win.hide()

    def write_on_certificate(self): # Eğer default isimde bir sertifika zaten varsa verilecek uyarı penceresi
        self.write_on_certificate_window = Gtk.Window()
        self.write_on_certificate_window.set_title("Üzerine yazılsın mı ? ")
        self.write_on_certificate_window.set_border_width(10)

        table13 = Gtk.Table(n_rows=2, n_columns=2, homogeneous=True)
        self.write_on_certificate_window.add(table13)

        write_on_certificate_label = Gtk.Label( label = "Zaten idrsa.pub isimli bir sertifikanız var. Oluşturacağınız yeni sertifika üzerine yazılacaktır.\n\t\t\t\t\t\t\t\t\tOnaylıyor musunuz ?")
        write_on_certificate_yes_btn = Gtk.Button(label = "Evet")
        write_on_certificate_no_btn = Gtk.Button(label = "Hayır")

        write_on_certificate_yes_btn.connect('clicked',self.on_click_write_on_yes_btn)
        write_on_certificate_no_btn.connect('clicked',self.on_click_write_on_no_btn)

        table13.attach(write_on_certificate_label,0,2,0,1)
        table13.attach(write_on_certificate_yes_btn,0,1,1,2)
        table13.attach(write_on_certificate_no_btn,1,2,1,2)

        self.write_on_certificate_window.present()
        self.write_on_certificate_window.show_all()

    def on_click_write_on_yes_btn(self,clicked): # Üzerine yazılma kabul edildiyse
        no_name_cert_input = '\n' + self.cert_pass_entry.get_text() + '\n'
        create_cert = run('ssh-keygen', stdout=PIPE, input=no_name_cert_input, encoding='utf-8')
        time.sleep(0.5)
        self.write_on_certificate_window.hide()
    
    def on_click_write_on_no_btn(self,clicked): # Üzerine yazılma reddedildiyse
        self.write_on_certificate_window.hide()

    def _close_cb(self, button): # Kapatma butonu görevi.
            self.notebook.remove_page(self.number_list[-1])
    
    def delete_defined_certificate(self,event):
        try:
            command = 'sed -i /' + getpass.getuser() +'/d ~/.ssh/authorized_keys'
            delete_def_cert = run(['ssh','-T',self.labelmenu], stdout=PIPE, input=command, encoding='utf-8',timeout=1)
        
        except subprocess.TimeoutExpired:
            print('Hata ! Bu sunucuya tanımlı bir sertifika yok.')

    ########################## Notebook İşlemleri #####################################
       
    def close_button(self): # Close butonu
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        label1 = Gtk.Label(label=self.labelmenu)

        _close_btn = Gtk.Button()
        _close_btn.get_style_context().add_class("titlebutton")
        _close_btn.get_style_context().add_class("close")

        _close_btn.add(get_icon("window-close-symbolic"))
        _close_btn.connect("clicked", self._close_cb)
        _close_btn.show_all()
        label1.show_all()
        
        self._button_box.pack_start(label1, False, False, 3)
        self._button_box.pack_start(_close_btn, False, False, 3)

    
    def close_button_2(self): # SFTP sayfasındaki close button.
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        label1 = Gtk.Label(label=self.get_host_before)

        _close_btn = Gtk.Button()
        _close_btn.get_style_context().add_class("titlebutton")
        _close_btn.get_style_context().add_class("close")

        _close_btn.add(get_icon("window-close-symbolic"))
        _close_btn.connect("clicked", self._close_cb)
        
        _close_btn.show_all()
        label1.show_all()
        
        self._button_box.pack_start(label1, False, False, 3)
        self._button_box.pack_start(_close_btn, False, False, 3)
    
    def index_host(self,wanted_host):#indeksi istenilen hostun labelname atılmalı String
        self.read_config()
        wanted_host_index=int()
        
        baglanti_key=list(self.baglantilar.keys())
        for i in range(0,len(baglanti_key)):
            if(baglanti_key[i]==wanted_host):
                wanted_host_index=i

    def notebooks(self,labelname): # Attributes sayfası
        self.read_config()
        self.notebook.remove_page(0)
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.notebook.prepend_page(self.page1, Gtk.Label(label = "Ana Sayfa"))
        self.notebook.set_current_page(0),
        self.toolbar()
        self.get_host_before = labelname

        grid = Gtk.Grid()
        self.page1.add(grid)
        self.label_dict={}
        self.entries_dict={}
        grid_count=2
        grid_count_2=2
        header = Gtk.Label( label = labelname+" Nitelikleri")
        grid.attach(header,0,1,1,1)

        for p_id, p_info in self.baglantilar.items():
                for key in p_info:
                    if(p_info['Host']==labelname):
                        labeltemp = "left_label_"+str(key)
                        oldlabel = labeltemp
                        labeltemp = Gtk.Label(label = key) 
                        self.label_dict[oldlabel] = labeltemp

                        grid.attach(labeltemp,0,grid_count,2,1)
                        grid_count += 1

                        temp = "right_entry_"+str(p_info[key])
                        oldname = temp
                        temp = Gtk.Entry()
                        self.entries_dict[oldname] = temp
                        temp.set_text(p_info[key])
                
                        grid.attach(temp,5,grid_count_2,2,1)
                        grid_count_2 += 1

        add_attribute_button = Gtk.Button(label = "Yeni Nitelik Ekle")
        add_attribute_button.connect("clicked",self.add_attribute)

        notebook_change_button = Gtk.Button(label ="Niteliği Değiştir")
        notebook_change_button.connect('clicked',self.on_click_change)

        start_sftp_button = Gtk.Button(label ="SFTP ile Bağlan")
        start_sftp_button.connect("clicked",self.on_click_sftp)

        grid.attach(add_attribute_button,0,19,2,1)   # Add Attribute button
        grid.attach(notebook_change_button,0,20,2,1) # Change butonu 
        grid.attach(start_sftp_button,0,21,2,1)      # Start SFTP Button
          
        self.notebook.show_all()
        self.listbox.show_all()
        
    def on_click_change(self,listbox_widget): # Change attribute butonu görevi
        values_list = list(self.entries_dict.values())
        labels_list = list(self.label_dict.values())
        updated_list=dict()
        for i in range(0,len(values_list)):
            updated_list[labels_list[i].get_text()]=values_list[i].get_text()
            if values_list[i].get_text() == "":
                updated_list.pop(labels_list[i].get_text())

        self.index_host(self.get_host_before)
        self.baglantilar[self.get_host_before]=updated_list
        self.baglantilar[values_list[0].get_text()] = self.baglantilar[self.get_host_before]#index değişimi bakılmalı sona eklenen kendi indexsine eklenmeli normalde
        self.write_config()
        self.notebooks(values_list[0].get_text())
        self.listbox_add_items()
        self.notebook.set_current_page(0)

    def add_attribute(self,widget): # Yeni attribute ekleme penceresi
        self.add_attribute_window = Gtk.Window()
        self.add_attribute_window.set_default_size(10,100)
        self.add_attribute_window.set_title("Nitelik Ekle")
        self.add_attribute_window.set_border_width(10)

        table3 = Gtk.Table(n_rows=3, n_columns=5, homogeneous=True)
        self.add_attribute_window.add(table3)

        self.attribute_name = Gtk.Entry()
        self.attribute_value = Gtk.Entry()
        add_attribute_submit_button = Gtk.Button(label ="Ekle")
  
        self.attribute_name.set_placeholder_text("Nitelik İsmi")
        self.attribute_value.set_placeholder_text("Nitelik Değeri")

        add_attribute_submit_button.connect('clicked',self.on_click_add_attribute)

        table3.attach(self.attribute_name,0,2,0,1)
        table3.attach(self.attribute_value,3,5,0,1)

        table3.attach(add_attribute_submit_button,1,4,2,3)

        self.add_attribute_window.present()
        self.add_attribute_window.show_all()    

    def on_click_add_attribute(self,widget): # Yeni attribute ekleme butonu görevi
        if self.attribute_name.get_text() == '':
            self.blank_entry_from_new_host()
        elif self.attribute_value.get_text() == '':
            self.blank_entry_from_new_host()
        else:
            self.add_attribute_window.hide()
            self.read_config()
            self.baglantilar[self.get_host_before][self.attribute_name.get_text()] = self.attribute_value.get_text()
            self.write_config()
            self.notebooks(self.get_host_before)
            self.notebook.set_current_page(0)
    
    def on_click_sftp(self,widget):
        try:
            control_command = 'grep -F ' + getpass.getuser() +' ~/.ssh/authorized_keys'
            control_auth = run(['ssh','-T',self.get_host_before], stdout=PIPE, input=control_command, encoding='utf-8',timeout=1)
            a = control_auth.stdout
            b = list()
            b = a.split('\n')
            for i in b:
                if getpass.getuser() in i:
                    c = b.index(i)
      
            os.chdir(self.home+'/.ssh')
            os.system('ls -d "$PWD"/* > /tmp/listOfFiles.list')

            with open('/tmp/listOfFiles.list') as y:
                s = list()
                s = y.readlines()

                for i in s:
                    os.system(' ')
                    i = i.rstrip('\n')
                    d = run(['cat',i],stdout=PIPE)
                    if d.stdout.decode('ascii') ==  b[c] + '\n':
                        e = i  
                        break      

            sftpURL   =  self.baglantilar[self.get_host_before]['Hostname']
            sftpUser  =  self.baglantilar[self.get_host_before]['User']
                    #sftpPass  =  self.connect_password.get_text()


            mySSHK   = e
            sshcon   = paramiko.SSHClient()  # will create the object
            sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # no known_hosts error
            sshcon.connect(sftpURL, username=sftpUser, key_filename=mySSHK)

            self.ftp = sshcon.open_sftp()
            self.localpath='/home'
            self.remotepath='/home' 
            self.sftp_file_transfer('clicked')
        except:
            self.enter_password()
            self.connect_button.connect('clicked',self.normal_auth)

            
    def normal_auth(self,clicked):
        try:
            sftpURL   =  self.baglantilar[self.get_host_before]['Hostname']
            sftpUser  =  self.baglantilar[self.get_host_before]['User']
            sftpPass  =  self.connect_password.get_text()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )  

            ssh.connect(sftpURL, username=sftpUser, password=sftpPass )
            self.ftp = ssh.open_sftp()
            self.localpath='/home'
            self.remotepath='/home'   
            self.sftp_file_transfer('clicked') 
            self.connect_window.hide()    

        except paramiko.ssh_exception.AuthenticationException:
            self.sftp_fail() 

    ########################## Parola Penceresi İşlemleri #####################################

    def enter_password(self): # Parola giriş ekranı
        self.connect_window = Gtk.Window()
        self.connect_window.set_title("Parola Giriş Ekranı")
        self.connect_window.set_border_width(10)
        table4 = Gtk.Table(n_rows=3, n_columns=3, homogeneous=False)

        self.connect_password = Gtk.Entry()
        self.connect_button = Gtk.Button(label = "Bağlan")
        connect_label = Gtk.Label(label = "Sunucu parolanızı girin.")

        self.connect_password.set_placeholder_text("Parola")
        self.connect_password.set_visibility(False)

        self.connect_window.add(table4)

        table4.attach(connect_label,0,3,0,1)
        table4.attach(self.connect_password,1,3,1,2)
        table4.attach(self.connect_button,1,3,2,3)

        self.connect_window.present()
        self.connect_window.show_all()

    def wrong_password_win(self): # Şifre yanlış olduğunda gösterilecek pencere
        table5 = Gtk.Table(n_rows=2, n_columns=3, homogeneous=True)
        self.wrong_pass_win = Gtk.Window()
        self.wrong_pass_win.set_title("Hata !")
        self.wrong_pass_win.add(table5)

        wrong_pass_label = Gtk.Label(label = "Hatalı Parola")
        table5.attach(wrong_pass_label,0,3,0,1)

        try_again_button = Gtk.Button(label = "Tekrar Deneyin")
        try_again_button.connect("clicked",self.hide)

        table5.attach(try_again_button,1,2,1,2)
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

                self.c_check()
                time.sleep(0.5)

                self.is_correct()
                self.connect_window.hide()
            
            else:
                self.connect_window.hide()
                self.first_connection()

    ########################## Login Kontrol İşlemleri #####################################

    def first_connection(self): # Makineye ilk kez bağlanılıyorsa
        table8 = Gtk.Table(n_rows=10, n_columns=20, homogeneous=False)
        self.first_connection_window = Gtk.Window()
        self.first_connection_window.set_default_size(300, 90)
        self.first_connection_window.add(table8)
        self.first_connection_window.set_title("Emin misiniz ? ")

        first_connection_yes_btn = Gtk.Button(label = "Devam Et")
        table8.attach(first_connection_yes_btn,1,10,4,8)
        first_connection_yes_btn.connect("clicked",self.yes_button_clicked)
        
        first_connection_no_btn = Gtk.Button(label = "Ayrıl")
        table8.attach(first_connection_no_btn,11,19,4,8)
        first_connection_no_btn.connect("clicked",self.no_button_clicked)

        first_connection_label = Gtk.Label(label = "     Bu sunucuya ilk kez bağlanıyorsunuz. Devam etmek istediğinize emin misiniz ?  (evet/hayır/[fingerprint])?    ")
        table8.attach(first_connection_label,0,20,0,2)

        self.first_connection_window.show_all()   
    
    def yes_button_clicked(self,event): # Sunucuya ilk kez bağlanılması kabul edildiyse
        self.terminal2.feed_child(self.command.encode("utf-8"))
        time.sleep(0.5) 

        answer = 'yes\n'

        self.terminal2.feed_child(answer.encode("utf-8"))
        time.sleep(0.5) 

        self.terminal2.feed_child(self.password.encode("utf-8"))
        time.sleep(2) 

        self.is_correct()
        self.connect_window.hide()
        self.first_connection_window.hide()
    
    def no_button_clicked(self,event): # Sunucuya ilk kez bağlanılması reddedildiyse
        self.first_connection_window.hide()
        self.connect_window.hide()
    
    def c_check(self): # Bağlanılmak istenen sunucunun IP'si başka bir sunucu tarafından alınmış mı kontrolü 
        
        with open('/tmp/control.txt','r') as y:
            string_change = y.read()
            word = "@@@@@@"

            if word in string_change:
                self.connect_window.hide()
                self.host_change()
            
            else:
                pass

    def host_change(self): # Bağlanılmak istenen sunucunun IP'si başka bir sunucu tarafından alınmışsa değişiklik için
                           # Gösterilecek ekran
        table9 = Gtk.Table(n_rows=1, n_columns=3, homogeneous=True)
        self.host_change_window = Gtk.Window()
        self.host_change_window.set_title("Dikkat !")
        
        self.host_change_entry = Gtk.Entry()
        self.host_change_entry.set_placeholder_text("Evet değişiklik yap.")

        host_change_label = Gtk.Label(label = "Bağlanmak istediğiniz sunucu ip'si başka bir sunucu tarafından alınmış olabilir.\nKnown değişimini onaylıyorsanız --  Evet değişiklik yap  -- yazın")
        table9.attach(host_change_label,0,3,0,1)
        table9.attach(self.host_change_entry,1,2,1,2)

        host_change_button = Gtk.Button(label = "Send")
        host_change_button.connect("clicked",self.on_click_host_change)

        table9.attach(host_change_button,1,2,2,3)
        self.host_change_window.show_all()   
        self.notebook.remove_page(-1)
    
    def on_click_host_change(self,event): # Host değişimi onaylandıysa 
        entry = self.host_change_entry.get_text()
        hostname = self.baglantilar[self.labelmenu]['Hostname']
        degistir = "ssh-keygen -R " + hostname +"\n"

        if entry.lower() == "evet değişiklik yap":
            self.terminal2.feed_child(degistir.encode("utf-8"))
            self.host_change_window.hide()
            self.enter_password()
            self.connect_button.connect('clicked',self.send_password)

    def is_correct(self):
        with open('/tmp/control.txt','r') as correct_file:            
            correct_list = list()
            correct_list = correct_file.readlines()
            length = len(correct_list)
            
            if length > 3:
                self.notebook.show_all()
                self.notebook.set_current_page(-1)
            else:
                self.notebook.remove(self.new_page)
                self.wrong_password_win()

    ########################## SCP İşlemleri #####################################
    
    def file_choose(self,event): # File choose dialog
        
        name_list = []
        filechooserdialog = Gtk.FileChooserDialog(title="Göndermek istediğiniz dosyayı seçin.",
             parent=None,
             action=Gtk.FileChooserAction.OPEN)
        filechooserdialog.add_buttons("_Gönder", Gtk.ResponseType.OK)
        filechooserdialog.add_buttons("_Ayrıl", Gtk.ResponseType.CANCEL)
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
        
    def send_file(self,event): # SCP Bağlantısı
        ssh = SSHClient()
        ssh.load_system_host_keys()

        ip_adress = self.baglantilar[self.labelmenu]['Hostname']
        username = self.baglantilar[self.labelmenu]['User']
        password = self.connect_password.get_text()

        try:
            ssh.connect(ip_adress,username=username,password=password)
            self.connect_window.hide()
            self.select_file()
            
        except paramiko.SSHException:
            print("Hatalı giriş bilgileri !")
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
    
    def scp_transfer(self,event): # Ara yönlendirme fonksiyonu


        self.enter_password()
        self.connect_button.connect('clicked',self.send_file)
        
    def select_file(self): # Dosya seçme ara penceresi
        choose_file_winbtn = Gtk.Window()
        choose_file_winbtn.set_title("Dosya Seç")
        choose_file_winbtn.set_default_size(200, 200)
        choose_file_winbtn.set_border_width(20)

        table6 = Gtk.Table(n_rows=1, n_columns=1, homogeneous=True)
        choose_file_winbtn.add(table6)
        
        choose_file_btn_ = Gtk.Button(label ="Dosya Seç")
        choose_file_winbtn.add(choose_file_btn_) 
        choose_file_btn_.connect("clicked",self.file_choose)      

        table6.attach(choose_file_btn_,0,1,0,1)
        choose_file_winbtn.show_all()
        self.connect_window.hide()
    
    ########################## SFTP İşlemleri #####################################
        
    def sftp_file_transfer(self,event):
        if self.notebook.get_current_page() != 0:
            degisken = self.notebook.get_current_page()
            self.notebook.remove_page(degisken)
            
        table7 = Gtk.Table(n_rows=10, n_columns=30, homogeneous=True)
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(table7)
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        
        self.close_button_2()

        self.localTree(self.localpath)
        self.remoteTree(self.remotepath)
        self.toolbar()        
 
        table7.attach(self.scrollView,0,15,1,10)       
        table7.attach(self.scrollView2,16,30,1,10)
        table7.attach(self.local_search,0,15,0,1)
        table7.attach(self.remote_search,16,30,0,1)
        self.notebook.append_page(self.page1, self._button_box)

        self.number = self.notebook.page_num(self.page1)
        self.number_list.append(self.number)
        self.number_list.pop()
        
        self.notebook.show_all()
        self.notebook.set_current_page(-1)
    
    def on_drag_data_get(self, widget, drag_context, data, info, time):
        select = widget.get_selection()
        model, treeiter = select.get_selected()
        if treeiter != None:
            data.set_text(model[treeiter][2],-1)

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        model=widget.get_model()
        drop_info = widget.get_dest_row_at_pos(x, y)
        if drop_info:
            path, position = drop_info
            iter = model.get_iter(path)
            remotepath=model[iter][2]
            localpath = data.get_text()
            localpath_list = []
            localpath_list = localpath.split('/')
            print("Received text: %s" % localpath)
            print("Received text: %s" % remotepath)

            if os.path.isdir(localpath):  
                self.put_dir(localpath,remotepath) 
            elif os.path.isfile(localpath):  
                remotepathfile=remotepath+"/"+localpath_list[-1]
                self.ftp.put(localpath, remotepathfile) 
        

    def put_dir(self, source, target):
        localpath_list = []
        localpath_list = source.split('/')

        self.ftp.mkdir(target+"/"+localpath_list[-1])
        self.ftp.chdir(target+"/"+localpath_list[-1])
        target=target+"/"+localpath_list[-1]
        for dirpath, dirnames, filenames in os.walk(source):
            remote_path = os.path.join(target, dirpath[len(source)+1:])
            try:
                self.ftp.listdir(remote_path)
            except IOError:
                self.ftp.mkdir(remote_path)

            for filename in filenames:
                self.ftp.put(os.path.join(dirpath, filename), os.path.join(remote_path, filename))
    
    def on_drag_data_get_2(self, widget, drag_context, data, info, time):
        select = widget.get_selection()
        model, treeiter = select.get_selected()
        if treeiter != None:
            data.set_text(model[treeiter][2],-1)

    def on_drag_data_received_2(self, widget, drag_context, x, y, data, info, time):
        model=widget.get_model()
        drop_info = widget.get_dest_row_at_pos(x, y)
        if drop_info:
            path, position = drop_info
            iter = model.get_iter(path)
            remotepath=model[iter][2]
            localpath = data.get_text()
            localpath_list = []
            localpath_list = localpath.split('/')
            print("Received text: %s" % localpath)
            print("Received text: %s" % remotepath)
            remotepath=remotepath+"/"+localpath_list[-1]

            fileattr = self.ftp.lstat(localpath)
            if S_ISDIR(fileattr.st_mode):
                self.download_dir(localpath,remotepath)
            if S_ISREG(fileattr.st_mode):
                self.ftp.get(localpath,remotepath)
        

    def download_dir(self,remote_dir, local_dir):
        
        os.path.exists(local_dir) or os.makedirs(local_dir)
        dir_items = self.ftp.listdir_attr(remote_dir) ##
        
        for item in dir_items:

            remote_path = remote_dir + '/' + item.filename         
            local_path = os.path.join(local_dir, item.filename)
            if S_ISDIR(item.st_mode):
                self.download_dir(remote_path, local_path)
            else:
                self.ftp.get(remote_path, local_path)

    def localTree(self,localroot):
        
        fileSystemTreeStore = Gtk.TreeStore(str, Pixbuf, str)
        populateFileSystemTreeStore(fileSystemTreeStore, localroot)
        fileSystemTreeView = Gtk.TreeView(model = fileSystemTreeStore)
        treeViewCol = Gtk.TreeViewColumn("Ana makina")
        
        colCellText = Gtk.CellRendererText()
        colCellImg = Gtk.CellRendererPixbuf()
        treeViewCol.pack_start(colCellImg, False)
        treeViewCol.pack_start(colCellText, True)
        treeViewCol.add_attribute(colCellText, "text", 0)
        treeViewCol.add_attribute(colCellImg, "pixbuf", 1)
        fileSystemTreeView.append_column(treeViewCol)
        fileSystemTreeView.connect("row-expanded", onRowExpanded)
        fileSystemTreeView.connect("row-collapsed", onRowCollapsed)
        fileSystemTreeView.columns_autosize()
    
        fileSystemTreeView.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, TARGETS, DRAG_ACTION)
        fileSystemTreeView.connect("drag-data-get", self.on_drag_data_get)

        fileSystemTreeView.enable_model_drag_dest(TARGETS, DRAG_ACTION)
        fileSystemTreeView.connect("drag-data-received", self.on_drag_data_received_2)

        self.scrollView = Gtk.ScrolledWindow()
        self.scrollView.set_min_content_width(225)
        self.scrollView.add(fileSystemTreeView)

    def remoteTree(self,remoteroot):
        ssh_connect(self.ftp)  
        fileSystemTreeStore2 = Gtk.TreeStore(str, Pixbuf, str)
        populateFileSystemTreeStore2(fileSystemTreeStore2, remoteroot)
        fileSystemTreeView2 = Gtk.TreeView(model = fileSystemTreeStore2)
        treeViewCol2 = Gtk.TreeViewColumn("Bağlanılan makina")
        treeViewCol2.set_min_width(225)
   
        colCellText2 = Gtk.CellRendererText()
        colCellImg2 = Gtk.CellRendererPixbuf()
        treeViewCol2.pack_start(colCellImg2, False)
        treeViewCol2.pack_start(colCellText2, True)
        treeViewCol2.add_attribute(colCellText2, "text", 0)
        treeViewCol2.add_attribute(colCellImg2, "pixbuf", 1)
        fileSystemTreeView2.append_column(treeViewCol2)
        fileSystemTreeView2.connect("row-expanded", onRowExpanded2)
        fileSystemTreeView2.connect("row-collapsed", onRowCollapsed2)
        select2 = fileSystemTreeView2.get_selection()
        select2.connect("changed", on_tree_selection_changed2)
        fileSystemTreeView2.columns_autosize()

        fileSystemTreeView2.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, TARGETS, DRAG_ACTION)
        fileSystemTreeView2.connect("drag-data-get", self.on_drag_data_get_2)

        fileSystemTreeView2.enable_model_drag_dest(TARGETS, DRAG_ACTION)
        fileSystemTreeView2.connect("drag-data-received", self.on_drag_data_received)

        self.scrollView2 = Gtk.ScrolledWindow()
        self.scrollView2.set_min_content_width(225)
        self.scrollView2.add(fileSystemTreeView2)

        self.local_search = Gtk.SearchEntry() # Searchbox tanımlanması
        self.local_search.connect("activate",self.on_local_search_activated)

        self.remote_search = Gtk.SearchEntry() # Searchbox tanımlanması
        self.remote_search.connect("activate",self.on_remote_search_activated)
        
    def on_local_search_activated(self,clicked):
        self.degisken=self.localpath
        try:
            self.localpath=self.local_search.get_text()
            self.sftp_file_transfer('clicked')
        except:
            self.localpath=self.degisken
            self.sftp_file_transfer('clicked')
        
    def on_remote_search_activated(self,clicked):
        self.degiskenrem=self.remotepath
        try:
            self.remotepath=self.remote_search.get_text()
            self.sftp_file_transfer('clicked')
        except:
            self.remotepath=self.degiskenrem
            self.sftp_file_transfer('clicked')
    
    def sftp_fail(self):
        self.auth_except_win = Gtk.Window()
        self.auth_except_win.set_title("Hata mesajı")
        self.auth_except_win.set_default_size(200, 200)
        self.auth_except_win.set_border_width(20)

        self.table10 = Gtk.Table(n_rows=1, n_columns=1, homogeneous=True)
        self.auth_except_win.add(self.table10)
            
        auth_except_label = Gtk.Label(label = "Giriş başarısız. Giriş bilgilerini kontrol edin.")
        self.auth_except_win.add(auth_except_label)       

        self.table10.attach(auth_except_label,0,1,0,1)
        self.auth_except_win.show_all()
        self.connect_window.hide()
    
window = MyWindow()
window.show_all()
Gtk.main()