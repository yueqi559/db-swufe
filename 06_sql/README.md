# 本周作业（第5次作业）

考虑关系模式`product(product_no, name, price)`，完成下面的题目：

## 题目一（4分）

在数据库中创建该关系，并自建上面关系的txt数据文件：

1. 使用`COPY`命令导入数据库（PostgreSQL）；或使用`LOAD DATA`命令导入数据库（MySQL）。
2. 将该关系导出为任意文件（如SQL、Txt、CSV、JSON等）。

答：

（1）创建关系模式

```sql
CREATE TABLE product (
    product_no INT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2)
);
```

（2）导入数据

```sql
LOAD DATA INFILE '/path/to/products.txt' INTO TABLE product
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
(product_no, name, price);
```

（3）导出数据

```sql
SELECT * INTO OUTFILE '/path/to/output.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM product;
```

## 题目二（6分）

1. 添加一个新的商品，编号为`666`，名字为`cake`，价格不详。

```sql
INSERT INTO product (product_no, name, price) 
VALUES (666, 'cake', NULL);
```
   
2. 使用一条SQL语句同时添加3个商品，内容自拟。

```sql
INSERT INTO product (product_no, name, price) 
VALUES 
(667, 'cookie', 5.99),
(668, 'juice', 3.50),
(669, 'bread', 4.25);
```
   
3. 将商品价格统一打8折。

```sql
UPDATE product 
SET price = price * 0.8 
WHERE price IS NOT NULL;
``` 
   
4. 将价格大于100的商品上涨2%，其余上涨4%。

```sql
UPDATE product 
SET price = 
    CASE 
        WHEN price > 100 THEN price * 1.02 
        ELSE price * 1.04 
    END
WHERE price IS NOT NULL;
``` 

5. 将名字包含`cake`的商品删除。

```sql
DELETE FROM product 
WHERE name LIKE '%cake%';
```
    
6. 将价格高于平均价格的商品删除。

```sql
DELETE FROM product 
WHERE price > (SELECT AVG(price) FROM product);
```

## 题目三（5分）

### 针对PostgreSQL

使用参考下面的语句添加10万条商品，

```sql
-- PostgreSQL Only
INSERT INTO product (name, price)
SELECT
    'Product' || generate_series, -- 生成名称 Product1, Product2, ...
    ROUND((random() * 1000)::numeric, 2) -- 生成0到1000之间的随机价格，保留2位小数
FROM generate_series(1, 100000);
```

比较`DELETE`和`TRUNCATE`的性能差异。

答：
`DELETE`是逐行删除，生成事务日志，触发触发器，可回滚。
`TRUNCATE`直接删除表的数据页，不记录逐行操作，效率极高，但不可回滚。

### 针对MySQL

参考`generate_data.py`生成数据，在MySQL比较`LOAD DATA`和[SELECT INTO](https://dev.mysql.com/doc/refman/8.0/en/select-into.html)的性能差异。

答：

（1）使用`LOAD DATA`导入数据

```sql
SET profiling = 1;
LOAD DATA INFILE '/path/to/products.csv' INTO TABLE product
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS; 
SHOW PROFILES; 
```

`LOAD DATA`直接读取文件，绕过SQL解析，批量插入，效率极高。


（2）使用`SELECT INTO`生成数据

```sql
INSERT INTO product (name, price)
SELECT 
  CONCAT('Product', id),
  ROUND(RAND() * 1000, 2)
FROM (
  SELECT 1 AS id UNION SELECT 2 ... 
) AS tmp_data; 
```

`SELECT INTO`逐行处理SQL逻辑，生成事务日志，效率较低。
