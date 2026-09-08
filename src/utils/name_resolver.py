from src.enums import NameType, VarType

def check_name_type(name, program, current_function = None):
    if isinstance(name, int):
        return NameType.INT_NUM
    
    for function in program.functions:
        if function.name == name:
            return NameType.FUNCTION

    if current_function is not None:
        for var in current_function.local_variables:
            if var == name:
                return NameType.INT_VARIABLE
        for parameter in current_function.parameters:
            if parameter == name:
                return NameType.PARAMETER
        for i in range(0, current_function.parameter_count):
            if name == f"parameter_{i}":
                return NameType.PARAMETER
            
    for var in (program.uninitialized_global_variables + program.initialized_global_variables):
        if var.name == name:
            if var.type == VarType.INTEGER:
                return NameType.INT_VARIABLE
            if var.type == VarType.STRING:
                return NameType.STRING_VARIABLE

    if name == "return_value":
        return NameType.RETURN_VALUE

    return NameType.NOT_FOUND
