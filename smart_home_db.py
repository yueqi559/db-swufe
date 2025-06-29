import re
import sqlite3
import argparse
from typing import List, Dict, Tuple, Optional
from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx
from transformers import pipeline


class ErrorType(Enum):
    SYNTAX_ERROR = 1
    TABLE_NOT_FOUND = 2
    COLUMN_NOT_FOUND = 3
    TYPE_MISMATCH = 4
    MISSING_CLAUSE = 5
    INVALID_OPERATOR = 6


class SQLValidator:
    def validate(self, query: str) -> Tuple[bool, Optional[ErrorType], Optional[str]]:
        # 简单的SQL语法验证实现
        query = query.strip().lower()

        if not query.endswith(';'):
            return False, ErrorType.SYNTAX_ERROR, "SQL语句应以分号(;)结尾"

        if query.startswith('select'):
            return self._validate_select(query)
        elif query.startswith('insert'):
            return self._validate_insert(query)
        elif query.startswith('update'):
            return self._validate_update(query)
        elif query.startswith('delete'):
            return self._validate_delete(query)
        else:
            return True, None, None  # 其他类型语句简化处理

    def _validate_select(self, query: str) -> Tuple[bool, Optional[ErrorType], Optional[str]]:
        # 验证SELECT语句
        if 'from' not in query:
            return False, ErrorType.MISSING_CLAUSE, "SELECT语句缺少FROM子句"

        # 简单的正则表达式匹配，实际应使用更复杂的解析
        pattern = r'select\s+(.*?)\s+from\s+(.*?)(\s+where\s+(.*))?(\s+group by\s+(.*))?(\s+order by\s+(.*))?;$'
        match = re.match(pattern, query)

        if not match:
            return False, ErrorType.SYNTAX_ERROR, "SELECT语句语法错误"

        return True, None, None


