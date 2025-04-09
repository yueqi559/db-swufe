本周学习了SQL中对空值的处理，聚集函数的使用。

# 本周作业（第4次作业）

## 题目一（2分）

请问下面的SQL语句是否合法？用实验验证你的想法。你从实验结果能得到什么结论？

```sql
SELECT dept_name, min(salary)
FROM instructor;

不合法
这个语句尝试选择dept_name列和使用聚合函数min(salary)，但没有对非聚合列dept_name进行GROUP BY分组
实验结论：执行时会报错，提示dept_name必须出现在GROUP BY子句中或用于聚合函数中。
正确写法：
SELECT dept_name, min(salary)
FROM instructor
GROUP BY dept_name;


SELECT dept_name, min(salary)
FROM instructor
GROUP BY dept_name
HAVING name LIKE '%at%';
不合法
虽然这个语句正确地使用了GROUP BY对dept_name分组，但HAVING子句中引用了name列，而该列既不是分组列也不是聚合函数结果。
实验结论：执行时会报错，提示name列在HAVING子句中无效，因为它不包含在聚合函数或GROUP BY子句中。
正确写法：
SELECT dept_name, min(salary)
FROM instructor
GROUP BY dept_name
HAVING dept_name LIKE '%at%'; 


SELECT dept_name
FROM instructor
WHERE AVG(salary) > 20000;
不合法
WHERE子句不能直接使用聚合函数（如AVG）。聚合函数只能在HAVING子句中使用，或者作为SELECT列表的一部分。
实验结论：执行时会报错，提示聚合函数不能在WHERE子句中使用。
正确写法：
SELECT dept_name
FROM instructor
GROUP BY dept_name
HAVING AVG(salary) > 20000;
```

## 题目二（3分+3分+2分）

1. 找到工资最高员工的名字，假设工资最高的员工只有一位（至少两种写法）。

（1）使用子查询
```sql
SELECT name
FROM employee
WHERE salary = (SELECT MAX(salary) FROM employee);
```

（2）使用ORDER BY和LIMIT
```sql
SELECT name
FROM employee
ORDER BY salary DESC
LIMIT 1;
```

（3）使用窗口函数
```sql
SELECT name
FROM (
    SELECT name, salary, RANK() OVER (ORDER BY salary DESC) as rnk
    FROM employee
) t
WHERE rnk = 1;
```



2. 找到工资最高员工的名字，假设工资最高的员工有多位（试试多种写法）。

（1）使用子查询
```sql
SELECT name
FROM employee
WHERE salary = (SELECT MAX(salary) FROM employee);
```

（2）使用窗口函数
```sql
SELECT name
FROM (
    SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) as drnk
    FROM employee
) t
WHERE drnk = 1;
```

（3）使用JOIN
```sql
SELECT e.name
FROM employee e
JOIN (SELECT MAX(salary) as max_salary FROM employee) m
ON e.salary = m.max_salary;
```

3. 解释下面四句。

```sql
SELECT 1 IN (1);
检查数字1是否在集合(1)中

SELECT 1 = (1);
比较数字1和单元素集合(1)是否相等

SELECT (1, 2) = (1, 2);
比较两个元组(1,2)是否相等

SELECT (1) IN (1, 2);
检查单元素集合(1)是否是集合(1,2)的成员

```
