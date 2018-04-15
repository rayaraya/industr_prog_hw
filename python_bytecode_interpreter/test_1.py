import virmachine as virm
import sys
from io import StringIO 


def get_stdout(str, func):
    res = StringIO()
    old, sys.stdout = sys.stdout, res
    func(str)
    sys.stdout = old
    return res.getvalue()
    
class TestClass(object):
    vm = virm.VitrualMachine()
    def test_print(self):
        vm_str = get_stdout('print(3)', self.vm.run_code)
        test_str = get_stdout('3', print)
        assert vm_str == test_str

    def test_add(self):
        assert get_stdout('a = 0\nb = 0 + a\nprint(b)', self.vm.run_code) == '0\n'
        assert get_stdout('a = 3\nb = 5 + a\nprint(b)', self.vm.run_code) == '8\n'
        
    def test_un_neg(self):
        assert get_stdout('a = 2\nb=-a\nprint(b)', self.vm.run_code) == '-2\n'
        assert get_stdout('a = 0.0\nb=-a\nprint(b)', self.vm.run_code) == '-0.0\n'

    def test_un_pos(self):
        assert get_stdout('a = -2\nb=+a\nprint(a)', self.vm.run_code) == '-2\n'
        assert get_stdout('a = 0.0\nb=+a\nprint(b)', self.vm.run_code) == '0.0\n'

    def test_un_not(self):
        assert get_stdout('a = not 2\nprint(a)', self.vm.run_code) == 'False\n'
        assert get_stdout('a = not 0.0\nprint(a)', self.vm.run_code) == 'True\n'
    
    def test_un_inv(self):
        assert get_stdout('a = ~0\nprint(a)', self.vm.run_code) == '-1\n'

    def test_lshift(self):
        assert get_stdout('a = 2 << 1\nprint(a)', self.vm.run_code) == '4\n'

    def test_rshift(self):
        assert get_stdout('a = 2 >> 1\nprint(a)', self.vm.run_code) == '1\n'

    def test_binand(self):
        assert get_stdout('a = 2 & 3\nprint(a)', self.vm.run_code) == '2\n'

    def test_binor(self):
        assert get_stdout('a = 2 | 3\nprint(a)', self.vm.run_code) == '3\n'

    def test_binxor(self):
        assert get_stdout('a = 2 ^ 3\nprint(a)', self.vm.run_code) == '1\n'

    def test_sub(self):
        assert get_stdout('a = 0\nb = 105\nprint(a - b)', self.vm.run_code) == '-105\n'
        assert get_stdout('a = 10\nb = 3\nc = a - b\nprint(c)', self.vm.run_code) == '7\n'

    def test_mul(self):
        assert get_stdout('a = 0\nb = -8\nprint(a * b)', self.vm.run_code) == '0\n'
        assert get_stdout('a = 4\nb = 5\nprint(a * b)', self.vm.run_code) == '20\n'
        assert get_stdout('a = 1\nb = 5\nprint(a * b)', self.vm.run_code) == '5\n'
    
    def test_power(self):
        assert get_stdout('a = 0\nb = 8\nprint(a ** b)', self.vm.run_code) == '0\n'
        assert get_stdout('a = 8\nb = 0\nprint(a ** b)', self.vm.run_code) == '1\n'
        assert get_stdout('a = 7\nb = 9\nprint(a ** b)', self.vm.run_code) == str(7 ** 9) + '\n'
        assert get_stdout('a = -2\nb = 2\nprint(a ** b)', self.vm.run_code) == '4\n'
        assert get_stdout('a = 0\nb = 0\nprint(a ** b)', self.vm.run_code) == '1\n'

    def test_div(self):
        assert get_stdout('a = 1\nb = 2\nprint(a / b)', self.vm.run_code) == '0.5\n'
        assert get_stdout('a = 0\nb = 5\nprint(a / b)', self.vm.run_code) == '0.0\n'
        assert get_stdout('a = -45\nb = 5\nprint(a / b)', self.vm.run_code) == '-9.0\n'

    def test_int_div(self):
        assert get_stdout('a = 1\nb = a // 2\nprint(b)', self.vm.run_code) == '0\n'

    def test_mod(self):
        assert get_stdout('a = 10\nb = a % 3\nprint(b)', self.vm.run_code) == '1\n'
        assert get_stdout('a = -1\nb = a % 5\nprint(b)', self.vm.run_code) == '4\n'

    def test_brackets(self):
        assert get_stdout('a = (7 + 3) * 2\nprint(a)', self.vm.run_code) == '20\n'
        assert get_stdout('a = 0 / (5 - 3)\nprint(a)', self.vm.run_code) == '0.0\n'
        assert get_stdout('b = 3\na = (-2) ** (b + 2)\nprint(a)', self.vm.run_code) == '-32\n'

    def test_var_num(self):
        assert get_stdout('a = 3\nb = -4\nprint(a + b)\n', self.vm.run_code) == '-1\n'
        assert get_stdout('a = 3\nb = -4.0\nprint(a + b)\n', self.vm.run_code) == '-1.0\n'

    def test_var_bool(self):
        assert get_stdout('a = True\nb = False\nprint(a == b)\n', self.vm.run_code) == 'False\n'
        assert get_stdout('a = True\nb = True\nprint(a == b)\n', self.vm.run_code) == 'True\n'

    def test_pop_jump(self):
        assert get_stdout('a = 3\nif 3 < 5: a = 4\nprint(a)', self.vm.run_code) == '4\n'
        assert get_stdout('a = 3\nif not 3 < 5: a = 4\nprint(a)\n', self.vm.run_code) == '3\n'

    def test_forw_jump(self):
        assert get_stdout('a = 3\nif 3 > 5: a = 4\nelse: a = 5\nprint(a)', self.vm.run_code) == '5\n'

    def test_cond(self):
        def f():
            if False:
                print(-1)
            else:
                print(1)
        assert get_stdout(f.__code__, self.vm.run_code) == '1\n'
        assert get_stdout('a = 3\nif 3 > 5: a = 4\nelif 2 < 3: a = 5\nelif 1 < 3: a = 6\nprint(a)', self.vm.run_code) == '5\n'

    #def test_while(self):
    #    def wf():
    #        i = 0
    #        while i < 2:
    #            i = i + 1
    #        print(i)
    #    assert get_stdout(wf.__code__, self.vm.run_code) == '2\n'

    def test_list(self):
        assert get_stdout('a = [2, 4, 5, 6]\nprint(a)\n', self.vm.run_code) == str([2,4,5,6]) + '\n'
        assert get_stdout('a = [2, 4, 5, 6]\nprint(a[1])\n', self.vm.run_code) == '4\n'

    def test_tuple(self):
        assert get_stdout('a = (2, 4, 5, 6)\nprint(a)\n', self.vm.run_code) == str((2,4,5,6)) + '\n'
        assert get_stdout('a = (2, 4, 5, 6)\nprint(a[1])\n', self.vm.run_code) == '4\n'

    def test_set(self):
        assert get_stdout('a = (2, 4, 5, 5)\nprint(a)\n', self.vm.run_code) == str((2,4,5,5)) + '\n'
        assert get_stdout('a = (2, 4, 5, 5)\nprint(a[1])\n', self.vm.run_code) == '4\n'
    
