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
def unpackage():
    # 遍历当前目录
    fileNames = os.listdir("./")
    for f in fileNames:
        if f[-4:] == ".apk":
            os.system("mkdir -p " + f[:-4]) # 创建同名文件夹
            os.system("apktool d " + f + " -o " + f[:-4] + " -f") # apk反编译
    # 删除空文件夹
    os.system("find . -type d -empty -delete")

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

            for per in permissions:
                per_list = rootNode.getElementsByTagName(per)
                for p in per_list:
                    all_per.append(p.getAttribute("android:name"))

            for com in compents:
                com_list = rootNode.getElementsByTagName(com)
                for c in com_list:
                    item = c.getAttribute("android:permission")
                    if item != '':
                        if c.getAttribute("android:permission") not in all_per:
                            unclaim.append(c.getAttribute("android:permission"))

            if not os.path.exists('unclaim.txt'):
                os.system("touch unclaim.txt")

            with open('unclaim.txt', 'a+') as f:
                unclaim_str  = ', '.join(unclaim)
                if unclaim_str != "":
                    f.write(file + " " +unclaim_str+"\n")
                    print(unclaim)

if __name__ == '__main__':
    #unpackage()

    if not os.path.exists('manifest'):
        os.mkdir('manifest')

    rename_and_extract("./", "./../manifest")

    Analysis_perm()
