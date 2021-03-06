# coding: utf-8
#!/usr/bin/env python

import pymysql
pymysql.install_as_MySQLdb()

class DatabaseManager:
    def __init__(self):
        self.host = "localhost"
        self.user = "language"
        self.password = "language"
        self.database = "test"
        self.charset = "utf8"
        self.connect_database()
            
    def connect_database(self):
        self.db = pymysql.connect(host = self.host,
                                  user = self.user,
                                  passwd = self.password,
                                  database = self.database,
                                  charset = self.charset)
        self.cursor = self.db.cursor()
        
    def close_database(self):
        try:
            self.db.close()
        except:
            pass

    def search(self, query_string):
        cmd_0 = ("select webpage.content, webpage.url,"
                 "w_relation.name "
                 "from webpage join w_relation "
                 "where webpage.id = w_relation.webpage_id "
                 "and w_relation.name like %s")
        # maybe cmd_0 is problematic, depending on 
        # whether MariaDB support utf8 natively
        # or not
        cmd_1 = ("select data.content, keyword "
               "from data join relation "
               "where data.id = relation.data_id "
               "and locate(keyword, %s) > 0")
        cmd = cmd_0
        self.cursor.execute(cmd, "%" + query_string + "%")
        ans = []
        for i in range(self.cursor.rowcount):
            result = self.cursor.fetchone()
            ans.append({"content": result[0], "url": result[1],
                        "keyword": result[2]})
        return ans
        #print(ans)
        #self.cursor.execute("select * from data", query_string)
        
    def deep_search(self, query_string):
        cmd_0 = ("select webpage.content, webpage.url,"
                 "w_relation.name "
                 "from webpage join w_relation "
                 "where webpage.id = w_relation.webpage_id "
                 "and webpage.content like %s")
        # maybe cmd_0 is problematic, depending on 
        # whether MariaDB support utf8 natively
        # or not
        cmd_1 = ("select data.content, keyword "
               "from data join relation "
               "where data.id = relation.data_id "
               "and locate(keyword, %s) > 0")
        cmd = cmd_0
        self.cursor.execute(cmd, "%" + query_string + "%")
        ans = []
        for i in range(self.cursor.rowcount):
            result = self.cursor.fetchone()
            ans.append({"content": result[0], "url": result[1],
                        "keyword": result[2]})
        return ans


    def get_all_data(self):
        temp_cursor = self.db.cursor()
        temp_cursor.execute("SELECT * FROM data")
        # may not be very efficient
        # print(temp_cursor.rowcount)
        # print(self.cursor.fetchone())
        for i in range(temp_cursor.rowcount):
            result = temp_cursor.fetchone()
            # print(result)
            yield {"id": result[0], "content": result[1]}
        return

    def insert_data(self, data):
        cmd = "INSERT INTO data(content) VALUES(%s)"
        select_cmd = "SELECT id from data where content = %s"
        # print(cmd, data)
        try:
            self.cursor.execute(cmd, data)
            self.db.commit()
        except:
            self.db.rollback()
        self.cursor.execute(select_cmd, data)
        return self.cursor.fetchone()[0]

    def insert_tag_data(self, keyword, data_id):
        cmd = ("INSERT INTO relation(keyword, data_id) "
               "SELECT %s, id from data where id = %s ")
        # print(cmd, (keyword, data_id))
        try:
            self.cursor.execute(cmd, (keyword, data_id))
            self.db.commit()
        except:
            self.db.rollback()

    def insert_webpage_data(self, url, page, names):
        print(url)
        # print(page)
        print(names)
        webpage_cmd = "INSERT INTO webpage(url, content) VALUES(%s, %s)"
        select_cmd = "SELECT id from webpage where url = %s"
        names_cmd = ("INSERT INTO w_relation(name, webpage_id) "
                     "SELECT %s, id from webpage where id = %s ")
        # print(cmd, data)
        try:
            self.cursor.execute(webpage_cmd, (url, str(page)))
            self.db.commit()
        except:
            print("in exception")
            self.db.rollback()
        self.cursor.execute(select_cmd, url)
        page_id = self.cursor.fetchone()[0]

        # print(cmd, (keyword, data_id))
        for name in names:
            try:
                self.cursor.execute(names_cmd, (name, page_id))
                self.db.commit()
            except:
                self.db.rollback()

    def create_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS relation")
        self.cursor.execute("DROP TABLE IF EXISTS data")
        cmd = ("CREATE TABLE data ("
               "id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
               "content TEXT NOT NULL,"
               "PRIMARY KEY (id))")
        self.cursor.execute(cmd)

    def create_webpage_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS w_relation")
        self.cursor.execute("DROP TABLE IF EXISTS webpage")
        cmd = ("CREATE TABLE webpage ("
               "id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
               "url TEXT NOT NULL,"
               "content TEXT NOT NULL,"
               "PRIMARY KEY (id))")
        self.cursor.execute(cmd)

    def create_webpage_relation_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS w_relation")
        cmd = ("CREATE TABLE w_relation ("
               "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"
               "name VARCHAR(16) NOT NULL,"
               "webpage_id MEDIUMINT UNSIGNED NOT NULL,"
               "PRIMARY KEY (id),"
               "FOREIGN KEY (webpage_id) REFERENCES webpage(id)"
               "    ON DELETE CASCADE ON UPDATE CASCADE)")
        self.cursor.execute(cmd)


    def create_relation_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS relation")
        cmd = ("CREATE TABLE relation ("
               "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"
               "keyword VARCHAR(16) NOT NULL,"
               "data_id MEDIUMINT UNSIGNED NOT NULL,"
               "PRIMARY KEY (id),"
               "FOREIGN KEY (data_id) REFERENCES data(id)"
               "    ON DELETE CASCADE ON UPDATE CASCADE)")
        self.cursor.execute(cmd)

    def __del__(self):
        try:
            self.close_database()
        except:
            pass

