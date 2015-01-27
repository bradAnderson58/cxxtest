Overview
=================
CxxTest is a unit testing framework for C++ that is similar in
spirit to JUnit, CppUnit, and xUnit. CxxTest is easy to use because
it does not require precompiling a CxxTest testing library, it
employs no advanced features of C++ (e.g. RTTI) and it supports a
very flexible form of test discovery.

In particular, the design of CxxTest was tailored for C++ compilers 
on embedded systems, for which many of these features are not 
supported. However, CxxTest can also leverage standard C++ features 
when they are supported by a compiler (e.g. catch unhandled exceptions).

Additionally, CxxTest supports test discovery. Tests are deﬁned in C++ 
header ﬁles, which are parsed by CxxTest to automatically generate a 
test runner. Thus, CxxTest is somewhat easier to use than alternative 
C++ testing frameworks, since you do not need to register tests.

CxxTest is available under the GNU Lesser General Public Licence (LGPL).

A user guide is available in doc/guide.pdf.

Python is a requirement.

##Installation
CxxTest requires little to no installation. You must have python installed and in your command terminal's path. For Xcode development you need to add the following lines to your `~/.bash_profile`:
```bash
export CXXTEST_CPP_UPDATE="/<full path to repo>/cxxtest/cxxtest_cpp_update.py"
export CXXTEST_PYTHON_DIR="/<full path to repo>/cxxtest/python"
```

##General Project Setup Steps
Clone the cxxtest code from github to your development machine. Be 
thoughtful about what directory it will live in. You might end up with a
lot of projects that relying on the relative paths to your cxxtest repo not changing.

###XCode setup
After creating your C++ library project (our example project will be "LibraryUtils") in XCode add a target that is an `OSX`->`Application`->`Command Line Tool` target. It should be a C++ application. Give it some kind of unit testing name. Maybe "UnitTests" is too generic a name, but we'll use that for this sample. Take the `main.cpp` file and rename it `runner.cpp`

Click the project settings icon in the Table of Contents (TOC) and change the target dropdown to point to "UnitTests". Click the `Build Settings` tab. Under `Build Settings` edit the `Header Search Paths` to include the cxxtest repo. Below is how my relative include path looks:
```
$(SRCROOT)/../../../<some directory that is relative to your projects>/cxxtest
```

Click the `Build Phases` tab next to the `Build Settings` tab. For `Target Dependencies` select the library you'll be testing. In our case we're selecting the `LibraryUtils(LibraryUtils)` library. If it has become unselected make sure that `runner.cpp` is present in the `Compile Sources` list. Under the `Link Binary With Libraries` make sure your library is selected. In our example that is `libLibraryUtils.dylib`

There is a `+` sign near the top of the `Build Phases`. Use this to create a `New Run Script Phase`. Place your `Run Script` definition block right before the `Compile Sources` block. In your script block place the following code:
```bash
source ~/.bash_profile
python $CXXTEST_CPP_UPDATE -c $CXXTEST_PYTHON_DIR -t $PROJECT_DIR/$TARGET_NAME
```

###Visual Studio Setup
To create a new unit test open Visual Studio and select File->New Project.
For ease of development it is nice to have your unit tests in the same solution
as your development project, so you can compile your changes and quickly run 
your unit tests with the ability to step into your code from the unit test.

In the "New Project" dialog there is a table of contents (TOC) on the left.
Select "Templates"->"Visual C++"->"General" and you will see the option in 
the window to select the "Empty Project" template. Name it something 
spiffy like "UnitTests".

In your "UnitTests" project create a cpp file named "runner.cpp". You can 
leave this blank as it will be populated by the cxxtestgen scripts during the 
pre-build steps. By creating the cpp file you will now be allowed to access 
C++ configuration properties that might otherwise be unavailable(weird that 
you create a c++ project and then have to create a cpp file to access 
settings, but whatever).

Right-click on the "UnitTests" in the "Solution Explorer" and from the 
drop-down select "Properties". In the "Properties" TOC on the left expand 
"Configuration Properties"->"General" and make sure that the "Target Extension"
field is ".exe" and that the "Configuration Type" field is set to 
"Application (.exe)"

