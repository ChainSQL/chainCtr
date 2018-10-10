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
   sudo ./chainCtr init
   ```

2. 加入网络

   ```
   sudo ./chainCtr join url
   ```

3. 启动网络

   ```
   sudo ./chainCtr start --wait
   ```

4. 停止网络

   ```
   sudo ./chainCtr stop
   ```
