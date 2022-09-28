import argparse

parser = argparse.ArgumentParser(description='Command Line Arguments For demo.py')
parser.add_argument('--file', help='used for storing output_fp in a temp folder', required=True)
argument = parser.parse_args()
fileoutput = argument.file

print("printing file information: ")
f = open(fileoutput, "r")
print(f.read()) 