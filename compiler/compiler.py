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
        self.globalVar = {}
        self.indexGlobal = 0
        self.globalValue = []
        

    def compileData(self, depth = 0):
        """
        """
        toWrite = []
        toWrite.append("#include \"base.h\"\n\nint main() {\n")
        for x in self.data:
            if x["type"]=="ExpressionStatement":
                toWrite.append(self.compileExpression(x["expression"])+"\n\n\tpop(r1);\n\tdebug_reg(r1);\n")
            elif x["type"]=="VariableDeclaration":
                    if (depth == 0):
                        toWrite.append("\t"+self.compileVariable(x["declarations"],0))
        toWrite.append("\n\treturn 0; \n }")
        return toWrite

    def compileExpression(self, expr, declaration=False):
        """
        """
        result = ""
        if expr["type"] == "NumericLiteral":
            if declaration:
                result = "iconst("+str(expr["value"])+")"
            else:
                result = "\tpush(iconst("+str(expr["value"])+"));"
        elif expr["type"] == "BinaryExpression" or expr["type"] == "LogicalExpression":
            result = str(self.compileExpression(expr["left"]))+"\n"+str(self.compileExpression(expr["right"]))+"\n\tpop(r1);\n\tpop(r2);\n\t"+self.ops[str(expr["operator"])]+"(r1,r2,r1);\n\tpush(r1);"
        return result

    def compileVariable(self, expr, indexVariable):
        """
        """
        self.globals = True
        if indexVariable != (len(expr)-1):
            if (((expr[indexVariable]["init"]) is None) or (expr[indexVariable]["init"]["type"]=="NullLiteral")): 
                self.globalValue.append("null")
                self.globalVar[expr[indexVariable]["id"]["name"]] = self.indexGlobal
                self.indexGlobal = self.indexGlobal+1
                return "globals["+str(self.indexGlobal-1)+"] = null;\n\t"+self.compileVariable(expr, indexVariable+1)
            else:
                self.globalValue.append(str(self.compileExpression(expr[indexVariable]["init"], True)))
                self.globalVar[expr[indexVariable]["id"]["name"]] = self.indexGlobal
                self.indexGlobal = self.indexGlobal+1
                return "globals["+str(self.indexGlobal-1)+"] = "+str(self.compileExpression(expr[indexVariable]["init"], True))+";\n\t"+self.compileVariable(expr, indexVariable+1)
        else :
            if (((expr[indexVariable]["init"]) is None) or (expr[indexVariable]["init"]["type"]=="NullLiteral")): 
                self.globalValue.append("null")
                self.globalVar[expr[indexVariable]["id"]["name"]] = self.indexGlobal
                self.indexGlobal = self.indexGlobal+1
                return "globals["+str(self.indexGlobal-1)+"] = null;\n\t"
            else:
                self.globalValue.append(str(self.compileExpression(expr[indexVariable]["init"], True)))
                self.globalVar[expr[indexVariable]["id"]["name"]] = self.indexGlobal
                self.indexGlobal = self.indexGlobal+1
                return "globals["+str(self.indexGlobal-1)+"] = "+str(self.compileExpression(expr[indexVariable]["init"], True))+";\n\t"
        
#    def compileLocalVariable(self, expr):
#        return "Not now"
    
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

