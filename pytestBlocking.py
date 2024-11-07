import numpy as np
import pytest
import psutil

def multiplyBlock(A,B,C,N,blockSize,rowBlock,colBlock,kBlock):
    for i in range(rowBlock,min((rowBlock+blockSize),N),1):
        for j in range(colBlock,min((colBlock+blockSize),N),1):
            suma=0
            for k in range(kBlock,min((kBlock+blockSize),N),1):
                suma+=A[i,k]*B[k,j]
            C[i,j]+=suma
    return C

def matrix_multiply(A,B,C,N,blockSize):
    if  A.shape[1] == B.shape[0]:
        for i in range(0,N,blockSize): 
            for j in range(0,N,blockSize):
                for k in range(0,N,blockSize):
                  C= multiplyBlock(A,B,C,N,blockSize,i,j,k)
        return C
    else:
        return "Sorry, cannot multiply A and B."

@pytest.fixture
def setup_matrices():
    size = 64
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    C = np.zeros((A.shape[0],B.shape[1]),dtype = float)
    blockSize = 64
    return A, B, C, size, blockSize

@pytest.mark.benchmark(min_rounds=5)
def test_matrix_multiply(benchmark, setup_matrices):
    A, B , C, N, blockSize= setup_matrices

    result = benchmark(matrix_multiply, A, B, C, N, blockSize)
    assert result is not None

size = 64
A = np.random.rand(size, size)
B = np.random.rand(size, size)
C = np.zeros((A.shape[0],B.shape[1]),dtype = float)
blockSize = 64
matrix_multiply(A,B,C,size,blockSize)
print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)
