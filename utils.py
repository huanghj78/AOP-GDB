import gdb
from pycparser import parse_file, c_ast, c_generator, c_parser

def get_value(v: gdb.Value):
    return v.cast(gdb.lookup_type(str(v.type)))

def get_type(v: gdb.Value):
    return str(v.type)

# 定义一个函数，用于在函数体第一行插入一条语句
def insert_statement(file_name, statement, func_name="inject"):
    # 解析C文件，获取AST
    ast = parse_file(file_name, use_cpp=False,
                     cpp_path='gcc',
                     cpp_args=['-E', r'-Iutils/fake_libc_include'])
    # 创建一个C代码生成器
    generator = c_generator.CGenerator()
    # 遍历AST，找到目标函数定义节点
    for node in ast.ext:
        if isinstance(node, c_ast.FuncDef) and node.decl.name == func_name:
            # 获取函数体节点
            body = node.body
            # 获取函数体中的语句列表
            stmts = body.block_items
            # 创建一个新的语句节点，根据给定的语句字符串解析
            new_stmt = c_parser.CParser().parse(statement).ext[0]
            # 在语句列表的第一位插入新的语句节点
            stmts.insert(0, new_stmt)
            # 用修改后的语句列表替换原来的函数体
            body.block_items = stmts
            # 生成修改后的C代码，并打印
            # print(generator.visit(ast))
            # 生成修改后的C代码，并赋值给一个变量
            new_code = generator.visit(ast)
            # 打开原文件，写入模式
            with open(file_name, "w") as f:
                # 写入新的C代码
                f.write(new_code)
            # 结束遍历
            break

def insert_attribute(file_name, attribute, func_name="inject"):
    # 解析C文件，获取AST
    ast = parse_file(file_name, use_cpp=False)
    # 创建一个C代码生成器
    generator = c_generator.CGenerator()
    # 遍历AST，找到目标函数定义节点
    for node in ast.ext:
        if isinstance(node, c_ast.FuncDef) and node.decl.name == func_name:
            # 获取函数声明节点
            decl = node.decl
            # 创建一个新的属性节点，根据给定的属性字符串解析
            new_attr = c_ast.CParser().parse(attribute).ext[0]
            # 在函数声明的属性列表中添加新的属性节点
            decl.funcspec.append(new_attr)