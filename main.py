from gui.uis.windows.main_window.functions_main_window import *
import sys,os,time
import requests,json
import random
from bs4 import BeautifulSoup as bs4
from qt_core import *
from gui.core.json_settings import Settings
from gui.uis.windows.main_window import *
# IMPORT PY ONE DARK WIDGETS
from gui.widgets import *
import threading,queue
from urllib import request,parse

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
os.environ["QT_FONT_DPI"] = "96"
#IF IS 4K MONITOR ENABLE
#os.environ["QT_SCALE_FACTOR"] = "2" 

# MAIN WINDOW
class MainWindow(QMainWindow):
    def selectDirectory(self):
        selected_directory = QFileDialog.getExistingDirectory()
        self.line_edit3.setText(selected_directory)
    
    def openDirectory(self):
        basepath=self.line_edit3.text()
        os.startfile(basepath)

    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items
        # SETUP MAIN WINDOW
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)
        # SHOW MAIN WINDOW
        self.show()
    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    def msg(self,title,content):
        #信息框
        QMessageBox.critical(self,title,content,QMessageBox.Ok,QMessageBox.Ok)
    
    def downfile(self,req):
        pass
        
    def download(self,data, headers={}, interval=0.5):
        basepath=self.line_edit3.text().replace('\\','/')
        def MB(byte):
            return round(byte / 1024 / 1024, 2)         

        row=data[0]
        cir1=data[1]
        name=data[2]
        url=data[3]
        path=data[4]        
        fullpath=basepath+path  
        if not fullpath.endswith('/'):
            fullpath=fullpath+'/'
        try:
            os.makedirs(fullpath)    
        except:
            pass                     

        self.table_widget.setItem(row,3,QTableWidgetItem('Downloading'))
        self.ui.credits.copyright_label.setText('下载:'+name)
        header={'Proxy-Connection': 'keep-alive'}
        res = requests.get(url, stream=True, headers=header)
        file_size = int(res.headers['content-length'])  # 文件大小 Byte
        
        f = open(fullpath+name, 'wb')
        down_size = 0  # 已下载字节数
        old_down_size = 0  # 上一次已下载字节数
        time_ = time.time()
        self.circular_progress_1.set_value(cir1)
        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
                down_size += len(chunk)
                if time.time() - time_ > interval:
                    # rate = down_size / file_size * 100  # 进度  0.01%
                    speed = (down_size - old_down_size) / interval  # 速率 0.01B/s                    
                    old_down_size = down_size
                    time_ = time.time()                    
                    print_params = [MB(speed), MB(down_size), MB(file_size), (file_size - down_size) / speed]
                    cir2=int(down_size/file_size*100)                    
                    self.circular_progress_2.set_value(cir2)
                    cir3=MB(speed)
                    self.circular_progress_3.set_value(cir3)
                    self.ui.credits.copyright_label.setText('开始下载'+name)
                    #print('\r{:.1f}MB/s - {:.1f}MB，共 {:.1f}MB，还剩 {:.0f} 秒   '.format(*print_params), end='')                    
        f.close()
        self.circular_progress_2.set_value(100)
        self.table_widget.setItem(row,3,QTableWidgetItem('Complete'))
        self.ui.credits.copyright_label.setText('完成')
        

    def dumpThread(self,baseurl,hosturl):        
        page_urls=[baseurl]
        _fileext=self.line_edit2.text()
        if _fileext=='':
            limfile=False
        else:
            limfile=True
            fileext=_fileext.split('.')
            fileext.remove('')
        

        for now_url in page_urls:
            self.ui.credits.copyright_label.setText('正在解析:'+now_url)
            response = requests.get(now_url)
            soup = bs4(response.text, "html.parser")
            a_tags = soup.find_all('a')            
            for tag in a_tags:
                #self.circular_progress_1.set_value(random.randint(1,90))
                #self.circular_progress_2.set_value(random.randint(1,90))
                #self.circular_progress_3.set_value(random.randint(1,90))

                href=tag.get('href','')
                title=tag.get('title')                
                if href=='/' or href=='' or href.startswith('https://') or href.startswith('http://'):
                    continue    
                if href.startswith('/'):
                    fullurl=hosturl+href
                else:
                    fullurl=baseurl+href
                if fullurl in page_urls or fullurl==hosturl:
                    continue
                _req=request.urlopen(fullurl)
                if 'text/html' in _req.info().get('Content-Type'):
                    page_urls.append(fullurl)
                else:   
                    need=True
                    if limfile:
                        need=False                 
                        for x in fileext:
                            if href.endswith(x):
                                need=True
                    
                    if need!=True:
                        continue    

                    row_number = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_number) # Insert row
                    self.table_widget.setItem(row_number, 0, QTableWidgetItem(title)) # Add name
                    self.table_widget.setItem(row_number, 1, QTableWidgetItem(fullurl)) # Add nick
                    _path=parse.urlparse(fullurl).path
                    _path=_path.split('/')
                    _path='/'.join(_path[0:-1])
                    self.table_widget.setItem(row_number, 2, QTableWidgetItem(parse.unquote(_path))) # Add nick
                    self.table_widget.setItem(row_number, 3, QTableWidgetItem('Padding')) # Add nick
                    self.table_widget.setCurrentCell(row_number,0)

        self.ui.credits.copyright_label.setText('抓取完成，开始下载')
        row_number = self.table_widget.rowCount()
        col_number = self.table_widget.columnCount()
        for x in range(row_number):  
            cir1=int(x/row_number*100)
            parms=[x,cir1]    
            for y in range(col_number):                   
                parms.append(self.table_widget.item(x,y).text())
            self.table_widget.setCurrentCell(x,0)
            self.download(parms)
        self.circular_progress_1.set_value(100)

    def start_download(self):
        url=self.line_edit.text()
        url_parse=parse.urlparse(url)
        if url_parse.netloc and url_parse.scheme:
            hosturl="://".join([url_parse.scheme,url_parse.netloc])
            baseurl=hosturl+url_parse.path
            if not baseurl.endswith('/'):
                baseurl=baseurl+'/'
            t1 = threading.Thread(target=self.dumpThread,args=[baseurl,hosturl])
            t1.start()
        else:            
            self.msg('URL错误','请输入正确的URL并重试')

        
    def clear(self):
        self.table_widget.clearContents()
        row_number = self.table_widget.rowCount()
        for x in range(row_number):
            self.table_widget.removeRow(0)

    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)
        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)
        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

# SETTINGS WHEN TO START

 
if __name__ == "__main__":
    # APPLICATION
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    # EXEC APP


    sys.exit(app.exec())