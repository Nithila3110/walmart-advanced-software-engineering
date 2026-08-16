public class PowerOfTwoMaxHeap {

    private int[] heap;
    private int size;
    private int exponent;
    private int childrenCount;

    public PowerOfTwoMaxHeap(int exponent) {

        this.exponent = exponent;

        childrenCount = 1 << exponent;

        heap = new int[10];
        size = 0;
    }

    public void insert(int value) {

        if (size == heap.length) {
            int[] newHeap = new int[heap.length * 2];

            for (int i = 0; i < heap.length; i++) {
                newHeap[i] = heap[i];
            }

            heap = newHeap;
        }

        int currentIndex = size;
        heap[size] = value;
        size++;

        while (currentIndex > 0) {

            int parentIndex =
                    (currentIndex - 1) / childrenCount;

            if (heap[parentIndex] >= heap[currentIndex]) {
                break;
            }

            int temp = heap[parentIndex];
            heap[parentIndex] = heap[currentIndex];
            heap[currentIndex] = temp;

            currentIndex = parentIndex;
        }
    }

    public int popMax() {

        if (size == 0) {
            throw new IllegalStateException("Heap is empty");
        }

        int maximum = heap[0];

        size--;

        if (size > 0) {

            heap[0] = heap[size];

            int currentIndex = 0;

            while (true) {

                int firstChild =
                        currentIndex * childrenCount + 1;

                if (firstChild >= size) {
                    break;
                }

                int largestChild = firstChild;

                int lastChild =
                        Math.min(
                            firstChild + childrenCount - 1,
                            size - 1
                        );

                for (int i = firstChild;
                     i <= lastChild;
                     i++) {

                    if (heap[i] > heap[largestChild]) {
                        largestChild = i;
                    }
                }

                if (heap[currentIndex] >= heap[largestChild]) {
                    break;
                }

                int temp = heap[currentIndex];
                heap[currentIndex] = heap[largestChild];
                heap[largestChild] = temp;

                currentIndex = largestChild;
            }
        }

        return maximum;
    }
}