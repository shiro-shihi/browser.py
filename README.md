# 非常に読みにくいコードであることをご了承ください。

バグだらけなので、各自で必要に応じて修正してください。  
pull requests投げてくれれば多分対応します。  
突然アプリが落ちるときもあります。そこの修正も各自で頑張ってください。  
そういうのを直す楽しみもあると思います。

## 必要な外部モジュール
> `pip`を用いてインストールしてください。

|Modules|command|
|:--:|:--:|
|PyQt5|`pip install PyQt5`|
|QtWebEngineWidgets|`pip install QtWebEngineWidgets`|

> もしexeファイル化したいときは

Pyinstallerというモジュールを用いるとexeアプリに出来ます。  
バグっても知りません。

```
pip install Pyinstaller
Pyinstaller browser.py --onefile --noconsole
```

## アプリ内ショートカット
`ctrl + t` : タブを追加します  
`ctrl + w` : 現在アプティブなタブを閉じます  
`ctrl + shift + w` : すべてのタブを閉じます  
`ctrl + b` : 現在アクティブなサイトをブックマークに追加します  
`ctrl + h` : 履歴を表示します  

> ショートカットはこの部分のコードからいじれます。
~~~python
    def setup_shortcuts(self):
        shortcut_new_tab = QShortcut(Qt.CTRL + Qt.Key_T, self)
        shortcut_new_tab.activated.connect(self.add_new_tab)

        shortcut_close_tab = QShortcut(Qt.CTRL + Qt.Key_W, self)
        shortcut_close_tab.activated.connect(self.close_active_tab)

        shortcut_close_all_tabs = QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_W, self)
        shortcut_close_all_tabs.activated.connect(self.close_all_tabs)

        shortcut_add_bookmark = QShortcut(Qt.CTRL + Qt.Key_B, self)
        shortcut_add_bookmark.activated.connect(self.add_bookmark)

        shortcut_history = QShortcut(Qt.CTRL + Qt.Key_H, self)
        shortcut_history.activated.connect(self.show_history)
~~~

## License
Apache License 2.0  
(連絡なしでLicenseの範囲内で自由に使用できますが、気になるのでこれを改変したアプリ等を公開した場合は[Twitter(現X)](https://twitter.com/shiro_shihi)にてご連絡いただけると幸いです。)
