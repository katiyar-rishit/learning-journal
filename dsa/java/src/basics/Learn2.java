package basics;

public class Learn2 {
    public static void main(String[] args){
        //constants
        final float PI = 3.14F;

        int result = 10 / 3; //gives whole number
        System.out.println(result);

        double accurateResult = (double)10 / (double)3;
        System.out.println(accurateResult);

        int x = 2;
        int y = x++;
        System.out.println(x);
        System.out.println(y);

        int p = 2;
        int q = ++p;
        System.out.println(p);
        System.out.println(q);


        //implicit casting (small to big)
        //byte > short > int > long > float > double
        short z = 4;
        int o = z + 2;
        System.out.println(o);

        //explicit casting (big to small)
        double u = 2.45;
        int v = (int)u + 3;
        System.out.println(v);

    }
}