class DatabaseManager:
    def __init__(self, db_name: str = "project2025.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.last_query_results = None  # 保存上次查询结果
        self.initialize_database()

    def initialize_database(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._create_tables()
            self._insert_sample_data()
            print("数据库初始化完成")
        except Exception as e:
            print(f"数据库初始化失败: {e}")

    def _create_tables(self):
        # 创建智能家居系统的表结构
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            house_area REAL,
            contact_info TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id INTEGER PRIMARY KEY,
            device_name TEXT NOT NULL,
            device_type TEXT NOT NULL,
            location TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_records (
            record_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            device_id INTEGER,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (device_id) REFERENCES devices(device_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_events (
            event_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            event_time DATETIME NOT NULL,
            event_type TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            feedback_time DATETIME NOT NULL,
            rating INTEGER,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')

        self.conn.commit()

    def _insert_sample_data(self):
        # 插入示例数据
        users = [
            (1, "Alice", 120.5, "alice@example.com"),
            (2, "Bob", 85.0, "bob@example.com"),
            (3, "Charlie", 150.2, "charlie@example.com")
        ]

        devices = [
            (1, "客厅灯", "照明", "客厅"),
            (2, "卧室空调", "空调", "主卧"),
            (3, "客厅电视", "娱乐", "客厅"),
            (4, "厨房冰箱", "电器", "厨房"),
            (5, "浴室热水器", "热水", "浴室")
        ]

        # 添加使用记录样本
        usage_records = [
            (1, 1, 1, "2025-06-01 08:00:00", "2025-06-01 09:00:00"),
            (2, 1, 3, "2025-06-01 19:00:00", "2025-06-01 21:00:00"),
            (3, 2, 2, "2025-06-01 21:00:00", "2025-06-01 23:00:00"),
            (4, 3, 4, "2025-06-01 06:00:00", None),
            (5, 3, 5, "2025-06-01 07:00:00", "2025-06-01 07:30:00")
        ]

        security_events = [
            (1, 1, "2025-06-01 12:30:00", "门禁异常", "前门未正常关闭"),
            (2, 3, "2025-06-01 13:15:00", "摄像头警报", "检测到未知移动")
        ]

        self.cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", users)
        self.cursor.executemany("INSERT OR IGNORE INTO devices VALUES (?, ?, ?, ?)", devices)
        self.cursor.executemany("INSERT OR IGNORE INTO usage_records VALUES (?, ?, ?, ?, ?)", usage_records)
        self.cursor.executemany("INSERT OR IGNORE INTO security_events VALUES (?, ?, ?, ?, ?)", security_events)
        self.conn.commit()

    def execute_query(self, query: str) -> Tuple[bool, str, Optional[List[Dict]]]:
        try:
            self.cursor.execute(query)
            if query.strip().lower().startswith('select'):
                columns = [desc[0] for desc in self.cursor.description]
                results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
                self.last_query_results = results  # 保存查询结果
                return True, "查询成功", results
            else:
                self.conn.commit()
                self.last_query_results = None
                return True, "操作成功", None
        except Exception as e:
            self.last_query_results = None
            return False, str(e), None

    def visualize_query_results(self):
        results = self.last_query_results
        if not results:
            print("没有结果可可视化")
            return

        # 简单示例：假设结果包含设备使用频率
        if 'device_name' in results[0] and 'usage_count' in results[0]:
            devices = [row['device_name'] for row in results]
            counts = [row['usage_count'] for row in results]

            plt.figure(figsize=(10, 6))
            plt.bar(devices, counts)
            plt.xlabel('设备名称')
            plt.ylabel('使用次数')
            plt.title('设备使用频率')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        elif 'user_id' in results[0] and 'username' in results[0]:
            users = [row['username'] for row in results]
            events = [row['security_count'] for row in results] if 'security_count' in results[0] else [1] * len(users)

            plt.figure(figsize=(10, 6))
            plt.pie(events, labels=users, autopct='%1.1f%%')
            plt.title('安全事件分布')
            plt.tight_layout()
            plt.show()
        else:
            print("当前结果无法可视化。支持的格式：设备使用频率、安全事件分布")

    def visualize_query_plan(self, query: str):
        # 简化的查询计划可视化
        print("生成查询计划可视化...")
        G = nx.DiGraph()

        # 为简化，这里创建一个简单的查询计划图
        G.add_node("解析器", shape="box")
        G.add_node("优化器", shape="box")
        G.add_node("执行引擎", shape="box")

        operations = []
        if 'where' in query.lower():
            operations.append("过滤")
        if 'group by' in query.lower():
            operations.append("分组")
        if 'order by' in query.lower():
            operations.append("排序")
        if 'join' in query.lower():
            operations.append("连接表")

        for i, op in enumerate(operations):
            G.add_node(f"操作{i + 1}: {op}", shape="ellipse")

        # 添加边
        G.add_edge("解析器", "优化器")
        G.add_edge("优化器", "执行引擎")
        for i in range(len(operations)):
            if i == 0:
                G.add_edge("执行引擎", f"操作{i + 1}: {operations[i]}")
            else:
                G.add_edge(f"操作{i}: {operations[i - 1]}", f"操作{i + 1}: {operations[i]}")

        # 绘制图形
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue",
                font_size=10, font_weight="bold", arrows=True, arrowsize=20)
        plt.title("查询执行计划")
        plt.show()

    def reset_database(self):
        try:
            self.conn.close()
            # 删除并重新创建数据库文件
            import os
            if os.path.exists(self.db_name):
                os.remove(self.db_name)
            self.initialize_database()
            print("数据库已重置")
        except Exception as e:
            print(f"重置数据库失败: {e}")


class NLPQueryEngine:
    def __init__(self):
        try:
            # 使用小型模型进行演示，实际应用中可使用更大的模型
            self.nlp = pipeline("text2text-generation", model="google/flan-t5-small")
        except Exception as e:
            print(f"自然语言处理引擎初始化失败: {e}")
            print("警告：部分功能受限")
            self.nlp = None

    def generate_sql(self, question: str) -> Optional[str]:
        if not self.nlp:
            print("NLP引擎不可用，使用简单规则处理")
            return self._simple_rule_based(question)

        # 简单的提示模板
        prompt = f"""将以下自然语言查询转换为SQL:
        数据库包含以下表:
        - users (user_id, username, house_area, contact_info)
        - devices (device_id, device_name, device_type, location)
        - usage_records (record_id, user_id, device_id, start_time, end_time)
        - security_events (event_id, user_id, event_time, event_type, description)
        - user_feedback (feedback_id, user_id, feedback_time, rating, comment)

        问题: {question}

        SQL查询:"""

        try:
            result = self.nlp(prompt, max_length=100, num_return_sequences=1)
            return result[0]['generated_text'].strip()
        except Exception as e:
            print(f"NLP处理失败: {e}")
            return None

    def _simple_rule_based(self, question: str) -> str:
        """简单的基于规则的自然语言转SQL"""
        question = question.lower()

        if "用户" in question or "username" in question:
            if "所有" in question:
                return "SELECT * FROM users;"
            elif "Alice" in question:
                return "SELECT * FROM users WHERE username='Alice';"
            elif "Bob" in question:
                return "SELECT * FROM users WHERE username='Bob';"
            elif "Charlie" in question:
                return "SELECT * FROM users WHERE username='Charlie';"
            else:
                return "SELECT * FROM users;"

        elif "设备" in question or "device" in question:
            if "所有" in question:
                return "SELECT * FROM devices;"
            elif "客厅" in question:
                return "SELECT * FROM devices WHERE location='客厅';"
            elif "卧室" in question:
                return "SELECT * FROM devices WHERE location='主卧';"
            elif "厨房" in question:
                return "SELECT * FROM devices WHERE location='厨房';"
            elif "浴室" in question:
                return "SELECT * FROM devices WHERE location='浴室';"
            else:
                return "SELECT * FROM devices;"

        elif "使用" in question or "usage" in question:
            if "记录" in question or "历史" in question:
                return "SELECT * FROM usage_records;"
            else:
                return "SELECT devices.device_name, COUNT(*) as usage_count FROM usage_records JOIN devices ON usage_records.device_id = devices.device_id GROUP BY devices.device_id;"

        elif "安全" in question or "security" in question:
            return "SELECT * FROM security_events;"

        return "SELECT * FROM users;"


class CommandLineInterface:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.validator = SQLValidator()
        self.nlp_engine = NLPQueryEngine()
        self.running = True

    def start(self):
        print("欢迎使用智能家居数据库管理工具")
        print("输入SQL查询，或使用命令: /help, /visualize, /nlp, /reset, /exit")

        while self.running:
            try:
                query = input("\n> ").strip()

                if not query:
                    continue

                # 处理命令
                if query == "/exit":
                    self.running = False
                    print("感谢使用，再见！")
                    continue

                if query == "/help":
                    self._print_help()
                    continue

                if query == "/reset":
                    self.db_manager.reset_database()
                    continue

                if query.startswith("/visualize"):
                    self._handle_visualization()
                    continue

                if query.startswith("/nlp"):
                    question = query[4:].strip()
                    self._handle_nlp_query(question)
                    continue

                # 验证查询
                is_valid, error_type, error_msg = self.validator.validate(query)
                if not is_valid:
                    print(f"查询验证失败: {error_msg}")
                    print("你可以尝试:")
                    if error_type == ErrorType.SYNTAX_ERROR:
                        print("  - 检查SQL语法是否正确")
                        print("  - 确保语句以分号(;)结尾")
                    elif error_type == ErrorType.TABLE_NOT_FOUND:
                        print("  - 检查表名是否拼写正确")
                        print("  - 使用SHOW TABLES查看可用表")
                    elif error_type == ErrorType.COLUMN_NOT_FOUND:
                        print("  - 检查列名是否拼写正确")
                        print("  - 使用PRAGMA table_info(table_name)查看表结构")
                    continue

                # 执行查询
                success, message, results = self.db_manager.execute_query(query)
                if success:
                    print(f"✅ {message}")
                    if results:
                        self._print_results(results)
                else:
                    print(f"❌ 查询执行失败: {message}")

            except KeyboardInterrupt:
                print("\n操作已取消")
            except Exception as e:
                print(f"发生错误: {e}")

    def _print_help(self):
        print("可用命令:")
        print("  /help            - 显示此帮助信息")
        print("  /exit            - 退出程序")
        print("  /reset           - 重置数据库")
        print("  /visualize       - 可视化上次查询结果")
        print("  /nlp [问题]      - 使用自然语言查询数据库")
        print("\n支持标准SQL语法，例如:")
        print("  SELECT * FROM users;")
        print(
            "  SELECT device_name, COUNT(*) as usage_count FROM usage_records JOIN devices ON usage_records.device_id = devices.device_id GROUP BY devices.device_id;")
        print("样本查询：")
        print("  SELECT * FROM devices WHERE location='客厅';")
        print(
            "  SELECT username, COUNT(*) as security_count FROM security_events JOIN users ON security_events.user_id = users.user_id GROUP BY users.user_id;")

    def _print_results(self, results: List[Dict]):
        if not results:
            print("查询结果为空")
            return

        # 计算每列的最大宽度
        max_widths = {}
        for row in results:
            for key, value in row.items():
                key_width = len(str(key))
                value_width = len(str(value))
                current_width = max_widths.get(key, 0)
                max_widths[key] = max(current_width, key_width, value_width)

        # 打印表头
        header = " | ".join([str(key).ljust(max_widths[key]) for key in results[0].keys()])
        print(header)
        print("-" * len(header))

        # 打印数据行
        for row in results:
            print(" | ".join([str(row[key]).ljust(max_widths[key]) for key in row.keys()]))

        print(f"\n共返回 {len(results)} 条记录")

    def _handle_visualization(self):
        print("可视化选项:")
        print("1. 可视化上次查询结果")
        print("2. 可视化查询计划")
        choice = input("请选择 (1-2): ").strip()

        if choice == "1":
            self.db_manager.visualize_query_results()
        elif choice == "2":
            query = input("请输入SQL查询: ").strip()
            if query:
                is_valid, error_type, error_msg = self.validator.validate(query)
                if is_valid:
                    self.db_manager.visualize_query_plan(query)
                else:
                    print(f"查询无效: {error_msg}")
        else:
            print("无效选择")

    def _handle_nlp_query(self, question: str):
        if not question:
            print("请提供问题，例如：/nlp 显示所有客厅设备")
            return

        print(f"处理自然语言查询: {question}")
        sql = self.nlp_engine.generate_sql(question)

        if not sql:
            print("无法生成SQL查询，请尝试其他问题")
            return

        print(f"生成的SQL: {sql}")

        # 验证生成的SQL
        is_valid, error_type, error_msg = self.validator.validate(sql)
        if not is_valid:
            print(f"生成的SQL验证失败: {error_msg}")
            print("尝试修正生成的查询...")
            if ";" not in sql:
                sql += ";"
            print(f"修正后的SQL: {sql}")

            # 重新验证
            is_valid, error_type, error_msg = self.validator.validate(sql)
            if not is_valid:
                print(f"仍然无效: {error_msg}")
                return

        # 执行查询
        success, message, results = self.db_manager.execute_query(sql)
        if success:
            print(f"✅ {message}")
            if results:
                self._print_results(results)
        else:
            print(f"❌ 查询执行失败: {message}")


if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.start()