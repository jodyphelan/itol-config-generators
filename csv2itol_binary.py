#! /usr/bin/env python
import sys
import csv
from collections import defaultdict, Counter
import palettable
import argparse


def list2colour_dict(l):
	pal = {
		1:["#000000"],
		2:["#1b9e77","#7570b3"],
		3:palettable.colorbrewer.qualitative.Dark2_3.hex_colors,
		4:palettable.colorbrewer.qualitative.Dark2_4.hex_colors,
		5:palettable.colorbrewer.qualitative.Dark2_5.hex_colors,
		6:palettable.colorbrewer.qualitative.Dark2_6.hex_colors,
		7:palettable.colorbrewer.qualitative.Dark2_7.hex_colors,
		8:palettable.colorbrewer.qualitative.Dark2_8.hex_colors,
		9:palettable.colorbrewer.qualitative.Paired_9.hex_colors,
		10:palettable.colorbrewer.qualitative.Paired_10.hex_colors,
		11:palettable.colorbrewer.qualitative.Paired_11.hex_colors,
		12:palettable.colorbrewer.qualitative.Paired_12.hex_colors
		}
	count = Counter(l)
	num_items = len(count)
	cols = pal.get(num_items,["black" for _ in range(num_items)])
	return {list(count)[i]:cols[i] for i in range(num_items)}


def main(args):
	columns = args.columns.split(",")
	meta = defaultdict(dict)
	samples = []
	for row in csv.DictReader(open(args.csv)):
		meta_columns = set(row.keys())-set(["id"])
		for x in meta_columns:
			meta[row[args.id]][x] = row[x] if row[x] != "" else "NA"
		samples.append(row[args.id])

	confcolours = defaultdict(dict)
	if args.conf:
		for row in csv.DictReader(open(args.conf)):
			confcolours[row["Type"]][row["Value"]] = row["Colour"]

	O = open("%s.binary.meta.itol.txt" % args.csv,"w")
	header = """DATASET_BINARY
SEPARATOR TAB
DATASET_LABEL\t%s
COLOR\t#ff0000

LEGEND_TITLE\t%s
""" % ("binary","binary")
	O.write(header)




	colour_dict = list2colour_dict(columns)
	O.write("FIELD_SHAPES\t%s\n" % "\t".join(["1" for _ in columns]))
	O.write("FIELD_LABELS\t%s\n" % "\t".join([x for x in columns]))
	O.write("FIELD_COLORS\t%s\n" % "\t".join([colour_dict[x] for x in columns]))
	O.write("\nDATA\n")
	for s in samples:
		#2,10,#ff0000,1,0.5
		O.write("%s\t%s\n" % (s,"\t".join([meta[s][c] for c in columns])))
	O.close()


parser = argparse.ArgumentParser(description='TBProfiler pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--csv',help='VCF file',required=True)
parser.add_argument('--conf',help='VCF file')
parser.add_argument('--columns',help='VCF file')
parser.add_argument('--id',default="id",help='VCF file')
parser.set_defaults(func=main)
args = parser.parse_args()
args.func(args)
