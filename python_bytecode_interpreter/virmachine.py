import builtins
import dis

class VitrualMachine:
    def run_code(self, code):
        if (type(code) == type(' ')):
            code = compile(code,'<string>', 'exec')

        self.byte_code = list(code.co_code)
        #print(self.byte_code)
        self.consts = list(code.co_consts)
        self.names = list(code.co_names)
        self.stack = []
        self.vars = {}
        self.byte_code_counter = 0

        self.instructions = {
            '101': self.LOAD_NAME, 
            '100': self.LOAD_CONST,
            '131': self.CALL_FUNCTION,
            '1': self.POP_TOP, 
            '83': self.RETURN_VALUE,
            '90': self.STORE_NAME,
            '107': self.COMPARE_OP,
            '23': self.BINARY_ADD,
            '26': self.BINARY_FLOOR_DIVIDE,
            '11': self.UNARY_NEGATIVE,
            '10': self.UNARY_POSITIVE,
            '12': self.UNARY_NOT,
            '15': self.UNARY_INVERT,
            '24': self.BINARY_SUBTRACT,
            '20': self.BINARY_MULTIPLY,
            '19': self.BINARY_POWER,
            '27': self.BINARY_TRUE_DIVIDE,
            '22': self.BINARY_MODULO,
            '62': self.BINARY_LSHIFT,
            '63': self.BINARY_RSHIFT,
            '64': self.BINARY_AND,
            '65': self.BINARY_XOR,
            '66': self.BINARY_OR,
            '103': self.BUILD_LIST,
            '25': self.BINARY_SUBSCR,
            '102': self.BUILD_TUPLE,
            '104': self.BUILD_SET,
            '114': self.POP_JUMP_IF_FALSE,
            '115': self.POP_JUMP_IF_TRUE,
            '110': self.JUMP_FORWARD,
            '112': self.JUMP_IF_TRUE_OR_POP,
            '111': self.JUMP_IF_FALSE_OR_POP,
            '113': self.JUMP_ABSOLUTE,
            '116': self.LOAD_GLOBAL,
            '55': self.INPLACE_ADD,
            '56': self.INPLACE_SUBTRACT,
            '57': self.INPLACE_MULTIPLY,
            '59': self.INPLACE_MODULO,
            '67': self.INPLACE_POWER,
            '75': self.INPLACE_LSHIFT,
            '76': self.INPLACE_RSHIFT,
            '77': self.INPLACE_AND,
            '78': self.INPLACE_XOR,
            '79': self.INPLACE_OR,
            '125': self.STORE_FAST
            #'120': self.SETUP_LOOP
        }

        self.exec_bcode(self.byte_code)
        
    def exec_bcode(self, bcode):
        for i in range(0, len(bcode), 2):
            try:
                ret = self.instructions[str(bcode[i])](bcode[i + 1])
                if ret == True: break
                self.byte_code_counter += 2
            except KeyError as e:
                raise ValueError('Undefined command: {}'.format(e.args[0]))
    
    def LOAD_NAME(self, arg):
        name = self.names[arg]
        if self.vars.get(name) is not None:
            name = self.vars[name]
        self.stack.append(name)

    def LOAD_CONST(self, arg):
        self.stack.append(self.consts[arg])

    def CALL_FUNCTION(self, arg):
        a = []
        for i in range(arg):
            a.append(self.stack.pop())
        name = self.stack[len(self.stack) - 1]
        ret = getattr(builtins, name)(*a)
        if ret is not None:
            iret = iter(ret)
            for i in iret:
                self.stack.append(i)
    
    def POP_TOP(self, arg):
        self.stack.pop()
    
    def RETURN_VALUE(self, arg): 
        pass

    def STORE_NAME(self, arg):
        self.vars[self.names[arg]] = self.stack.pop()

    def STORE_FAST(self, arg):
        self.vars[self.names[arg]] = self.stack.pop()
    
    def COMPARE_OP(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        op = dis.cmp_op[arg] 
        if op == '<':
            self.stack.append(a < b)
        elif op == '<=':
            self.stack.append(a <= b)
        elif op == '==':
            self.stack.append(a == b)
        elif op == '!=':
            self.stack.append(a != b)
        elif op == '>':
            self.stack.append(a > b)
        elif op == '>=': 
            self.stack.append(a >= b)

    def UNARY_NEGATIVE(self, arg):
        a = self.stack.pop()
        self.stack.append(-a)

    def UNARY_POSITIVE(self, arg):
        a = self.stack.pop()
        self.stack.append(+a)

    def UNARY_NOT(self, arg):
        a = self.stack.pop()
        self.stack.append(not a)

    def UNARY_INVERT(self, arg):
        a = self.stack.pop()
        self.stack.append(~a)

    def BINARY_ADD(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def BINARY_FLOOR_DIVIDE(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a // b)
    
    def BINARY_SUBTRACT(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def BINARY_MULTIPLY(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)
    
    def BINARY_POWER(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a ** b)

    def BINARY_TRUE_DIVIDE(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a / b)

    def BINARY_MODULO(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a % b)

    def BINARY_LSHIFT(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a << b)
    
    def BINARY_RSHIFT(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a >> b)

    def BINARY_AND(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a & b)
    
    def BINARY_OR(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a | b)
    
    def BINARY_XOR(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a ^ b)

    def BINARY_SUBSCR(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a[b])

    def INPLACE_ADD(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def INPLACE_FLOOR_DIVIDE(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a // b)
    
    def INPLACE_SUBTRACT(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def INPLACE_MULTIPLY(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)
    
    def INPLACE_POWER(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a ** b)

    def INPLACE_TRUE_DIVIDE(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a / b)

    def INPLACE_MODULO(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a % b)

    def INPLACE_LSHIFT(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a << b)
    
    def INPLACE_RSHIFT(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a >> b)

    def INPLACE_AND(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a & b)
    
    def INPLACE_OR(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a | b)
    
    def INPLACE_XOR(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a ^ b)

    def INPLACE_SUBSCR(self, arg):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a[b])
    
    def BUILD_LIST(self, arg):
        list = []
        for i in range(arg):
            list.insert(0, self.stack.pop())
        self.stack.append(list)

    def BUILD_TUPLE(self, arg):
        list = []
        for i in range(arg):
            list.insert(0, self.stack.pop())
        self.stack.append(tuple(list))

    def BUILD_SET(self, arg):
        list = []
        for i in range(arg):
            list.insert(0, self.stack.pop())
        self.stack.append(set(list))
    
    def POP_JUMP_IF_FALSE(self, arg):
        if self.stack.pop() == False:
            self.byte_code_counter = arg
            self.exec_bcode(self.byte_code[arg:])
            return True
            
    def POP_JUMP_IF_TRUE(self, arg):
        if self.stack.pop() == True:
            self.byte_code_counter = arg
            self.exec_bcode(self.byte_code[arg:])
            return True

    def JUMP_FORWARD(self, arg):
        self.byte_code_counter = self.byte_code_counter + 2 + arg
        self.exec_bcode(self.byte_code[self.byte_code_counter:])
        return True

    def JUMP_IF_TRUE_OR_POP(self, arg):
        tos = self.stack.pop()
        if tos == True:
            self.stack.append(tos)
            self.byte_code_counter = arg
            self.exec_bcode(self.byte_code[arg:])
            return True

    def JUMP_IF_FALSE_OR_POP(self, arg):
        tos = self.stack.pop()
        if tos == False:
            self.stack.append(tos)
            self.exec_bcode(self.byte_code[arg:])
            return True
    
    def JUMP_ABSOLUTE(self, arg):
        self.exec_bcode(self.byte_code[arg:])
        return True

    def LOAD_GLOBAL(self, arg):
        name = self.names[arg]
        if self.vars.get(name) is not None:
            name = self.vars[name]
        self.stack.append(name)

    def SETUP_LOOP(self, arg):
         pass
