import asyncio
import qrcode
import random
import requests
import json
import socket
import os
import subprocess
import sys
import hashlib


qrkilitpopover = None
qrkilitimage = None
qrkilittext = None
qrkilitfile ="/tmp/qrekilit.png"
qrkilitinput= None
random_label_text=""
_last_random_label_text=""
_last_random_label_duyuru=""
random_label_duyuru=""
result_pass_str=""
kurumkodinput=None
qrkilitduyuru_id=None
qrkilitduyuru_type=None
qrkilitduyuru_title=None
qrkilitduyuru_content=None
qrkilitduyuru_date=None
#----------------------------------------------------------------------------------------------
def runid(cmd):
  try:
    return subprocess.run(cmd, shell=True, capture_output=True, check=True, encoding="utf-8") \
                     .stdout \
                     .strip()
  except:
    return None

def guid():
  if sys.platform == 'darwin':
    return runid(
      "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'",
    )

  if sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'msys':
    return run('wmic csproduct get uuid').split('\n')[2] \
                                         .strip()

  if sys.platform.startswith('linux'):
    return runid('cat /var/lib/dbus/machine-id') or \
           runid('cat /etc/machine-id')

  if sys.platform.startswith('openbsd') or sys.platform.startswith('freebsd'):
    return runid('cat /etc/hostid') or \
           runid('kenv -q smbios.system.uuid')
#----------------------------------------------------------------------------------------------

def _qrkilitqrkod_button_event(widget=None):
    global random_label_text
    random_label_text=_("Loading...")
    #loginwindow.o("ui_popover_network").popup()
    os.system("rm /tmp/qrekilit.png")
    qrkilitpopover.popup()
    qrkilitqrcode_control_event()
    #update_popover_qrkilit_duyuru()
    


def update_popover_qrkilit_text():
    global _last_random_label_text
    global result_pass_str
    global kurumkodinput
    global qrkilitduyuru_content
    sid=str(guid())
    systemid=sid[:10]
    sha256 = hashlib.sha256()
    sha256.update(systemid.encode())
    bilgi=random_label_text+"-"+kurumkodinput.get_text()+"-"+str(sha256.hexdigest())+"-0"
    if _last_random_label_text != random_label_text:
        _last_random_label_text = random_label_text
        qrkilittext.set_text("qrkilit.com.tr")
        img = qrcode.make(str(bilgi))
        img.save(qrkilitfile)
        qrkilitimage.set_from_file(qrkilitfile)
             
    GLib.timeout_add(500,update_popover_qrkilit_text)
    

def update_popover_qrkilit_duyuru():
    global kurumkodinput
    global qrkilitduyuru_id
    global qrkilitduyuru_type
    global qrkilitduyuru_title
    global qrkilitduyuru_content
    global qrkilitduyuru_date

    qrkilitduyuru_id.set_line_wrap(True)
    qrkilitduyuru_type.set_line_wrap(True)
    qrkilitduyuru_title.set_line_wrap(True)
    qrkilitduyuru_content.set_line_wrap(True)
    qrkilitduyuru_date.set_line_wrap(True)
    qrkilitduyuru_content.set_max_width_chars(10)

    if kurumkodinput.get_text() != "":
        sid=str(guid())
        systemid=sid[:10]
        sha256 = hashlib.sha256()
        sha256.update(systemid.encode())
        url = 'https://qrkilit.com.tr/wp-admin/admin-ajax.php?action=notifications&kurumkodu='+kurumkodinput.get_text()+'&id='+str(sha256.hexdigest())+'&system=0'
        #url = 'https://qrkilit.com.tr/wp-admin/admin-ajax.php?action=notifications&kurumkodu=111&id=4545&system=0'


        response = requests.get(url)
        if response.status_code == 200:
        	data = response.json()  # JSON formatında veri al
        	qrkilitduyuru_id.set_text(str(data["notifications"][0]["id"]))
        	qrkilitduyuru_type.set_text(data["notifications"][0]["type"])
        	qrkilitduyuru_title.set_text(data["notifications"][0]["title"])
        	qrkilitduyuru_content.set_text(data["notifications"][0]["content"])
        	#qrkilitduyuru_content.set_text(url)
        	qrkilitduyuru_date.set_text(data["notifications"][0]["date"])
        	
        	    
    #GLib.timeout_add(500,update_popover_qrkilit_duyuru)





def qrkilitqrcode_control_event():
    global random_label_text
    global result_pass_str
    random_label_text=str(random.randrange(100000, 999999))
    p1=random_label_text[0]
    p2=random_label_text[1]
    p3=random_label_text[2]
    p4=random_label_text[3]
    p5=random_label_text[4]
    p6=random_label_text[5]
    #------------------
    p1=str(abs(((int(p1)+int(p1))-int(p2))*int(p3)))
    p2=str(abs(((int(p2)+int(p1))-int(p2))*int(p3)))
    p3=str(abs(((int(p3)+int(p1))-int(p2))*int(p3)))
    p4=str(abs(((int(p4)+int(p1))-int(p2))*int(p3)))
    p5=str(abs(((int(p5)+int(p1))-int(p2))*int(p3)))
    p6=str(abs(((int(p6)+int(p1))-int(p2))*int(p3)))
    result_pass_str=str(p1[0]+p2[0]+p3[0]+p4[0]+p5[0]+p6[0])


