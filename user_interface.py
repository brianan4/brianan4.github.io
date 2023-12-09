def print_list(list: list, header: str = "") -> None:
    if header != "":
        print(header)

    i = 1
    for item in list:
        print(f"{i}. {item}")
        i += 1

def print_dict(dict: dict, header: str = "") -> None:
    print(header)

    i = 1
    for (key, value) in dict.items():
        print(f"{i}. {key}: {value}")
        i += 1

def get_user_int(max) -> int:
    try:
        i = input("Input #: ")
        i = int(i)
    except ValueError:
        print(f"Input = {i}, Not an int")
        return None
    
    if i > max:
        print(f"Input = {i + 1}, Out of Index")
        return None
    
    return i