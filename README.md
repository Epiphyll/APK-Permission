## APK-Permission

主要功能：1. 使用Apktool反编译apk文件  
         2. 提取AndroidManifest.xml至manifest文件夹  
         3. 对比activity、receiver、provider组件中使用的权限是否声明或申请  
         4. 保存未声明的权限名及其包名至unclaim.txt文件中  
#######################################################

使用方法：1.将该代码和所有apk文件放在同一目录  
         2. python3 Analysis_perm.py  
