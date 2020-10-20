# coding=utf-8
import collections
import os, sys
from xml.dom.minidom import parse
import pymongo
from pymongo import MongoClient, collection

#1.链接本地数据库服务
conn = MongoClient('localhost')
#2.链接本地数据库 demo 没有会创建
db = conn['permission']   #demo数据库名
#3.创建，连接集合
permissiondb = db['xml_analysis']  #employees集合名

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
import xmltodict


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
    li = []
    perm_dict = {}
    for file in files:
        if (os.path.isdir(file)):
            os.chdir(file) # 进入该目录
            if os.path.exists("AndroidManifest.xml"):
                with open('AndroidManifest.xml') as f:
                    doc = xmltodict.parse(f.read())
                    print(file)
                    # uses-permission
                    for i in range(len(doc['manifest']['uses-permission'])):
                        try:
                            name = doc['manifest']['uses-permission'][i]['@name']
                        except:
                            name = doc['manifest']['uses-permission'][i]['@android:name']
                        li.append(name)
                    perm_dict['uses-permission'] = li

                    # permission
                    doc2 = None
                    if type(doc['manifest']['permission']) == collections.OrderedDict:
                        doc2 = [doc['manifest']['permission']]
                    else:
                        doc2 = doc['manifest']['permission']

                    perm = {}
                    for i in range(len(doc2)):                        

                        try:
                            name = doc2[i]['@name']
                        except:
                            name = doc2[i]['@android:name']
                        try:
                            level = doc2[i]['@protectionLevel']
                        except:
                            try:
                                level = doc2[i]['@android:protectionLevel']
                            except:
                                level = "normal"


                        perm[name] = level
                        li.append(perm)
                    perm_dict['permission'] = li

                    # provider
                    provider = {}
                    provider_item = []
                    try:
                        for i in range(len(doc['manifest']['provider'])):
                            name = doc['manifest']['application']['provider'][i]['@name']
                            export = doc['manifest']['application']['provider'][i]['@export']
                            if(export != 'false') :
                                try:
                                    perm = doc['manifest']['permission'][i]['@permission']
                                except:
                                    perm = ""

                                try:
                                    writeperm = doc['manifest']['permission'][i]['@writePermission']
                                except:
                                    writeperm = ""
                                try:
                                    readperm = doc['manifest']['permission'][i]['@readPermission']
                                except:
                                    readperm = ""

                                provider_item.append(perm).append(writeperm).append(readperm)
                                provider[name] = provider_item
                            li.append(provider)
                    except:
                        li.append("no provider")
                        print("#################")

                    perm_dict['proivder'] = li

                    # receiver
                    receiver = {}
                    receiver_item = []
                    try:
                        for i in range(len(doc['manifest']['receiver'])):
                            name = (doc['manifest']['receiver'][i]['@name'])
                            export = doc['manifest']['application']['receiver'][i]['@export']
                            if (export != 'false'):
                                try:
                                    perm = doc['manifest']['receiver'][i]['@permission']
                                except:
                                    perm = ""
                            receiver_item.append(perm)
                            receiver[name] = receiver_item
                            li.append(receiver)
                    except:
                        li.append("no receiver")

                    perm_dict["receiver"] = li

                    # activity
                    activity = {}
                    activity_item = []
                    category_item = []
                    action_item = []
                    try:
                        for i in range(len(doc['manifest']['activity'])):
                            name = (doc['manifest']['activity'][i]['@name'])
                            export = doc['manifest']['application']['activity'][i]['@export']
                            if (export != 'false'):
                                try:
                                    perm = doc['manifest']['activity'][i]['@permission']
                                except:
                                    perm = ""

                                try:
                                    for n in range(len(doc['manifest']['activity'][i]['intent-filter'])):
                                        category = doc['manifest']['activity'][i]['intent-filter'][n]['category']['@name']
                                        action = doc['manifest']['activity'][i]['intent-filter'][n]['category']['@name']
                                        category_item.append(category)
                                        action_item.append(action)
                                except:
                                    category = ""
                                    action = ""
                                    category_item.append(category)
                                    action_item.append(action)

                                activity_item.append(perm).append(category_item).append(action_item)
                                activity[name] = activity_item
                                li.append(activity)
                    except:
                        li.append("no activity")
                    perm_dict["activity"] = li

                    # service
                    service = {}
                    service_item = []
                    try:
                        for i in range(len(doc['manifest']['service'])):
                            name = doc['manifest']['service'][i]['@name']
                            export = doc['manifest']['application']['service'][i]['@export']
                            if (export != 'false'):
                                try:
                                    perm = doc['manifest']['activity'][i]['@permission']
                                except:
                                    perm = ""

                            service_item.append(perm)
                            service[name] = service_item
                            li.append(service)
                            perm_dict["service"] = li

                            li.append(name)
                    except:
                        li.append("no service")
                    perm_dict['service'] = li

            os.chdir("./..")

    if not os.path.exists('unclaim.txt'):
        os.system("touch unclaim.txt")

    x = permissiondb.insert(perm_dict, check_keys=False)
    print(x)

    result = permissiondb.find()
    print(type(result))
    print(result)
    with open('unclaim.txt', 'a+') as f:
        f.write(str(perm_dict))


if __name__ == '__main__':
    #unpackage()

    if not os.path.exists('manifest'):
        os.mkdir('manifest')

    rename_and_extract("./", "./../manifest")

