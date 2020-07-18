variables = {
}


def change_operator(old_operator, new_operator):
    if old_operator == new_operator:
        operator = "+"
    else:
        operator = "-"
    return operator


def resolve_variables(data):
    index = 0
    new_data = []
    while index < len(data):
        # If is a letter
        # test = "a+ ab + abbc+ a"
        if data[index].isalpha():
            start = index
            stop = index
            index += 1
            while index < len(data):
                if data[index].isalpha():
                    stop += 1
                    index += 1
                else:
                    break
            variable = data[start:stop+1]
            if variable in variables:
                new_data.append(str(variables[data[start:stop+1]]))
            else:
                raise ValueError
        # If index is overcharger
        if index >= len(data):
            break
        new_data.append(data[index])
        index += 1

    return "".join(new_data)


def resolve_multiples_operators(data):
    index = 0
    new_data = []
    while index < len(data):
        # If is a operator + or -
        # test = "a+ ab ++++ abbc+-++ a"
        if data[index] in "+-":
            operator = change_operator("+", data[index])
            index += 1
            while index < len(data):
                if data[index] in "+-":
                    operator = change_operator(operator, data[index])
                    index += 1
                else:
                    new_data.append(operator)
                    break
        # If index is overcharger
        if index >= len(data):
            break
        new_data.append(data[index])
        index += 1

    return "".join(new_data)


def infix_2_posfix(data):
    prec = {
        "^": 4,
        "*": 3,
        "/": 3,
        "+": 2,
        "-": 2,
        "(": 1,
    }
    data = data.replace("(", " ( ")
    data = data.replace(")", " ) ")
    data = data.replace("+", " + ")
    data = data.replace("-", " - ")
    data = data.replace("*", " * ")
    data = data.replace("/", " / ")
    data = data.replace("^", " ^ ")

    op_stack = []
    postfix_list = []
    token_list = data.split()
    for token in token_list:
        if token.isdigit():
            postfix_list.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while (len(op_stack) != 0) and \
                    (prec[op_stack[-1]] >= prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.append(token)

    while len(op_stack) != 0:
        postfix_list.append(op_stack.pop())
    return " ".join(postfix_list)


def resolve_postfix(data):
    operand_stack = []
    token_list = data.split()

    for token in token_list:
        if token.isdigit():
            operand_stack.append(int(token))
        else:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = resolve(token, operand1, operand2)
            operand_stack.append(result)
    return operand_stack.pop()


def resolve(op, op1, op2):
    if op == "^":
        return op1 ** op2
    elif op == "*":
        return op1 * op2
    elif op == "/":
        return op1 // op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


def check_parenthesis(data):
    stack = []
    for element in data:
        if element == '(':
            stack.append(element)
        elif element == ')':
            try:
                stack.pop()
            except IndexError:
                raise IndexError
    if len(stack) != 0:
        raise IndexError
    return


def check_order_elements(data):
    operators = ['+', '-', '*', '/', '^']
    insert_0 = []

    # after number nothing or an number or an operator
    # after ')' nothing or an ')' or operator
    # after operator a number or '('
    # after '(' a number or '('
    for index, element in enumerate(data):
        # after number nothing or an number or an operator or ')'
        if element.isdigit():
            if len(data) != index + 1:
                next_element = data[index + 1]
                if next_element.isdigit() or next_element in operators or next_element == ')':
                    continue
                else:
                    raise IndexError
            else:
                continue

        # after ')' nothing or an ')' or operator
        if element == ')':
            if len(data) != index + 1:
                next_element = data[index + 1]
                if next_element in operators or next_element == ')':
                    continue
                else:
                    raise IndexError
            else:
                continue

        # after operator a number or '('
        if element in operators:
            if len(data) != index + 1:
                next_element = data[index + 1]
                if next_element.isdigit() or next_element == '(':
                    continue
                else:
                    raise IndexError
            else:
                raise IndexError

        # after '(' a number or '('
        if element == '(':
            if len(data) != index + 1:
                next_element = data[index + 1]
                if next_element.isdigit() or next_element == '(':
                    continue
                elif next_element == "-":
                    insert_0.append(index)
                else:
                    raise IndexError
            else:
                raise IndexError
    while insert_0:
        index = insert_0.pop()
        data = data[:index + 1] + "0" + data[index + 1:]

    return data


def process(data):
    data = data.replace(" ", "")

    # Check if is a command
    if data.startswith("/"):
        list_commands = {
            "/help": "The program calculates the sum of numbers",
        }
        print(list_commands.get(data, "Unknown command"))
        return

    # Check empty string
    if data == "":
        return

    # Check if is a variable
    if data.isalpha():
        print(variables.get(data, "Unknown variable"))
        return

    # Check if is a assignment
    if "=" in data:
        try:
            a, b = data.split("=")
            a, b = a.strip(), b.strip()
        except ValueError:
            print("Invalid assignment")
            return
        if not a.isalpha():
            print("Invalid identifier")
            return
        if b.isalpha() and b not in variables:
            print("Unknown variable")
            return
        if b.isalpha():
            b = variables[b]
        try:
            b = int(b)
        except ValueError:
            print("Invalid assignment")
        variables[a] = b
        return

    if data.startswith("-"):
        data = "0" + data

    # Resolve all variables in the string
    try:
        data = resolve_variables(data)
    except ValueError:
        print("Unknown variable")
        return

    # Check if the number of '(' and ')' are correct
    try:
        check_parenthesis(data)
    except IndexError:
        print("Invalid expression")
        return

    # # Check if the string ends correctly (number or ')')
    # if not data[-1].isdigit() and data[-1] != ")":
    #     print("Invalid expression")

    # Resolve multiple-operators (+ or -)
    try:
        data = resolve_multiples_operators(data)
    except ValueError:
        print("Invalid expression")
        return

    # Check order elements in string
    # after number an number or ')' or '+' or '-' or '*' or '/' or '^' or nothing
    # after '+' or '-' or '*' or '/' or '^' a number or '('
    # after '(' a number or '('
    # after ')' an ')' or '+' or '-' or '*' or '/' or '^' or nothing
    try:
        data = check_order_elements(data)
    except IndexError:
        print("Invalid expression")
        return

    data = infix_2_posfix(data)

    print(resolve_postfix(data))
    return


data_in = input()
while data_in != "/exit":
    process(data_in)
    data_in = input()
print("Bye!")
