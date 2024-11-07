package example;
import org.example.MatrixMultiplication;
import org.openjdk.jmh.annotations.*;

import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import java.util.Random;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.example.MatrixMultiplication.convertToCOO;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
public class BlockingBenchmark {

    @State(Scope.Thread)
    public static class Operands{
        private final int N = 256;
        private final double[][] A = new double[N][N];
        private final double[][] B = new double[N][N];
        private final double[][] C1 = new double[N][N]; // For naive multiplication
        private final double[][] C2 = new double[N][N];

        private MatrixMultiplication.COOMatrix cooA = convertToCOO(A);
        private MatrixMultiplication.COOMatrix cooB = convertToCOO(B);

        @Setup
        public void setup() {
            Random random = new Random();
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    A[i][j] = random.nextDouble();
                    B[i][j] = random.nextDouble();
                }
            }
            cooA = convertToCOO(A);
            cooB = convertToCOO(B);
        }

    }

    @Benchmark
    @Fork(value=1,warmups = 1)
    @Warmup(iterations = 3)


    public void multiplication(Operands operands){
        MatrixMultiplication.COOMatrix resultMatrix = operands.cooA.multiply(operands.cooB);
        //long memory =getUsedMemory();
        //double cpu = getProcessCpuLoad();
        //System.out.println("CPU Usage: " + cpu + "%");
        //System.out.println("Memory Usage: " + memory / (1024 * 1024) + " MB");
    }

    private double getProcessCpuLoad() {
        OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
        // The com.sun.management.OperatingSystemMXBean has a method to get CPU load
        if (osBean instanceof com.sun.management.OperatingSystemMXBean) {
            return ((com.sun.management.OperatingSystemMXBean) osBean).getProcessCpuLoad() * 100;
        }
        return -1;
    }

    private long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
}
