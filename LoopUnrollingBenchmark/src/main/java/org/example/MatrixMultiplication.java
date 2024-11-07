package org.example;

public class MatrixMultiplication {

	public void execute(double[][] A, double[][] B, double[][] C, int N) {
		int n = A.length;

		int unrollFactor = 4;  // Unroll by a factor of 4

		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				double sum = 0;

				// Unrolled loop
				int k;
				for (k = 0; k <= n - unrollFactor; k += unrollFactor) {
					sum += A[i][k] * B[k][j]
							+ A[i][k + 1] * B[k + 1][j]
							+ A[i][k + 2] * B[k + 2][j]
							+ A[i][k + 3] * B[k + 3][j];
				}

				// Handle remaining elements if n is not a multiple of the unroll factor
				for (; k < n; k++) {
					sum += A[i][k] * B[k][j];
				}

				C[i][j] = sum;
			}
		}
	}
}
