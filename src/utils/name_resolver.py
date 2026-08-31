from src.enums.name_type import NameType

def check_name_type(name, parsed_program, current_function = None):
    if isinstance(name, int):
        return NameType.INT_NUM
    
    for function in parsed_program["functions"]:
        if function.name == name:
            return NameType.FUNCTION

    if current_function != None:
        for var in current_function.local_variables:
            if var == name:
                return NameType.INT_VARIABLE

        for parameter in current_function.parameters:
            if parameter == name:
                return NameType.PARAMETER
            
    for var in (parsed_program["uninitialized_global_variables"] + parsed_program["initialized_global_variables"]):
        if var["name"] == name:
            if var["type"] == "int":
                return NameType.INT_VARIABLE
            if var["type"] == "string":
                return NameType.STRING_VARIABLE

    for i in range(0, 6):
        if name == f"parameter_{i}":
            return NameType.PARAMETER

    if name == "return_value":
        return NameType.RETURN_VALUE

    return NameType.NOT_FOUND