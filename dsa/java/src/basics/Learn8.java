package basics;

public class Learn8 {
    public static void main(String[] args){

        String s = new String("hello world");

        char[] ch = s.toCharArray();

        char temp;
        for (int i=0;i<ch.length / 2;i++){
            temp = ch[i];
            ch[i] = ch[ch.length - 1 - i];
            ch[ch.length- 1 - i] = temp;
        }
        System.out.println(ch);
    }
}
