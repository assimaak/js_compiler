import sys
from PythonApplication1 import Parser

class Interpreter:
    """
    """
    def __init__(self, parsedData):
        self.data = parsedData
        self.ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y),
                    "*": (lambda x,y: x*y), "/": (lambda x,y: x/y),
                    "%": (lambda x,y: x%y)}

    def evaluateData(self):
        list_string = []
        if not(self.data is None):
            for x in self.data:
                if x["type"]=="ExpressionStatement":
                    toAdd = "ExpressionStatement : "+str(self.evaluateExpression(x["expression"]))
                    #possible to avoid that if statement 
                    #if toAdd[0] == "(":
                    #    toAdd = toAdd[1:-1]
                    list_string.append((toAdd)+";")
                elif x["type"]=="VariableDeclaration":
                    toAdd=str(self.evaluateVariable(x["declarations"],0))
                    list_string.append(x["kind"]+" "+(toAdd)+";")
                elif x["type"]=="WhileStatement" :
                    block = Evaluator(x["body"]["body"])
                    toAdd="while "+str(self.evaluateExpression(x["test"])+" {\n\t"+('\n\t'.join(block.evaluateData()))+" \n}")
                    list_string.append(toAdd)
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
                    forBlock = Evaluator(x["body"]["body"]).evaluateData()
                    init = ""
                    if not (x["init"] is None):
                        init = self.evaluateExpression(x["init"])
                    toAdd = "for ("+init+"; "+self.evaluateExpression(x["test"])+"; "+self.evaluateExpression(x["update"])+") {\n\t"+"\n\t".join(forBlock)+"\n}"
                    list_string.append(toAdd)
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
        
    
    def evaluateExpression(self, expr):
        result = ""
        if expr["type"] == "NumericLiteral":
            result = str(expr["value"])
        elif expr["type"] == "BinaryExpression" or expr["type"] == "LogicalExpression":
            result = self.ops[str(expr["operator"])] (int(self.evaluateExpression(expr["left"])),int(self.evaluateExpression(expr["right"])))
        return result

def main(filename):
    p = Parser(filename)
    interpreter = Interpreter(p.getData())
    l = interpreter.evaluateData()
    for x in l:
        print(x)
    
if __name__ == "__main__":
    main(sys.argv[1])
