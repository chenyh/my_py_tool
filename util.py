#-*- coding:utf-8 -*-

def encode(val, encoding=None):
        import locale
	res = ''
	if not encoding: 
        	encoding = locale.getdefaultlocale()[1]
	try : 
		res = val.encode(encoding)
        except :
		print "none", error
		res = val
        return res

def write_file(filename, content, encoding = None):
	msg = "writting to file " + filename
	try :
		f = file(filename, "w+b")
	except :
		msg = "can not write to " + filename + "\n"
		sys.exit(-1)
	content = encode(content, encoding)
	f.write(content)
	f.close()

