import sys
from PythonApplication1 import Parser

class Compiler:
    """
    """
    def __init__(self, parsedData):
        self.data = parsedData
        self.globals = False
        self.ops = {"+":"iadd", "-":"isub", "*":"imul", "/":"idiv",
                    "%":"imod", "<":"ilt", "<=":"ile", "==":"ieq"}

    def compileData(self):
        """
        """
        toWrite = []
        toWrite.append("#include \"base.h\"\n\nint main() {\n")
        for x in self.data:
            if x["type"]=="ExpressionStatement":
                toWrite.append(self.compileExpression(x["expression"])+"\n\n\tpop(r1);\n\tdebug_reg(r1);\n")
        toWrite.append("\n\treturn 0; \n }")
        return toWrite

    def compileExpression(self, expr):
        """
        """
        result = ""
        if expr["type"] == "NumericLiteral":
            result = "\tpush(iconst("+str(expr["value"])+"));"
        elif expr["type"] == "BinaryExpression" or expr["type"] == "LogicalExpression":
            result = str(self.compileExpression(expr["left"]))+"\n"+str(self.compileExpression(expr["right"]))+"\n\tpop(r1);\n\tpop(r2);\n\t"+self.ops[str(expr["operator"])]+"(r1,r2,r1);\n\tpush(r1);"
        return result

def main(filename):
    p = Parser(filename)
    compiler = Compiler(p.getData())
    l = compiler.compileData()
    cpt=0
    for x in l:
        if cpt==1:
            if (not(compiler.globals)):
                print("\tinit(8192, 0, 0);")
            else:
                print("\tinit(8192, 0, 8192);")
        print(x)
        cpt = cpt+1
if __name__ == "__main__":
    main(sys.argv[1])