def loginqrkilitbutton_clicked(button):
    global qrkilitpopover
    global result_pass_str
    global qrkilitduyuru
    global kurumkodinput
    #qrkilitinput.set_text("hii")
    if qrkilitinput.get_text() == result_pass_str:
        #print(random_label_text)
        qrkilitpopover.hide()
        print("giriş yapılıyor..")
        os.system("echo 'ebaqrebaqr:ebaqr:ebaqr' | netcat localhost 7777 &")

        	        
def kurumkodbutton_clicked(button):
    global kurumkodinput
    os.system("echo 'kurumkod:"+kurumkodinput.get_text()+"|:ebaqr' | netcat localhost 7777 &")
    try:
        with open("/etc/qrkilit.conf", 'r', encoding='utf-8') as dosya:
        	icerik = dosya.read()
        	kurumkodinput.set_text(icerik.split("|")[0])
        if kurumkodinput.get_text() != "":
        	kurumkodinput.hide()
        	kurumkodbutton.hide()
    except:
        print("hata oluştu")
        kurumkodinput.hide()
        kurumkodbutton.hide()
        	        
def duyuruyenilebutton_clicked(button):
    update_popover_qrkilit_duyuru()
            
def internet_baglantisi_testi(url='http://www.google.com'):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def module_init():
    global qrkilitpopover
    global qrkilitimage
    global qrkilittext
    global qrkilitinput
    global loginqrkilitbutton
    global kurumkodinput
    global kurumkodbutton
    global qrkilitduyuru_id
    global qrkilitduyuru_type
    global qrkilitduyuru_title
    global qrkilitduyuru_content
    global qrkilitduyuru_date

    qrkilitpopover = Gtk.Popover()
    qrkilitimage = Gtk.Image()
    qrkilittext = Gtk.Label()
    qrkilitduyuru_id = Gtk.Label()
    #qrkilitduyuru_id.set_size_request(800,20)
    qrkilitduyuru_type = Gtk.Label()
    #qrkilitduyuru_type.set_size_request(800,200)
    qrkilitduyuru_title = Gtk.Label()
    #qrkilitduyuru_title.set_size_request(800,200)
    qrkilitduyuru_content = Gtk.Label()
    qrkilitduyuru_content.set_size_request(800,150)
    qrkilitduyuru_date = Gtk.Label()
    #qrkilitduyuru_date.set_size_request(800,200)
    
    duyuruyenilebutton = Gtk.Button.new_with_label("Duyuru Yenile")
    duyuruyenilebutton.connect("clicked",duyuruyenilebutton_clicked)
    
    qrkilitinput=Gtk.Entry()
    loginqrkilitbutton = Gtk.Button.new_with_label("Giriş")
    loginqrkilitbutton.connect("clicked",loginqrkilitbutton_clicked)
    #---------------------------------------------------------------
    kurumkodinput=Gtk.Entry()
    kurumkodbutton = Gtk.Button.new_with_label("Kurum Kod Kaydet")
    kurumkodbutton.connect("clicked",kurumkodbutton_clicked)
    #---------------------------------------------------------------
    yataypanel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    solpanel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    solpanel.pack_start(qrkilitimage,False,False,0)
    
    solpanel.pack_start(qrkilittext,False,False,0)
    solpanel.pack_start(qrkilitinput,False,False,0)
    solpanel.pack_start(loginqrkilitbutton,False,False,0)
    
    sagpanel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    sagpanel.pack_start(qrkilitduyuru_id,False,False,0)
    sagpanel.pack_start(qrkilitduyuru_type,False,False,0)
    sagpanel.pack_start(qrkilitduyuru_title,False,False,0)
    sagpanel.pack_start(qrkilitduyuru_content,False,False,0)
    sagpanel.pack_start(qrkilitduyuru_date,False,False,0)
    sagpanel.pack_start(duyuruyenilebutton,False,False,0)
    
    qrkilitduyuru_id.set_text("")
    qrkilitduyuru_type.set_text("")
    qrkilitduyuru_title.set_text("")
    qrkilitduyuru_content.set_text("")
    qrkilitduyuru_date.set_text("")
    
    #------------------------------------------------------------------

    try:
        with open("/etc/qrkilit.conf", 'r', encoding='utf-8') as dosya:
        	icerik = dosya.read()
        	kurumkodinput.set_text(icerik.split("|")[0])
        if kurumkodinput.get_text() == "":
        	solpanel.pack_start(kurumkodinput,False,False,0)
        	solpanel.pack_start(kurumkodbutton,False,False,0)
    except:
        if os.path.isfile("/etc/qrkilit.conf")==False:
        	solpanel.pack_start(kurumkodinput,False,False,0)
        	solpanel.pack_start(kurumkodbutton,False,False,0)
        
    #solpanel.pack_start(kurumkodinput,False,False,0)
    #solpanel.pack_start(kurumkodbutton,False,False,0)
    
    qrkilitpopover.add(yataypanel)
    qrkilitpopover.set_position(Gtk.PositionType.BOTTOM)
    button = Gtk.MenuButton(label="QRKILIT", popover=qrkilitpopover)
    button.connect("clicked",_qrkilitqrkod_button_event)
    loginwindow.o("ui_box_bottom_left").pack_end(button, False, True, 10)
    button.get_style_context().add_class("icon")
    button.show_all()
    solpanel.show_all()
    sagpanel.show_all()
    yataypanel.pack_start(solpanel,False,False,0)
    yataypanel.pack_start(sagpanel,False,False,0)
    yataypanel.show_all()
    #loginwindow.o("ui_button_network").connect("clicked",_qrkilitqrkod_button_event)
    update_popover_qrkilit_text()
    update_popover_qrkilit_duyuru()
    qu=Qrkilit_Update()
    qu.qrkilit_guncelle()
