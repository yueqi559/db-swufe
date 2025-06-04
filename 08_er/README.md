# 本周作业（第8次作业）

## 题目一（3分+2分）

考虑一个用于记录学生（student）在不同课程段（section）在不同考试中取得成绩（grade）的数据库，其中课程段属于某个课程（course）。

1. 绘制E-R图，只用二元联系。确保能够表示一个学生在不同考试中获得的成绩，且一个课程段可能有多次考试。（提示：使用多值属性）

答：如图所示

![image](https://github.com/user-attachments/assets/1a707033-5c6a-4274-8bfb-81073bfbc15f)


2. 写出上面E-R图的关系模式（要求注明主码）

```sql
course(course_id, ...) 
  PRIMARY KEY (course_id)

student(student_id, ...) 
  PRIMARY KEY (student_id)

section(course_id, sec_id, semester, year, ...) 
  PRIMARY KEY (course_id, sec_id, semester, year)
  FOREIGN KEY (course_id) REFERENCES course

exam(course_id, sec_id, semester, year, exam_id, exam_date, ...) 
  PRIMARY KEY (course_id, sec_id, semester, year, exam_id)
  FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section

takes_exam(student_id, course_id, sec_id, semester, year, exam_id, grade) 
  PRIMARY KEY (student_id, course_id, sec_id, semester, year, exam_id)
  FOREIGN KEY (student_id) REFERENCES student
  FOREIGN KEY (course_id, sec_id, semester, year, exam_id) REFERENCES exam
```

## 题目二（5分）

如果一个关系模式中只有两个属性，证明该关系模式必定属于BCNF。

证明：

1、无任何非平凡函数依赖

此时唯一可能的依赖是平凡依赖（如 A → A或 AB → B），模式自动满足BCNF。

2、存在非平凡函数依赖

（1）仅依赖 A → B，左边 A 是超码，满足BCNF。

（2）仅依赖 B → A，左边 B 是超码，满足BCNF。

（3）同时存在 A → B和 B → A，均满足BCNF。

可证

## 题目三（5分）

考虑关系模式`r(A, B, C, D, E)`，有如下函数依赖：

- A → BC
- BC → E
- CD → AB

请给出一个满足BCNF的分解，并说明你的分解符合BCNF。

答：

R ( B , C , E ) , 函数依赖 BC → E，BC 是超键。
