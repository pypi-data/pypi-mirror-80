# jsonAssured

## 安装
pip3 install jsonAssured

## 使用
### mapping文件编写
见sample中mapping yaml文件

- ignore: 忽略字段，例如在json数据中的时间戳等不需要比对的字段，格式： - "key",一行一个忽略字段

- is_allflag: 是否全量比对，如果是false，只会比对keymappings中的字段；如果是true，会根据所有字段（忽略ignore中）生成jsonpath进行比对

- keyMappings: 设置比对字段，需要is_allflag设置为false，格式 - source：老接口key target: 新接口key

- keyjsonpathmapping: 根据keymappings自动生成的jsonpath映射，可以自行调整

### source、target文件
新老接口的json文件

### 使用
jsonAssured [mapping_path] [source_path] [target_path]

比对结果会在console打印输出

