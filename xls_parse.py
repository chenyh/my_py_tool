# -*- coding: utf-8 -*-

import xlrd

class easy_excel:
	def __init__(self, filename=None):
		if filename:
			self.xlsdata = xlrd.open_workbook(filename, formatting_info=True)
			self.filename = filename
		else:
			self.filename = ''

	def get_sheet(self, sheet):
		for sheetid in xrange(self.xlsdata.nsheets):
			sh = self.xlsdata.sheet_by_index(sheetid)
			if sh.name == sheet:
				return sh

	def get_cell(self, sheet, row, col): 
		sh = get_sheet()
		if row >= sh.nrows or col >= sh.ncols:
			return None
        	return sh.cell_value(row, col)
	

if __name__ == '__main__':
	xls = easy_excel("play_units.xls")
	sheet = xls.get_sheet("units")
	print sheet.nrows, sheet.ncols

