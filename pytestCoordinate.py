import numpy as np
import pytest
import psutil


class COOMatrix:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.rowIndices=[]
        self.colIndices=[]
        self.values=[]
    def addValue(self,row,col,value):
        if value != 0:
            self.rowIndices.append(row)
            self.colIndices.append(col)
            self.values.append(value)
    def multiply(self,B):
        if self.cols==B.rows:
            result=COOMatrix(self.rows,B.cols)
            tempResult=np.zeros((self.rows,B.cols),dtype = int)
            for i in range(0,len(self.values),1):
                rowA=self.rowIndices[i]
                colA=self.colIndices[i]
                valA=self.values[i]
                for j in range(0,len(B.values),1):
                    if B.rowIndices[j]==colA:
                        colB=B.colIndices[j]
                        valB=B.values[j]
                        tempResult[rowA,colB]+= valA*valB
            for i in range(0,self.rows,1):
                for j in range(0,B.cols,1):
                    if tempResult[i,j]!=0:
                        result.addValue(i,j,tempResult[i,j])
            return result

def convertToCOO(matrix,N):
    cooMatrix=COOMatrix(N,N)
    for i in range(0,N,1):
        for j in range(0,N,1):
            if matrix[i,j] > 0.95:
                cooMatrix.addValue(i,j,matrix[i][j])
    return cooMatrix
def matrix_multiply(A,B):
    resultMatrix=A.multiply(B)
    return resultMatrix
    
@pytest.fixture
def setup_matrices():
    size = 128
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    cooA=convertToCOO(A,size)
    cooB=convertToCOO(B,size)
    return cooA, cooB

@pytest.mark.benchmark(min_rounds=5)
def test_matrix_multiply(benchmark, setup_matrices):
    A, B = setup_matrices

    result = benchmark(matrix_multiply, A, B)
    assert result is not None

size = 128
A = np.random.rand(size, size)
B = np.random.rand(size, size)
cooA=convertToCOO(A,size)
cooB=convertToCOO(B,size)
resultMatrix=cooA.multiply(cooB)
print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)


