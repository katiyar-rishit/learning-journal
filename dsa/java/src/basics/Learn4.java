package basics;

import java.util.Scanner;

public class Learn4 {
    public static int sumN(int n){
        if(n>0){
            return n + sumN(n-1);
        }else {
            return 0;
        }
    }

    public static void main(String[] args){
        System.out.println(sumN(10));

        Scanner myObj = new Scanner(System.in);

        String username = myObj.nextLine();
        System.out.println(username);
    }
}
