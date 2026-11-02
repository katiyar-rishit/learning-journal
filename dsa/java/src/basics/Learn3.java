package basics;

import java.util.ArrayList;

public class Learn3 {
    static int plusMethod(int a, int b){
        return a + b;
    }

    static double plusMethod(double a, double b){
        return a + b;
    }

    public static void main(String[] args){
        var cars = new ArrayList<String>();

        //widening casting
        int age = 56;
        double newAge = age;
        System.out.println(age);
        System.out.println(newAge);

        //narrowing casting
        double cgpa = 9.56;
        int newCGPA = (int) cgpa;
        System.out.println(cgpa);
        System.out.println(newCGPA);

        String[] brands = {"Mahindra", "Volvo", "Cadbury"};
        for(String brand : brands){
            System.out.println(brand);
        }

        for(int i=0;i<brands.length;i++){
            System.out.println(brands[i]);
        }


        int isum = plusMethod(5,9);
        double dsum = plusMethod(5.5, 5);

    }
}
