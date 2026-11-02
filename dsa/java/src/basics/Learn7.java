package basics;

class Human {
    int age;
    float height;

    Human(int age, float height) {
        this.age = age;
        this.height = height;
    }

    void greet() {
        System.out.println("Hi");
    }
}

class Female extends Human {
    Female(int age, float height) {
        super(age, height);
    }

    void StateGender() {
        System.out.println("Female");
    }
}

class Male extends Human {
    Male(int age, float height) {
        super(age, height);
    }

    void StateGender() {
        System.out.println("Male");
    }
}

public class Learn7 {
    public static void main(String[] args) {
        Female f1 = new Female(34, 174);
        Human h1 = new Human(32, 156);

        System.out.println(f1);
        f1.StateGender();

        System.out.println(h1);
        System.out.println(h1.age);
    }
}