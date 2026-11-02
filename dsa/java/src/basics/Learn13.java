package basics;

class Animals {
    void makeSound() {
        System.out.println("The animal makes a sound");
    }
}

class Dogs extends Animals {
    @Override
    void makeSound() {
        System.out.println("The dog barks");
    }
}

public class Learn13 {
    public static void main(String[] args) {
        Animals myAnimal = new Animals();
        Animals myDog = new Dogs();

        myAnimal.makeSound();
        myDog.makeSound();
    }
}

