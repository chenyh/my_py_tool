# -*- coding: utf-8 -*-

import os, sys
import locale


def encode(val):
	return val

'''
        import locale
        encoding = locale.getdefaultlocale()[1]
        res = ''
        try : 
                res = val.encode(encoding)
        except :
                res = val
        return res
'''

#返回表的dict
#请注意格式是按cell的概念先行后列: dictRes[sheet_index][row][col] 和平时表述习惯不同
#sheet_id: 0 sh.name: 表格1 row: 7 col: 4 cellname: E8 value: this_cell = res[0][7][4]
def Xls2Dict(xls_name):
        import xlrd

        dictRes = {}
        book = xlrd.open_workbook(xls_name, formatting_info=True)

        for sheet_id in xrange(book.nsheets):
                sh = book.sheet_by_index(sheet_id)

                tmp_book_dict = {"name": sh.name, "nrows":sh.nrows, "ncols": sh.ncols, }

                for r in xrange(sh.nrows):
                        tmp_row_dict = {}
                        for c in xrange(sh.ncols):
                                cell_value = sh.cell_value(r,c)
                                cell_type  = sh.cell_type(r,c)
                                tmp_row_dict[c] = { "type": cell_type, "value": cell_value }
                                #print "sheet_id:", sheet_id,"sh.name:", sh.name, "row:", r, "col:", c, "cellname:", xlrd.cellname(r,c), "value:", cell_value
                        tmp_book_dict[r] = tmp_row_dict

                dictRes[sheet_id] = tmp_book_dict

        return dictRes

def XlsSheet2Dict(xls_name, sheet_name = ""):
        import xlrd

        dictRes = {}
        book = xlrd.open_workbook(xls_name, formatting_info=True)

        for sheet_id in xrange(book.nsheets):
                sh = book.sheet_by_index(sheet_id)
                if len(sheet_name) and encode(sheet_name) != encode(sh.name):
                        continue
                tmp_book_dict = {"name": sh.name, "nrows":sh.nrows, "ncols": sh.ncols, }
                for r in xrange(sh.nrows):
                        tmp_row_dict = {}
                        for c in xrange(sh.ncols):
                                cell_value = sh.cell_value(r,c)
                                cell_type  = sh.cell_type(r,c)
                                if isinstance(cell_value, unicode):
                                        cell_value = cell_value.encode("utf-8")
                                tmp_row_dict[c] = { "type": cell_type, "value": cell_value }
                                #print "sheet_id:", sheet_id,"sh.name:", sh.name, "row:", r, "col:", c, "cellname:", xlrd.cellname(r,c), "value:", cell_value
                        tmp_book_dict[r] = tmp_row_dict
                return tmp_book_dict
        return dictRes


def ChineseEncode(name):
        if not isinstance(name, unicode):
                return name
        encoding = locale.getdefaultlocale()[1]
        try :
                res = name.encode(encoding)
        except :
                res = name
        return res

indent_space = ' ' * 4
max_indent_cnt = 100


# 计算缩进
def getIndent( indentFlg, indentCnt):
        result = ''

        if not indentFlg:
                return result

        for i in range( 0, indentCnt):
                result = result + indent_space

        return result

# 将python dict 转换为lpc dict
def PythonDict2Lpc( data, indentFlg=False, indentCnt=0):

        if indentCnt > max_indent_cnt:
                indentFlg = False

        result = '{'
        if indentFlg :
                result = result + "\n"

        # 遍历 数据
        keys = data.keys()

        keys.sort()

        for key in keys:
                value = data[key]

                result = result + getIndent(indentFlg, indentCnt+1)

                strKey = (PythonData2Lpc(key,indentFlg, indentCnt+1))
                strValue = (PythonData2Lpc(value,indentFlg, indentCnt+1))

                result = result  + ("%s:%s, "%(strKey, strValue))
                if indentFlg:
                        result = result + "\n"

        result = result + getIndent(indentFlg, indentCnt) + '}'
        return result

# 将python list 转换为lpc list
def PythonList2Lpc( data, indentFlg=False, indentCnt=0):
        if indentCnt > max_indent_cnt:
                indentFlg = False
        
        result = '['
        
        if indentFlg:
                result = result + "\n"
        # 遍历 数据
        reslen = 0
        for value in data:
                        tmpres = getIndent(indentFlg, indentCnt+1) + ("%s, "%(PythonData2Lpc(value,indentFlg, indentCnt+1)))
                        result = "%s%s"%(result,tmpres)
                        if indentFlg:
                                result = result + "\n"
                        reslen += len(tmpres)
                        if reslen > 200:
                                reslen = 0
                                result = result + "\n"
                
        result = result + getIndent(indentFlg, indentCnt) + ']'
        return result


