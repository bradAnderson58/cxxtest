import sys
import os
from os.path import expanduser

# set TEST_PATH=$(ProjectDir)
# set FILES=%TEST_PATH%*.h
# set RUNNER=%TEST_PATH%runner.cpp
# set CXXPATH=%TEST_PATH%..\..\..\..\ThirdPartyLibraries\cxxtest\bin
# echo %CXXPATH%
# set XML_FULL_NAME=%TEST_PATH%$(ProjectName)_TestResults.xml
# set cxxCommand=%CXXPATH%\cxxtestgen --xunit-printer --xunit-file %XML_FULL_NAME% -o %RUNNER% 
# for %%f in (%FILES%) do set cxxCommand="%cxxCommand% %%f

def usageSummary(arg):
	print "The cxxtest_cpp_update.py script can run with 0, 1, 2 or 3 inputs"
	print
	print "1st Arg: The name of the parent directory(not the full path) of the cxxtest framework is necessary to\
	compile a new cpp file. It is assumed that the parent directory of the test framework is in one of the directories\
	above the test path. cxxtest_cpp_update.py will search upwards from the test directory until it finds the directory name\
	This is the directory of where you installed your cxxtest framework. If one is not defined the default will be \"third-party-libraries\""
	print
	print "2nd Arg: The directory of the unit test header files and that of your destination cpp file. If this isn't defined it is \
	assumed that the director of the python file is the directory of the headers and cpp file that need to be parsed"
	print
	print "3rd Arg: The prefix to the test file name: <prefix>_TestResults.xml. If left unused default is \"TestResults.xml\""

count = 1
test_path = ""
CXXTEST_DIR_NAME = "cxxtest"
PYTHON_DIR_NAME = "python"
THIRD_PARTY_LIBRARY_DIR_NAME = "third-party-libraries"
GENERIC_RESULTS_NAME = "TestResults.xml"
GENERIC_CPP_NAME = "runner.cpp"
CXXTESTGEN_FILENAME = "cxxtestgen"

# define the name of the parent directory for the cxxtest framework
cxx_parent_folder_name = THIRD_PARTY_LIBRARY_DIR_NAME
if (len(sys.argv) > 1 and len(sys.argv[1]) > 0):
	cxx_parent_folder_name = sys.argv[1]

# define the directory of test header files that are to be used to create the tests
test_path = os.getcwd()
if (len(sys.argv) > 2 and len(sys.argv[2]) > 0):
	test_path = sys.argv[2]

# define a name for the test results
xml_results_name = GENERIC_RESULTS_NAME #os.path.join(test_path,sys.argv[2] + "_TestResults.xml")
if (len(sys.argv) > 3 and len(sys.argv[3]) > 0):
	xml_results_name = sys.argv[3] + "_" + xml_results_name

# find the directory for the cxxtest suit files
base_directory = os.path.join(test_path, os.pardir)
cxx_path = os.path.join(base_directory, cxx_parent_folder_name)
while (os.path.exists(cxx_path) is False):
	if (base_directory is expanduser("~")):
		print "The folder " + cxx_parent_folder_name + " is not in any of the parent directories of your current cxx_setup.py execution directory."
		print os.getcwd()
		usageSummary()
		sys.exit(-1)
		
	#print os.path.normpath(base_directory)
	#print os.path.normpath(cxx_path)
	base_directory = os.path.join(base_directory, os.pardir)
	cxx_path = os.path.join(base_directory, cxx_parent_folder_name)

#cxx_path = os.path.normpath(os.path.join(cxx_path, CXXTEST_DIR_NAME, PYTHON_DIR_NAME, CXXTESTGEN_FILENAME))
cxx_path = os.path.normpath(os.path.join(cxx_path, CXXTEST_DIR_NAME, PYTHON_DIR_NAME))

# collect all the header files for cxxtestgen
test_path
header_files = []
for f in os.listdir(test_path):
    if f.endswith('.h'):
        header_files.append(os.path.join(test_path, f))

#define fullpath of cpp file
runner_file = os.path.join(test_path, GENERIC_CPP_NAME)

# prep arguments for command line
arguments = [os.path.join(cxx_path, 'cxxtestgen'), '--xunit-printer', '--xunit-file', xml_results_name, '-o', runner_file]
for header_file in header_files:
    arguments.append(' ')
    arguments.append(header_file)
	
print arguments

if sys.version_info >= (3, 0):
    sys.path.insert(0, os.path.dirname(cxx_path))
else:
    sys.path.insert(0, os.path.dirname(os.path.join(cxx_path, 'python3')))
sys.path.append(".")

import cxxtest

cxxtest.main(arguments)