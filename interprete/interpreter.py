import sys
import builtins
from PythonApplication1 import Parser

class Interpreter:
    """
    """
    def __init__(self, parsedData):
        self.data = parsedData
        self.ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y),
                    "*": (lambda x,y: x*y), "/": (lambda x,y: x/y),
                    "%": (lambda x,y: x%y), "<": (lambda x,y: x<y),
                    ">": (lambda x,y: x>y), "==":(lambda x,y: x==y),
                    "!=":(lambda x,y: x!=y),">=":(lambda x,y: x>=y),
                    "<=":(lambda x,y: x<=y),"++":(lambda x: x+1),
                    "--":(lambda x: x-1), "+=":(lambda x,y: x+y),
                    "-=":(lambda x,y: x-y)}
        self.var = {"print" : "print"}
        self.builtins = ["print"]

    def evaluateData(self):
        list_string = []
        if not(self.data is None):
            for x in self.data:
                if x["type"]=="ExpressionStatement":
                    print("ExpressionStatement: "+str(self.evaluateExpression(x["expression"])))
                    #possible to avoid that if statement 
                    #if toAdd[0] == "(":
                    #    toAdd = toAdd[1:-1]
                elif x["type"]=="VariableDeclaration":
                    print(str(self.evaluateVariable(x["declarations"],0)))
                elif x["type"]=="WhileStatement" :
                    block = Interpreter(x["body"]["body"])
                    block.var = self.var
                    print("WhileStatement: \n")
                    while self.evaluateExpression(x["test"]):
                        block.evaluateData()
                    print("\nEndWhileStatement\n")
                elif x["type"]=="IfStatement" :
                    ifBlock = Evaluator(x["consequent"]["body"])
                    elseEvaluation = []
                    if not (x["alternate"] is None):
                        elseBlock = Evaluator(x["alternate"]["body"])
                        elseEvaluation = elseBlock.evaluateData()
                    toAdd="if "+str(self.evaluateExpression(x["test"])+" {\n\t"+('\n\t'.join(ifBlock.evaluateData()))+" \n}")
                    if elseEvaluation != []:
                        toAdd = toAdd+"\nelse { \n\t"+"\n\t".join(elseEvaluation)+"\n}"              
                    list_string.append(toAdd)
                elif x["type"] == "ForStatement":
                    block = Interpreter(x["body"]["body"])
                    if x["init"] != None:
                        self.evaluateExpression(x["init"])
                    block.var = self.var
                    print("ForStatement: \n")
                    while self.evaluateExpression(x["test"]):
                        block.evaluateData()
                        self.evaluateExpression(x["update"])
                    print("\nEndForStatement\n")
                elif x["type"] == "BreakStatement":
                    list_string.append("break;")
                elif x["type"] == "ContinueStatement":
                    list_string.append("continue;")
                elif x["type"] == "FunctionDeclaration":
                    funcBlock = Evaluator(x["body"]["body"]).evaluateData()
                    params=[]
                    if not(x["params"] is None):
                        for y in x["params"]:
                            params.append(self.evaluateExpression(y))
                    str_params = ", ".join(params)
                    toAdd = "function "+x["id"]["name"]+"("+str_params+") {\n\t"+"\n\t".join(funcBlock)+"\n}"
                    list_string.append(toAdd)
                elif x["type"]=="ReturnStatement":
                    list_string.append("return "+self.evaluateExpression(x["argument"])+";")
                elif x["type"]=="SwitchStatement":
                    switchBlock = Evaluator(x["cases"]).evaluateData()
                    list_string.append("switch("+self.evaluateExpression(x["discriminant"])+") {\n\t"+"\n\t".join(switchBlock)+"\n}")
                elif x["type"]=="SwitchCase":
                    if not( x["test"] is None):
                        list_string.append("\tcase "+self.evaluateExpression(x["test"])+":\n\t\t"+"\n\t\t".join(Evaluator(x["consequent"]).evaluateData())+"\n}")
                    else:
                        list_string.append("\tdefault:\n\t\t"+"\n\t\t".join(Evaluator(x["consequent"]).evaluateData())+"\n}")
        return list_string
        
    
    def evaluateExpression(self, expr, opt=False):
        result = ""
        if expr["type"] == "NumericLiteral":
            result = int(expr["value"])
        elif expr["type"] == "BinaryExpression" or expr["type"] == "LogicalExpression":
            result = self.ops[str(expr["operator"])] (int(self.evaluateExpression(expr["left"])),int(self.evaluateExpression(expr["right"])))
        elif expr["type"] == "StringLiteral":
            result = expr["value"]
        elif expr["type"] == "Identifier":
            if opt:
                result = expr["name"]
            else:
                result = self.var[(expr["name"])]
        elif expr["type"]=="UpdateExpression":
            self.var[(expr["argument"]["name"])] = self.ops[str(expr["operator"])] (int(self.evaluateExpression(expr["argument"])))
            print("UpdateExpression: "+expr["argument"]["name"]+" "+str(expr["operator"]))
        elif expr["type"]=="CallExpression":
            func_name = self.evaluateExpression(expr["callee"])
            func_arguments= []
            for x in expr["arguments"]:
                func_arguments.append(self.evaluateExpression(x))
            if func_name in self.builtins:
                my_func = getattr(builtins, func_name)
                print("CallExpression: "+func_name+" "+" ".join(str(v) for v in func_arguments)+" -> (function_execution below)")
                my_func(*func_arguments)
        elif expr["type"]=="AssignmentExpression":
            operator = expr["operator"]
            if str(operator) == "=":
                self.var[self.evaluateExpression(expr["left"], True)] = int(self.evaluateExpression(expr["right"]))
            else:
                self.var[self.evaluateExpression(expr["left"], True)] = self.ops[str(operator)] (int(self.evaluateExpression(expr["left"])),int(self.evaluateExpression(expr["right"])))
            print(str(self.evaluateExpression(expr["left"]))+str(expr["operator"])+str(self.evaluateExpression(expr["right"])))
        return result

    def evaluateVariable(self, expr, indexVariable):
        if indexVariable != (len(expr)-1):
            if ((expr[indexVariable]["init"]) is None):
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+"\n"+self.evaluateVariable(expr, indexVariable+1)
            elif (expr[indexVariable]["init"]["type"]=="NullLiteral"):
                self.var[(expr[indexVariable]["id"]["name"])]= None
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+" null"+"\n"+self.evaluateVariable(expr, indexVariable+1)
            elif ((expr[indexVariable]["init"]["type"])=="MemberExpression"):
                self.var[(expr[indexVariable]["id"]["name"])]="MemberExpression not treated yet"
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+" "+self.evaluateExpression(expr[indexVariable]["init"])+"\n"+self.evaluateVariable(expr, indexVariable+1)
            else:
                self.var[(expr[indexVariable]["id"]["name"])]=self.evaluateExpression(expr[indexVariable]["init"])
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+" "+str(self.evaluateExpression(expr[indexVariable]["init"]))+"\n"+self.evaluateVariable(expr, indexVariable+1)
        else :
            if ((expr[indexVariable]["init"]) is None):
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]
            elif (expr[indexVariable]["init"]["type"]=="NullLiteral"):
                self.var[(expr[indexVariable]["id"]["name"])]=None
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+" null"
            elif ((expr[indexVariable]["init"]["type"])=="MemberExpression"):
                self.var[(expr[indexVariable]["id"]["name"])]="MemberExpression not treated yet"
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+" "+self.evaluateExpression(expr[indexVariable]["init"])
            else:
                self.var[(expr[indexVariable]["id"]["name"])]=self.evaluateExpression(expr[indexVariable]["init"])
                return "VariableDeclaration: "+expr[indexVariable]["id"]["name"]+" "+str(self.evaluateExpression(expr[indexVariable]["init"]))



def main(filename):
    p = Parser(filename)
    interpreter = Interpreter(p.getData())
    l = interpreter.evaluateData()
    for x in l:
        print(x)
    
if __name__ == "__main__":
    main(sys.argv[1])

