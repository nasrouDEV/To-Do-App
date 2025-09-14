from PySide6.QtWidgets import QApplication ,QDialog, QMainWindow,QMessageBox, QPushButton,QVBoxLayout ,QHBoxLayout ,QCheckBox,QListWidget,QListWidgetItem, QWidget, QLineEdit , QLabel , QGraphicsOpacityEffect
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt , QEvent
from datetime import datetime
from PySide6.QtGui import QFont
import webbrowser
import sys
import json,os
import time
import pygame

pygame.mixer.init()
check_sound = pygame.mixer.Sound("wav/check.wav")
uncheck_sound = pygame.mixer.Sound("wav/uncheck.wav")
delete_sound = pygame.mixer.Sound("wav/delete.wav")
menu_sound = pygame.mixer.Sound("wav/menu1.wav")
delMen_sound = pygame.mixer.Sound("wav/delMen1.wav")
add_sound = pygame.mixer.Sound("wav/add.wav")
edit_sound = pygame.mixer.Sound("wav/edit.wav")
saveedit_sound = pygame.mixer.Sound("wav/saveedit.wav")

is_muted = False

Task_File = "tasks.json"
editing_lable = None
app = QApplication(sys.argv)
window = QMainWindow()
effect1 = QGraphicsOpacityEffect()
effect1.setOpacity(0.7)

def set_all_task_widgets_enabled(list_widget, enabled: bool):
    """Enable/disable all widgets inside the task list and update styles."""
    if not is_muted:   
        saveedit_sound.play()
    for i in range(list_widget.count()):
        item = list_widget.item(i)
        row_widget = list_widget.itemWidget(item)
        if row_widget:
            for w in row_widget.findChildren(QWidget):
                w.setEnabled(enabled)
                if isinstance(w, QPushButton):
                    if not enabled:
                        # Apply "editing" styles
                        if w.objectName() == "edit":
                            w.setStyleSheet("""
QPushButton {
    border-radius:13px;
    background-image: url('btns/editClick.png');
    background-repeat: no-repeat;
    background-position: center;
}
""")
                        else:
                            w.setStyleSheet("""
QPushButton {
    border-radius:13px;
    background-image: url('del/deleteClick.png');
    background-repeat: no-repeat;
    background-position: center;
}
""")
                    else:
                        # Restore default styles
                        if w.objectName() == "edit":
                            w.setStyleSheet("""
QPushButton {
    border-radius:13px;
    background-image: url('btns/edit.png');
    background-repeat: no-repeat;
    background-position: center;
}
QPushButton:hover {
    background-image: url('btns/editHover.png');
    background-repeat: no-repeat;
    background-position: center;
}
QPushButton:pressed {
    background-image: url('btns/editClick.png');
    background-repeat: no-repeat;
    background-position: center;
}
""")
                        else:
                            w.setStyleSheet("""
QPushButton {
    border-radius:13px;
    background-image: url('del/delete.png');
    background-repeat: no-repeat;
    background-position: center;
}
QPushButton:hover {
    background-image: url('del/deleteHover.png');
    background-repeat: no-repeat;
    background-position: center;
}
QPushButton:pressed {
    background-image: url('del/deleteClick.png');
    background-repeat: no-repeat;
    background-position: center;
}
""")

    # Restore add button style
    button.setStyleSheet("""
#addButton {
    border-radius: 24px;
    background-color:#903375 ;
    background-image: url('btns/plus1.png');
    background-repeat: no-repeat;
    background-position: center;
}
#addButton:hover {
    background-color:#972447 ;
    background-image: url('btns/plusHover1.png');
    background-repeat: no-repeat;
    background-position: center;
}
#addButton:pressed {
    background-color:#6a1a33 ;
    background-image: url('btns/plusClick1.png');
    background-repeat: no-repeat;
    background-position: center;
}
""")




