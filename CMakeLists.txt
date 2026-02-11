# Setting environment rules
cmake_minimum_required (VERSION 3.20)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project ("UkiUki")

# Set the standard to C++20
# Set the standard globally to C++20 for all sub-folders/targets
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON) # Forces it to error if C++20 isn't available
set(CMAKE_CXX_EXTENSIONS OFF)  # Stick to clean, standard C++ (no compiler-specific stuff)     

# Find Drogon (vcpkg makes this work)
find_package(Drogon CONFIG REQUIRED)

# 4. BUILDING: Define the executable and its source files
# Note: If PingController.cpp is inside a folder named "Controllers", 
# the path must reflect that relative to this CMakeLists.txt file.
add_executable(UkiUki 
    "main.cpp"   
    "Controllers/PingController.h"
    "Controllers/PingController.cpp"
)

# 5. LINKING: Stitch the code and the framework together
target_link_libraries(UkiUki PRIVATE Drogon::Drogon)