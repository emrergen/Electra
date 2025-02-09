import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
import os
import re
from collections import defaultdict
import base64
from PyQt5.QtGui import QIcon, QPixmap
from io import BytesIO

ICON_BASE64 = b"""
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAIAAABMXPacAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAE
uGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0w
TXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRh
Lyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYt
c3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRy
aWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgog
ICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxB
dHRyaWI6Q3JlYXRlZD4yMDI1LTAyLTA5PC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkV4
dElkPjJhN2ZjOTEwLTFmMzMtNGFiYy04MTVjLWU1OTM0OTk5ODc3MTwvQXR0cmliOkV4dElkPgog
ICAgIDxBdHRyaWI6RmJJZD41MjUyNjU5MTQxNzk1ODA8L0F0dHJpYjpGYklkPgogICAgIDxBdHRy
aWI6VG91Y2hUeXBlPjI8L0F0dHJpYjpUb3VjaFR5cGU+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6
U2VxPgogIDwvQXR0cmliOkFkcz4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRp
b24gcmRmOmFib3V0PScnCiAgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8x
LjEvJz4KICA8ZGM6dGl0bGU+CiAgIDxyZGY6QWx0PgogICAgPHJkZjpsaSB4bWw6bGFuZz0neC1k
ZWZhdWx0Jz5ST1MyIFBhY2thZ2UgQ3JlYXRvciAtIDE8L3JkZjpsaT4KICAgPC9yZGY6QWx0Pgog
IDwvZGM6dGl0bGU+CiA8L3JkZjpEZXNjcmlwdGlvbj4KCiA8cmRmOkRlc2NyaXB0aW9uIHJkZjph
Ym91dD0nJwogIHhtbG5zOnBkZj0naHR0cDovL25zLmFkb2JlLmNvbS9wZGYvMS4zLyc+CiAgPHBk
ZjpBdXRob3I+U2FpZCBFbXJlIEVyZ2VuPC9wZGY6QXV0aG9yPgogPC9yZGY6RGVzY3JpcHRpb24+
CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczp4bXA9J2h0dHA6Ly9ucy5h
ZG9iZS5jb20veGFwLzEuMC8nPgogIDx4bXA6Q3JlYXRvclRvb2w+Q2FudmEgZG9jPURBR2VveENf
VmpvIHVzZXI9VUFFcGh6ZkgzVU0gYnJhbmQ9QkFFcGh3SEd6cjggdGVtcGxhdGU9PC94bXA6Q3Jl
YXRvclRvb2w+CiA8L3JkZjpEZXNjcmlwdGlvbj4KPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KPD94
cGFja2V0IGVuZD0ncic/Pgy7fuAAACAASURBVHic7X0HXFNpuvfu/r5v795v7+7dvd/u/XZn9+6O
U1dHZ3acceyVKoplFB0VdUZRsQuiggUFxYpixYKKDURAmvQSShICSQhJSIP03ntCEgjwPScHMoiI
OOPsFDm/5wfJyXve877P/6lvOednPW73CH2P9LPvvQWvOY0AMALA600jAIwA8HrTCAAjALzeNALA
CACvN40AMALA600jAIwA8HrTCAAjALzeNALACACvN40A8IMFoLNzWOQtPPy7Dr/a51B3Z2d3RwdC
g5YcZssHtP8btWTwW78CALq6eoZ5oOXh6O4e1i2h2EvV/DTTB7+8q+trMIZfv/cuw+gscvfhcBa9
+7cFoKur0+HQiCVqkWgIUgmFWqm0pxNhjUYsdlqtL8agq8tls2mGrBat2aBQDOA+MAFhtculFgo5
jcRmTDW1pqaN3AQlu5BfUT51W7RalUAwoEJoHtCg93I7nR12+xCNMcgVTputl7NDY9DdbVKrdVJZ
97cBwNPVHmBB3MpVcStWxoeujl8V+iwdDV19ePkX57fv6OrogPbFrVzZgsUiDAIhfc6dEPnt6QGW
HVoaMmidvTWvXgMFUo/EeZW626NhOpks/9r1k+vDoFVw9xPr1h//ah00D74mbgrPTU4WM1lQrDAl
Zf+ixcdWr+lfJ5SB1g64EXQQ/hqUSgGdfnDJ0ue15wgwYVXo7cNHoBiqCoN0zcM0i053ct36A58v
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
gk5ijjdCAAAAAElFTkSuQmCC
"""

