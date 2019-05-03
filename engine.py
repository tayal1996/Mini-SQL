import os
import sys
import sqlparse
import csv

def standard_print(result_table, distinct):
	if distinct == True:
		o = result_table
		result_table = []
		for row in o:
			if row not in result_table:
				result_table.append(row)

	for i in range(len(result_table)):
		output_line = ""
		for j in range(len(result_table[i])):
			if j != 0:
				output_line += ','
			output_line += result_table[i][j]
		print(output_line)

def join_two(table1, table2):
	if len(table1) == 0:
		return table2
	
	main_table = list()
	main_table.append(table1[0] + table2[0])
	for i in range(1,len(table1)):
		for j in range(1,len(table2)):
			main_table.append(table1[i]+table2[j])
	return main_table

def join_table(table_list, table_columns):
	main_table = list()
	for table_name in table_list:
		encoded_data = list(csv.reader(open(table_name + '.csv')))
		data = []
		for i in range(len(encoded_data)):
			data.append([])
			for j in range(len(encoded_data[i])):
				if encoded_data[i][j][0] == '“':
					data[i].append(encoded_data[i][j][1:-1])
				else:
					data[i].append(encoded_data[i][j])
		data.insert(0,table_columns[table_name])
		main_table = join_two(main_table,data)
	return main_table

def find_table_columns(table_list):
	metadata = open('metadata.txt', 'r').readlines()
	metadata = [x.strip() for x in metadata]
	table_columns = dict()

	for table in set(table_list):
		for i in range(len(metadata)):
			if table == metadata[i]:
				i += 1
				while metadata[i] != '<end_table>':
					table_columns.setdefault(table, []).append(table+'.'+metadata[i])
					i += 1
	return table_columns

def column_name_helper(dotted_list):
	without_dot = list()
	for column_name in dotted_list:
		without_dot.append(column_name.split('.')[1])
	return without_dot

def operation(a, b, operator):
	if operator == '=':
		return a == b
	elif operator == '<':
		return a < b
	elif operator == '>':
		return a > b
	elif operator == '<=':
		return a <= b
	elif operator == '>=':
		return a >= b
	else:
		raise NotImplementedError('operator ' + str(operator) + ' is invalid')

def find_column_index(column, column_list_in_table, without_dot):
	column_no = -1
	for i in range(len(column_list_in_table)):
		if column == column_list_in_table[i] or column == without_dot[i]:
			if column_no != -1:
				raise NameError('Ambiguous column name')
			else:
				column_no = i
	if column_no == -1:
		raise NameError('Column ' + column + ' does not exist')
	return column_no

def special_condition(main_table, op1, op2, operator):
	column_list_in_table = main_table[0]
	without_dot = column_name_helper(column_list_in_table)
	column_no1 = find_column_index(op1, column_list_in_table, without_dot)
	column_no2 = find_column_index(op2, column_list_in_table, without_dot)

	table = list()
	table.append(column_list_in_table)
	for row in main_table:
		if row != column_list_in_table:		#first row is header
			if operation(int(row[column_no1]),int(row[column_no2]),operator) == True:
				table.append(row)
	if operator == '=':
		to_delete = max(column_no2,column_no1)
		for row in main_table:
			del row[to_delete]
	return table


def apply_condition(main_table, op1, op2, operator):
	column_list_in_table = main_table[0]
	without_dot = column_name_helper(column_list_in_table)

	if (op1.isdigit() == True or op1[0] == '-') and (op2.isdigit() == True or op2[0] == '-'):
		if operation(int(op1),int(op2),operator) == True:
			return main_table
		else:
			return [main_table[0]]
	
	if op1.isdigit() == True or op1[0] == '-':
		value_first = True
		column,value = op2,int(op1)
	else:
		column,value = op1,int(op2)
		value_first = False
	
	column_no = find_column_index(column,column_list_in_table,without_dot)

	table = list()
	table.append(column_list_in_table)
	for row in main_table:
		if row != column_list_in_table:		#first row is header
			if (value_first == False and operation(int(row[column_no]),value,operator) == True) or \
			(value_first == True and operation(value,int(row[column_no]),operator) == True):
				table.append(row)
	return table

def intersection(table1, table2):
	table3 = list()
	for row in table1:
		if row in table2:
			table3.append(row)
	return table3

def union(table1, table2):
	table3 = table1
	for row in table2:
		if row not in table1:
			table3.append(row)
	return table3

