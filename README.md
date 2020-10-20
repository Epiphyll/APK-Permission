## APK-Permission
### Analysis_perm.py  
主要功能：  
1. 使用Apktool反编译apk文件  
2. 提取AndroidManifest.xml至manifest文件夹  
3. 对比activity、receiver、provider组件中使用的权限是否声明或申请  
4. 保存未声明的权限名及其包名至unclaim.txt文件中  

使用方法：  
1. 将该代码和所有apk文件放在同一目录  
2. python3 Analysis_perm.py  
#

### extract_xml.py  
功能：提取AndroidManifest.xml文件中的内容, 其中各组件中只提取export=true时的内容。  
apk-name = {  
        uses-permission:[name1, name2]  
        permission:[{name1: protectLevel1}, {name2: protectLevel2}]  
        provider:[{name1: [permisson1, writePermission, readPermission]}, {name2:[...]}]  
        receiver:[{name1: permisson1}, {name2:...}]  
        activity:[{name1: [permisson1, category_name, action_name], name2:[...]]  
        service: [{name1: permisson1}, {name2:...}]  
}
