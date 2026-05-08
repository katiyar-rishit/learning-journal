package basics;

import java.awt.Point;
import java.util.Arrays;
import java.util.Date;

public class Learn1 {
    public static void main(String[] args) {
        String name = "John";
        int age = 30;
        int herAge = age;
        System.out.println("Hello " + name + " pushing " + age + " huh");
        System.out.println(herAge);

        //primitive types
        byte myAge = 39;
        int viewCount = 123_456_789;
        long longNumber = 3_123_456_789L;
        float price = 10.99F;
        double moneyCount = 56.73;
        char letter = 'a';
        boolean isEligible = false;

        //reference types
        Date now = new Date();
        System.out.println(now);

        Point point1 = new Point(1 , 1);
        Point point2 = point1;
        point1.x = 2;
        System.out.println(point2);

        //string
        String message = new String("  Hello user");
        //same as
        String ask = "Who?";

        System.out.println(message.endsWith("er"));
        System.out.println(message.length());
        System.out.println(message.startsWith("hey"));
        System.out.println(message.indexOf("H"));
        System.out.println(message.indexOf("hy"));
        System.out.println(message.replace("user", "world"));
        System.out.println(message); //the original string not changed
        System.out.println(message.trim()); //removes unnecessary spaces


        //escape sequences
        String info = "User \"validated\"";
        System.out.println(info);

        String path = "c:\nWindows\\Users\trishit";
        System.out.println(path);


        //arrays
        int[] numbers = new int[5];
        numbers[0] = 1;
        numbers[1] = 2;
        System.out.println(numbers); //returns string of memory address

        System.out.println(Arrays.toString(numbers));

        //arrays - better syntax
        int[] childrenAge = { 2, 3, 5, 1, 4};
        System.out.println(childrenAge.length);
        Arrays.sort(childrenAge);
        System.out.println(Arrays.toString(childrenAge));

        //multi-dimensional arrays
        int[][] matrix = new int[2][3];
        matrix[0][0] = 1;
        System.out.println(Arrays.deepToString(matrix));


    }
}
