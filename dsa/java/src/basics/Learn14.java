package basics;

class GenericClass<T1, T2, T3> {
    T1 value1;
    T2 value2;
    T3 value3;

    GenericClass(T1 value1, T2 value2, T3 value3) {
        this.value1 = value1;
        this.value2 = value2;
        this.value3 = value3;
    }

    void display() {
        System.out.println("Value 1: " + value1);
        System.out.println("Value 2: " + value2);
        System.out.println("Value 3: " + value3);
    }
}

public class Learn14 {
    public static void main(String[] args) {

        GenericClass<Integer, Double, String> obj =
                new GenericClass<>(10, 25.5, "Hello");

        obj.display();
    }
}