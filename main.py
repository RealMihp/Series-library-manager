import sys
import os
import time
import re
import json
import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QHeaderView, QListWidget
from PySide6.QtGui import QPixmap, QDesktopServices, QIcon, QColor
from ui.ui_main import Ui_MainWindow
from PySide6.QtCore import Qt, QUrl, QSize, QByteArray
from PySide6.QtWidgets import QWidget
from ui.ui_preferences import Ui_Preferences
from PySide6.QtWidgets import QDialog 
from ui.ui_apikey import Ui_APIkeyDialog
import requests
from typing import Optional, Union, List




class LibraryManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.img_dir = "posters"
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

        header = self.ui.treeWidget.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.resizeSection(0, 250)
        header.resizeSection(1, 400) 
        header.setStretchLastSection(True)

        self.ui.fileExplorerListWidget.itemDoubleClicked.connect(self.FE_item_open)


        self.ui.actionAdd_folder.triggered.connect(self.add_folder)
        self.ui.actionClose.triggered.connect(self.close_folder)


        self.pref_win = PreferencesWindow()
        self.api_win = APIKeyWindow()

        self.ui.startScanPushButton.pressed.connect(self.start_scan)
        
        self.ui.actionPreferences.triggered.connect(self.open_preferences)

        self.ui.fileExplorerListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.fileExplorerListWidget.customContextMenuRequested.connect(self.FE_show_context_menu)

        self.ui.treeWidget.itemClicked.connect(self.render_seriesInfo)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.MF_show_context_menu)
        self.ui.treeWidget.sortItems(0, Qt.AscendingOrder)
        
        

        self.check_api_key()

        cache = self.search_titles_in_db("",[])
        self.show_titles(cache)
        self.ui.scanProgressBar.setValue(0)

    def render_seriesInfo(self):
        print("----------------------render_seriesInfo----------------------")
        item = self.ui.treeWidget.currentItem()
        item_info_text = item.text(1)

        icon = item.icon(0)
        pixmap = icon.pixmap(icon.actualSize(QSize(680, 1000)))
        scaled_pixmap = pixmap.scaled(
            self.ui.posterLabel.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        tvdb_id = str(str(item_info_text.split("\n")[2]).split("TVDB id: ")[1])
        year = str(item_info_text.split("\n")[0])
        status = str(item_info_text.split("\n")[1])
        self.ui.posterLabel.setPixmap(scaled_pixmap)
        self.ui.posterLabel.setScaledContents(False)

        self.ui.titleLabel.setText(item.text(0))
        self.ui.yearLabel.setText(year)
        self.ui.statusLabel.setText(status)
        

    def start_scan(self):
        print("----------------------start_scan----------------------")
        key = self.check_api_key()
        token = None
        try: 
            with open("token.txt", "r") as f:
                token = f.read().strip()
                if token == "":
                    token = None
        except Exception as e:
            print(f"Failed to extract token from file: {e}")
        
        if token is None:
            token = self.update_tvdb_token(key)
            if token is None:
                print("Failed to get token")
                return
       
        self.ui.scanProgressBar.setValue(10)

        titles = self.scan_library()

        if titles is None:
            print("Директория пуста")
            self.ui.scanProgressBar.setValue(0)
            return
        print(titles)

        self.ui.scanProgressBar.setValue(20)
        titles.sort()
        cache = self.search_titles_in_db(token, titles)
        
        self.ui.scanProgressBar.setValue(90)

        self.show_titles(cache)

        self.ui.scanProgressBar.setValue(100)


    def show_titles(self, cache: dict):
        print("----------------------show_titles----------------------")
        self.ui.treeWidget.setColumnCount(2)
        self.ui.treeWidget.setHeaderLabels(["Title", "Info"])
        self.ui.treeWidget.setIconSize(QSize(96, 96))
        self.ui.treeWidget.setWordWrap(True)

        shown_titles = set()
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            shown_titles.add(item.text(0))

        for i, title in enumerate(cache):

            if title in shown_titles:
                continue

            tvdb_id = cache[title]["tvdb_id"]
            if tvdb_id is not None:
                title_item = QTreeWidgetItem([title])
                

                url = cache[title]["data"]["image_url"]
                pixmap = self.load_poster(url,tvdb_id)
                
                if pixmap:
                    title_item.setIcon(0, QIcon(pixmap))
                else:
                    title_item.setIcon(0, self.create_placeholder_icon())

                status = cache[title]["data"]["status"]
                year = cache[title]["data"]["year"]

                info_text = f"{year}\n{status}\nTVDB id: {tvdb_id}"

                title_item.setText(1, info_text)
                self.ui.treeWidget.addTopLevelItem(title_item)
 
                progress = 90 + int(((i + 1) / len(cache)) * 10)
                self.ui.scanProgressBar.setValue(progress)
                count = self.ui.treeWidget.topLevelItemCount()
                self.ui.statusBarLabel.setText(f"Found series: {count}")

                QApplication.processEvents()
                

    def load_poster(self, link: str, tvdb_id: str) -> QPixmap | None:
        print("----------------------load_poster----------------------")
        file_path = os.path.join(self.img_dir, f"{tvdb_id}.jpg")

        if os.path.exists(file_path):
            return QPixmap(file_path)

        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                return pixmap
        except Exception as e:
            print(f"Failed to save picture: {e}")
        
        return None
    

            

    def create_placeholder_icon(self):
        print("----------------------create_placeholder_icon----------------------")
        pixmap = QPixmap(50, 70)
        pixmap.fill(QColor("blue"))
        return QIcon(pixmap)

    def search_titles_in_db(self, token: str, titles: list) -> dict | None:
        print("----------------------search_titles_in_db----------------------")
        path = "dbcache.json"
        
        
        cache = {}
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except json.JSONDecodeError:
                print("Cache file is corrupted")

        headers = {"Authorization": f"Bearer {token}"}
        FAKE_WORDS = {"abridged", "parody", "fan", "dub", "re-cut", "fandub"}

        for i, title in enumerate(titles):
            if title in cache and cache[title].get("tvdb_id"):
                print(f"From cache: {title}")
            else:
                print(f"Searching in TVDB: {title}")
                params = {
                    "query": title,
                    "type": "series",
                    "limit": 5 
                }

                try:
                    response = requests.get("https://api4.thetvdb.com/v4/search", headers=headers, params=params, timeout=10)
                    results = response.json()
                    
                    best_match = None
                    
                    if results.get("data"):
                        for candidate in results["data"]:
                            name_low = candidate.get("name", "").lower()
                            
                            is_fake = any(fake in name_low for fake in FAKE_WORDS)
                            
                            if not is_fake:
                                best_match = candidate
                                break
                        
                        if not best_match:
                            best_match = results["data"][0]

                    if best_match:
                        cache[title] = {
                            "tvdb_id": best_match["tvdb_id"],
                            "last_updated": datetime.datetime.now().isoformat(),
                            "data": best_match
                        }
                    else:
                        cache[title] = {
                            "tvdb_id": None,
                            "last_updated": datetime.datetime.now().isoformat(),
                            "data": None
                        }

                except Exception as e:
                    print(f"Request error for {title}: {e}")

            progress = 20 + int(((i + 1) / len(titles)) * 70)
            self.ui.scanProgressBar.setValue(progress)
            QApplication.processEvents()
            
            time.sleep(0.2) 

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save dbcache.json: {e}")

        return cache

            
    def scan_library(self) -> list | None:
        print("----------------------scan_library----------------------")
        folder = self.ui.pathLine.text()
        if os.path.isdir(folder):
            IGNORED_EXTS = {'.ttf', '.otf', '.ttc', '.ass', '.srt', '.txt', '.png', '.jpg', '.jpeg', 
                            '.mka', '.ac3', '.rtf', '.parts', '.mkv', '.mp4', '.avi', '.m4a', '.ini'}

            GARBAGE_WORDS = {"rus", "eng", "sub", "sound", "font", "fonts", "signs", "rus sound", "eng sound", 
                            "rus subs", "eng subs", "rus sounds", "eng sounds", "надписи", "bonus", 
                            "extra", "preview", "scans", "scan", "previews", "commentatory", 
                            "bd menu", "bd", "pv", "anilibria", "anidub", "sovetromantica", 
                            "shiza", "anifilm", "animedia", "aniplay", "crunchyroll", "netflix", "anisense",
                            "booklet", "zendos", "eladiel", "zendos & eladiel", "анимевод", 
                            "ryuji", "seiya & axtr25", "trouble & акварелька", "св-дубль", "субтитры", "alvakarp", 
                            "alisma", "getsmart", "ambiente", "rg genshiken", "studioband", "stan warhammer", 
                            "animereactor", "yss шрифты", "powerwar & co", "aniliberty", "get smart group", "opendub", "antravoco", "1080p", "720p", "480p", "x264", "x265", "h264", "h265", "av1", "10bit", "8bit",
                            "bluray", "bdrip", "web-dl", "webrip", "tvrip", "dvdrip", "hdtv",
                            "dual audio", "multi-sub", "aac", "flac", "dts", "ac3",
                            "repack", "remux", "softsubs", "hardsubs", "raw",
                            "vostfr", "ita", "esp", "ger", "jpn", "dub", "multi",
                            "v0", "v1", "v2", "v3",
                            "preview", "promo", "commercial", "teaser", "opening", "ending", "op", "ed",
                            "shinkai", "miyazaki", "makoto", "ghibli",
                            "anidust", "dreamers", "shikimori", "jut su", "yummyani", "smotret-anime", "sa4ko aka kiyoso", "kbm team"}

            STRICT_GARBAGE = {"sub", "subs", "sound", "font", "fonts", "надписи", "sign", "signs", 
                            "bonus", "nc", "nced", "ncop", "extra", "preview", "scans", "scan", 
                            "previews", "commentatory", "bd menu", "bd", "pv", "novel", "шрифты", "полные",
                            "yss полные", "audio", "lostyears", "box", "op", "ed", "ncop", "nced", "ost", 
                            "music", "soundtrack", "covers", "art", "artbook", "wallpapers", "artwork", 
                            "docs", "info", "read me", "specials", "omake", "shorts", "movies", "sp", "clips", "trailer",
                            "sample", "metadata", "extrafiles", "thumbnails", "temp", "cache",
                            "subtitles", "subs_rus", "subs_eng", "scripts", "ass", "srt",
                            "vol", "volume", "folder", "images", "pics", "screenshots", "cd"}
            


            PATTERNS = [
                r'\s+S\d+E\d+.*',                       # S01E01...
                r'\s+\d{1,2}(st|nd|rd|th)?\s+Stage.*',  # 1st Stage, 2nd Stage...
                r'\s+Season\s+\d+.*',                   # Season 1...
                r'\s+Episode\s+\d+.*',                  # Episode 1...
                r'\s+OVA.*',                            # OVA...
                r'\s+TV.*',                             # TV...
                r'\s+S\d+.*',                           # S1, S2...
                r'\s+-\s+\d+.*',                        # - 01...
                r'\s+\d{1,3}$',                         # Numbers in the end
                r'\s+[0-9]{2,3}(?:\s|$).*'              # 2-3 digit numbers in the middle or at the end
            ]

            self.ui.fileExplorerListWidget.clear()
            clean_titles = set()

            for root, dirs, files in os.walk(folder):
                for d in dirs:
                    low_d = d.lower()
                    if any(word in low_d for word in GARBAGE_WORDS) or low_d in STRICT_GARBAGE:
                        continue

                    name = re.sub(r'\[.*?\]|\(.*?\)', '', d)
                    name = name.replace('_', ' ').replace('.', ' ')
                    

                    for p in PATTERNS:
                        name = re.split(p, name, flags=re.IGNORECASE)[0]
                    

                    name = re.sub(r'\s+(?:Season|Stage|S|St|nd|rd|th|Part)\s*\d+$', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'\s+\d+$', '', name) 

                    name = ' '.join(name.split()).strip(" -.")
                    
                    if name.lower() in STRICT_GARBAGE or len(name) < 3:
                        continue

                    if name:
                        clean_titles.add(name)

                for item in files:
                    low_item = item.lower()
                    if any(low_item.endswith(ext) for ext in IGNORED_EXTS): continue
                    
                    name, _ = os.path.splitext(item)
                    name = re.sub(r'\[.*?\]|\(.*?\)', '', name)
                    name = name.replace('.', ' ').replace('_', ' ')

                    for p in PATTERNS:
                        name = re.split(p, name, flags=re.IGNORECASE)[0]


                    name = re.sub(r'\s+(?:Season|Stage|S|St|nd|rd|th|Part)\s*\d+$', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'\s+\d+$', '', name) 

                    name = name.strip(" -.")

                    if name.lower() in STRICT_GARBAGE or len(name) < 3:
                        continue

                    if name:
                        clean_titles.add(name)

            clean_titles.discard('')
            

            return list(clean_titles)
            
        else:
            print("Directory wasn't found")
            return None



    def open_preferences(self):
        print("----------------------open_preferences----------------------")
        self.pref_win.show()
        self.check_api_key()

    def check_api_key(self) -> str:
        print("----------------------check_api_key----------------------")
        if not os.path.exists("api_key.txt"):
            self.prompt_for_key()
        else:
            with open("api_key.txt", "r") as f:
                key = f.read().strip()
                if not key:
                    self.prompt_for_key()
                else:
                    print("API key found")
                    return(key)

    def prompt_for_key(self):
        print("----------------------prompt_for_key----------------------")
        if self.api_win.exec(): 
            print("API key found and saved")
        else:
            print("API key wasn't entered")

    def request_api_key(self):
        print("----------------------request_api_key----------------------")
        result = self.api_win.exec() 
        if result == QDialog.Accepted:
            print("User updated their API key")

    def update_tvdb_token(self, api_key: str) -> str | None:
        print("----------------------update_tvdb_token----------------------")
        url = "https://api4.thetvdb.com/v4/login"
        
        payload = {
            "apikey": api_key
        }
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                token = data['data']['token']
                print("Token acquired!")
                try:
                    with open("token.txt", "w") as f:
                        f.write(token)
                        print("Тoken successfully saved")
                        return token
                except Exception as e:
                    print(f"Failed to save token: {e}")
                    return token
                        
            else:
                print(f"Auth error: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"Failed to contact the server: {e}")
            return None

    def update_files(self):
        print("----------------------update_files----------------------")
      
        folder = self.ui.pathLine.text()
        if os.path.isdir(folder):
            self.ui.fileExplorerListWidget.clear()
            files = os.listdir(folder)
            self.ui.fileExplorerListWidget.addItems(files)
            self.ui.scanProgressBar.setValue(0)
        else:
            self.ui.pathLine.setText("Path not found")


    def add_folder(self):
        print("----------------------add_folder----------------------")

        folder = QFileDialog.getExistingDirectory(self, "Select a library folder")
    
        if folder:
            self.ui.pathLine.setText(folder)


    def close_folder(self):
        print("----------------------close_folder----------------------")

        self.ui.pathLine.setText("")
        self.ui.fileExplorerListWidget.clear()

    
    def FE_item_open(self, item):
        print("----------------------FE_item_open----------------------")
        current_item = self.ui.fileExplorerListWidget.currentItem()
        if current_item:
            file_name = current_item.text()
            folder_path = self.ui.pathLine.text()
            

            full_path = os.path.join(folder_path, file_name)
            
            QDesktopServices.openUrl(QUrl.fromLocalFile(full_path))

    
    def FE_show_context_menu(self, pos):
        print(f"----------------------FE_show_context_menu----------------------")

        global_pos = self.ui.fileExplorerListWidget.mapToGlobal(pos)
        menu = QMenu(self)
        action1 = menu.addAction("Open in explorer")
        

        action = menu.exec(global_pos)
        
        if action == action1:
            folder_path = self.ui.pathLine.text()
            if os.path.exists(folder_path):

                os.startfile(folder_path)

    def MF_show_context_menu(self, pos):
        print(f"----------------------MF_show_context_menu----------------------")

        global_pos = self.ui.treeWidget.mapToGlobal(pos)
        menu = QMenu(self)
        action1 = menu.addAction("View on TVDB")
        action2 = menu.addAction("Remove from series list")
        
        action = menu.exec(global_pos)
        
        if action == action1:
            item = self.ui.treeWidget.currentItem()
            if item:
                info_text = item.text(1)
                tvdb_id = str(str(info_text.split("\n")[2]).split("TVDB id: ")[1])
                url = QUrl(f"https://www.thetvdb.com/search?query={tvdb_id}")
                QDesktopServices.openUrl(url)
        elif action == action2:
            pass




class PreferencesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Preferences()
        self.ui.setupUi(self)

        self.check_api_key()

    def check_api_key(self):
        if not os.path.exists("api_key.txt"):
            pass
        else:
            with open("api_key.txt", "r") as f:
                key = f.read().strip()
                if not key:
                    self.ui.P1LineEdit.setPlaceholderText("Enter your API key")
                else:
                    self.ui.P1LineEdit.setText(key)

class APIKeyWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_APIkeyDialog()
        self.ui.setupUi(self)
        
        self.ui.buttonBox.clicked.connect(self.save_and_close)

    def save_and_close(self):
        key = self.ui.APIkeyLineEdit.text().strip()
        
        if key:
            with open("api_key.txt", "w") as f:
                f.write(key)
            
            self.accept()
        else:
            self.ui.APIkeyLineEdit.setText("")
            self.ui.APIkeyLineEdit.setPlaceholderText("Enter your API key")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryManager()
    window.show()
    sys.exit(app.exec())