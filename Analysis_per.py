# coding=utf-8
import os, sys
from xml.dom.minidom import parse

#######################################################
# 主要功能：1. 使用Apktool反编译apk文件
#           2. 提取AndroidManifest.xml至manifest文件夹
#           3. 对比activity、receiver、provider组件中使用的权限是否声明或申请
#           4. 保存未声明的权限名及其包名至unclaim.txt文件中
#######################################################
# 使用方法：1.将该代码和所有apk文件放在同一目录
#           2. python3 Analysis_perm.py
######################################################

# desdir = "manifest"
# filepath = "./"
# 解压文件

system_perm = [
                "andriod.permission.ACCESS_CHECKIN_PROPERTIES"
                "android.permission.ACCESS_COARSE_LOCATION"
                "android.permission.ACCESS_FINE_LOCATION"
                "android.permission.ACCESS_LOCATION_EXTRA_COMMANDS"
                "android.permission.ACCESS_NETWORK_STATE"
                "android.permission.ACCESS_NOTIFICATION_POLICY"
                "android.permission.ACCESS_WIFI_STATE"
                "android.permission.ACCOUNT_MANAGER"
                "android.permission.ADD_VOICEMAIL"
                "android.permission.BATTERY_STATS"
                "android.permission.BIND_ACCESSIBILITY_SERVICE"
                "android.permission.BIND_CARRIER_MESSAGING_SERVICE"
                "android.permission.BIND_CARRIER_SERVICES"
                "android.permission.BIND_CHOOSER_TARGET_SERVICE"
                "android.permission.BIND_DEVICE_ADMIN"
                "android.permission.BIND_CONDITION_PROVIDER_SERVICE"
                "android.permission.BIND_DREAM_SERVICE"
                "android.permission.BIND_INCALL_SERVICE"
                "android.permission.BIND_INPUT_METHOD"
                "android.permission.BIND_MIDI_DEVICE_SERVICE"
                "android.permission.BIND_NFC_SERVICE"
                "android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"
                "android.permission.BIND_PRINT_SERVICE"
                "android.permission.BIND_QUICK_SETTINGS_TILE"
                "android.permission.BIND_REMOTEVIEWS"
                "android.permission.BIND_SCREENING_SERVICE"
                "android.permission.BIND_TELECOM_CONNECTION_SERVICE"
                "android.permission.BIND_TEXT_SERVICE"
                "android.permission.BIND_TV_INPUT"
                "android.permission.BIND_VOICE_INTERACTION"
                "android.permission.BIND_VPN_SERVICE"
                "android.permission.BIND_VR_LISTENER_SERVICE"
                "android.permission.BIND_WALLPAPER"
                "android.permission.BLUETOOTH"
                "android.permission.BLUETOOTH_ADMIN"
                "android.permission.BLUETOOTH_PRIVILEGED"
                "android.permission.BODY_SENSORS"
                "android.permission.BROADCAST_PACKAGE_REMOVED"
                "android.permission.BROADCAST_SMS"
                "android.permission.BROADCAST_STICKY"
                "android.permission.BROADCAST_WAP_PUSH"
                "android.permission.CALL_PHONE"
                "android.permission.CALL_PRIVILEGED"
                "android.permission.CAMERA"
                "android.permission.CAPTURE_AUDIO_OUTPUT"
                "android.permission.CAPTURE_SECURE_VIDEO_OUTPUT"
                "android.permission.CAPTURE_VIDEO_OUTPUT"
                "android.permission.CHANGE_COMPONENT_ENABLED_STATE"
                "android.permission.CHANGE_CONFIGURATION"
                "android.permission.CHANGE_NETWORK_STATE"
                "android.permission.CHANGE_WIFI_MULTICAST_STATE"
                "android.permission.CHANGE_WIFI_STATE"
                "android.permission.CLEAR_APP_CACHE"
                "android.permission.CONTROL_LOCATION_UPDATES"
                "android.permission.DELETE_CACHE_FILES"
                "android.permission.DELETE_PACKAGES"
                "android.permission.DIAGNOSTIC"
                "android.permission.DISABLE_KEYGUARD"
                "android.permission.DUMP"
                "android.permission.EXPAND_STATUS_BAR"
                "android.permission.FACTORY_TEST"
                "android.permission.GET_ACCOUNTS"
                "android.permission.GET_ACCOUNTS_PRIVILEGED"
                "android.permission.GET_PACKAGE_SIZE"
                "android.permission.GET_TASKS"
                "android.permission.GLOBAL_SEARCH"
                "android.permission.INSTALL_LOCATION_PROVIDER"
                "android.permission.INSTALL_PACKAGES"
                "android.permission.INSTALL_SHORTCUT"
                "android.permission.INTERNET"
                "android.permission.KILL_BACKGROUND_PROCESSES"
                "android.permission.LOCATION_HARDWARE"
                "android.permission.MANAGE_DOCUMENTS"
                "android.permission.MASTER_CLEAR"
                "android.permission.MEDIA_CONTENT_CONTROL"
                "android.permission.MODIFY_AUDIO_SETTINGS"
                "android.permission.MODIFY_PHONE_STATE"
                "android.permission.MOUNT_FORMAT_FILESYSTEMS"
                "android.permission.MOUNT_UNMOUNT_FILESYSTEMS"
                "android.permission.NFC"
                "android.permission.PACKAGE_USAGE_STATS"
                "android.permission.PERSISTENT_ACTIVITY"
                "android.permission.PROCESS_OUTGOING_CALLS"
                "android.permission.READ_CALENDAR"
                "android.permission.READ_CALL_LOG"
                "android.permission.READ_CONTACTS"
                "android.permission.READ_EXTERNAL_STORAGE"
                "android.permission.READ_FRAME_BUFFER"
                "android.permission.READ_INPUT_STATE"
                "android.permission.READ_LOGS"
                "android.permission.READ_PHONE_STATE"
                "android.permission.READ_SMS"
                "android.permission.READ_SYNC_SETTINGS"
                "android.permission.READ_SYNC_STATS"
                "android.permission.READ_VOICEMAIL"
                "android.permission.REBOOT"
                "android.permission.RECEIVE_BOOT_COMPLETED"
                "android.permission.RECEIVE_MMS"
                "android.permission.RECEIVE_SMS"
                "android.permission.RECEIVE_WAP_PUSH"
                "android.permission.RECORD_AUDIO"
                "android.permission.REORDER_TASKS"
                "android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"
                "android.permission.REQUEST_INSTALL_PACKAGES"
                "android.permission.RESTART_PACKAGES"
                "android.permission.SEND_RESPOND_VIA_MESSAGE"
                "android.permission.SEND_SMS"
                "android.permission.SET_ALARM"
                "android.permission.SET_ALWAYS_FINISH"
                "android.permission.SET_ANIMATION_SCALE"
                "android.permission.SET_DEBUG_APP"
                "android.permission.SET_PREFERRED_APPLICATIONS"
                "android.permission.SET_PROCESS_LIMIT"
                "android.permission.SET_TIME"
                "android.permission.SET_TIME_ZONE"
                "android.permission.SET_WALLPAPER"
                "android.permission.SET_WALLPAPER_HINTS"
                "android.permission.SIGNAL_PERSISTENT_PROCESSES"
                "android.permission.STATUS_BAR"
                "android.permission.SYSTEM_ALERT_WINDOW"
                "android.permission.TRANSMIT_IR"
                "android.permission.UNINSTALL_SHORTCUT"
                "android.permission.UPDATE_DEVICE_STATS"
                "android.permission.USE_FINGERPRINT"
                "android.permission.USE_SIP"
                "android.permission.VIBRATE"
                "android.permission.WAKE_LOCK"
                "android.permission.WRITE_APN_SETTINGS"
                "android.permission.WRITE_CALENDAR"
                "android.permission.WRITE_CALL_LOG"
                "android.permission.WRITE_CONTACTS"
                "android.permission.WRITE_EXTERNAL_STORAGE"
                "android.permission.WRITE_GSERVICES"
                "android.permission.WRITE_SECURE_SETTINGS"
                "android.permission.WRITE_SETTINGS"
                "android.permission.WRITE_SYNC_SETTINGS"
                "android.permission.WRITE_VOICEMAIL"
    ]

