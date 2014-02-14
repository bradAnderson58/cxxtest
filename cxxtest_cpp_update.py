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
	print "1st Arg: The complete or relative path to the cxxtest\python directory in the cxxtest framework."
	print
	print "2nd Arg (optional): The directory of the unit test header files and that of your destination cpp file. \
	If this isn't defined it is assumed that the current working directory of the python execution is the directory \
	of the headers and cpp file that need to be parsed. If you keep the cxxtest_cpp.update.py in the same directory \
	as the header files you're about to parse then this argument isn't necessary"
	print
	print "3rd Arg (optional): The prefix to the test file name: <prefix>_TestResults.xml. If left unused default is \
	\"TestResults.xml\""

count = 1
test_path = ""
CXXTEST_DIR_NAME = "cxxtest"
PYTHON_DIR_NAME = "python"
THIRD_PARTY_LIBRARY_DIR_NAME = "third-party-libraries"
GENERIC_RESULTS_NAME = "TestResults.xml"
GENERIC_CPP_NAME = "runner.cpp"
CXXTESTGEN_FILENAME = "cxxtestgen"

# define the directory of test header files that are to be used to create the tests
test_path = os.getcwd()
if (len(sys.argv) > 2 and len(sys.argv[2]) > 0):
	test_path = sys.argv[2]

# define the name of the parent directory for the cxxtest framework
relative_path = ""
cxx_path = ""
if (len(sys.argv) > 1 and len(sys.argv[1]) > 0):
	relative_path = sys.argv[1]
else:
	print
	print "Script requires at least the input of the relative or complete path to the cxxtest\python directory"
	sys.exit(-1)

cxx_path = os.path.join(test_path, relative_path)
print cxx_path
print os.path.normpath(cxx_path)
if (not os.path.exists(cxx_path)):
	if (os.path.exists(relative_path)):
		cxx_path = relative_path
	else:
		print "The path " + os.path.normpath(cxx_path) + " does not exist"
		sys.exit(-1)

# define a name for the test results
xml_results_name = GENERIC_RESULTS_NAME
if (len(sys.argv) > 3 and len(sys.argv[3]) > 0):
	xml_results_name = sys.argv[3] + "_" + xml_results_name

# collect all the header files for cxxtestgen
header_files = []
for f in os.listdir(test_path):
    if f.endswith('.h') or f.endswith('.hpp'):
        header_files.append(os.path.join(test_path, f))

#define fullpath of cpp file
runner_file = os.path.join(test_path, GENERIC_CPP_NAME)

# prep arguments for command line
arguments = [os.path.join(cxx_path, 'cxxtestgen'), '--xunit-printer', '--xunit-file', xml_results_name, '-o', runner_file]
for header_file in header_files:
    arguments.append(' ')
    arguments.append(header_file)
	
print "cxxtestgen arguments"
print arguments

if sys.version_info >= (3, 0):
    sys.path.insert(0, os.path.dirname(cxx_path))
else:
    sys.path.insert(0, os.path.dirname(os.path.join(cxx_path, 'python3')))
sys.path.append(".")

import cxxtest

cxxtest.main(arguments)