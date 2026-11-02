package basics;

class Learn12 {

    int add(int a, int b) {
        return a + b;
    }

    int add(int a, int b, int c) {
        return a + b + c;
    }

    void printData(int text) {
        System.out.println("Integer: " + text);
    }

    void printData(String text) {
        System.out.println("String: " + text);
    }

    void identity(String name, int id) {
        System.out.println("Name: " + name + ", ID: " + id);
    }

    void identity(int id, String name) {
        System.out.println("ID: " + id + ", Name: " + name);
    }

    public static void main(String[] args) {
        Learn12 demo = new Learn12();

        System.out.println(demo.add(5, 10));
        System.out.println(demo.add(5, 10, 15));

        demo.printData(100);
        demo.printData("Hello");

        demo.identity("Alice", 101);
        demo.identity(102, "Bob");
    }
}
