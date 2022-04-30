# MushroomCheckin
蘑菇钉签到脚本
需要自行填写个人信息 第51行～第59行

修改好脚本后 在vps上定时运行即可（不建议国内的腾讯云等） ip已经被蘑菇钉公司封锁 
定时运行可以用crontab程序（linux ubuntu）

编辑 /etc/crontab 文件 增加一下 路径更改为你的脚本所在的路径
>>> 0 0 0，10 * * root python **/YourPath/MushroomCheckin.py**
