#!/bin/bash

# 测试配置 mysql
./configChainSQL sync_db.type=mysql sync_db.host=SKY-20160717UWK sync_db.user=root sync_db.pass=3.16 sync_db.db=chainsql sync_db.charset=utf8 --path ~/

# 测试配置 public key 和 seed
./configChainSQL validation_public_key=n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn validation_seed=xnvq8z6C1hpcYPP94dbBib1VyoEQ1 --path ~/

./configChainSQL --path ~/ ssl_verify=0 auto_sync=0


./configChainSQL --path ~/ node_db.type=RocksDB node_db.path=./db

./configChainSQL --path ~/ ips_fixed=172.16.18.2 ips_fixed=172.16.18.3

./configChainSQL --path ~/ validator=n9MGgvfSe1B9FvkPwLJ1HZQKBAiT7fH4Yn4a7BGnkBhH7BK1jL25 validator=n94KRVNkuSqGi71cPxZZCQGGDRga1DV3YTHbKZzsewFgAV8iwEjZ validator=n9Jbd6Rj9xuftDCcvfECEFUmXDcoTM7yTSVAHjVtA6ku1dCbJZ3b