def get_icon():
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(ICON_BASE64))
    return QIcon(pixmap)

def convert_to_lowercase_with_underscore(name):
    # Convert to lowercase and add underscores before each uppercase letter (except the first one)
    name_with_underscores = re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()
    return name_with_underscores

def create_ros2_package(package_name,package_description, maintainer, email, class_name, publishers_info, subscribers_info, timer_callbacks_info):
    base_dir = os.getcwd()

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # PyInstaller tarafından geçici dizine taşınan dosyalar
    else:
        base_path = os.path.abspath(".")  # Normal geliştirme modunda
    template_dir = os.path.join(base_path, "templates")
    # template_dir = os.path.join(base_dir, "templates")
    package_dir = os.path.join(base_dir, package_name)
    include_dir = os.path.join(package_dir, "include", package_name)
    src_dir = os.path.join(package_dir, "src")
    config_dir = os.path.join(package_dir, "config")
    launch_dir = os.path.join(package_dir, "launch")
    
    os.makedirs(include_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(launch_dir, exist_ok=True)
    
    def generate_file(template_name, output_path, replacements):
        with open(os.path.join(template_dir, template_name), "r") as template_file:
            content = template_file.read()
        for key, value in replacements.items():
            content = content.replace(f"{{{key}}}", value)
        with open(output_path, "w") as output_file:
            output_file.write(content)

    subscriber_count = defaultdict(int)
    publisher_count = defaultdict(int)

    # Create the dynamic 
    package_name_upper = package_name.upper()
    subscribers_hpp = ""
    subscriber_callbacks_hpp = ""
    subscribers_cpp = ""
    subscriber_callbacks_cpp = ""
    publishers_hpp = ""
    publishers_cpp = ""
    timers_hpp = ""
    timer_callbacks_hpp = ""
    timers_cpp = ""
    timer_callbacks_cpp = ""
    variables_hpp = ""
    msgs = ""
    depend_msgs_xml = ""
    find_package_msgs = ""
    header_include_msgs = ""
    publishers_readme = ""
    subscribers_readme = ""
    

    for topic, msg_lib, msg_type in publishers_info:
        base_name = msg_type.lower()  
        count = publisher_count[msg_type]  
        publisher_count[msg_type] += 1  
        unique_name = f"{base_name}_{count}" if count > 0 else base_name

        publishers_hpp += f"    rclcpp::Publisher<{msg_lib}::msg::{msg_type}>::SharedPtr {unique_name}_publisher;\n"
        publishers_cpp += f"    {unique_name}_publisher = this->create_publisher<{msg_lib}::msg::{msg_type}>(\"{topic}\", 10);\n"
        msgs += f"{msg_lib}\n"
        depend_msgs_xml += f"  <depend>{msg_lib}</depend>\n"
        find_package_msgs += f"find_package({msg_lib} REQUIRED)\n"
        header_include_msgs += f"#include <{msg_lib}/msg/{convert_to_lowercase_with_underscore(msg_type)}.hpp>\n"
        publishers_readme += f"| {unique_name}_publisher | \"{topic}\" | {msg_lib}::msg::{msg_type} |\n"
    
    for topic, msg_lib, msg_type in subscribers_info:
        base_name = msg_type.lower()  
        count = subscriber_count[msg_type]  
        subscriber_count[msg_type] += 1  
        unique_name = f"{base_name}_{count}" if count > 0 else base_name

        subscribers_hpp += f"    rclcpp::Subscription<{msg_lib}::msg::{msg_type}>::SharedPtr {unique_name}_subscription;\n"
        subscriber_callbacks_hpp += f"    void {unique_name}_callback(const {msg_lib}::msg::{msg_type}::ConstSharedPtr &msg);\n"
        subscribers_cpp += f"    {unique_name}_subscription = this->create_subscription<{msg_lib}::msg::{msg_type}>(\"{topic}\", 10, std::bind(&{class_name}::{unique_name}_callback, this, std::placeholders::_1));\n"
        subscriber_callbacks_cpp += f"  void {class_name}::{unique_name}_callback(const {msg_lib}::msg::{msg_type}::ConstSharedPtr &msg) \n  {{\n"
        subscriber_callbacks_cpp += f"    RCLCPP_INFO(this->get_logger(), \"Received message on {topic}\");\n"
        subscriber_callbacks_cpp += f"    recived_{unique_name}_msg = msg;\n"
        subscriber_callbacks_cpp += f"  }}\n\n"
        msgs += f"{msg_lib}\n"
        depend_msgs_xml += f"  <depend>{msg_lib}</depend>\n"
        find_package_msgs += f"find_package({msg_lib} REQUIRED)\n"
        header_include_msgs += f"#include <{msg_lib}/msg/{convert_to_lowercase_with_underscore(msg_type)}.hpp>\n"
        variables_hpp += f"    {msg_lib}::msg::{msg_type}::ConstSharedPtr recived_{unique_name}_msg;\n"
        subscribers_readme += f"| {unique_name}_subscription | \"{topic}\" | {msg_lib}::msg::{msg_type} |\n"

        
    
    for timer_callback in timer_callbacks_info:
        timers_hpp += f"    rclcpp::TimerBase::SharedPtr {timer_callback}_;\n"
        timer_callbacks_hpp += f"    void {timer_callback}_callback();\n"
        timers_cpp += f"    {timer_callback}_ = this->create_wall_timer(std::chrono::milliseconds(1000), std::bind(&{class_name}::{timer_callback}_callback, this));\n"
        timer_callbacks_cpp += f"  void {class_name}::{timer_callback}_callback() \n  {{\n    // TODO: Implement the callback\n  }}\n\n"


    # check msgs if there are any duplicates in the list delete some of them
    msgs_list = msgs.split("\n")
    msgs = ""
    for i in range(len(msgs_list)):
        if msgs_list[i] not in msgs_list[:i]:
            msgs += msgs_list[i] + "\n"

    
    # check depend_msgs_xml if there are any duplicates in the list delete some of them
    depend_msgs_xml_list = depend_msgs_xml.split("\n")
    depend_msgs_xml = ""
    for i in range(len(depend_msgs_xml_list)):
        if depend_msgs_xml_list[i] not in depend_msgs_xml_list[:i]:
            depend_msgs_xml += depend_msgs_xml_list[i] + "\n"


    # check find_package_msgs if there are any duplicates in the list delete some of them
    find_package_msgs_list = find_package_msgs.split("\n")
    find_package_msgs = ""
    for i in range(len(find_package_msgs_list)):
        if find_package_msgs_list[i] not in find_package_msgs_list[:i]:
            find_package_msgs += find_package_msgs_list[i] + "\n"


    # check header_include_msgs if there are any duplicates in the list delete some of them
    header_include_msgs_list = header_include_msgs.split("\n")
    header_include_msgs = ""
    for i in range(len(header_include_msgs_list)):
        if header_include_msgs_list[i] not in header_include_msgs_list[:i]:
            header_include_msgs += header_include_msgs_list[i] + "\n"

    
    # Generate the C++ logic for the class (including dynamic publishers/subscribers)
    replacements = {
        "package_name": package_name,
        "package_name_upper": package_name_upper,
        "package_description": package_description,
        "maintainer": maintainer,
        "email": email,
        "class_name": class_name,
        "subscribers_hpp": subscribers_hpp,
        "subscriber_callbacks_hpp": subscriber_callbacks_hpp,
        "subscribers_cpp": subscribers_cpp,
        "subscriber_callbacks_cpp": subscriber_callbacks_cpp,
        "publishers_hpp": publishers_hpp,
        "publishers_cpp": publishers_cpp,
        "timers_hpp": timers_hpp,
        "timer_callbacks_hpp": timer_callbacks_hpp,
        "timers_cpp": timers_cpp,
        "timer_callbacks_cpp": timer_callbacks_cpp,
        "variables_hpp": variables_hpp,
        "msgs": msgs,
        "depend_msgs_xml": depend_msgs_xml,
        "find_package_msgs": find_package_msgs,
        "header_include_msgs": header_include_msgs,
        "publishers_readme": publishers_readme,
        "subscribers_readme": subscribers_readme
    }

    # Generate CMakeLists.txt, package.xml, and C++ files with dynamic content
    generate_file("CMakeLists.txt.template", os.path.join(package_dir, "CMakeLists.txt"), replacements)
    generate_file("package.xml.template", os.path.join(package_dir, "package.xml"), replacements)
    generate_file("package.hpp.template", os.path.join(include_dir, f"{package_name}.hpp"), replacements)
    generate_file("package.cpp.template", os.path.join(src_dir, f"{package_name}.cpp"), replacements)
    generate_file("package.launch.xml.template", os.path.join(launch_dir, f"{package_name}.launch.xml"), replacements)
    generate_file("package.param.yaml.template", os.path.join(config_dir, f"{package_name}.param.yaml"), replacements)
    generate_file("README.md.template", os.path.join(package_dir, "README.md"), replacements)

    def clean_extra_blank_lines(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

        cleaned_lines = []
        blank_line = False

        for line in lines:
            if line.strip() == "":
                if not blank_line:
                    cleaned_lines.append(line)
                    blank_line = True
            else:
                cleaned_lines.append(line)
                blank_line = False

        with open(file_path, "w") as file:
            file.writelines(cleaned_lines)

    # Clean all generated files
    for root, _, files in os.walk(package_dir):
        for file in files:
            file_path = os.path.join(root, file)
            clean_extra_blank_lines(file_path)



class ROS2PackageCreator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ELECTRA")
        self.setGeometry(100, 100, 750, 900)
        self.setMinimumSize(750, 900)
        self.setWindowIcon(get_icon())

        # Dark mode styles
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QTableWidget {
                background-color: #3C3C3C;
                color: #FFFFFF;
                gridline-color: #4A4A4A;
            }
            QTableWidget::item {
                border: 1px solid #141414;
            }
            QPushButton {
                background-color: #4C4C4C;
                color: #FFFFFF;
                border: 1px solid #6A6A6A;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2F5C8F;
            }
            QLabel {
                font-size: 16px;
            }
        """)

        # Initialize UI elements
        self.layout = QVBoxLayout()
        self.image_label = QLabel(self)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # PyInstaller tarafından geçici dizine taşınan dosyalar
        else:
            base_path = os.path.abspath(".")  # Normal geliştirme modunda
        template_dir = os.path.join(base_path, "data")
        banner_dir = os.path.join(template_dir, "banner.png")
        pixmap = QPixmap(banner_dir)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.form_layout = QFormLayout()

        self.layout.addSpacing(20)

        # Input fields for package info (without spaces in labels except for Description and Maintainer)
        self.package_name_input = QLineEdit()
        self.package_description_input = QLineEdit()
        self.maintainer_input = QLineEdit()
        self.email_input = QLineEdit()
        self.class_name_input = QLineEdit()

        # Set default values for input fields
        self.package_name_input.setText("aesk_electra")
        self.package_description_input.setText("Example ROS2 package")
        self.maintainer_input.setText("Said Emre Ergen")
        self.email_input.setText("saidemreergenp@gmail.com")
        self.class_name_input.setText("Electra")

        # Modify labels to ensure no spaces in titles (except for Description and Maintainer)
        self.form_layout.addRow("PackageName:", self.package_name_input)
        self.form_layout.addRow("PackageDescription:", self.package_description_input)
        self.form_layout.addRow("Maintainer:", self.maintainer_input)
        self.form_layout.addRow("Email:", self.email_input)
        self.form_layout.addRow("ClassName:", self.class_name_input)

        self.layout.addLayout(self.form_layout)
        self.layout.addSpacing(20)

        # Section for Publishers Table
        self.publisher_layout = QVBoxLayout()
        self.publisher_table = QTableWidget()
        self.publisher_table.setColumnCount(4)
        self.publisher_table.setHorizontalHeaderLabels(["Topic", "Message Library", "Message Type", "Actions"])

        self.publisher_table.setColumnWidth(0, 200)  # Topic column
        self.publisher_table.setColumnWidth(1, 150)  # Message Library column
        self.publisher_table.setColumnWidth(2, 150)  # Message Type column
        self.publisher_table.setColumnWidth(3, 50)  # Actions column

        # Make the columns resizable
        self.publisher_table.horizontalHeader().setSectionResizeMode(0, 1)  # Allow resize
        self.publisher_table.horizontalHeader().setSectionResizeMode(1, 2)  # Allow resize
        self.publisher_table.horizontalHeader().setSectionResizeMode(2, 1)  # Allow resize
        self.publisher_table.horizontalHeader().setSectionResizeMode(3, 3)  # Allow resize

        # Set default values for the publisher table
        self.publisher_table.setRowCount(1)
        self.publisher_table.setItem(0, 0, QTableWidgetItem("/string_pub_topic"))
        self.publisher_table.setItem(0, 1, QTableWidgetItem("std_msgs"))
        self.publisher_table.setItem(0, 2, QTableWidgetItem("String"))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda row=0: self.delete_row(self.publisher_table, row))
        self.publisher_table.setCellWidget(0, 3, delete_button)

        # Add Publisher Header and button
        self.publisher_header = QLabel("Publishers")
        self.publisher_header.setAlignment(Qt.AlignCenter)
        self.publisher_layout.addWidget(self.publisher_header)
        self.publisher_layout.addWidget(self.publisher_table)

        self.add_publisher_button = QPushButton("Add Publisher")
        self.add_publisher_button.clicked.connect(self.add_publisher)
        self.publisher_layout.addWidget(self.add_publisher_button)

        # Add a space between Publisher and Subscriber sections
        self.publisher_layout.addSpacing(20)

        # Section for Subscribers Table
        self.subscriber_layout = QVBoxLayout()
        self.subscriber_table = QTableWidget()
        self.subscriber_table.setColumnCount(4)
        self.subscriber_table.setHorizontalHeaderLabels(["Topic", "Message Library", "Message Type", "Actions"])
    
        self.subscriber_table.setColumnWidth(0, 200)  # Topic column
        self.subscriber_table.setColumnWidth(1, 150)  # Message Library column
        self.subscriber_table.setColumnWidth(2, 150)  # Message Type column
        self.subscriber_table.setColumnWidth(3, 50)  # Actions column

        # Make the columns resizable
        self.subscriber_table.horizontalHeader().setSectionResizeMode(0, 1)  # Allow resize
        self.subscriber_table.horizontalHeader().setSectionResizeMode(1, 2)  # Allow resize
        self.subscriber_table.horizontalHeader().setSectionResizeMode(2, 1)  # Allow resize
        self.subscriber_table.horizontalHeader().setSectionResizeMode(3, 3)  # Allow resize

        # Set default values for the subscriber table
        self.subscriber_table.setRowCount(1)
        self.subscriber_table.setItem(0, 0, QTableWidgetItem("/string_sub_topic"))
        self.subscriber_table.setItem(0, 1, QTableWidgetItem("std_msgs"))
        self.subscriber_table.setItem(0, 2, QTableWidgetItem("String"))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda row=0: self.delete_row(self.subscriber_table, row))
        self.subscriber_table.setCellWidget(0, 3, delete_button)

        # Add Subscriber Header and button
        self.subscriber_header = QLabel("Subscribers")
        self.subscriber_header.setAlignment(Qt.AlignCenter)
        self.subscriber_layout.addWidget(self.subscriber_header)
        self.subscriber_layout.addWidget(self.subscriber_table)

        self.add_subscriber_button = QPushButton("Add Subscriber")
        self.add_subscriber_button.clicked.connect(self.add_subscriber)
        self.subscriber_layout.addWidget(self.add_subscriber_button)

        # Add a space between Subscriber and Timer sections
        self.subscriber_layout.addSpacing(20)

        # Section for Timers Table
        self.timer_layout = QVBoxLayout()
        self.timer_table = QTableWidget()
        self.timer_table.setColumnCount(2)
        self.timer_table.setHorizontalHeaderLabels(["Timer Callback", "Actions"])

        self.timer_table.setColumnWidth(0, 500)  # Timer Callback column
        self.timer_table.setColumnWidth(1, 210)  # Actions column
        self.subscriber_table.horizontalHeader().setSectionResizeMode(0, 1)  # Allow resize
        self.subscriber_table.horizontalHeader().setSectionResizeMode(1, 2)  # Allow resize

        # Set default values for the timer table
        self.timer_table.setRowCount(1)
        self.timer_table.setItem(0, 0, QTableWidgetItem("timer"))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda row=0: self.delete_row(self.timer_table, row))
        self.timer_table.setCellWidget(0, 1, delete_button)

        # Add Timer Header and button
        self.timer_header = QLabel("Timers")
        self.timer_header.setAlignment(Qt.AlignCenter)
        self.timer_layout.addWidget(self.timer_header)
        self.timer_layout.addWidget(self.timer_table)

        self.add_timer_button = QPushButton("Add Timer")
        self.add_timer_button.clicked.connect(self.add_timer)
        self.timer_layout.addWidget(self.add_timer_button)

        # Add all sections to the main layout
        self.layout.addLayout(self.publisher_layout)
        self.layout.addLayout(self.subscriber_layout)
        self.layout.addLayout(self.timer_layout)

        self.layout.addSpacing(20)

        # Add start button
        self.start_button = QPushButton("CREATE")
        self.start_button.clicked.connect(self.start_package_creation)
        self.layout.addWidget(self.start_button)

        # Set layout for the main window
        self.setLayout(self.layout)

    def add_publisher(self):
        row_position = self.publisher_table.rowCount()
        self.publisher_table.insertRow(row_position)
        self.publisher_table.setItem(row_position, 0, QTableWidgetItem("/string_pub_topic"))
        self.publisher_table.setItem(row_position, 1, QTableWidgetItem("std_msgs"))
        self.publisher_table.setItem(row_position, 2, QTableWidgetItem("String"))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda row=row_position: self.delete_row(self.publisher_table, row))
        self.publisher_table.setCellWidget(row_position, 3, delete_button)


    def add_subscriber(self):
        row_position = self.subscriber_table.rowCount()
        self.subscriber_table.insertRow(row_position)
        self.subscriber_table.setItem(row_position, 0, QTableWidgetItem("/string_sub_topic"))
        self.subscriber_table.setItem(row_position, 1, QTableWidgetItem("std_msgs"))
        self.subscriber_table.setItem(row_position, 2, QTableWidgetItem("String"))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda row=row_position: self.delete_row(self.subscriber_table, row))
        self.subscriber_table.setCellWidget(row_position, 3, delete_button)

    def add_timer(self):
        row_position = self.timer_table.rowCount()
        self.timer_table.insertRow(row_position)
        self.timer_table.setItem(row_position, 0, QTableWidgetItem("timer_"))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda row=row_position: self.delete_row(self.timer_table, row))
        self.timer_table.setCellWidget(row_position, 1, delete_button)

    def delete_row(self, table, row_position):
        table.removeRow(row_position)

    def start_package_creation(self):
        # Start package creation logic
        print("Package creation started")
        # You can now process the data entered in the form and tables as needed
        package_name = self.package_name_input.text()
        package_description = self.package_description_input.text()
        maintainer = self.maintainer_input.text()
        email = self.email_input.text()
        class_name = self.class_name_input.text()

        # Collect publishers info from the publisher table
        publishers_info = []
        for row in range(self.publisher_table.rowCount()):
            topic = self.publisher_table.item(row, 0).text()
            msg_lib = self.publisher_table.item(row, 1).text()
            msg_type = self.publisher_table.item(row, 2).text()
            publishers_info.append((topic, msg_lib, msg_type))

        # Collect subscribers info from the subscriber table
        subscribers_info = []
        for row in range(self.subscriber_table.rowCount()):
            topic = self.subscriber_table.item(row, 0).text()
            msg_lib = self.subscriber_table.item(row, 1).text()
            msg_type = self.subscriber_table.item(row, 2).text()
            subscribers_info.append((topic, msg_lib, msg_type))

        # Collect timer callbacks info
        timer_callbacks_info = []
        for row in range(self.timer_table.rowCount()):
            timer_callback = self.timer_table.item(row, 0).text()
            timer_callbacks_info.append(timer_callback)

        create_ros2_package(package_name, package_description, maintainer, email, class_name, publishers_info, subscribers_info,timer_callbacks_info)

app = QApplication(sys.argv)
window = ROS2PackageCreator()
window.show()
sys.exit(app.exec_())
