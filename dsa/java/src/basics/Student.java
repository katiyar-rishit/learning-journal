package basics;

public class Student {
    int age;
    String name;

    Student(int age, String name){
        this.age = age;
        this.name = name;
    }


    public static void main(String[] args){
        Student s1 = new Student(20, "Rahul");
        Student s2 = new Student(45, "Ravi");

        System.out.println(s1.age);
        System.out.println(s1.name);
        System.out.println(s1);
        System.out.println(s2);

    }
}
