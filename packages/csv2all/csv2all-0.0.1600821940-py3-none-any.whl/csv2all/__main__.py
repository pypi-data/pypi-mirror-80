#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='CSV to JSON (array) converter', prog="csv2all")
parser.add_argument('-f', '--format', dest='format', required=True, help="Output format (json or xml)")
parser.add_argument('-o', '--output', dest='output', required=True, help="Output file")
parser.add_argument('-i', '--input', dest='input', required=True,  help="Input CSV file")

args = parser.parse_args()

n = 0

if args.format != "json":
	print("Format not supported (yet?)")

if True:

	fp_in = open(file=args.input, mode="r")
	fp_out = open(file=args.output, mode="w", buffering=(10*1024*1024)) # 1MB write buffer

	headers = fp_in.readline().replace("\n", "").replace("\r", "").split(",")

	#print("Headers: "+str(headers))

	fp_out.write("[\n")

	next_line = None

	last_line = False


	while True:

		data_line = next_line

		next_line = fp_in.readline().replace("\n", "").replace("\r", "").split(",")


		if len(next_line) == 1: #Last line

			last_line = True


		if data_line == None: #First line

			data_line = next_line

			continue

		else:

			n += 1



		json_line = "{"

		for i in range(0,len(headers)):

			json_line += "\""+headers[i]+"\": \""+data_line[i]+"\""

			if i != (len(headers)-1):

				json_line += ","



		if not last_line:

			json_line += "},\n"

		else:

			json_line += "}\n"

		fp_out.write(json_line)

		if last_line:

			print("Processed: ",n,"lines")

			break

	fp_out.write("]")




'''
except Exception as e:

	print(e)

	print("Unable to open input or output file!")

finally:

	fp_in.close()
	fp_out.close()
'''

