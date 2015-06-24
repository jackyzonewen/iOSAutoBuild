# iOSAutoBuild
自动打包上传至蒲公英或FIR的脚本

### 上传FIR需官方工具 
```python
$ sudo gem install fir-cli --no-ri --no-rdoc
```

### 使用
> * xcode中配置好证书
> * 将脚本拖进项目目录 
> * 执行 
 ```
  $ python iOSAutoBuild.py --target=YOURTARGETNAME
  ```
  

### 注意
脚本中的发布模式需自行修改,默认InHouse发布