""" Function to add a task to the list widget """
def add_task():
    global task_label
    global editing_lable
    global delete_button
    global edit_button
    if editing_lable is not None:
        if entry.text()=="":
            return

        editing_lable.setText(entry.text())
        editing_lable = None
        set_all_task_widgets_enabled(list_widget, True)
        entry.clear()
        return
    if entry.text()=="":
        return
    # Checkbox
    check = QCheckBox()
    check.setCursor(Qt.PointingHandCursor)
    check.setObjectName('checkbox') 
    check.setStyleSheet("""
        #checkbox::indicator {
            width: 12px;
            height: 12px;
        }
        #checkbox::indicator:unchecked {
            border: 1px solid #ff6085;
            border-radius: 4px;
            background: white;
        }
        #checkbox:indicator:hover{
            background: #c8ffba;
        }
        #checkbox::indicator:checked {
            background: white;
            border-radius: 4px;
            border: 1px solid #75ccc8;
            background-image: url('btns/check.png');
            background-position: center;
            background-repeat: no-repeat;
        }
    """)
    
    # Label
    task_label = QLabel(entry.text())
    task_label.setObjectName("label")
    effect = QGraphicsOpacityEffect(task_label)
    effect.setOpacity(0.7)
    # Play add sound only when not loading
    if not suppress_save:
        if not is_muted:
            add_sound.play()


    def toggle_strike(lbl, state):
        if state == 2:
            if not is_muted:
                check_sound.play()
            lbl.setStyleSheet("text-decoration: line-through; color: grey;")
        else:
            #uncheck_sound.play()
            lbl.setStyleSheet("text-decoration: none;")

    check.stateChanged.connect(lambda state, lbl=task_label:toggle_strike(lbl,state))
    #  Buttons
    edit_button = QPushButton()
    edit_button.setCursor(Qt.PointingHandCursor)
    edit_button.setObjectName('edit')
    edit_button.setFixedSize(27,27)
    edit_button.setStyleSheet("""
QPushButton {
            border-radius:13px;
            background-image: url('btns/edit.png');
            background-repeat: no-repeat;
            background-position: center;               
                              }
QPushButton:hover {

            background-image: url('btns/editHover.png');
            background-repeat: no-repeat;
            background-position: center;                
                              }          
QPushButton:pressed {
            background-image: url('btns/editClick.png');
            background-repeat: no-repeat;
            background-position: center;                
                              }
""")


    delete_button = QPushButton()
    delete_button.setCursor(Qt.PointingHandCursor)
    delete_button.setFixedSize(27,27)
    delete_button.setStyleSheet("""
QPushButton {
            border-radius:13px;
            background-image: url('del/delete.png');
            background-repeat: no-repeat;
            background-position: center;               
                              }
QPushButton:hover {
            background-image: url('del/deleteHover.png');
            background-repeat: no-repeat;
            background-position: center;                
                              }          
QPushButton:pressed {
            background-image: url('del/deleteClick.png');
            background-repeat: no-repeat;
            background-position: center;                
                              }
""")
    delete_button.clicked.connect(lambda _, b=delete_button: delete_task(b))
    edit_button.clicked.connect(lambda _, lbl=task_label , del_btn=delete_button: edit_task(lbl , del_btn))

    # Container 1: rounded box with checkbox + label
    container1 = QWidget()
    container1.setGraphicsEffect(effect)
    container1.setObjectName("taskContainer")
    container1.setStyleSheet("""
        #taskContainer {
            background-color: white;
            border-radius: 11px;
        }
    """)
    container1_layout = QHBoxLayout(container1)
    container1_layout.setContentsMargins(10, 5, 10, 5)
    container1_layout.setSpacing(5)
    container1_layout.addWidget(check)
    container1_layout.addWidget(task_label, 1)

    # Container 2: buttons
    container2 = QWidget()
    container2_layout = QHBoxLayout(container2)
    container2_layout.setContentsMargins(0, 0, 0, 0)
    container2_layout.setSpacing(5)
    container2_layout.addWidget(edit_button)
    container2_layout.addWidget(delete_button)

    # Main row: container1 + container2
    row = QWidget()
    row.setFixedSize(300, 30)
    row_layout = QHBoxLayout(row)
    row_layout.setContentsMargins(1, 3, 10, 0)
    row_layout.setSpacing(10)
    row_layout.addWidget(container1, 1)
    row_layout.addWidget(container2)

    # Add row to list
    list_item = QListWidgetItem()
    list_item.setSizeHint(row.size())
    list_widget.addItem(list_item)
    list_widget.setItemWidget(list_item, row)
    list_widget.scrollToItem(list_widget.item(list_widget.count()-1))

    # Clear entry
    entry.clear()

