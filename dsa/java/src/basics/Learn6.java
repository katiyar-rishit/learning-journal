package basics;

class Animal{
    protected void sound(){
        System.out.println("Animal makes sound.");
    }
}

class Dog extends Animal{
    void display() {
        sound();
    }
}

class Learn6{
    public static void main(String[] args){
        Dog d1 = new Dog();
        d1.display();

    }
}

