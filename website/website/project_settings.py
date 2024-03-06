# <----- Project Settings ----->

# - InvokerPool -
MAX_INVOKERS_COUNT = 14

# - InvokerRequest -
DEFAULT_EXECUTION_TL = 10

# - Environment -
ENABLE_DOCKER = False

# - Compiler -
SUPPORTED_LANGUAGES = ['py', 'cpp']

# Language / Time(Seconds)
COMPILE_TL = {
    "cpp": 4,
    "py": 1,
}
# Language / [tags, "%1"], %1 = file
COMPILER_COMMANDS = {
    "py": None,
    "cpp": ["g++", "-o", "compiled.ecpp", "-std=c++17", "%1"]
}

# - Launcher -
# !!! EVERY FILE SHOULD HAVE `e` BEFORE the LANGUAGE TYPE.

# Language / [tags, "%1"], %1 = file
LAUNCHER_COMMANDS = {
    "epy": ["python3", "%1"],
    "ecpp": ["%1"]
}

LAUNCHER_RUN_TL = {
    "epy": 10,
    "ecpp": 4
}
# <----- End Project Settings ----->
