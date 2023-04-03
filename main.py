# qemUI - Interface for Qemu
# Nick Roussis (Neek8044)
# https://github.com/neek8044/qemUI
# This project is licensed under Apache License 2.0. See the LICENSE file (https://github.com/neek8044/qemUI/blob/master/LICENSE) for more information.


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QCheckBox, QMessageBox, QFileDialog
import os, sys, time
import subprocess

debug = True


# Exit
def exit():
    sys.exit(app.exec_())

# Start Qemu process
def start_virtual_machine():
    try:
        number_of_cores = int(txt_number_of_cores.text())
        memory_in_mb = int(txt_memory_mb.text())
        enable_kvm = chk_enable_kvm.isChecked()
        cpu_host = chk_cpu_host.isChecked()

        hda = vm_disk_file[0]
        try:
            cdrom = cdrom_image_file[0]
        except:
            msg_cdrom_warning = QMessageBox()
            msg_cdrom_warning.setWindowTitle("No CD-ROM")
            msg_cdrom_warning.setText("No CD-ROM (.iso) was selected. QEMU will start without one.")
            msg_cdrom_warning.exec()
            cdrom = ''

        qemu_command = f"qemu-system-x86_64 {'-enable-kvm' if enable_kvm else ''} {'-cpu host' if cpu_host else ''} -smp {number_of_cores} -m {memory_in_mb} -hda {hda} {'-cdrom' if cdrom != '' else ''} {cdrom}"

        print(qemu_command if debug else "\r")
        subprocess.Popen(
            qemu_command,
            shell=True,
            cwd=os.getcwd(),
            stderr=subprocess.STDOUT,
            stdout=(None if debug else subprocess.DEVNULL)
        )
        

    except ValueError:
        msg_value_error = QMessageBox()
        msg_value_error.setWindowTitle("Value Error")
        msg_value_error.setText("Integer-only text box received text/string as input.")
        msg_value_error.exec()
    
    except IndexError:
        msg_index_error = QMessageBox()
        msg_index_error.setWindowTitle("Index Error")
        msg_index_error.setText("Please fill up the whole form before starting QEMU.")
        msg_index_error.exec()


# Open HDA file
def open_vm_disk_file():
    global vm_disk_file
    global txt_vm_disk_file
    vm_disk_file = QFileDialog.getOpenFileName(caption="Open Virtual Disk File", directory="", filter="All Files (*)")
    txt_vm_disk_file.setText(vm_disk_file[0])


# Open CD-ROM file
def open_cdrom_image_file():
    global cdrom_image_file
    global txt_cdrom_image_file
    cdrom_image_file = QFileDialog.getOpenFileName(caption="Open CD-ROM Image File", directory="", filter="All Files (*)")
    txt_cdrom_image_file.setText(cdrom_image_file[0])



# Defaults for Qemu
enable_kvm = True
number_of_cores = 1
memory_in_mb = 128
vm_disk_file = ""
cdrom_image_file = ""


# Qt5 Initialization
app = QApplication(sys.argv)
win = QMainWindow()
xpos, ypos = 100, 100
width, height = 720, 420
win.setGeometry(xpos, ypos, width, height)
win.setWindowTitle("qemUI - Interface for Qemu")
win.setFixedSize(width, height)


# Qt5 Widgets
lbl_machine_settings = QLabel(win, text="Machine Settings")
lbl_machine_settings.setGeometry(30, 30, 150, 20)

lbl_number_of_cores = QLabel(win, text="Amount of CPU cores")
lbl_number_of_cores.setGeometry(50, 60, 150, 20)

txt_number_of_cores = QLineEdit(win)
txt_number_of_cores.setText(str(number_of_cores))
txt_number_of_cores.move(220, 55)

lbl_memory_mb = QLabel(win, text="RAM memory allocation")
lbl_memory_mb.setGeometry(50, 100, 150, 20)

txt_memory_mb = QLineEdit(win)
txt_memory_mb.setText(str(memory_in_mb))
txt_memory_mb.move(220, 95)

lbl_arguments = QLabel(win, text="Arguments")
lbl_arguments.setGeometry(480, 30, 150, 20)

chk_enable_kvm = QCheckBox(win, text="-enable-kvm")
chk_enable_kvm.move(500, 60)
chk_enable_kvm.setChecked(True)

chk_cpu_host = QCheckBox(win, text="-cpu host")
chk_cpu_host.move(500, 90)

txt_vm_disk_file = QLineEdit(win)
txt_vm_disk_file.setReadOnly(True)
txt_vm_disk_file.setText("Nothing Selected (file type example: .img)")
txt_vm_disk_file.setGeometry(35, 200, 460, 35)

btn_vm_disk_file = QPushButton(win, text="Select Virtual Disk File")
btn_vm_disk_file.setGeometry(505, 200, 180, 35)
btn_vm_disk_file.clicked.connect(open_vm_disk_file)


txt_cdrom_image_file = QLineEdit(win)
txt_cdrom_image_file.setReadOnly(True)
txt_cdrom_image_file.setText("Nothing Selected (file type example: .iso)")
txt_cdrom_image_file.setGeometry(35, 260, 460, 35)

btn_cdrom_image_file = QPushButton(win, text="Select CD-ROM Image File")
btn_cdrom_image_file.setGeometry(505, 260, 180, 35)
btn_cdrom_image_file.clicked.connect(open_cdrom_image_file)


btn_start_vm = QPushButton(win, text="Start QEMU")
btn_start_vm.setGeometry(round(width/2-width/3), round(height/2+height/3), round(width/2), 50)
btn_start_vm.clicked.connect(start_virtual_machine)

btn_start_vm = QPushButton(win, text="Exit")
btn_start_vm.setGeometry(round(width/2+width/5), round(height/2+height/3), round(width/8), 50)
btn_start_vm.clicked.connect(exit)


# Mainloop
win.show()
exit()
