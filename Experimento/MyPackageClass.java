package mypack;
class MyPackageClass {
  public static void main(String[] args) {
    System.out.println("This is my package!");
  }
}
//Intentando crear un paquete desde cmd

/*
Pasos:
1 Navegar por el cmd y crear una archivo java yo uso notepad elnombredelarchivo.java
2 En la parte superior del codigo creamos un paquete con la palabra package (los nombres de los paquetes deben ir en minusculas para que no haya problemas con otros archivos)
3 Guardamos el codigo en el caso de notepad es con control+g
4 Compilamos el archivo con javac nombredelarchivo.java
5 Compilamos el paquete con javac -d . nombredelarchivo.java (el -d es para especificar el destino donde se va a guardar el punto indica que en la misma carpeta)
6 Corremos el codigo con java nombredelarchivo.java  :)