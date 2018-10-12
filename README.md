# chainCtr
deploy chainSQL network



## 0x00 Fake Network

1. 初始化环境

   ```
   sudo ./chainCtr init --fake
   ```

2. 启动网络

   ```
   sudo ./chainCtr start --fake --wait
   ```

3. 测试网络

   ```
   sudo ./chainCtr test
   ```

4. 停止网络

   ```
   sudo ./chainCtr stop --fake
   ```

## 0x01 Normal Network

1. 初始化网络

   ```
   # 只需在一个节点运行一次
   sudo ./chainCtr init
   ```

2. 加入网络

   ```
   sudo ./chainCtr join
   
   # 或是指定 mysql, 必须使用 -- 表示 mysql 参数结束
   sudo ./chainCtr join --host 127.0.0.1:7076 --mysql host:127.0.0.1 port:3306 user:root pwd:3306 db:chainsql --
   ```

3. 启动网络

   ```
   sudo ./chainCtr start
   # wait 参数表示必须等待 chainsqld 启动并且链已经创建成功，目前上下两个指令命运区别
   sudo ./chainCtr start --wait
   ```

4. 停止网络

   ```
   sudo ./chainCtr stop
   # 或是停止本地节点的 chainsqld
   sudo ./chainCtr stop --local
   ```
