#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function
import sys

"""
	The purpose is to map existing site variables with the corresponding variable in the SADaCC dictionary       
	In the new harmonized site dictionary, the order of the new dictionary should remain the same as in the old site data dictionary.
	The form names in the harmonized site dictionary should remain the same as the site form names
	If there is non corresponding variable name in the standard SADaCC dictionary, then use the site variable ensuring that SADaCC is informed about that!
	If the SADaCC variable name is not in the site variable name list, then make it HIDDEN in the harmonised dictionary [@HIDDEN]: last column (R) of SADaCC dictionary
	If the current site design is longitudinal, special consideration to change the design back to longitudinal design. In this case we will see how is it designed.
	Create a harmonized site data dictionary
	Adjust the SOP with regard to HIDDEN variable in the new SADaCC dictionary.
"""

if __name__=='__main__':
# python DataMigrationCodeFinal14April.py SCDRegistry_DATA_2018-11-02_1657.csv MappingFile1.tsv SADaCCVariables.tsv
	print(100*'*', "\n*", "This code performs the harminization of site variable names to the SADaCC variables".center(97)+'*\n'+100*'*', '\n*', " Before you run this code, we urge you to read in depth the data migration SOP".ljust(96), '*\n*', " To proceed, three files listed below are required:".ljust(96),'*\n*', "\t(1) Site SCDRegistry_DATA file in the csv format".ljust(91),'*\n*', "\t(2) Site to SADaCC variable mapping file in the tsv format,".ljust(91), '*\n*', "\t    complying to the Data Migration SOP".ljust(91), '*\n*', "\t(3) The SADaCC variable file in tsv format".ljust(91), '*\n*', " ".ljust(96), '*\n*', " If the code runs well, it should produce following three files:".ljust(96),  '*\n*', "\t(1) The Site SCDRegistry_DATA_Harmonized file in the csv format".ljust(91),'*\n*', "\t(2) The Site SCD_Harmonized_Dictionary file in the csv format, and".ljust(91),'*\n*', "\t(3) The SADaCC SCD_Dictionary_Mapped file in the tsv format in which variables not mapped".ljust(91),'*\n*', "\t    are annotated with @HIDDEN".ljust(91),  '*\n*', "\t(4) The Site-SADaCC variable mapping annotation file in tsv format, providing ".ljust(91),  '*\n*', "\t\tSite variables mapped or not, with harmonized variable name if mapped,".ljust(84),  '*\n*', "\t\tsame variable name if matched, or".ljust(84),  '*\n*', "\t\t'-' if not mapped or missing in the SADaCC dictionary".ljust(84), '*\n*', " ".ljust(96), '*\n*', " This code is run with three parameters as follows".ljust(96), '*\n*', "\tpython DataMigrationCodeFinal14April.py SCDRegistry_DATA.csv Site_to_SADaCC_variable_Mapping_File.tsv SADaCC_Variable.tsv".ljust(96), '\n*', " ".ljust(96), '*')
	if len(sys.argv) != 4:
		print("* Now, not enough argument to continue, 3 arguments required,".ljust(98), '*')
		print("* Insufficient number of arguments, please read instruction and SOP and try again".ljust(98), '*')
		print(100*'*')
		print("\nExiting ...\n")
		sys.exit(0)
	print(100*'*')
	
	if sys.version_info.major < 3: raw_pass = raw_input
	else: raw_pass = input
	
	a = raw_pass("\nPlease, enter\n\t0 to exit and \n\t1 to continue\n\nPlease enter your option below\n\n> ")
	while True:
		try:
			a = int(a)
			if a in [0,1]: break
			else:
				print("please type 0 to exit or 1 to continue")
				a = raw_pass("\nPlease, enter\n\t0 to exit and \n\t1 to continue\n\nPlease enter your option below\n\n> ")
		except:
			print("Please do not type any thing other than 0 to exit or 1 to continue")
			a = raw_pass("\nPlease, enter\n\t0 to exit and \n\t1 to continue\n\nPlease enter your option below\n\n> ")
	if int(a)==0: 
		print("\nExiting ...\n")
		sys.exit(1)
	print("\nNow running ...\n")
	 
	# Reading the mapping file
	fm = open(sys.argv[2].strip())
	header = fm.readline(); DictMap = {}; DictMapr = {}; DataType = {}; AllData = []
	header = [a.strip() for a in header.split('\t')]
	
	AllData.append(header[:6])
	
	# Building the mapping dictionary
	for line in fm:
		if not line.strip(): continue
		tline = [a.strip() for a in line.split('\t')]
		DictMap[tline[0]] = tline[6]; DictMapr[tline[6]] = tline[0]; AllData.append(tline[:6])
		if tline[3]=='radio': # This is were mapping options are needed
			try: 
				td = dict([tuple([a.strip() for a in s.split(':')]) for s in tline[12].split(',')])
				DataType[tline[0]] = [tline[3], td.copy()]
			except:
				print("Please make sure that you have read the data migration SOP and provide\nthe site and SADaCC 'yesno' and radio variable type mapping\n\nThe code execution should not continue until you have read the data migration SOP\nand provide the the site and SADaCC 'yesno' and radio variable type mapping \non column 'M' of the xls sheet before converting to an tsv format\n\nExiting the code execution ...\n")
				sys.exit(2)
		else: DataType[tline[0]] = [tline[3], tline[12].strip()]
	fm.close()
	
	# SADaCC variables mapped to site variables
	SADaCCMapped = set([DictMap[a] for a in DictMap if DictMap[a] != '#N/A'])
	
	# Reading the main registry file
	fp = open(sys.argv[1].strip())
	header = fp.readline()
	header = [a.strip() for a in header.split(',')]
	
	fw = open('Site-SADaCC_Mapping_Annotation.tsv', 'w')
	fw.write("Site Variable\tSADaCC variable\tStatus\n")
	for a in header:
		if a in DictMap and DictMap[a]!='#N/A': 
			fw.write('\t'.join([a, DictMap[a], 'Match'] if a==DictMap[a] else [a, DictMap[a], 'Mapped'])+'\n')
		else: fw.write('\t'.join([a, '-', 'Not Mapped'])+'\n')
	fw.close()
	
	mheader = [(header.index(a), DictMap[a]) if a in DictMap and DictMap[a] != '#N/A' else (header.index(a), a) for a in DictMap] # Take the one in SADaCC if mapped otherwise maintain that of the site
	mheader = sorted(mheader) # Sorted by index to go from small index to bigger!
	
	# Output file with the suffix '_Harmonized.tsv'
	fw = open(sys.argv[1].split('.')[0].strip()+'_Harmonized.csv', 'w')
	fw.write(','.join([a[1] for a in mheader])+'\n')
	
	# Migrate now to the new data elements for exportation to REDCap
	i = 1
	for line in fp:
		if not line.strip(): continue
		tline = [a.strip() for a in line.split(',')]
		tstr = ''
		i += 1
		for a in mheader:
			if isinstance(DataType[header[a[0]]][1],dict) and tline[a[0]]:
				try:
					tstr += DataType[header[a[0]]][1][tline[a[0]]]+'\t'
				except:
					print("Please make sure that you have read the data migration SOP and provide\nthe site and SADaCC 'yesno' and radio variable type mapping\n\nThe code execution should not continue until you have read the data migration SOP\nand provide the the site and SADaCC 'yesno' and radio variable type mapping \non column 'M' of the xls sheet before converting to an tsv format\nThere may be inconsistency for [%s], please check it ...\nOr check the record [%d] in your site data file\n\nExiting the code execution ...\n"%(a[1], i))
					sys.exit(2)
			else: tstr += tline[a[0]]+'\t'
		fw.write(','.join([s for s in tstr.strip().split('\t')])+'\n')
	fw.close()
		
	# Now dealing with site variable dictionary
	fp = open(sys.argv[3])
		
	# Creating map SADaCC to site by putting @HIDDEN to the last Field Annotation if there is no map to sites
	fw = open(sys.argv[3].split('.')[0].strip()+'_MappedToSite.csv', 'w')
	header = fp.readline()
	fw.write(header)
	columnS = len(header.strip().split('\t')); AllDataSADaCC = {}
	#print SADaCCMapped
	for line in fp:
		if not line.strip(): continue
		tline = line.split('\t')[:columnS]
		if not tline[0] in SADaCCMapped: tline[-1] = '@HIDDEN'
		fw.write('\t'.join(tline)+'\n')
		AllDataSADaCC[tline[0].strip()] = [s.strip() for s in tline[1:]]
	fw.close()
	
	fw = open('Site_HarmonizedDictionary.tsv', 'w')
	fw.write(header)
	for data in AllData[1:]:
		if data[0] in DictMap and DictMap[data[0]] != '#N/A':
			fw.write('\t'.join([DictMap[data[0]]]+AllDataSADaCC[DictMap[data[0]]])+'\n')
		else: fw.write('\t'.join(data)+'\n')
	fw.close()
	outputs = ['Site-SADaCC_Mapping_Annotation.tsv', sys.argv[1].split('.')[0].strip()+'_Harmonized.csv', sys.argv[3].split('.')[0].strip()+'_MappedToSite.csv', 'Site_HarmonizedDictionary.tsv']
	n = max([len(a) for a in outputs])
	print("\nThe process has now been fully completed and following four files has been produced:\n")
	print("   - %s"%(outputs[1],)+((n-len(outputs[1]))*' ')+": The harmonized new data sets")
	print("   - Site-SADaCC_Mapping_Annotation.tsv"+((n-len(outputs[0]))*' ')+": Mapped variables annotation file")
	print("   - Site_HarmonizedDictionary.tsv"+((n-len(outputs[-1]))*' ')+": New site harmonized dictionary")
	print("   - %s"%(outputs[2],)+((n-len(outputs[2]))*' ')+": The SADaCC variables mapped to the site with\n%s @HIDDEN indicating that the variable was not \n %sfound in the site dictionary"%((n+6)*' ',(n+6)*' '))
	print(100*'*')