# 将python tuple 转换为lpc tuple
def PythonTuple2Lpc( data, indentFlg=False, indentCnt=0):
        return PythonList2Lpc(data, indentFlg, indentCnt)

# 将python数据转换为lpc数据
def PythonData2Lpc( data, indentFlg=False, indentCnt=0):
        if isinstance(data, str):
                #data = data.decode("utf-8")
                if data.startswith("@@"):
                        return '%s'%(data[2:len(data)])
                if HasCn(data):
                        return 'T("%s")'%(data)
                return '"%s"'%(data)
        elif isinstance(data, unicode):
                if data.startswith("@@"):
                        return '%s'%(data[2:len(data)])
                if HasCn(data):
                        return 'T("%s")'%(data)
                return '"%s"'%(data)
        elif isinstance(data, int):
                return "%d"%data
        elif isinstance(data, float):
                return "%f"%data
        elif isinstance(data, list):
                return PythonList2Lpc( data, indentFlg, indentCnt)
        elif isinstance(data, tuple):
                return PythonList2Lpc( data, indentFlg, indentCnt)
        elif isinstance(data, dict):
                return PythonDict2Lpc( data, indentFlg, indentCnt)

# 将python dict 转换为lua dict
def PythonDict2Lua( data, indentFlg=False, indentCnt=0):
        if indentCnt > max_indent_cnt:
                indentFlg = False

        result = '{'
        if indentFlg :
                result = result + "\n"
        # 遍历 数据
        keys = data.keys()
        keys.sort()

        for key in keys:
                value = data[key]
                result = result + getIndent(indentFlg, indentCnt+1)

                strKey = (PythonData2Lua(key,indentFlg, indentCnt+1))
                strValue = (PythonData2Lua(value,indentFlg, indentCnt+1))
                result = result  + ("[%s] = %s, "%(strKey, strValue))
                if indentFlg:
                        result = result + "\n"
        result = result + getIndent(indentFlg, indentCnt) + '}'
        return result

# 将python list 转换为lua list
def PythonList2Lua(data, indentFlg=False, indentCnt=0):
        if indentCnt > max_indent_cnt:
                indentFlg = False

        result = '{' 
        #if indentFlg:
        #        result = result + "\n"
        # 遍历 数据
        index = 0
        while index < len(data):
                value = data[index]
                strValue = PythonData2Lua(value,indentFlg, indentCnt+1)
                result = result  + ("%s, "%(strValue))
                index += 1
                if indentFlg and index < len(data):
                        result = result + "\n"
        result = result + '}'
        return result


# 将python tuple 转换为lua tuple
def PythonTuple2Lua( data, indentFlg=False, indentCnt=0):
        return PythonList2Lua(data, indentFlg, indentCnt)

def HasCn(s):
        if not len(s):
                return False
        i = 0
        while i < len(s):
                if ord(s[i]) >= 0xa1:
                        return True
                i += 1
        return False
        

# 将python数据转换为lua数据
def PythonData2Lua( data, indentFlg=False, indentCnt=0):
        if isinstance(data, str):
                if data.startswith("@@"):
                        return "%s"%(data[2:len(data)])
                if HasCn(data):
                        #return "TEXT('%s')"%(data)
                        return "'%s'"%(data)
                return "'%s'"%(data)
        elif isinstance(data, unicode):
                if data.startswith("@@"):
                        return "%s"%(data[2:len(data)])
                if HasCn(data):
                        #return "TEXT('%s')"%(data)
                        return "'%s'"%(data)
                return "'%s'"%(data)
        elif isinstance(data, int):
                return "%d"%data
        elif isinstance(data, float):
                return "%f"%data
        elif isinstance(data, list):
                return PythonList2Lua( data, indentFlg, indentCnt)
        elif isinstance(data, tuple):
                return PythonList2Lua( data, indentFlg, indentCnt)
        elif isinstance(data, dict):
                return PythonDict2Lua( data, indentFlg, indentCnt)

def WriteUpdateFile(WorkDir, UpdateFile):
        filename = WorkDir + "/tmp/update_file.txt"
        try :
                f = file(filename, "a+b")
        except :
                sys.exit(-1)
        f.write(UpdateFile)
        f.close()

def write_file(filename, content ):
        msg = "writting to file " + filename
        try :
                f = file(filename, "w+b")
        except :
                msg = "can not write to " + filename + "\n"
                sys.exit(-1)
        f.write(content)
        f.close()


#if __name__ == "__main__":
#test
