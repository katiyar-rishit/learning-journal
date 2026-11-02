package basics;

public class Learn17 implements Printer<String> {
    public void print(String value){
        System.out.println(value);
    }

    public static void main(String[] args){
        Learn17 t = new Learn17();
        t.print("Hello Java");
    }
}

interface Printer<T> {
    void print(T value);
}