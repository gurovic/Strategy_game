# <----- Project Settings ----->

# - InvokerPool -
MAX_INVOKERS_COUNT = 14

# - InvokerRequest -
DEFAULT_EXECUTION_TL = 10

# - Environment -
ENABLE_DOCKER = False

# - Compiler -
# Language / Time(Seconds)
COMPILE_TL = {
    "cpp": 4,
    "py": 1,
}
# Language / [tags, "%1"], %1 = file
COMPILER_COMMANDS = {
    "py" : None,
    "cpp" : ["g++", "-std=c++17", "%1"]
}

# <----- End Project Settings ----->