import numpy as np
import pytest
import psutil

def matrix_multiply(a, b):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    unroll_factor = 4  # Set the unrolling factor

    for i in range(n):
        for j in range(n):
            sum = 0
            k = 0

            # Unroll loop in chunks of 4
            while k <= n - unroll_factor:
                sum += (A[i][k] * B[k][j] +
                        A[i][k + 1] * B[k + 1][j] +
                        A[i][k + 2] * B[k + 2][j] +
                        A[i][k + 3] * B[k + 3][j])
                k += unroll_factor

            # Handle any remaining elements if n is not a multiple of 4
            while k < n:
                sum += A[i][k] * B[k][j]
                k += 1

            C[i][j] = sum

    return C

@pytest.fixture
def setup_matrices():
    size = 256
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return A, B

@pytest.mark.benchmark(min_rounds=5)
def test_matrix_multiply(benchmark, setup_matrices):
    A, B = setup_matrices

    result = benchmark(matrix_multiply, A, B)
    assert result is not None

size = 256
A = np.random.rand(size, size)
B = np.random.rand(size, size)
print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)