def delete_dialog(task_name):
    dialog = QDialog(window)
    dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) 
    dialog.setAttribute(Qt.WA_TranslucentBackground)
    dialog.setFixedSize(240, 180)

    #Main container
    container = QWidget(dialog)
    container.setStyleSheet("""
        QWidget {
            background-color: #feffd3;
            border-radius: 15px;
        }
    """)
    layout = QVBoxLayout(container)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15) 
    title = QLabel("Delete Task")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("""
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: #903375;
        }
    """)
    layout.addWidget(title)

    #Message if delete
    message = QLabel(f"Are you sure you want to delete:\n“{task_name}”?")
    message.setWordWrap(True)
    message.setAlignment(Qt.AlignCenter)
    message.setStyleSheet("""
        QLabel {
            font-size: 13px;
            color: black;
        }
    """)
    layout.addWidget(message)

    layout.addStretch()

    # Buttons
    btn_layout = QHBoxLayout()
    btn_layout.setSpacing(20)

    yes_btn = QPushButton("Yes")
    yes_btn.setCursor(Qt.PointingHandCursor)
    yes_btn.setStyleSheet("""
        QPushButton {
            background-color: #cf3968;
            color: white;
            border-radius: 12px;
            min-width: 60px;
            min-height: 28px;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #972447;
        }
        QPushButton:pressed {
            background-color: #6a1a33;
        }
    """)

    no_btn = QPushButton("No")
    no_btn.setCursor(Qt.PointingHandCursor)
    no_btn.setStyleSheet("""
        QPushButton {
            background-color: #999;
            color: white;
            border-radius: 12px;
            min-width: 60px;
            min-height: 28px;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #666;
        }
        QPushButton:pressed {
            background-color: #444;
        }
    """)

    # connect buttons
    yes_btn.clicked.connect(lambda: dialog.done(QDialog.Accepted))
    no_btn.clicked.connect(lambda: dialog.done(QDialog.Rejected))

    btn_layout.addWidget(yes_btn)
    btn_layout.addWidget(no_btn)
    layout.addLayout(btn_layout)

    # Final layout
    main_layout = QVBoxLayout(dialog)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.addWidget(container)
    parent_rect = window.geometry()
    x = parent_rect.x() + (parent_rect.width() - dialog.width()) // 2   
    y = parent_rect.y() + (parent_rect.height() - dialog.height()) // 2  
    dialog.move(x, y)
    result = dialog.exec()  # blocks until user clicks Yes/No
    return result == QDialog.Accepted


def delete_task(button):
    delMen_sound.play()
    row = button.parentWidget().parentWidget()
    task_label = row.findChild(QLabel, "label")  # get the label
    task_name = task_label.text() if task_label else "this task"
    if delete_dialog(task_name):  # if user pressed Yes
        row = button.parentWidget().parentWidget()
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if list_widget.itemWidget(item) == row:
                delete_sound.play()
                time.sleep(0.15)
                list_widget.takeItem(i)
                break


def edit_task(label,delete_button):
    global editing_lable
    set_all_task_widgets_enabled(list_widget, False)
    editing_lable = label
    entry.setText(label.text())
    button.setStyleSheet("""
#addButton {
    border-radius: 24px;
    background-color:#903375 ;
    background-image: url('btns/updated.png');
    background-repeat: no-repeat;
    background-position: center;
}
#addButton:hover {
    background-color:#972447 ;
    background-image: url('btns/updatedHover.png');
    background-repeat: no-repeat;
    background-position: center;
    }
#addButton:pressed {
    background-color:#6a1a33 ;
    background-image: url('btns/updatedClick.png');
    background-repeat: no-repeat;
    background-position: center;
    }
""")
    if not is_muted:
        edit_sound.play()



# customizing the window 
window.setWindowTitle("To Do.")
window.setObjectName("MainWindow")
window.setStyleSheet("""
                     #MainWindow {
    background-image: url('main/bg.png');
    background-repeat: no-repeat;
    background-position: center;
    }
""")
window.setFixedSize(330,400)
window.setWindowIcon(QIcon("icon.png"))

# adding widgets to my window 
""" ADD TASK BUTTON """
central = QWidget()
window.setCentralWidget(central)
button=QPushButton( central)
button.setCursor(Qt.PointingHandCursor)
button.setObjectName("addButton")
button.setGeometry(274.1,343.6,48,48)
button.setStyleSheet("""
#addButton {
    border-radius: 24px;
    background-color:#903375 ;
    background-image: url('btns/plus1.png');
    background-repeat: no-repeat;
    background-position: center;
}
#addButton:hover {
    background-color:#972447 ;
    background-image: url('btns/plusHover1.png');
    background-repeat: no-repeat;
    background-position: center;
    }
#addButton:pressed {
    background-color:#6a1a33 ;
    background-image: url('btns/plusClick1.png');
    background-repeat: no-repeat;
    background-position: center;
    }
""")
button.clicked.connect(add_task)
"""Menu Button"""
menu=QPushButton(central)
menu.setCursor(Qt.PointingHandCursor)
menu.setObjectName("menuButton")
menu.setGeometry(284.4,12.1,40,40)
menu.setStyleSheet("""
#menuButton {
    border-radius: 20px;
    background-image: url('main/menu.png');
    background-repeat: no-repeat;
    background-position: center; 
    }
#menuButton:hover {
    background-image: url('main/menuHover.png');
    background-repeat: no-repeat;
    background-position: center; 
    }
#menuButton:pressed {
    background-image: url('main/menuClick.png');
    background-repeat: no-repeat;
    background-position: center;                   
    }
""")

