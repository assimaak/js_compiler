import sys
from PythonApplication1 import Parser
from copy import deepcopy

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
        self.bp_param = 3
        self.bp_varLoc = -1
        self.locVar = {}
        self.cptLoc = 0
        

    def compileData(self, depth = 0):
        """
        """
        toWrite = []
        if depth==0:
            toWrite.append("#include \"base.h\"\n#include <stdio.h>\nint main() {\n")
        for x in self.data:
            if x["type"]=="ExpressionStatement":
                drop = ""
                if (x["expression"]["type"] == "CallExpression"):
                    drop = "\n\tdrop("+str(self.cptLoc)+");"
                toWrite.append(self.compileExpression(x["expression"])+"\n\n\tpop(r1);"+drop+"\n\tdebug_reg(r1);\n")
               # if (x["expression"]["type"] == "CallExpression") and x["expression"]["callee"]["name"]=="print":
                #    toWrite.append("\n\n\tdebug_reg(globals["+str(self.globalVar[str(x["expression"]["arguments"][0]["name"])])+"]);\n")
            elif x["type"]=="VariableDeclaration":
                    if (depth == 0):
                        toWrite.append("\t"+self.compileVariable(x["declarations"],0))
                    else:
                        for var in x["declarations"]:
                            toWrite.append("\t"+self.compileLocalVariable(var))
            elif x["type"]=="WhileStatement" :
                    block = Compiler(x["body"]["body"])
                    block.globals = self.globals
                    block.globalVar = self.globalVar
                    block.indexGlobal = self.indexGlobal
                    block.globalValue = self.globalValue
                    strWhile = str(self.nbWhile)
                    toWrite.append("\tgoto endwhile"+strWhile+";")
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
                    value = self.compileExpression(x["test"])
                    toWrite.append(value+"\n\tpop(r1);\n\tlneg(r1,r1);\n\tpush(r1);\n\tpop(r1);\n\tif(asbool(r1)) goto else"+strIf+";\t\t")
                    toWrite.append("\n".join(block.compileData(1))+"\t\n")
                    toWrite.append("else"+strIf+":\t\t")
                    if x["alternate"]:
                         alter = Compiler(x["alternate"]["body"])
                         alter.globals = self.globals
                         alter.globalVar = self.globalVar
                         alter.indexGlobal = self.indexGlobal
                         alter.globalValue = self.globalValue
                         toWrite.append("\n".join(block.compileData(1)))
                    toWrite.append("\tgoto endif"+strIf+";")
                    toWrite.append("endif"+strIf+":")
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
            elif x["type"]=="FunctionDeclaration":
                self.cptLoc = 0
                functname = x["id"]["name"]
                toWrite.append("\tgoto functend_"+functname+";")
                toWrite.append("\nfunct_"+functname+":")
                params = []
                for i in range(len(x["params"])):
                    self.globalVar[x["params"][i]["name"]] = ("bp["+str(self.bp_param+i)+"]")
                    self.indexGlobal = self.indexGlobal+1
                funBlock = (x["body"]["body"])
                block = Compiler(funBlock)
                block.globalVar = self.globalVar 
                block.indexGlobal = self.indexGlobal 
                block.gloabalValue = self.globalValue  
                block.nbWhile = self.nbWhile  
                block.nbIf = self.nbIf 
                block.nbFor = self.nbFor   
                toWrite.append("\n".join(block.compileData(1)))
                toWrite.append("functend_"+functname+":")
                self.cptLoc = block.cptLoc
            elif x["type"]=="ReturnStatement":
                toWrite.append("\tpop(r1);")
                toWrite.append("\tdrop("+str(self.cptLoc)+");")
                toWrite.append("\tret(r1);")
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
            if "bp" in str(self.globalVar[expr["name"]]):
                value = self.globalVar[expr["name"]]
                result = "\tpush("+str(value)+");"
            elif expr["name"] in self.locVar:
                value = self.locVar[expr["name"]]
                result = "\tpush("+str(value)+");"
            else:
                value = int(self.globalVar[expr["name"]])
                result = "\tpush(globals["+str(value)+"]);"
        elif expr["type"] == "UpdateExpression":
            index = int(self.globalVar[expr["argument"]["name"]])
            result = "\n\tpush(globals["+str(index)+"]);\n\tpush(iconst(1));"
            if str(expr["operator"]) == "++":
                result = result+"\n\tpop(r1);\n\tpop(r2);\n\tiadd(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
        elif expr["type"]=="AssignmentExpression":
            index = int(self.globalVar[expr["left"]["name"]])
            if str(expr["operator"]) == "=":
                result = "\n"+str(self.compileExpression(expr["right"]))+";"
            else:
                result = "\n\tpush(globals["+str(index)+"]);\n"+str(self.compileExpression(expr["right"]))+";"
            if str(expr["operator"]) == "+=":
                result += "\n\tpop(r1);\n\tpop(r2);\n\tiadd(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
            elif str(expr["operator"]) == "-=":
                result += "\n\tpop(r1);\n\tpop(r2);\n\tisub(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
            elif str(expr["operator"]) == "*=":
                result += "\n\tpop(r1);\n\tpop(r2);\n\timul(r1,r2,r1);\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
            else:
                result+="\n\tglobals["+str(index)+"]=r1;\n\tpush(r1);"
        elif expr["type"] == "CallExpression":
            args = ""
            for x in expr["arguments"]:
                    args = self.compileExpression(x)+args
            if expr["callee"]["name"] == "print":
                result = args
            else:
                result = args+"\n\tcall(funct_"+expr["callee"]["name"]+");"
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
        
    def compileLocalVariable(self, expr):
        self.locVar[expr["id"]["name"]] = "bp["+str(self.bp_varLoc)+"]"
        self.bp_varLoc = self.bp_varLoc-1
        self.cptLoc = self.cptLoc+1
        return str(self.compileExpression(expr["init"]))
    
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

