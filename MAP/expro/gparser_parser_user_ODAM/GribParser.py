#! /usr/bin/env python
#-*- coding: utf-8 -*-
# 파이썬 버전 : 2.7.10
# 외부 라이브러리 : 사용안함 
# 외부 프로그램 : wgrib 
# 프로그램 버전 : v0.5
# 한글을 사랑합시다...

# 종료코드 목록
# 0 : 정상종료
# 1 : 프로그램 옵션이 부족하거나 잘못 입력됨
# 2 : 입력 파일 문제
# 3 : 외부 프로그램 문제

import os
import sys
import subprocess
import ConfigParser
from optparse import OptionParser

PROG_DIR = os.path.dirname(os.path.realpath(__file__))

class GribParserFormat:
	# 파일 포맷을 저장하는 클래스.
	# 여기서 파일의 포맷, 파일명 포맷, 결과파일의 출력 경로를 저장한다.
	def __init__(self, FileFormat, FileNameFormat):
		
		self.FileFormat = FileFormat
		self.FileNameFormat = FileNameFormat
	# 클래스의 끝
	
class GribParserSetter:
	# 설정파일을 읽어 설정을 저장하는 클래스
	# 기본 세팅과 파일별 포맷을 저장한다.
	def __init__(self):
		GribParserConfig = ConfigParser.ConfigParser()
		GribParserConfig.read(os.path.join(PROG_DIR, 'GribParser.ini'))
		
		self.FormatList = GribParserConfig.get('SETTING', 'FormatList').split(',')
		self.GribParserFormat = {}
		
		for Format in self.FormatList:
			StrName = GribParserConfig.get(Format, 'StrName')
			FormatTable = GribParserFormat(Format, StrName)
			
			self.GribParserFormat[Format] = FormatTable
	# 클래스의 끝
	
def ExistChecker(FileName):
	# 파일을 검색하여 파일이 존재하는지 확인한다.
	return os.path.exists(FileName)
	
def ParseODAM(Input, Output):
	# ODAM 형태의 파일은 이 함수를 통해서 1차 텍스트로 변환한다.
	# 추가적인 옵션은 추후에 추가
	ParseStr = "wgrib {0} -d all -text -o {1}".format(Input, Output)
	result = subprocess.check_call(ParseStr, shell=True)
	
	if result == 0:
		return True
	else:
		return False
	# 간단하게 파일을 푼다. 리턴값을 확인하여 0이 아니면 문제가 발생한 것
	
def ParseSHRT(Input, Output, PredictHour):
	# SHRT 형태의 파일은 이 함수를 통해서 1차 텍스트로 변환한다.
	# 추가적인 옵션은 추후에 추가
	ParseStr = "wgrib {0} | grep :{1}hr | wgrib -i {0} -text -o {2}".format(Input, PredictHour, Output)
	result = subprocess.check_call(ParseStr, shell=True)
	
	if result == 0:
		return True
	else:
		return False
	# 간단하게 파일을 푼다. 리턴값을 확인하여 0이 아니면 문제가 발생한 것
		
def ParseVSRT(Input, Output, PredictHour):
	# VSRT 형태의 파일은 이 함수를 통해서 1차 텍스트로 변환한다.
	# 추가적인 옵션은 추후에 추가
	if PredictHour == "0":
		ParseStr = "wgrib {0} | grep 1:0:d | wgrib -i {0} -text -o {1}".format(Input, Output)
	if PredictHour == "1":
		ParseStr = "wgrib {0} | grep 2:189 | wgrib -i {0} -text -o {1}".format(Input, Output)
	if PredictHour == "2":
		ParseStr = "wgrib {0} | grep 3:378 | wgrib -i {0} -text -o {1}".format(Input, Output)
	if PredictHour == "3":
		ParseStr = "wgrib {0} | grep 4:568 | wgrib -i {0} -text -o {1}".format(Input, Output)
	result = subprocess.check_call(ParseStr, shell=True)
	
	if result == 0:
		return True
	else:
		return False
	# 간단하게 파일을 푼다. 리턴값을 확인하여 0이 아니면 문제가 발생한 것
	
def ParseLDAPS(Input, Output, Var):
	# LDAPS 형태의 파일은 이 함수를 통해서 1차 텍스트로 변환한다.
	ParseStr = "kwgrib2 {0} | grep :{1} | kwgrib -i {0} -text {2}".format(Input, Var, Output)
	result = subprocess.check_call(ParseStr, shell=True)
	
	if result == 0:
		return True
	else:
		return False
		
def ParseLDAPSLevel(Input, Output, Var, Level):
	# LDAPS 형태의 파일은 이 함수를 통해서 1차 텍스트로 변환한다.
	ParseStr = "kwgrib2 {0} | grep :{1} | sed -n '{2}p' | kwgrib -i {0} -text {3}".format(Input, Var, Level, Output)
	result = subprocess.check_call(ParseStr, shell=True)
	
	if result == 0:
		return True
	else:
		return False
		