class PreProcess():
    def __init__(self):
        import jieba
        self.jieba = jieba
        import jieba.analyse
        self.jieba.analyse = jieba.analyse
        self.database = DatabaseManager()
        
    def analyse(self):
        self.database.create_relation_database()
        for data in self.database.get_all_data():
            for tag in self.jieba.cut(data["content"], cut_all=True):
                self.database.insert_tag_data(tag, data["id"])
            # print(data)
            # for tag in self.jieba.analyse.extract_tags(data["content"], topK = 10):
            #     print(tag, data["id"])
            #     self.database.insert_tag_data(tag, data["id"])
        
            
        
    def __del__(self):
        self.database.__del__()

def add_test_data():
    dm = DatabaseManager()
    dm.create_database()
    dm.create_relation_database()
    dm.insert_data("SQL 语句后面的分号？\n"
                   "某些数据库系统要求在每条 SQL 命令的末端使用分号。在我们的教程中不使用分号。\n"
                   "分号是在数据库系统中分隔每条 SQL 语句的标准方法，这样就可以在对服务器的相同请求中执行一条以上的语句。\n"
                   "如果您使用的是 MS Access 和 SQL Server 2000，则不必在每条 SQL 语句之后使用分号，不过某些数据库软件要求必须使用分号。")
    dm.insert_data("“计算机科学实验班（姚班）”由迄今为止唯一亚裔图灵奖得主姚期智院士于2005年创办，致力于培养与美国麻省理工学院、普林斯顿大学等世界一流高校本科生具有同等、甚至更高竞争力的领跑国际拔尖创新计算机科学人才。\n"
                   "“计算机科学实验班（姚班）”由姚期智院士主持，专业名为“计算机科学与技术（计算机科学实验班）”。该班专注于“因材施教”和“深耕精耕”相结合的特色人才培养模式，施行特色培养方案，注重学科基础教育，并设置覆盖计算机科学前沿领域的全英文教学专业核心课程；率先实施阶梯式培养模式：前两年以“通才教育”为主，实施计算机科学基础知识强化训练，后两年以“专才教育”为主，实施“理论和安全”“系统和应用”两大方向上的专业教育；着力营造多元化、富有活力的学术氛围，建立多方位、多层次的国际学术交流平台；注重提升专业水平，大四全年在著名高校和研究机构开展科研实践。\n"
                   "在姚期智院士亲力亲为的不懈努力下，姚班的办学理念和办学成果得到了国家领导人和教育部的充分肯定与大力支持，为国内拔尖创新人才培养模式的探索树立了突出典范。姚班“最优秀的本科生和最优秀的本科教育”已受到广泛关注和肯定，绝大多数毕业生踏上了继续学术深造的道路，正活跃在计算机科学领域的世界舞台上，逐渐崭露头角。")

