import sys
from PythonApplication1 import Parser

class Compiler:
    """
    """
    def __init__(self, parsedData):
        self.data = parsedData
        self.globals = False
        self.ops = {"+":"iadd", "-":"isub", "*":"imul", "/":"idiv",
                    "%":"imod", "<":"ilt", "<=":"ile", "==":"ieq",
                    "!":"lneg", "&&":"land", "||":"lor"}
        self.globalVar = {}
        self.indexGlobal = 0
        self.globalValue = []
        self.nbWhile = 1
        self.nbIf = 1
        self.nbFor = 1
        

    def compileData(self, depth = 0):
        """
        """
        toWrite = []
        if depth==0:
            toWrite.append("#include \"base.h\"\n\nint main() {\n")
        for x in self.data:
            if x["type"]=="ExpressionStatement":
                if (x["expression"]["type"] != "CallExpression"):
                    toWrite.append(self.compileExpression(x["expression"])+"\n\n\tpop(r1);\n\tdebug_reg(r1);\n")
                if (x["expression"]["type"] == "CallExpression") and x["expression"]["callee"]["name"]=="print":
                    toWrite.append("\n\n\tpop(r1);\n\tdebug_reg(r1);\n")
            elif x["type"]=="VariableDeclaration":
                    if (depth == 0):
                        toWrite.append("\t"+self.compileVariable(x["declarations"],0))
            elif x["type"]=="WhileStatement" :
                    block = Compiler(x["body"]["body"])
                    block.globals = self.globals
                    block.globalVar = self.globalVar
                    block.indexGlobal = self.indexGlobal
                    block.globalValue = self.globalValue
                    strWhile = str(self.nbWhile)
                    toWrite.append("\n\tgoto endwhile"+strWhile+";")
                    toWrite.append("\nwhile"+strWhile+":"+"\n".join(block.compileData(1))+"\n\tgoto endwhile"+strWhile+";")
                    toWrite.append("\nendwhile"+strWhile+":")
                    value = self.compileExpression(x["test"])
                    toWrite.append(value+"\n\tpop(r1);\n\tif(asbool(r1)) goto while"+strWhile+";")
                    self.nbWhile = self.nbWhile+1
            elif x["type"]=="IfStatement" :
                    block = Compiler(x["consequent"]["body"])
                    block.globals = self.globals
                    block.globalVar = self.globalVar
                    block.indexGlobal = self.indexGlobal
                    block.globalValue = self.globalValue
                    strIf = str(self.nbIf)
                    #toWrite.append("\n\tgoto iftest"+strIf+";")
                    toWrite.append("\niftest"+strIf+":")
                    value = self.compileExpression(x["test"])
                    toWrite.append(value+"\n\tpop(r1);\n\tif(asbool(r1)) {\t\t")
                    toWrite.append("\n".join(block.compileData(1))+"\t}\n")
                    if x["alternate"]:
                         toWrite.append("\telse {\t\t")
                         alter = Compiler(x["alternate"]["body"])
                         alter.globals = self.globals
                         alter.globalVar = self.globalVar
                         alter.indexGlobal = self.indexGlobal
                         alter.globalValue = self.globalValue
                         toWrite.append("\n".join(block.compileData(1))+"\t}\n")                    
                    self.nbIf = self.nbIf+1
            elif x["type"]=="ForStatement" :
                    block = Compiler(x["body"]["body"])
                    block.globals = self.globals
                    block.globalVar = self.globalVar
                    block.indexGlobal = self.indexGlobal
                    block.globalValue = self.globalValue
                    strFor = str(self.nbFor)
                    update = self.compileExpression(x["update"])
                    if self.nbFor == 1:
                        toWrite.append("\tint index = 0;")
                    toWrite.append("\n\tgoto endfor"+strFor+";")
                    toWrite.append("\nfor"+strFor+":"+"\n".join(block.compileData(1))+"\n\t"+update+"\n\tgoto endfor"+strFor+";")
                    toWrite.append("\nendfor"+strFor+":")
                    value = self.compileExpression(x["test"])
                    if x["init"] :
                        init = self.compileExpression(x["init"])
                        toWrite.append("\tif (index==0) {\t"+init+"\n\tindex++;\n\t}")
                    toWrite.append(value+"\n\tpop(r1);\n\tif(asbool(r1)) goto for"+strFor+";")
                    self.nbFor = self.nbFor+1
                    
        if depth==0:
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
        elif (expr["type"] == "BinaryExpression" or expr["type"] == "LogicalExpression") and expr["operator"]!="!=":
            result = str(self.compileExpression(expr["left"]))+"\n"+str(self.compileExpression(expr["right"]))+"\n\tpop(r1);\n\tpop(r2);\n\t"+self.ops[str(expr["operator"])]+"(r1,r2,r1);\n\tpush(r1);"
        elif (expr["type"] == "BinaryExpression" or expr["type"] == "LogicalExpression") and expr["operator"]=="!=":
            result = str(self.compileExpression(expr["left"]))+"\n"+str(self.compileExpression(expr["right"]))+"\n\tpop(r1);\n\tpop(r2);\n\tieq(r1,r2,r1);\n\tlneg(r1,r1);\n\tpush(r1);"
        elif expr["type"]=="Identifier":
            value = int(self.globalVar[expr["name"]])
            result = "\tpush(globals["+str(value)+"]);"
        elif expr["type"] == "UpdateExpression":
            index = int(self.globalVar[expr["argument"]["name"]])
            result = "\n\tpush(globals["+str(index)+"]);\n\tpush(iconst(1));"
            if str(expr["operator"]) == "++":
                result = result+"\n\tpop(r1);\n\tpop(r2);\n\tiadd(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
        elif expr["type"]=="AssignmentExpression":
            index = int(self.globalVar[expr["left"]["name"]])
            result = "\n\tpush(globals["+str(index)+"]);\n"+str(self.compileExpression(expr["right"]))+";"
            if str(expr["operator"]) == "+=":
                result += "\n\tpop(r1);\n\tpop(r2);\n\tiadd(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
            if str(expr["operator"]) == "-=":
                result += "\n\tpop(r1);\n\tpop(r2);\n\tisub(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
            if str(expr["operator"]) == "*=":
                result += "\n\tpop(r1);\n\tpop(r2);\n\timul(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"

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
                return "globals["+str(self.indexGlobal-1)+"];\n\t"
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

