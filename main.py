# This Python file uses the following encoding: utf-8
import sys
import os
from shlex import split
import subprocess
from multiprocessing import Process
import psutil
import time
from datetime import datetime
import signal

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Signal, Property, QUrl, Slot
from PySide2.QtWidgets import *
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import gspread

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
JSON_FILE_PATH = 'pyramid-vision-4b762634fb0b.json'     #　各自の環境に合わせてください（Google Cloud Platformのサービスアカウントを使います）
FILE_ID = '1Pqm0L5dAddBl23gB8nigj3h3k9Y-JTYQ'           #　各自の環境に合わせてください（画像保存フォルダのIDです）
sheet_name = '画像データベース'                             #　各自の環境に合わせてください（Spread Sheetのファイル名です）

def func():
    subprocess.call(split('libcamera-still -t 0 --info-text "Focus : %focus" -p 0,0,960,720 -o test.jpg -s'))

class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)
        credentials = service_account.Credentials.from_service_account_file(JSON_FILE_PATH, scopes=SCOPE)
        self.service = build('drive', 'v3', credentials=credentials)
        self.gc = gspread.authorize(credentials)

    # Shot
    @Slot()
    def shot(self):
        os.kill(pid, signal.SIGUSR1)
        time.sleep(1)
        date = datetime.now()
        time1 = date.strftime('%Y/%m/%d %H:%M:%S')
        media = MediaFileUpload('test.jpg', mimetype='image/jpeg')
        file_metadata = {'name': 'photo.jpg', 'parents': [FILE_ID]}
        try:
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(file['id'])
        except Exception as ex:
            print(ex)

        # wks = self.gc.open(sheet_name).worksheet('型番')
        # model = wks.get_all_values()
        # print(model)
        try:
            wks = self.gc.open(sheet_name).worksheet('ID')
            input_value = [time1,'0010001001','','','','','https://drive.google.com/file/d/' + file['id'],False]
            wks.append_row(input_value)
            # logger.info(input_value)
        except Exception as ex:
            print(ex)
            # logger.info(input_value)
            # logger.error(ex)

if __name__ == "__main__":
    p = Process(target=func)
    p.start()
    time.sleep(2)
    for proc in psutil.process_iter(['pid','name']):
        if proc.info['name'] == 'libcamera-still':
            pid=proc.info['pid']
            print(pid)
            break
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # QML経由でアクセスするBackendクラスのインスタンスを生成する
    backend = Backend()
    # backend クラスを QML の backend としてバインディングする
    engine.rootContext().setContextProperty("backend", backend)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
