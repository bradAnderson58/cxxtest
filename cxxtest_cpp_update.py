import sys
import os
import getopt
from os.path import expanduser

# set TEST_PATH=$(ProjectDir)
# set FILES=%TEST_PATH%*.h
# set RUNNER=%TEST_PATH%runner.cpp
# set CXXPATH=%TEST_PATH%..\..\..\..\ThirdPartyLibraries\cxxtest\bin
# echo %CXXPATH%
# set XML_FULL_NAME=%TEST_PATH%$(ProjectName)_TestResults.xml
# set cxxCommand=%CXXPATH%\cxxtestgen --xunit-printer --xunit-file %XML_FULL_NAME% -o %RUNNER% 
# for %%f in (%FILES%) do set cxxCommand="%cxxCommand% %%f

def usage():
    input_summmary =    "The cxxtest_cpp_update.py script can run with 0, 1, 2 or 3 inputs"
    cxx_path_usage =    "    -c,    --cxx_path=        The complete or relative path to the cxxtest\python directory in the cxxtest framework."
    test_path_usage =   "    -t,    --test_path=       The directory of the unit test header files and that of your destination cpp file. \
                        If this isn't defined it is assumed that the current working directory of the python execution is the directory \
                        of the headers and cpp file that need to be parsed. If you keep the cxxtest_cpp.update.py in the same directory \
                        as the header files you're about to parse then this argument isn't necessary"
    prefix_usage =      "    -p,    --prefix=          The prefix to the test file name: <prefix>_TestResults.xml. If left unused default is \
                        \"TestResults.xml\""

    print(input_summmary)
    print()
    print(cxx_path_usage)
    print(test_path_usage)
    print(prefix_usage)
    

shortargs='c:t:p:h'
longargs = ['cxx_path=','test_path=', 'prefix=', 'help']   

def get_input_args():
    
    # roar
    cxx_path = ''
    test_path = ''
    prefix = ''
    try:
        #parse it chihuahua breath
        opts, args = getopt.getopt(os.sys.argv[1:], shortargs, longargs)
        
        for o, a in opts:    
            if o in ('-c', '--cxx_path'):
                cxx_path = a
            elif o in ('-t', '--test_path'):
                test_path = a
            elif o in ('-p', '--prefix'):
                prefix = a
            elif o in ('-h', '--help'):
                usage()

    except getopt.GetoptError as err:
        print(err)
        usage()
        os.sys.exit()
        
    return cxx_path, test_path, prefix
    
    
def main():
    
    cxx_path, test_path, prefix = get_input_args()
    count = 1
    
    CXXTEST_DIR_NAME = "cxxtest"
    PYTHON_DIR_NAME = "python"
    THIRD_PARTY_LIBRARY_DIR_NAME = "third-party-libraries"
    GENERIC_RESULTS_NAME = "TestResults.xml"
    GENERIC_CPP_NAME = "runner.cpp"
    CXXTESTGEN_FILENAME = "cxxtestgen"

    # define the directory of test header files that are to be used to create the tests
    if len(test_path) == 0:
        test_path = os.getcwd()

    # define the name of the parent directory for the cxxtest framework
    relative_path = ""
    if len(cxx_path) == 0:
        usage()
        return
    
    if not os.path.exists(cxx_path):
        relative_path = os.path.join(test_path, cxx_path)
        if not os.path.exists(relative_path):
            usage()
            return;
        else:
            cxx_path = relative_path
        
    # define a name for the test results
    xml_results_name = GENERIC_RESULTS_NAME
    if len(prefix) > 0:
        xml_results_name = prefix + "_" + GENERIC_RESULTS_NAME
    
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
    
    if sys.version_info >= (3, 0):
        cxx_path = os.path.join(cxx_path, 'python3')
    
    sys.path.insert(1, cxx_path)
    sys.path.append(".")
    
    import cxxtest
    
    cxxtest.main(arguments)    
    
if __name__ == "__main__":
    main()