def open_menu():
    dialog = QDialog(window)  # parent = main window
    dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.Popup)
    dialog.setAttribute(Qt.WA_TranslucentBackground)
    dialog.setFixedSize(250, 300)

    #Main container
    container = QWidget(dialog)
    container.setStyleSheet("""
        QWidget {
            background-color: #feffd3;
            border-radius: 20px;
        }
    """)
    layout = QVBoxLayout(container)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(10)

    #(title + close)
    top_bar = QHBoxLayout()
    top_bar.setContentsMargins(0, 0, 0, 0)

    title = QLabel("       Hi there! :)")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("""
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: #903375;
        }
    """)

    close_btn = QPushButton()
    close_btn.setFixedSize(24, 24)
    close_btn.setCursor(Qt.PointingHandCursor)
    close_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            background-image: url('del/clear.png');
            background-repeat: no-repeat;
            background-position: center;
            border: none;
        }
    """)
    close_btn.clicked.connect(lambda: (dialog.close(), globals().__setitem__('dialog', None)))

    top_bar.addWidget(title, 1, Qt.AlignCenter)   # center title
    top_bar.addWidget(close_btn, 0, Qt.AlignRight)  
    layout.addLayout(top_bar)


    description = QLabel("Hi, I’m Nasrou — a medical student who loves coding.\n \nPlease check this links 👇")
    description.setWordWrap(True)
    description.setAlignment(Qt.AlignCenter)
    description.setStyleSheet("""
        QLabel {
            font-size: 12px;
            color: black;
        }
    """)
    layout.addWidget(description)

    layout.addStretch()  # push buttons down

    #Social media buttons
    def make_button(url, color, image):
        btn = QPushButton()
        btn.setFixedSize(120, 30)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                background-image: url({image});
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: #6a1a33;
            }}
        """)
        btn.clicked.connect(lambda: webbrowser.open(url))
        return btn

    github_btn = make_button("https://github.com/nasrouDEV", "#E5E6E3", "socials/github.png")
    youtube_btn = make_button("https://youtube.com/@Sahraoui_Nasreddine", "#FFFFFF", "socials/youtube.png")
    twitter_btn = make_button("https://www.instagram.com/nasrou_sahraoui/", "#FF5F38", "socials/instagram.png")

    # keep them at bottom center
    socials = QVBoxLayout()
    socials.setAlignment(Qt.AlignCenter)
    socials.addWidget(github_btn)
    socials.addWidget(youtube_btn)
    socials.addWidget(twitter_btn)
    layout.addLayout(socials)


    main_layout = QVBoxLayout(dialog)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.addWidget(container)

    parent_rect = window.geometry()
    x = parent_rect.x() + (parent_rect.width() - dialog.width()) // 2
    y = parent_rect.y() + (parent_rect.height() - dialog.height()) // 2
    dialog.move(x, y)
    
    menu_sound.play()
    mute_button = QPushButton("🔊", menu)   # default: sound on
    mute_button.setGeometry(10, 10, 40, 40)  # top-left corner
    mute_button.setCheckable(True)
    def toggle_mute():
        global is_muted
        is_muted = not is_muted
        mute_button.setText("🔇" if is_muted else "🔊")

    mute_button.clicked.connect(toggle_mute)
    dialog.show()
    dialog.activateWindow()
    dialog.setFocus()

# Connect menu button
menu.clicked.connect(open_menu)




""" TASK ENTRY """

