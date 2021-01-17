import sys
from PythonApplication1 import Parser

class Evaluator:
    """
    """
    def __init__(self, parsedData):
        self.data = parsedData

    def evaluateData(self):
        list_string = []
        for x in self.data:
            if x["type"]=="ExpressionStatement":
                toAdd = str(self.evaluateExpression(x["expression"]))
                #possible to avoid that if statement 
                if toAdd[0] == "(":
                    toAdd = toAdd[1:-1]
                list_string.append((toAdd)+";")
            elif x["type"]=="VariableDeclaration":
                toAdd=str(self.evaluateVariable(x["declarations"],0))
                list_string.append(x["kind"]+" "+(toAdd)+";")
        return list_string
        
    
    def evaluateExpression(self, expr):
        result = ""
        if expr["type"] == "NumericLiteral":
            result = str(expr["value"])
        elif expr["type"] == "BinaryExpression":
            result = "("+str(self.evaluateExpression(expr["left"]))+str(expr["operator"])+str(self.evaluateExpression(expr["right"]))+")"
        return result

    def evaluateVariable(self, expr, indexVariable):
        if indexVariable != (len(expr)-1):
            if ((expr[indexVariable]["init"]) is None):
                return expr[indexVariable]["id"]["name"]+", "+self.evaluateVariable(expr, indexVariable+1)
            elif (expr[indexVariable]["init"]["type"]=="NullLiteral"):
                return expr[indexVariable]["id"]["name"]+" = null"+", "+self.evaluateVariable(expr, indexVariable+1)    
            else:    
                return expr[indexVariable]["id"]["name"]+" = "+expr[indexVariable]["init"]["extra"]["raw"]+", "+self.evaluateVariable(expr, indexVariable+1)
        else :
            if ((expr[indexVariable]["init"]) is None):
                return expr[indexVariable]["id"]["name"]
            elif (expr[indexVariable]["init"]["type"]=="NullLiteral"):
                return expr[indexVariable]["id"]["name"]+" = null"
            else:
                return expr[indexVariable]["id"]["name"]+" = "+expr[indexVariable]["init"]["extra"]["raw"]

def main(filename):
    p = Parser(filename)
    evaluator = Evaluator(p.getData())
    l = evaluator.evaluateData()
    for x in l:
        print(x)
    
if __name__ == "__main__":
    main(sys.argv[1])

