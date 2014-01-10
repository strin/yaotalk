#!/usr/bin/env python
#coding:utf-8


class Manager():
    def __init__(self):
        import shelve
        #from fetcher import DatabaseManager
        self.shelve_db = shelve.open('iiis-shelve')
        self.db = self.shelve_db['db']
        self.translate = self.shelve_db['translate']
        #self.mysql_db = DatabaseManager()

    def __del__(self):
        #self.mysql_db.close_database()
        self.shelve_db.close()

    def real_str(self, string):
        if string in self.translate:
            return self.translate[string]
        else:
            return string

    def query(self, word_list):
        real_list = [self.real_str(string) for string in word_list]
        ret = []
        for entry in self.db:
            add = False
            count = 0
            for tag in entry['tag']:
                for word in real_list:
                    if tag.find(word) >= 0:
                        count += 1
                        add = True
                        break
            if add:
                entry['value'] = count / len(entry['tag'])
                ret.append(entry)
        return ret

    def query_old(self, word):
        ans = []
        #self.mysql_db.connect_database()
        ans = self.mysql_db.search(word)
        #self.mysql_db.close_database()
        if ans:
            print("after query in database")
            return ans

        #self.mysql_db.connect_database()
        #ans_dict = self.mysql_db.deep_search(word)
        #self.mysql_db.close_database()
        print("look up in mysql")
        return [ans_dict]

    
    def add(self, tag_list, content):
        content['tag'] = tag_list
        self.db.append(content)
                        
        