entry=QLineEdit(central)
entry.setObjectName('taskEntry')
entry.setGeometry(15,354.2,287,30)
entry.setPlaceholderText('Type something...')
entry.lower()
entry.setMaxLength(35)
entry.setGraphicsEffect(effect1)
entry.setStyleSheet("""
#taskEntry{
    border-radius: 15px;
    color: black;
    font-size: 12px;
    font-family: 'Canva Sans';
    background-color: white;
    selection-color: yellow;
    selection-background-color: #FF6085;
    padding-left: 10px;
}
""")
entry.returnPressed.connect(add_task)
""" TITLE LABEL """
label = QLabel(central)
label.setGeometry(7.8,8.4,239.7,64.6)
label.setObjectName("titleLabel")
label.setStyleSheet("""
#titleLabel {
    background-image: url('main/heading.png');
    background-repeat: no-repeat;
    background-position: center;
    }
""")
""" DATE LABEL """
current_time = datetime.now()
time_label = QLabel(central)
time_label.setGeometry(15,10,150,20)
time_label.setText(current_time.strftime("%A, %d %B %Y"))
time_label.setObjectName("dateLabel")
time_label.setStyleSheet("""
#dateLabel {
    color: black;
    font-size: 10px;
    font-family: 'Libre Baskerville';
    background: transparent;
    }

""")

""" Scrollbar label """
scrollLabel = QWidget(central)
scrollLabel.setGeometry(316.5,68,25.1,266.4)
scrollLabel.setObjectName("scroller")
scrollLabel.lower()
scrollLabel.setStyleSheet("""
#scroller{
    background-image: url('main/scrollBarLabel.png');
    background-position: center ;
    background-repeat: no-repeat ; 
                          
                          }


""")

""" creating a list widget to hold tasks """
list_widget = QListWidget(central)
list_widget.setGeometry(13, 95, 320,213) # height is 230
list_widget.setObjectName("taskList")
list_widget.setStyleSheet("""
QListWidget {
    background: transparent;
    border: none;
    outline: 0;
}
QListWidget::item:selected {
    background: transparent;
}
QListWidget::item:hover {
    background: transparent;
}
QScrollBar:vertical {
    background: #8d3072;
    border: none;
    width: 8px;
    margin: 4px 0 4px 0;
    border-radius: 6px; /* rounded background edges */
}

QScrollBar::handle:vertical {
    background: white;
    min-height: 20px;
    border-radius: 4px; /* rounded scroller */
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: none;
    border: none;
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

""")
suppress_save = False
def save_tasks():
    if suppress_save:
        return
    data = []
    for i in range(list_widget.count()):
        item = list_widget.item(i)
        row = list_widget.itemWidget(item)
        if not row:
            continue
        label = row.findChild(QLabel, "label")
        checkbox = row.findChild(QCheckBox, "checkbox")
        text = label.text() if label else ""
        checked = True if (checkbox and checkbox.checkState() == Qt.Checked) else False
        data.append({"text": text, "checked": checked})
    try:
        with open(Task_File, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

orig_add = add_task

def add_task_wrapper():
    orig_add()
    if not suppress_save:
        last_index = list_widget.count() - 1
        if last_index >= 0:
            item = list_widget.item(last_index)
            row = list_widget.itemWidget(item)
            if row:
                checkbox = row.findChild(QCheckBox, "checkbox")
                if checkbox:
                    checkbox.stateChanged.connect(lambda *_: save_tasks())
        save_tasks()

try:
    button.clicked.disconnect()
except Exception:
    pass
button.clicked.connect(add_task_wrapper)
try:
    entry.returnPressed.disconnect()
except Exception:
    pass
entry.returnPressed.connect(add_task_wrapper)

list_widget.model().rowsRemoved.connect(lambda *args: save_tasks())

def load_tasks():
    global suppress_save
    suppress_save = True
    if os.path.exists(Task_File):
        try:
            with open(Task_File, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        for t in data:
            entry.setText(t.get("text", ""))
            orig_add()
            if list_widget.count() > 0:
                item = list_widget.item(list_widget.count() - 1)
                row = list_widget.itemWidget(item)
                if row:
                    chk = row.findChild(QCheckBox, "checkbox")
                    if chk:
                        chk.stateChanged.connect(lambda *_: save_tasks())
                        if t.get("checked", False):
                            # set state without emitting signals to avoid playing sounds
                            chk.blockSignals(True)
                            chk.setCheckState(Qt.Checked)
                            chk.blockSignals(False)
                            # apply strike-through style manually
                            lbl = row.findChild(QLabel, "label")
                            if lbl:
                                lbl.setStyleSheet("text-decoration: line-through; color: grey;")
        entry.clear()
    suppress_save = False
    save_tasks()

load_tasks()
window.show()
app.exec()

# my color picker 
"#a7c8d4"