# 메인 프로그램 	
if __name__ == "__main__":
	# 옵션을 받고 처음 처리하는 부분
	# 따로 분리할걸 그랬나.... 생각보다는 길다. 
	GribParserConf = GribParserSetter()
	
	print "GribParser.py - Grib File Parsing Program"
	
	usage = """
	%prog -i [FileName] -f [FileFormat] -o [OutputFile]
	%prog --input=[FileName] --format=[FileFormat] --output=[OutputFile]
	ex) %prog -i DFS_ODAM_GRB1_T1H.201509100000 -f ODAM -o /home/ODAM/output
	ex) %prog --input=DFS_ODAM_GRB1_T1H.201509100000 --format=ODAM --output=/home/ODAM/output
	ex) %prog -i DFS_SHRT_GRB1_T3H.201509100200 -f SHRT -o /home/SHRT/output -h 4
	ex) %prog --input=DFS_SHRT_GRB1_T3H.201509100200 --format=SHRT --output=/home/SHRT/output --hour=4
	Format List : {0}
	""".format(', '.join(GribParserConf.FormatList))
	
	Options = OptionParser(usage = usage)
	
	Options.add_option("-i", "--input", dest="FileName", metavar="FILENAME", help="Input FileName", default="")
	Options.add_option("-f", "--format", dest="FileFormat", metavar="FILEFORMAT", help="Processing Format", default="")
	Options.add_option("-o", "--output", dest="OutputFile", metavar="OUTPUTFILE", help="Output FileName", default="")
	Options.add_option("-v", "--Variable", dest="Var", metavar="VARIABLE", help="Variable", default="")
	Options.add_option("-p", "--predict", dest="PredictHour", metavar="PREDICTHOUR", help="Prediction Hour(VSRT, SHRT, LDAPS)", default="")
	Options.add_option("-l", "--level", dest="Level", metavar="LEVEL", help="Height Level(Pres, Depth, Height, etc.)", default="")
		
	Option, args = Options.parse_args()
	
	FileName = Option.FileName
	FileFormat = Option.FileFormat.upper()
	OutputFile = Option.OutputFile
	PredictHour = Option.PredictHour
	Variable = Option.Var
	Level = Option.Level
	LvFlag = False
	
	if FileName == "" or FileFormat == "" or OutputFile == "":
		print Options.usage
		Options.print_help()
		sys.exit(1)
		
	# 추가!!! SHRT나 LDAPS 등의 시간단위 예측 자료는 출력할 예측 시간이 필요하다.
	if (FileFormat == "SHRT" or FileFormat == "LDAPS" or FileFormat == "SHRT_OLD" or FileFormat == "VSRT" or FileFormat == "VSRT_OLD") and PredictHour == "":
		print "If Select SHRT or LDAPS Format, Set -p Option"
		Options.print_help()
		sys.exit(1)
		
	# 추가!! LDAPS나 RDPS은 자료를 처리할 Var값을 가져와야한다.
	if (FileFormat == "LDAPS_UNIS" or FileFormat == "LDAPS_PRES" or FileFormat == "RDPS") and Variable == "":
		print "If Select LDAPS Format, Set -v Option"
		Options.print_help()
		sys.exit(1)
		
	# 추가!! LDAPS에서 Level 변수가 지정될 경우 플래그를 넣는다.
	if (FileFormat == "LDAPS_UNIS" or FileFormat == "LDAPS_PRES" or FileFormat == "RDPS") and Level == "":
		LvFlag = False
	else:
		LvFlag = True
		
	# 옵션 처리 부분 끝 
	
	# 파일 검사, 파일의 존재여부를 확인한다.
	if ExistChecker(FileName):
		pass
	else:
		print "File is not Exist"
		print "FileName    : {0}".format(FileName)
		sys.exit(2)
	# 파일 검사 완료, 파일이 없으면 종료된다. (코드 2)
		
		
	# 포맷에 따른 파일 처리, 각자 wgrib을 사용하는 함수로 구현한다.
	if FileFormat == "ODAM" or FileFormat == "ODAM_OLD":
		if ParseODAM(FileName, OutputFile):
			pass
			
		else:
			print "Parsing Failed, Check Input File"
			print "FileName    : {0}".format(FileName)
			
			sys.exit(3)
			
	elif FileFormat == "SHRT" or FileFormat == "SHRT_OLD":
		if ParseSHRT(FileName, OutputFile, PredictHour):
			pass
			
		else:
			print "Parsing Failed, Check Input File"
			print "FileName    : {0}".format(FileName)
	
			sys.exit(3)
			
	elif FileFormat == "VSRT" or FileFormat == "VSRT_OLD":
		if ParseVSRT(FileName, OutputFile, PredictHour):
			pass
			
		else:
			print "Parsing Failed, Check Input File"
			print "FileName    : {0}".format(FileName)
	
			sys.exit(3)
						
	elif FileFormat == "LDAPS_UNIS" or FileFormat == "LDAPS_PRES" or FileFormat == "RDPS":
		if LvFlag:
			if ParseLDAPSLevel(FileName, OutputFile, Variable, Level):
				pass
				
			else:
				print "Parsing Failed, Check Input File"
				print "FileName    : {0}".format(FileName)
		else:
			if ParseLDAPS(FileName, OutputFile, Variable):
				pass
				
			else:
				print "Parsing Failed, Check Input File"
				print "FileName    : {0}".format(FileName)
		
	sys.exit(0)