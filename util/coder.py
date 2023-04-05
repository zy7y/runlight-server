import ast

from util.loguru import LOG


class PyCodeRunner:
    def __init__(self):
        self._global_vars = {}

    def execute(self, code_str, local_vars=None):
        """
        执行 Python 代码串，并返回执行结果和生成的变量等信息。
        """
        try:
            ast.parse(code_str, "<string>", "exec")
        except SyntaxError as err:
            raise SyntaxError(f"语法错误：{err.msg}，在第 {err.lineno} 行") from err

        # 编译代码，并创建本地和全局命名空间
        if local_vars is None:
            local_vars = {}
        global_vars = self.get_global_vars()
        exec(
            compile(code_str, filename="<string>", mode="exec"), global_vars, local_vars
        )
        # 更新全局变量
        self.set_global_vars(global_vars)
        LOG.info(f"local vars {local_vars}| global vars {global_vars}")

        return local_vars

    def get_global_vars(self):
        return self._global_vars.copy()

    def set_global_vars(self, new_vars):
        self._global_vars = new_vars.copy()