def after_where(main_table, where_line):
	s = ""
	i = 0
	while i < len(where_line) and where_line[i] not in ['=','<','>']:
		s += where_line[i]
		i += 1
	op1 = s.strip()
	s = ""
	while i < len(where_line) and where_line[i].isalnum() == False and where_line[i] != '-':
		s += where_line[i]
		i += 1
	operator1 = s.strip()
	s = ""
	while i < len(where_line) and where_line[i:i+3].lower() != 'and' and  where_line[i:i+2].lower() != 'or' and where_line[i] != ';':
		s += where_line[i]
		i += 1
	op2 = s.strip()
	s = ""
	while i < len(where_line) and where_line[i] != ' ' and where_line[i] != ';':
		s += where_line[i]
		i += 1
	i+=1
	logic_op = s.strip()
	s = ""
	while i < len(where_line) and where_line[i] not in ['=','<','>']:
		s += where_line[i]
		i += 1
	op3 = s.strip()
	s = ""
	while i < len(where_line) and where_line[i].isalnum() == False and where_line[i] != '-':
		s += where_line[i]
		i += 1
	operator2 = s.strip()
	s = ""
	while i < len(where_line) and where_line[i] != ';':
		s += where_line[i]
		i += 1
	op4 = s.strip()

	if ((op1 != "" or op2 != "" or operator1 != "") and (op1 == "" or op2 == "" or operator1 == "")) or \
	((op3 != "" or op4 != "" or operator2 != "") and (op3 == "" or op4 == "" or operator2 == "")):
		raise Exception("Invalid syntax")

	if (op1.find('.') != -1 and op2.find('.') != -1) or (op1.isalpha() == True and op2.isalpha() == True):
		table1 = special_condition(main_table,op1,op2,operator1)
	else:
		table1 = apply_condition(main_table,op1,op2,operator1)

	# print(op1,op2,operator1,logic_op)
	if logic_op != "":
		table2 = apply_condition(main_table,op3,op4,operator2)
		if logic_op.lower() == "and":
			main_table = intersection(table1,table2)
		if logic_op.lower() == "or":
			main_table = union(table1,table2)
	else:
		main_table = table1
	return main_table

def filter(main_table, result_column_list):
	column_list_in_table = main_table[0]
	without_dot = column_name_helper(column_list_in_table)
	# without_dot like ['A', 'B', 'C', 'B', 'D', ...]
	# column_list_in_table like ['table1.A', 'table1.B', 'table1.C', 'table2.B', 'table2.D', ...]

	table = list()
	for i in range(len(main_table)):
		table.append([])
	for column in result_column_list:
		column_no = find_column_index(column,column_list_in_table,without_dot)
		for j in range(len(main_table)):
			table[j].append(main_table[j][column_no])
	return table

def aggregate_preprocessing(aggregate_line, column_list_in_table):
	s = ""
	i = 0
	while i < len(aggregate_line) and aggregate_line[i] != '(':
		s += aggregate_line[i]
		i += 1
	i += 1
	operator = s.strip()
	s = ""
	while i < len(aggregate_line) and aggregate_line[i] != ')':
		s += aggregate_line[i]
		i += 1
	column = s.strip()

	without_dot = column_name_helper(column_list_in_table)
	column_no = find_column_index(column,column_list_in_table,without_dot)
	return operator, column_no

def aggregate_operation(column, operator):
	if operator.lower() == 'max':
		return max(column)
	elif operator.lower() == 'min':
		return min(column)
	elif operator.lower() == 'sum':
		return sum(column)
	elif operator.lower() == 'avg' or operator.lower() == 'average':
		return sum(column)/len(column)
	else:
		raise NotImplementedError('operator ' + str(operator) + ' is invalid')


def main():
	agrv = ' '.join(sys.argv[1].split()) #replacing long spaces to one space
	parsed = sqlparse.parse(agrv) 
	query = parsed[0].tokens
	query = [x for x in query if str(x) != ' ']
	# for x in query:
	# 	print(x)

	if str(query[0]).lower() != 'select':
		raise NotImplementedError('Only select supported')

	where_line = ""
	column_list = ""
	table_list = ""
	for i in range(len(query)):
		if str(query[i]).lower() == 'from':
			if i+1 < len(query):
				table_list = [x.strip() for x in str(query[i+1]).split(',')]
			else:
				raise Exception("Invalid syntax")
			if i+2 < len(query):
				where_line = str(query[i+2])[6:]
			if str(query[i-1]).lower() != 'select':
				column_list = [x.strip() for x in str(query[i-1]).split(',')]
			break

	# table_list like ['table1', 'table2', ...]
	# column_list like ['col1', 'col2', ...]

	table_columns = find_table_columns(table_list)
	for table in table_list:
		if table not in table_columns.keys():
			raise NameError('Table ' + table + ' does not exist')

	# table_columns like {'table2': ['table2.B', 'table2.D'], 'table1': ['table1.A', 'table1.B', 'table1.C']}
	
	main_table = join_table(table_list,table_columns)

	# main_table like [['table1.A', 'table1.B', 'table1.C', 'table2.B', 'table2.D'], ['922', '158', '5727', '158', '11191'], ...]

	distinct = False
	if str(query[1]).lower() == 'distinct':
		distinct = True

	if where_line != "":
		main_table = after_where(main_table,where_line)

	if column_list == ['*']:
		standard_print(main_table,distinct)

	elif len(column_list) == 1 and column_list[0].find('(') != -1 and column_list[0].find(')') != -1:
		operator,column_no = aggregate_preprocessing(column_list[0],main_table[0])
		aggregate_column = list()
		for row in main_table:
			if row != main_table[0]:
				aggregate_column.append(int(row[column_no]))
		ans = aggregate_operation(aggregate_column,operator)
		print(ans)

	elif column_list != "":
		main_table = filter(main_table,column_list)
		standard_print(main_table,distinct)

	else:
		raise Exception("Invalid syntax")

if __name__ == '__main__':
	main()