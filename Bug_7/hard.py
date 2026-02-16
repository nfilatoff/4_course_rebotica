import ast

class Analyze:
    def __init__(self, code: str):
        self.code = code
        self.result = None

    def start(self):
        self.result = self.estimate_algorithm_complexity(self.code)
        return self.result

    def estimate_algorithm_complexity(self, block):
        try:
            tree = ast.parse(self.code)
        except SyntaxError:
            return "Ошибка: Неверный синтаксис кода."

        # Счетчики для операций, циклов и сортировки
        operation_count = 0
        loop_count = 0
        sorting_detected = False

        def visit(node):
            nonlocal operation_count, loop_count, sorting_detected
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                loop_count += 1
            elif isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
                operation_count += 1
            elif isinstance(node, ast.Call):
                function_name = node.func.id if isinstance(node.func, ast.Name) else ""
                if function_name == "sorted" or function_name == "sort":
                    sorting_detected = True
            for child in ast.iter_child_nodes(node):
                visit(child)

        visit(tree)

        # Вернуть приблизительную оценку сложности
        if sorting_detected:
            return "Приблизительная сложность алгоритма: O(n*log(n))"
        elif loop_count >= 2:
            return f"Приблизительная сложность алгоритма: O(n^{loop_count})"
        else:
            return "Приблизительная сложность алгоритма: O(n)"
