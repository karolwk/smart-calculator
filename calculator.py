import re
from collections import deque

class Calculator:

    def __init__(self):
        self.commands = {"/exit": "Bye!", "/help": "The program calculates the sum of numbers"}
        self.variable = {}

    def reduce_op(self, op):
        """Reduces multi-operators in single string to one"""
        if "++" in op:
            return self.reduce_op(op.replace("++", "+"))
        if "--" in op:
            return self.reduce_op(op.replace("--", "+"))
        if "+-" in op:
            return self.reduce_op(op.replace("+-", "-"))
        if "-+" in op:
            return self.reduce_op(op.replace("-+", "-"))

        return op.replace(" ", "")

    def infix_splitter(self, expression):
        """Splits expression to list for further postfix conversion"""
        # Spliting expresion using regex groups
        infix = re.split('(\+|\-|\*|\(|\)|\/|\^)', self.reduce_op(expression))
        # Filtering empty slots from list
        infix = list(filter(lambda x: False if x == "" else True, infix))
        # Converting string digits to int
        infix = list(map(self.convert_to_int, infix))
        # Dealing with unary minus
        i = 0
        while i < len(infix):
            if i == 0 and infix[i] == "-":
                infix[i + 1] = -infix[i + 1]
                infix.pop(0)
            if infix[i] == "(" and infix[i + 1] == "-":
                infix[i + 2] = -infix[i + 2]
                infix.pop(i + 1)
            i += 1
        return infix

    @staticmethod
    def convert_to_int(num):
        """Helping function to convert to int"""
        try:
            return int(num)
        except ValueError:
            return num

    def test_varible(self, text):
        """Testing declaration of the variable, and saving it to the variable dictionary"""
        v_name, v_value = text.replace(" ", "").split("=", 1)
        if not v_name.isalpha():
            raise TypeError()
        if v_value.isalpha() and v_value not in self.variable:
            raise NameError()
        if v_value in self.variable:
            v_value = self.variable[v_value]
            self.variable[v_name] = int(v_value)
            return
        if not v_value.isdigit():
            raise SyntaxError()
        self.variable[v_name] = int(v_value)

    def declare_varible(self, var):
        """Error handling for variables declaration"""
        try:
            self.test_varible(var)
        except TypeError:
            print("Invalid identifier")
        except NameError:
            print("Unknown variable")
        except SyntaxError:
            print("Invalid assignment")

    def postfix_converter(self, expression):
        """Converts infix notation to postfix"""
        result = []
        stack = deque()
        priority = {"-": 0, "+": 0, "*": 1, "/": 1, "^": 2, "(": 3, ")": 3}
        for ele in expression:
            if isinstance(ele, int) or ele.isalpha():
                result.append(ele)
                continue
            if ele == ")":
                while True:
                    # Add to result from stack until left parentheses found
                    temp = stack.pop()
                    if temp == "(":
                        break
                    result.append(temp)
                continue
            if not stack or (stack and stack[-1] == "("):
                stack.append(ele)
                continue
            if priority[ele] > priority[stack[-1]]:
                stack.append(ele)
                continue
            else:
                while stack and stack[-1] != "(":
                    result.append(stack.pop())
                stack.append(ele)
        while stack:
            result.append(stack.pop())
        return result

    def calculate_result(self, expression):
        """Calculating expression in postfix notation"""
        stack = deque()
        calc = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y,
                "/": lambda x, y: x / y, "^": lambda x, y: x ** y}
        for num in expression:
            if isinstance(num, int):
                stack.append(num)
            if isinstance(num, str) and num.isalpha():
                try:
                    stack.append(self.variable[num])
                except KeyError:
                    return "Unknown variable"
            if num in calc:
                try:
                    b, a = stack.pop(), stack.pop()
                except IndexError:
                    return "Invalid expression"
                stack.append(calc[num](a, b))
        return int(stack[0])

    def check_expression(self, expression) -> bool:
        """Checking for basic errors"""
        # Checks for multiple '*' and '\' operators
        check_sequence = re.findall("\\*[\\s]*\\*|/[\\s]*/", expression)
        if check_sequence or not self.check_parentheses(expression):
            print("Invalid expression")
            return False
        return True

    @staticmethod
    def check_parentheses(expr):
        """Helping function for checking correct parentheses"""
        stack = deque()
        for i in expr:
            if i == "(":
                stack.append(i)
            if i == ")":
                try:
                    stack.pop()
                except IndexError:
                    return False
        if stack:
            return False
        return True


    def check_command(self, command):
        if command not in self.commands:
            print("Unknown command")
            return False
        return True

    def main(self):
        while True:
            inp = input()
            if inp.startswith("/"):
                if self.check_command(inp):
                    if inp == '/exit':
                        print(self.commands[inp])
                        break
                    if inp == "/help":
                        print(self.commands[inp])
                        continue
                continue
            if inp != "":
                if self.check_expression(inp):
                    if inp.count("=") > 0:
                        self.declare_varible(inp)
                    else:
                        result = self.postfix_converter(self.infix_splitter(inp))
                        print(self.calculate_result(result))


if __name__ == "__main__":
    Calculator().main()
