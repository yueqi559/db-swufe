本周通过Postgresql软件实践基本的SQL，并学习了集合操作等知识。

# 本周作业（第3次作业）

## 题目一（3分+1分）

> **需要**使用PostgreSQL及DataGrip软件操作，并对操作页面及结果进行截图。

1. 新建一个`university`数据库，并执行`largeRelationsInsertFile.sql`，导入数据。

![屏幕截图 2025-04-05 203005](https://github.com/user-attachments/assets/d64229c4-d339-43bc-9d71-a330a7b6515e)

2. 运行第2次作业的题目三代码。注意：把原题目中的`会计`改成`History`。

![屏幕截图 2025-04-05 212826](https://github.com/user-attachments/assets/05df066d-d59b-4634-a40f-ad7330e33577)

## 题目二（3分）

参考[Pattern Matching](https://www.postgresql.org/docs/17/functions-matching.html)，在PG中使用至少三种方法实现找到所有以`S`开头教师的名字。

答：
（1）

SELECT name
FROM instructor
WHERE name LIKE 'S%';

![image](https://github.com/user-attachments/assets/a487fc48-8a0c-4f3a-aff2-defaa45a8403)

（2）

SELECT name
FROM instructor
WHERE name SIMILAR TO 'S%';

![image](https://github.com/user-attachments/assets/ee6bc712-ba45-47ed-b5a9-987414473cec)

（3）

SELECT name
FROM instructor
WHERE name ~ '^S';

![image](https://github.com/user-attachments/assets/8f239796-8550-4b0e-9d4b-6d214da30bf8)

## 题目三（3分）

`psql`是PostgreSQL的命令行工具。请使用`psql`命令行工具：

- 实现题目二
- 列出所有的数据库
- 列出当前数据库的所有表
- 显示某张表的关系模式

  答：

（1）

SELECT name FROM instructor WHERE name LIKE 'S%';

SELECT name FROM instructor WHERE name SIMILAR TO 'S%';

SELECT name FROM instructor WHERE name ~ '^S';

（2）

psql -U postgres -h localhost -p 5432

\l

\c university

\dt

\d instructor