Still in the "Properties" TOC on the left expand "Configuration Properties"->"C/C++" 
and then select "General". In the properties window on the right select the 
"Additional Include Directories". Edit the include directories so that you've 
included your top level "cxxtest" directory, your project's include directories 
and any additional include directories.

In the "Properties" TOC select "Configuration Properties"->"C/C++" and 
select "Preprocessor" to define any preprocessor variables necessary for your 
project.

In the "Properties" TOC select "Configuration Properties"->"Linker" and 
select "General". In the properties window on the right select the "Additional 
Library Directories" and point to the current build location for your project 
that you'll be unit testing. If there are any additional libraries required
for functionality of your library then include those as well.

In the "Properties" TOC select "Configuration Properties"->"Linker" and 
select "Input". In the properties window on the right select the "Additional 
Dependencies" and your libraries to test and any additional libraries.

In the "Properties" TOC select "Configuration Properties"->"Build Events" 
and select "Pre-Build Event". As a Pre-Build command you are providing
a Python call that is necessary in parsing your header files and updating
your "runner.cpp" file. This requires knowing the path relative path to your
cxxtest_cpp.update.py file (comes with github cloning) and the relative path
to the /cxxtest/python directory. Your relative path is with respect to the 
vxproj project file of the unit tests(not the sln solution file). In 
the "Command Line" field your call is going to look like the following:
"call <path to cxxtest_cpp_update.py> -c <path to python directory in cxxtest clone> -t <path to your unit test project's source directory>
In order to be epic and a master of relative paths and visual studio macros
your command line might be organized something like the following:
"call $(ProjectDir)<relative path from VS project to cxxtest_cpp_update.py> -c $(ProjectDir)<relative path to to python directory in cxxtest clone> -t $(ProjectDir)"

for example my cxxtest_cpp_update.py file is in:
C:\third-party-libraries\cxxtest
my \cxxtest\python directory is in:
C:\third-party-libraries\cxxtest\python
my vxproj file (the $(ProjectDir)) is in:
C:\myCompanyName\acronym\SoftwareProject\Library\UnitTests
and my project header files are in:
C:\myCompanyName\acronym\SoftwareProject\Library\UnitTests
and my current directory "Command Line" is:
call $(ProjectDir)..\..\..\..\..\third-party-libraries\cxxtest\cxxtest_cpp_update.py -c $(ProjectDir)..\..\..\..\..\third-party-libraries\cxxtest\python -t $(ProjectDir)

Sometimes in visual studio when you create a project there is an option to
have the source code one directory below the vxproj project file. In this 
case your headers are in $(ProjectDir)$(ProjectName)

If you have problems, check that python is installed on your machine and
that the path to the python exe is in your environment variables. Check that 
your relative paths are correct.

Pro Tips:
-Your xml file for test results is saved in the same directory as your unit 
test source code.
-If you want to look at the test results quickly in the command app that the
unit tests use then in your runner.cpp file put a break point in the main
method at the "return status;" line
-In order to easily fire off your unit tests with f5 you 
must make your new "UnitTests" project the default Startup project.
Right-click on "UnitTests" in the "Solution Explorer" and in the 
drop-down select "Set As Startup Project"


## A Simple Example

1. Create a test suite header file:

`MyTest.h:`
``` cpp
  #include <cxxtest/TestSuite.h>

  class MyTestSuite : public CxxTest::TestSuite 
  {
  public:
      void testAddition( void )
      {
          TS_ASSERT( 1 + 1 > 1 );
          TS_ASSERT_EQUALS( 1 + 1, 2 );
      }
  };
```

2. Generate the tests file (or use the above visual studio or xcode scripts described above to generate tests):
``` bash
cxxtestgen --error-printer -o tests.cpp MyTestSuite.h
```

3. Compile and run!
``` bash
g++ -o main tests.cpp
./main
Running 1 test(s).OK!
```
