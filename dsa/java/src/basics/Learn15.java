package basics;

public class Learn15 {
    <T1,T2,T3> void display(T1 value1,T2 value2,T3 value3 ){
        System.out.println("EmployeeID: "+value1);
        System.out.println("EmployeeName: "+value2);
        System.out.println("EmployeeSalary: "+value3);
    }

    public static void main(String[] args){
        Learn15 d = new Learn15();
        d.display(102,"Aarti",45678.23);
    }
}
