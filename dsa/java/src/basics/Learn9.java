package basics;

public class Learn9 {
    public static void main(String[] args){
        String s = new String("hello world");

        System.out.println(s.charAt(0));
        System.out.println(s.toUpperCase());
        System.out.println(s.toLowerCase());
        System.out.println(s.substring(0, 5));
        System.out.println(s.replace("world", "harvard"));
        System.out.println(s.length());
        System.out.println(s.indexOf("har"));
        System.out.println(s.isEmpty());
        System.out.println(s.lastIndexOf('o'));

        int num = 56;
        String s1 = String.valueOf(num);
        System.out.println(s1+10);
        System.out.println(s.equals(s1));
    }
}
