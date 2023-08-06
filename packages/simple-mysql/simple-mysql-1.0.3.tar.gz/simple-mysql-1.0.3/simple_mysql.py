# -*- coding: utf-8 -*-
import re
import sys
import traceback
import mysql
import mysql.connector
from mysql.connector import errorcode

'''
config default set

config = {
    "host": '127.0.0.1',
    "user": 'root',
    'password': 'root',
    'database': 'test',
    'port': '3306',
    'dbms': 'mysql',
    'charset': 'utf8',
    'debug': True,
    'autocommit': True
}
'''

def is_numeric(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

def pdo_quote(string):
    return "'" + re.sub(r'(?<=[^\\])([\'\"])', r'\\\1', str(string)) + "'"

class db():
    configs = {}
    links = {}
    NumberLink = 0

    current = 0
    config = {}
    con = None
    cur = None
    dbdebug = False
    database = ''
    table_name = ''
    columns = []
    connected = False
    queryStr = ''
    SQLerror = {}
    lastInsertId = 0
    numRows = 0

    tmp_table = ''
    aliasString = ''
    fieldString = ''
    joinString = ''
    whereString = ''
    groupString = ''
    havingString = ''
    orderString = ''
    limitString = ''
    fetchSql = False

    whereStringArray = []
    whereValueArray = []

    SQL_logic = ['AND', 'OR', 'XOR']

    #connecton
    def connection(self,dbConfig):
        self.columns = []
        self.whereStringArray = []
        self.whereValueArray = []
        self.SQLerror = {}

        if 'debug' in dbConfig:
            if dbConfig['debug'] == True:
                self.dbdebug = True
            del dbConfig['debug']

        if 'password' not in dbConfig:
                self.throw_exception('database password no set')

        if 'host' not in dbConfig:
            dbConfig['host'] = '127.0.0.1'

        if 'user' not in dbConfig:
            dbConfig['user'] = 'root'

        if 'port' not in dbConfig:
            dbConfig['port'] = '3306'

        if 'autocommit' not in dbConfig:
            dbConfig['autocommit'] = True

        if 'dbms' not in dbConfig:
            dbConfig['dbms'] = 'mysql'
            self.throw_exception('database type no set')

        db.configs[0] = dbConfig
        self.current = 0
        self.config = dbConfig
        self.database = dbConfig['database']
        del dbConfig['dbms']

        try:
            self.con = mysql.connector.connect(**dbConfig)
            self.cur = self.con.cursor(dictionary=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                msg = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                msg = "Database does not exist"
            else:
                msg = err
            self.throw_exception('connection error：' + msg)
        if self.cur:
            db.links[self.current] = self.con
        else:
            self.throw_exception('connection error')

        self.connected = True
        db.NumberLink += 1
        return self

    # init
    def init(self, current, dbtable):
        self.current = current
        self.config = db.configs[current]
        self.con = db.links[current]
        self.cur = self.con.cursor(dictionary=True)
        if 'debug' in self.config and self.config['debug'] == True:
            self.dbdebug = True
        self.database = self.config['database']
        if self.in_db(dbtable):
            self.table_name = dbtable
        else:
            self.throw_exception('database' + self.config['database'] + 'no exsit' + dbtable + 'table')
        self.connected = True

    def in_db(self, dbtable):
        self.cur.execute('show tables')
        tables = self.cur.fetchall()
        key = 'Tables_in_' + self.database
        for table in tables:
            if dbtable == table[key]:
                return True
        return False

    def set_columns(self, dbtable):
        self.cur.execute("SHOW COLUMNS FROM `" + dbtable + "`")
        columns = self.cur.fetchall()
        self.columns = ['', ]
        for column in columns:
            if column['Key'] == 'PRI':
                self.columns[0] = column['Field']
            self.columns.append(column['Field'])

    def get_columns(self):
        return self.cur.column_names

    def where(self, *where):
        param_number = len(where)
        if isinstance(where[0], str):
            if param_number == 1:
                whereSubString = '( ' + where[0] + ' )'
            elif param_number > 1:
                if isinstance(where[1], tuple):
                    whereSubString = where[0] % where[1]
                elif isinstance(where[1], list):
                    whereSubString = where[0] % tuple(where[1])
                else:
                    param_array = []
                    for i in range(1, param_number):
                        param_array.append(where[i])
                    whereSubString = where[0] % tuple(param_array)
                whereSubString = '( ' + whereSubString + ' )'
        elif isinstance(where[0], dict):
            whereSubString = self._parseWhereArrayParam(where[0])
        else:
            self.throw_exception("string or dict need")
        self.whereStringArray.append(whereSubString)
        return self

    def parseWhere(self):
        length = len(self.whereStringArray)
        if length == 0:
            return
        if length > 1:
            self.whereString = ' WHERE ( ' + self.whereStringArray[0] + ' )'
            for i in range(1, length):
                self.whereString += ' AND ( ' + self.whereStringArray[i] + ' )'
        else:
            self.whereString = ' WHERE ' + self.whereStringArray[0]

    # table('table_name') | table('table_name AS t') | table('database.table_name AS t1')
    # table({'table_name':'', 'table_name':'t', 'database.table_name':'t1'})
    def table(self, table):
        if isinstance(table, str):
            self.tmp_table = table
        elif isinstance(table, dict):
            if len(table) == 0:
                self.throw_exception('empyt dict is fobirdden')
            self.tmp_table = ''
            for key, val in table.items():
                if val != '':
                    strpos = key.find('.')
                    if strpos == -1:
                        self.tmp_table += '`' + key.strip() + '` AS `' + val.strip() + '`,'
                    else:
                        self.tmp_table += key.strip() + ' AS `' + val.strip() + '`,'
                else:
                    strpos = key.find('.')
                    if strpos == -1:
                        self.tmp_table += '`' + key.strip() + '`,'
                    else:
                        self.tmp_table += key.strip() + ','
            self.tmp_table = self.tmp_table.rstrip(',')
        else:
            self.throw_exception('param type error："' + table + '"')
        return self

    def alias(self, alias):
        self.aliasString = ' AS `' + alias + '`'
        return self

    # field() | field('') | field('*') | field(True) | field('id,username as name, db.pass')
    # field({'id':'', 'username':'name', 'db.pass':''})
    # field('sex,head', True) | field(('sex', 'head'), True)

    def field(self, field='', filter=False):
        if field == True:
            self.set_columns(self.table_name if not self.tmp_table else self.tmp_table)
            self.fieldString += ' '
            columns_array = self.columns
            columns_array.pop(0)
            for column in columns_array:
                self.fieldString += '`' + column + '`,'
            self.fieldString = self.fieldString.rstrip(',')
            return self
        if filter:
            # 过滤字段
            if not isinstance(field, (str, set, list, tuple)):
                self.throw_exception("set、list、tuple need")
            self.set_columns(self.table_name if self.tmp_table == '' else self.tmp_table)
            columns_list = self.columns
            columns_list.pop(0)
            columns_dict = {}
            for index, item in enumerate(columns_list):
                columns_dict[str(index)] = item
            explode_array = []
            if isinstance(field, str):
                explode_array = re.split('\s{0,},\s{0,}', field.strip())
            else:
                for single_field in field:
                    explode_array.append(single_field.strip())
            for index, item in list(columns_dict.items()):
                if item in explode_array:
                    columns_dict.pop(index)
            for index, item in columns_dict.items():
                self.fieldString += '`' + item + '`,'
            self.fieldString = ' ' + self.fieldString.rstrip(',')
            return self
        if field == '' or field == '*':
            self.fieldString = ' *'
            return self
        if isinstance(field, str):
            field_array = field.split(',')
            field_array = list(map(self._addSpecialChar, field_array))
            self.fieldString = ','.join([item for item in field_array])
        elif isinstance(field, dict):
            for key, val in field.items():
                if val == '':
                    after_process_key = self._addSpecialChar(key)
                    self.fieldString += after_process_key + ','
                else:
                    after_process_key = self._addSpecialChar(key)
                    after_process_val = self._addSpecialChar(val)
                    self.fieldString += after_process_key + ' AS ' + after_process_val + ','
            self.fieldString = self.fieldString.rstrip(',')
        else:
            self.throw_exception("dict need")
        self.fieldString = ' ' + self.fieldString
        return self

    def order(self, order):
        if isinstance(order, str):
            self.orderString = ' ORDER BY ' + order
        elif isinstance(order, dict):
            self.orderString = ' ORDER BY '
            for key, val in order.items():
                if val == '':
                    self.orderString += '`' + key.strip() + '`,'
                else:
                    if val.lower() != 'asc' and val.lower() != 'desc':
                        self.throw_exception("please use asc or desc")
                    self.orderString += '`' + key.strip() + '` ' + val + ','
            self.orderString = self.orderString.rstrip(',')
        else:
            self.throw_exception("string or dict need")
        return self

    def limit(self, *limit):
        param_number = len(limit)
        if param_number == 1:
            if not isinstance(limit[0], (int, str)):
                self.throw_exception("param error")
            if isinstance(limit[0], str):
                if not re.match('^\d+\s{0,},\s{0,}\d+$', limit[0].strip()) and not re.match('^\d+$', limit[0].strip()):
                    self.throw_exception("param error")
            self.limitString = ' LIMIT ' + str(limit[0])
        elif param_number == 2:
            for i in range(2):
                if not is_numeric(limit[i]):
                    self.throw_exception("param error")
            self.limitString = ' LIMIT ' + str(limit[0]) + ',' + str(limit[1])
        else:
            self.throw_exception("need one or two param")
        return self

    def page(self, page_number, amount):
        if not is_numeric(page_number) or not is_numeric(amount):
            self.throw_exception("number need")
        start = (int(page_number) - 1) * int(amount)
        self.limitString = ' LIMIT ' + str(start) + ',' + str(amount)
        return self

    def group(self, group):
        if not isinstance(group, str):
            self.throw_exception("string need")
        self.groupString = ' GROUP BY ' + group
        return self

    def having(self, having):
        if not isinstance(having, str):
            self.throw_exception("string need")
        self.havingString = ' HAVING BY ' + having
        return self

    def join(self, join):
        if isinstance(join, str):
            self.joinString += ' INNER JOIN ' + join
        elif isinstance(join, (list, tuple)):
            if len(join) != 2:
                self.throw_exception("need two param")
            self.joinString += ' ' + join[1] + ' JOIN ' + join[0]
        else:
            self.throw_exception("join子句的参数只支持字符串或list、tuple")
        return self

    def fetchSql(self, fetchSql=True):
        self.fetchSql = fetchSql
        return self

    def count(self, field='*'):
        self.fieldString = ' COUNT(' + field + ') AS f_count'
        self.limitString = ' LIMIT 1'
        is_fetchSql = False
        if self.fetchSql == True:
            is_fetchSql = True
        res = self.select()
        if is_fetchSql:
            return res
        else:
            # print(res)
            return res[0]['f_count']

    def max(self, field):
        self.fieldString = ' MAX(' + field + ') AS f_max'
        self.limitString = ' LIMIT 1'
        is_fetchSql = False
        if self.fetchSql == True:
            is_fetchSql = True
        res = self.select()
        if is_fetchSql:
            return res
        else:
            return res[0]['f_max']

    def min(self, field):
        self.fieldString = ' MIN(' + field + ') AS f_min'
        self.limitString = ' LIMIT 1'
        is_fetchSql = False
        if self.fetchSql == True:
            is_fetchSql = True
        res = self.select()
        if is_fetchSql:
            return res
        else:
            return res[0]['f_min']

    def avg(self, field):
        self.fieldString = ' AVG(' + field + ') AS f_avg'
        self.limitString = ' LIMIT 1'
        is_fetchSql = False
        if self.fetchSql == True:
            is_fetchSql = True
        res = self.select()
        if is_fetchSql:
            return res
        else:
            return res[0]['f_avg']

    def sum(self, field):
        self.fieldString = ' SUM(' + field + ') AS f_sum'
        self.limitString = ' LIMIT 1'
        is_fetchSql = False
        if self.fetchSql == True:
            is_fetchSql = True
        res = self.select()
        if is_fetchSql:
            return res
        else:
            return res[0]['f_sum']

    def buildSql(self):
        sqlString = ''
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        self.fieldString = ' *' if self.fieldString == '' else self.fieldString
        self.parseWhere()
        sqlString += 'SELECT' + self.fieldString + ' FROM ' + table_name + self.joinString + self.whereString + self.groupString + self.havingString + self.orderString + self.limitString
        buildSql = self._replaceSpecialChar('%s', self.whereValueArray, sqlString)
        self._clearSubString()
        return '( ' + buildSql.replace("`","") + ' )'

    def find(self, primary_key_value=''):
        sqlString = ''
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        if primary_key_value != '':
            self.set_columns(self.table_name if self.tmp_table == '' else self.tmp_table)
            self.whereStringArray.append('`' + self.columns[0] + '` = %s')
            self.whereValueArray.append(primary_key_value)
        self.limitString = ' LIMIT 1'
        self.fieldString = ' *' if self.fieldString == '' else self.fieldString
        self.parseWhere()
        sqlString += 'SELECT' + self.fieldString + ' FROM ' + table_name + self.joinString + self.whereString + self.groupString + self.havingString + self.orderString + self.limitString
        res = self.query(sqlString.replace("`",""), True)
        return res

    def select(self, query=True):
        sqlString = ''
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        self.fieldString = ' *' if self.fieldString == '' else self.fieldString
        self.parseWhere()
        sqlString += 'SELECT' + self.fieldString + ' FROM ' + table_name + self.joinString + self.whereString + self.groupString + self.havingString + self.orderString + self.limitString
        if query == False:
            self.fetchSql = True
        # print(sqlString)
        res = self.query(sqlString.replace("`",""))
        # print(sqlString)
        return res

    def add(self, data=''):
        field_str = ''
        if data != '':
            if not isinstance(data, dict):
                self.throw_exception('dict need')
            length = len(data)
            if length == 0:
                placeholder = ''
            else:
                for key, val in data.items():
                    field_str += '`' + key + '`,'
                    self.whereValueArray.append(val)
                field_str = field_str.rstrip(',')
                placeholder = '%s'
                for i in range(1, length):
                    placeholder += ',%s'
        else:
            placeholder = ''
        if self.tmp_table != '':
            table_name = self.tmp_table
        else:
            table_name = '`' + self.table_name + '`'
        sqlString = 'INSERT INTO ' + table_name + ' (' + field_str + ') VALUES (' + placeholder + ')'
        # print(sqlString)
        res = self.execute(sqlString)
        if isinstance(res, str) or res == False:
            return res
        self.lastInsertId = self.cur.lastrowid
        return self.lastInsertId

    def addAll(self, dataList):
        if not isinstance(dataList, (list, tuple)):
            self.throw_exception('list or tuple need')
        field_str = ''
        fieldList = []
        number = len(dataList)
        valueListStr = ''
        if number == 0:
            self.throw_exception('empty list')
        if not isinstance(dataList[0], dict):
            self.throw_exception('list or tuple need')
        number_field = len(dataList[0])
        if number_field == 0:
            valueListStr += '()'
            for i in range(1, number):
                if not isinstance(dataList[i], dict):
                    self.throw_exception('list or tuple need')
                valueListStr += ',()'
        else:
            valueStr = '('
            for key, val in dataList[0].items():
                fieldList.append(key)
                self.whereValueArray.append(val)
                field_str += key + ','
                valueStr += '%s,'
            field_str = field_str.rstrip(',')
            valueStr = valueStr.rstrip(',')
            valueStr += ')'
            valueListStr += valueStr
            for i in range(1, number):
                for j in range(number_field):
                    self.whereValueArray.append(dataList[i][fieldList[j]])
                valueListStr += ',' + valueStr
        if self.tmp_table != '':
            table_name = self.tmp_table
        else:
            table_name = '`' + self.table_name + '`'
        sqlString = 'INSERT INTO ' + table_name + ' (' + field_str + ') VALUES ' + valueListStr
        res = self.execute(sqlString)
        if isinstance(res, str) or res == False:
            return res
        self.lastInsertId = self.cur.lastrowid
        return self.lastInsertId

    def setField(self, *field):
        param_number = len(field)
        if field == 0:
            self.throw_exception('The setField clause must pass in parameters')
        self.parseWhere()
        if self.whereString == '':
            self.set_columns(self.table_name if self.tmp_table == '' else self.tmp_table)
            if isinstance(field[0], dict) and self.columns[0] != '' and self.columns[0] in field[0]:
                if isinstance(field[0][self.columns[0]], (list, tuple)):
                    if field[0][self.columns[0]][0].upper() == 'EXP':
                        self.whereString = ' WHERE `' + self.columns[0] + '` = ' + field[0][self.columns[0]][1].strip()
                    else:
                        self.throw_exception('The setField clause only supports exP expression updates')
                else:
                    self.whereString = ' WHERE `' + self.columns[0] + '` = %s'
                    self.whereValueArray.append(field[0][self.columns[0]])
                del field[0][self.columns[0]]
            elif self.columns[0] == '':
                self.throw_exception('Does not have any update criteria and specifies that the data table does not have a primary key and is not allowed to perform an update operation')
            else:
                self.throw_exception('There are no update conditions, and the data object itself does not contain primary key fields and is not allowed to perform update operations')
        setFieldStr = ''
        updateValueArray = []
        if isinstance(field[0], str):
            if param_number != 2:
                self.throw_exception('The setField clause takes two parameters (property name, property value)')
            if field[0].find('.') == -1:
                setFieldStr += '`' + field[0].strip() + '` = %s'
            else:
                setFieldStr += field[0].strip() + ' = %s'
            updateValueArray.append(field[1])
        elif isinstance(field[0], dict):
            if param_number != 1:
                self.throw_exception('The setField clause accepts only one array argument')
            for key, val in field[0].items():
                if isinstance(val, (list, tuple)):
                    if val[0].upper() == 'EXP':
                        if key.find('.') == -1:
                            setFieldStr += '`' + key.strip() + '` = ' + val[1].strip() + ','
                        else:
                            setFieldStr += key.strip() + ' = ' + val[1].strip() + ','
                    else:
                        self.throw_exception('The setField clause only supports exP expression updates')
                else:
                    if key.find('.') == -1:
                        setFieldStr += '`' + key.strip() + '` = %s,'
                    else:
                        setFieldStr += key.strip() + ' = %s,'
                    updateValueArray.append(val)
            setFieldStr = setFieldStr.rstrip(',')
        else:
            self.throw_exception('Wrong parameter type passed in the setField clause：' + field[0])
        self.whereValueArray = updateValueArray + self.whereValueArray
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        sqlString = 'UPDATE ' + table_name + self.joinString + ' SET ' + setFieldStr + self.whereString + self.orderString + self.limitString
        res = self.execute(sqlString)
        return res

    def setInc(self, field, value=1):
        data = {}
        data[field] = ['EXP', field + ' + ' + str(value)]
        return self.save(data)

    def setDec(self, field, value=1):
        data = {}
        data[field] = ['EXP', field + ' - ' + str(value)]
        return self.save(data)

    def save(self, data):
        if not isinstance(data, dict):
            self.throw_exception('The save clause accepts only array parameters')
        self.parseWhere()
        if self.whereString == '':
            self.set_columns(self.table_name if self.tmp_table == '' else self.tmp_table)
            if self.columns[0] != '' and self.columns[0] in data:
                if isinstance(data[self.columns[0]], (list, tuple)):
                    if data[self.columns[0]][0].upper() == 'EXP':
                        self.whereString = ' WHERE `' + self.columns['PRI'] + '` = ' + data[self.columns[0]][1].strip()
                    else:
                        self.throw_exception('The save clause supports only exP expression updates')
                else:
                    self.whereString = ' WHERE `' + self.columns[0] + '` = %s'
                    self.whereValueArray.append(data[self.columns[0]])
                del data[self.columns[0]]
            elif self.columns[0] == '':
                self.throw_exception('Does not have any update criteria and specifies that the data table does not have a primary key and is not allowed to perform an update operation')
            else:
                self.throw_exception('There are no update conditions, and the data object itself does not contain primary key fields and is not allowed to perform update operations')
        setFieldStr = ''
        updateValueArray = []
        for key, val in data.items():
            if isinstance(val, (list, tuple)):
                # 支持exp表达式进行数据更新
                if val[0].upper == 'EXP':
                    if key.find('.') == -1:
                        setFieldStr += '`' + key.strip() + '` = ' + val[1].strip() + ','
                    else:
                        setFieldStr += key.strip() + ' = ' + val[1].strip() + ','
                else:
                    self.throw_exception('The save clause supports only exP expression updates')
            else:
                if key.find('.') == -1:
                    setFieldStr += '`' + key.strip() + '` = %s,'
                else:
                    setFieldStr += key.strip() + ' = %s,'
                updateValueArray.append(val)
        setFieldStr = setFieldStr.rstrip(',')
        self.whereValueArray = updateValueArray + self.whereValueArray
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        sqlString = 'UPDATE ' + table_name + self.joinString + ' SET ' + setFieldStr + self.whereString + self.orderString + self.limitString
        res = self.execute(sqlString)
        return res

    def delete(self, table=''):
        sqlString = ''
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        if table != '':
            table = ' ' + table
        self.parseWhere()
        if self.whereString == '':
            if self.joinString == '' or self.joinString.upper().find(' ON ') == -1:
                self.throw_exception('No conditions are passed in and the delete operation is not allowed')
        sqlString = 'DELETE' + table + ' FROM ' + table_name + self.joinString + self.whereString + self.orderString + self.limitString
        res = self.execute(sqlString)
        return res

    def deleteById(self, primary_key_value, table=''):
        sqlString = ''
        if self.tmp_table != '':
            table_name = self.tmp_table + self.aliasString
        else:
            table_name = '`' + self.table_name + '`' + self.aliasString
        if table != '':
            table = ' ' + table
        if primary_key_value != '':
            self.set_columns(self.table_name if self.tmp_table == '' else self.tmp_table)
            self.whereStringArray.append('`' + self.columns[0] + '` = %s')
            self.whereValueArray.append(primary_key_value)
        self.parseWhere()

        sqlString = 'DELETE' + table + ' FROM ' + table_name + self.joinString + self.whereString
        res = self.execute(sqlString)
        return res

    def query(self, queryStr, is_find=False):
        if not isinstance(queryStr, str):
            self.throw_exception('string is need')
        if self.fetchSql == True:
            buildSql = self._replaceSpecialChar('%s', self.whereValueArray, queryStr)
            self._clearSubString()
            return buildSql
        try:
            self.queryStr = self._replaceSpecialChar('%s', self.whereValueArray, queryStr)
            tmp_whereValueArray = self.whereValueArray
            self._clearSubString()
            # print(tmp_whereValueArray)
            if len(tmp_whereValueArray) > 0:
                self.cur.execute(queryStr, tmp_whereValueArray)
            else:
                self.cur.execute(queryStr)
            if is_find == True:
                res = self.cur.fetchone()
            else:
                res = self.cur.fetchall()
            return res
        except mysql.connector.Error as err:
            return self.haveErrorThrowException(err)

    def execute(self, execStr):
        if not isinstance(execStr, str):
            self.throw_exception('string is need')
        if self.fetchSql == True:
            buildSql = self._replaceSpecialChar('%s', self.whereValueArray, execStr)
            self._clearSubString()
            return buildSql
        try:
            self.queryStr = self._replaceSpecialChar('%s', self.whereValueArray, execStr)
            tmp_whereValueArray = self.whereValueArray
            self._clearSubString()
            if len(tmp_whereValueArray) > 0:
                self.cur.execute(execStr, tmp_whereValueArray)
            else:
                self.cur.execute(execStr)
            self.numRows = self.cur.rowcount
            return self.numRows
        except mysql.connector.Error as err:
            return self.haveErrorThrowException(err)

    # If consistent_snapshot is True, Connector/Python sends WITH CONSISTENT SNAPSHOT with the statement. MySQL ignores this for isolation levels for which that option does not apply.
    # isolation_level: permitted values are 'READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', and 'SERIALIZABLE'
    # The readonly argument can be True to start the transaction in READ ONLY mode or False to start it in READ WRITE mode. If readonly is omitted, the server's default access mode is used.
    def startTrans(self, consistent_snapshot=False, isolation_level=None, readonly=False):
        for link in db.links.values():
            link.start_transaction(consistent_snapshot, isolation_level, readonly)

    def inTrans(self):
        return self.con.in_transaction

    def rollback(self):
        for link in db.links.values():
            link.rollback()

    def commit(self):
        for link in db.links.values():
            link.commit()

    def getLastSql(self):
        if not self.dbdebug:
            self.throw_exception('Please turn on DEBUG mode first')
        return self.queryStr

    def _sql(self):
        # mysql.connector的MySQLCursor类有statement属性，可以直接拿到最后执行的SQL语句
        return self.cur.statement

    def _parseWhereArrayParam(self, whereArrayParam):
        logic = ' AND '
        whereSubString = ''
        if '_complex' in whereArrayParam:
            whereSubString = '( ' + self._parseWhereArrayParam(whereArrayParam['_complex']) + ' )'
            del whereArrayParam['_complex']
        if '_logic' in whereArrayParam:
            if whereArrayParam['_logic'].upper() in self.SQL_logic:
                logic = ' ' + whereArrayParam['_logic'].upper() + ' '
            else:
                self.throw_exception('The logic operator specified by the _logic parameter is not supported："' + whereArrayParam['_logic'] + '"')
            del whereArrayParam['_logic']
        if '_string' in whereArrayParam:
            whereSubString += logic + '( ' + whereArrayParam['_string'] + ' )'
            del whereArrayParam['_string']
        if '_query' in whereArrayParam:
            explode_query = whereArrayParam['_query'].split('&')
            explode_array = {}
            for key_val in explode_query:
                explode_sub_query = key_val.split('=')
                explode_array[explode_sub_query[0]] = explode_sub_query[1]
            if '_logic' in explode_array:
                if explode_array['_logic'].upper() in self.SQL_logic:
                    sub_logic = ' ' + explode_array['_logic'].upper() + ' '
                else:
                    self.throw_exception('he logic operator specified by the _logic parameter in _query is not supported："' + explode_array['_logic'] + '"')
                del explode_array['_logic']
            querySubString = ''
            for key, val in explode_array.items():
                start = key.find('.')
                if start != -1:
                    querySubString += sub_logic + key + " = '" + val + "'"
                else:
                    querySubString += sub_logic + "`" + key + "` = '" + val + "'"
            querySubString = querySubString.lstrip(sub_logic)
            whereSubString += logic + '( ' + querySubString + ' )'
            del whereArrayParam['_query']
        for key, val in whereArrayParam.items():
            whereArraySubString = ''
            have_and = key.find('&')
            have_or = key.find('|')
            if isinstance(val, (list, tuple)):
                if have_and == -1 and have_or == -1:
                    whereArraySubString += self._singleKey2Array(key, val)
                elif (have_and != -1 and have_or == -1) or (have_and == -1 and have_or != -1):
                    if have_and != -1:
                        string_logic = '&'
                        sub_logic = ' AND '
                    else:
                        string_logic = '|'
                        sub_logic = ' OR '
                    explode_array = key.split(string_logic)
                    signal = 1
                    if len(explode_array) == len(val):
                        signal = 1
                    else:
                        if val[-1] == '' or val[-1] == 's':
                            signal = 1
                        elif val[-1] == 'm':
                            signal = 2
                        elif val[-1] == 'e':
                            signal = 3
                        else:
                            self.throw_exception('指定的查询方式不受支持："' + val[-1] + '"')
                    if signal == 1:
                        index = 0
                        for explode_val in explode_array:
                            if isinstance(val[index], (list, tuple)):
                                whereArraySubString += self._singleKey2Array(explode_val, val[index])
                            else:
                                start = explode_val.find('.')
                                if start != -1:
                                    whereArraySubString += sub_logic + explode_val + " = %s"
                                else:
                                    whereArraySubString += sub_logic + "`" + explode_val + "` = %s"
                                self.whereValueArray.append(val[index])
                            index += 1
                    elif signal == 2:
                        for explode_val in explode_array:
                            get_parseMultiQuery = self._parseMultiQuery(explode_val, val)
                            whereArraySubString += sub_logic + get_parseMultiQuery
                    else:
                        for explode_val in explode_array:
                            get_parseExpQuery = self._parseExpQuery(explode_val, val)
                            whereArraySubString += sub_logic + get_parseExpQuery
                    whereArraySubString = whereArraySubString.lstrip(sub_logic)
                    whereArraySubString = '( ' + whereArraySubString + ' )'
                else:
                    self.throw_exception('"|" and "&" cannot be used together in quick query mode')
            else:
                start = key.find('.')
                if have_and == -1 and have_or == -1:
                    if start != -1:
                        whereArraySubString += key + " = %s"
                    else:
                        whereArraySubString += "`" + key + "` = %s"
                    self.whereValueArray.append(val)
                elif (have_and != -1 and have_or == -1) or (have_and == -1 and have_or != -1):
                    if have_and != -1:
                        string_logic = '&'
                        sub_logic = ' AND '
                    else:
                        string_logic = '|'
                        sub_logic = ' OR '
                    explode_array = key.split(string_logic)
                    whereArraySubString = ''
                    for explode_val in explode_array:
                        start = explode_val.find('.')
                        if start != -1:
                            whereArraySubString += sub_logic + explode_val + " = %s"
                        else:
                            whereArraySubString += sub_logic + "`" + explode_val + "` = %s"
                        self.whereValueArray.append(val)
                    whereArraySubString = whereArraySubString.lstrip(sub_logic)
                    whereArraySubString = '( ' + whereArraySubString + ' )'
                else:
                    self.throw_exception('"|" and "&" cannot be used together in quick query mode')
            whereSubString += logic + whereArraySubString
        whereSubString = whereSubString.lstrip(logic)
        return whereSubString

    def _singleKey2Array(self, key, array):
        # and or is need
        if array[-1] == '' or array[-1] == 'm':
            # mult condition
            return self._parseMultiQuery(key, array)
        elif array[-1] == 'e':
            # complex
            return self._parseExpQuery(key, array)
        else:
            self.throw_exception('not supported："' + array[-1] + '"')

    def _parseExpQuery(self, column, array):
        # 记得，传进来的array参数末尾留有两个位，一个记录逻辑符，一个记录查询类型
        expQueryString = ''
        start = column.find('.')
        specialChar_index = column.find('`')
        if specialChar_index == -1 and start == -1:
            column = '`' + column + '`'
        exp_type = array[0].upper()
        if exp_type == "EQ":
            expQueryString += column + ' = %s'
            self.whereValueArray.append(array[1])
        elif exp_type == "NEQ":
            expQueryString += column + ' <> %s'
            self.whereValueArray.append(array[1])
        elif exp_type == "GT":
            expQueryString += column + ' > %s'
            self.whereValueArray.append(array[1])
        elif exp_type == "EGT":
            expQueryString += column + ' >= %s'
            self.whereValueArray.append(array[1])
        elif exp_type == "LT":
            expQueryString += column + ' < %s'
            self.whereValueArray.append(array[1])
        elif exp_type == "ELT":
            expQueryString += column + ' <= %s'
            self.whereValueArray.append(array[1])
        elif exp_type == "LIKE" or exp_type == "NOTLIKE" or exp_type == "NOT LIKE":
            if exp_type == "LIKE":
                string = ' LIKE '
            else:
                string = ' NOT LIKE '
            if isinstance(array[1], (list, tuple, set)):
                logic = ' AND '
                if array[2] != '':
                    if array[2].upper() in self.SQL_logic:
                        logic = ' ' + array[2].upper() + ' '
                    else:
                        self.throw_exception('[NOT] LIKE The logical operator in the query"' + array[2] + '"not supported')
                for val in array[1]:
                    expQueryString += logic + column + string + ' %s'
                    self.whereValueArray.append(str(val))
                expQueryString = expQueryString.lstrip(logic)
                expQueryString = '( ' + expQueryString + ' )'
            elif isinstance(array[1], str):
                expQueryString += column + string + ' %s'
                self.whereValueArray.append(array[1])
            else:
                self.throw_exception('[NOT] LIKEThe second parameter in the query must be a string or list、tuple、set')
        elif exp_type == "BETWEEN" or exp_type == "NOTBETWEEN" or exp_type == "NOT BETWEEN":
            # 示例 array('between','1,8') | array('between',1,8) | array('between',array('1','8'))
            if exp_type == "BETWEEN":
                string = ' BETWEEN '
            else:
                string = ' NOT BETWEEN '
            expQueryString += column + string + '%s AND %s'
            if isinstance(array[1], (list, tuple)):
                self.whereValueArray.append(array[1][0])
                self.whereValueArray.append(array[1][1])
            elif isinstance(array[1], str):
                explode_array = array[1].split(',')
                if len(explode_array) != 2:
                    self.throw_exception('Error parameter after [NOT]BETWEEN expression query：' + array[1])
                self.whereValueArray.append(explode_array[0].strip())
                self.whereValueArray.append(explode_array[1].strip())
            elif is_numeric(array[1]):
                if not is_numeric(array[2]):
                    self.throw_exception('Error parameter after [NOT]BETWEEN expression query(two number expected)');
                self.whereValueArray.append(array[1])
                self.whereValueArray.append(array[2])
            else:
                self.throw_exception('Parameter error after [NOT]BETWEEN expression query:' + array[1])
        elif exp_type == "IN" or exp_type == "NOTIN" or exp_type == "NOT IN":
            # for example ：array('not	in',array('a','b','c')) | array('not in','a,b,c')
            if exp_type == "IN":
                string = ' IN '
            else:
                string = ' NOT IN '
            if isinstance(array[1], (list, tuple)):
                length = len(array[1])
                if length == 0:
                    self.throw_exception('The array argument after the [NOT]IN expression query is empty：array()')
                expQueryString += column + string + '('
                expQueryString += '%s'
                self.whereValueArray.append(array[1][0])
                for i in range(1, length):
                    expQueryString += ',%s'
                    self.whereValueArray.append(array[1][i])
                expQueryString += ')'
            elif isinstance(array[1], str):
                explode_array = array[1].split(',')
                length = len(explode_array)
                expQueryString += column + string + '('
                expQueryString += '%s'
                self.whereValueArray.append(explode_array[0])
                for i in range(1, length):
                    expQueryString += ',%s'
                    self.whereValueArray.append(explode_array[i])
                expQueryString += ')'
            else:
                self.throw_exception('Parameter error after [NOT]IN expression query:' + array[1])
        elif exp_type == "EXP":
            if isinstance(array[1], str):
                expQueryString += column + array[1]
            else:
                self.throw_exception('Error parameter after exP for expression query：' + array[1])
        else:
            self.throw_exception('Error parameter after exP for expression query："' + array[0] + '"')
        return expQueryString

    def _parseMultiQuery(self, column, array):
        multiQueryString = ''
        start = column.find('.')
        specialChar_index = column.find('`')
        if specialChar_index == -1 and start == -1:
            column = '`' + column + '`'
        length = len(array) - 2
        logic = ' AND '
        if array[-2] != '':
            if array[-2].upper() in self.SQL_logic:
                logic = ' ' + array[-2].upper() + ' '
            else:
                self.throw_exception(array[-2] + '"not supported')
        for i in range(length):
            if isinstance(array[i], (list, tuple)):
                multiQueryString += logic + self._singleKey2Array(column, array[i])
            else:
                multiQueryString += logic + column + ' = %s'
                self.whereValueArray.append(array[i])
        multiQueryString = multiQueryString.lstrip(logic)
        multiQueryString = '( ' + multiQueryString + ' )'
        return multiQueryString

    def _addSpecialChar(self, value):
        value = value.strip()
        if value.find(' as ') != -1:
            value = re.sub('\s+', ' ', value)
            MatchObject = re.search('(?<=\s{1}as\s{1})\w+$', value, re.I)
            if MatchObject == None:
                self.throw_exception('"' + value + '"match error')
            else:
                table_alias = MatchObject.group(0)
            value = re.sub('(?<=\s{1}as\s{1})\w+$', '`' + table_alias + '`', value, 0, re.I)
            table_name = re.search('^.*(?=\s{1}as\s{1}`)', value, re.I).group(0)
            if re.match('^\w+$', table_name):
                value = re.sub('^\w+(?=\s{1}as\s{1}`)', '`' + table_name + '`', value, 0, re.I)
        elif re.match('^\w+\.\w+$', value):
            pass
        else:
            if not re.search('\W+', value):
                value = '`' + value + '`'
        return value

    def _replaceSpecialChar(self, pattern, replacement, subject):
        for val in replacement:
            if isinstance(val, int):
                subject = re.sub(pattern, str(val), subject, 1)
            else:
                subject = re.sub(pattern, pdo_quote(val), subject, 1)
        return subject

    # get last line from someone file
    def _get_file_lastline(self, file_name, n=1):
        try:
            with open(file_name, 'rb') as f:
                f.seek(-1, 2)
                content = ''
                while n > 0:
                    s = f.read(1).decode('ascii')
                    if s == '\n' and content:
                        n -= 1
                        if n == 0:
                            break
                        content = ''
                    content = s + content
                    f.seek(-2, 1)
                return content.strip()
        except BaseException as e:
            self.throw_exception(e)

    def _clearSubString(self):
        self.SQLerror = {}
        self.fieldString = ''
        self.joinString = ''
        self.whereString = ''
        self.groupString = ''
        self.havingString = ''
        self.orderString = ''
        self.limitString = ''
        self.aliasString = ''
        self.tmp_table = ''
        self.fetchSql = False
        self.whereStringArray = []
        self.whereValueArray = []

    def haveErrorThrowException(self, err):
        if self.dbdebug:
            self.SQLerror = {
                'errno': err.errno,
                'sqlstate': err.sqlstate,
                'msg': err.msg,
                'sql': self.queryStr
            }
        return False

    def showError(self):
        if self.dbdebug:
            if 'errno' in self.SQLerror:
                print('Error Code:    ' + str(self.SQLerror['errno']))
                print('SQLSTATE:      ' + str(self.SQLerror['sqlstate']))
                print('Error Message: ' + str(self.SQLerror['msg']))
                print('Error SQL:     ' + str(self.SQLerror['sql']))
            else:
                print("no error happen")
        else:
            print("take on debug model")

    def getNumRows(self):
        return self.numRows

    def close(self):
        if self.connected:
            # self.cur.close()
            self.con.close()

    def __del__(self):
        self.close()

    def throw_exception(self, errMsg, ignore_debug=False):
        if self.dbdebug or ignore_debug:
            print('Error: ' + errMsg + '\n\n' + 'error: \n')
            length = len(traceback.format_stack())
            for i in range(length - 1):
                print(traceback.format_stack()[i])
        else:
            errMsg = "error happen"
            print(errMsg)
        sys.exit(0)

if __name__ == '__main__':
    print('mysql orm for humans')
