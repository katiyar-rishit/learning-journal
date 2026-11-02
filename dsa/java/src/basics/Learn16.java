package basics;

class GenClass<T> {

    T value;

    GenClass(T value) {
        this.value = value;
    }

    void display() {
        System.out.println("Value: " + value);
    }

    <U> void show(U data) {
        System.out.println("Data: " + data);
    }

    void printTwice() {
        System.out.println(value);
        System.out.println(value);
    }
}

public class Learn16 {
    public static void main(String[] args) {

        GenClass<Integer> obj = new GenClass<>(10);

        obj.display();

        obj.show("Hello");
        obj.show(25.5);

        obj.printTwice();
    }
}