def unpackage():
    # 遍历当前目录
    fileNames = os.listdir("./")
    for f in fileNames:
        if f[-4:] == ".apk":
            os.system("apktool d -f " + f) # apk反编译
    # 删除空文件夹
    #os.system("find . -type d -empty -delete")

#修改名称提取至manifest文件夹
def rename_and_extract(filepath, desdir):
    #遍历当前目录
    files = os.listdir(filepath)
    for file in files:
        if (os.path.isdir(file)):
            os.chdir(file) # 进入该目录
            if os.path.exists("AndroidManifest.xml"):
                os.system("cp AndroidManifest.xml " + file + ".xml" + " && mv " + file  + ".xml" + " " + desdir) # 复制并重命名该xml文件至manifest
            os.chdir("./..")

def Analysis_perm():
    permissions = {"uses-permission", "permission"}
    compents = {"activity", "provider", "receiver"}
    results = {}
    all_per = []
    unclaim = []

    files = os.listdir("./manifest")

    for file in files :
        # 判断是不是xml文件
        if file[-4:] == ".xml" :
            file_path = os.path.join("./manifest",file)
            domTree = parse(file_path)
            rootNode = domTree.documentElement

            # 将申请的权限和声明的权限放入all_per中
            for per in permissions:
                per_list = rootNode.getElementsByTagName(per)
                for p in per_list:
                    all_per.append(p.getAttribute("android:name"))

            # 取出组件中权限，判断是否在all_per中
            for com in compents:
                com_list = rootNode.getElementsByTagName(com)
                for c in com_list:
                    item = c.getAttribute("android:permission")
                    if item != '':
                        if c.getAttribute("android:permission") not in all_per and\
                                c.getAttribute("android:permission") not in system_perm:
                            unclaim.append(c.getAttribute("android:permission"))

            if not os.path.exists('unclaim.txt'):
                os.system("touch unclaim.txt")

            with open('unclaim.txt', 'a+') as f:
                unclaim_str  = ', '.join(unclaim)
                if unclaim_str != "":
                    f.write(file + " " +unclaim_str+"\n")
                    print(unclaim)

if __name__ == '__main__':
    unpackage()

    if not os.path.exists('manifest'):
        os.mkdir('manifest')

    rename_and_extract("./", "./../manifest")

    Analysis_perm()