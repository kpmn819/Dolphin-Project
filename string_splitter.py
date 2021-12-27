# code to break up long strings
import textwrap
max_length = 24 # line can be this may char

def parse_string(long_string, final_length):
	lines_list = textwrap.wrap(long_string, final_length)
	#print(lines_list)
	return lines_list 

long_string = 'This is a test of the textwrap function to see how it does with a long string'
parsed_lines = parse_string(long_string)
print(parsed_lines[0])