/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package misc;

/**
 *
 * @author sajja
 */
public class Misc {

    /**
     * @param args the command line arguments
     */
    
//
//    public Misc() {
//       NumToWord._main();
//    }
//    public static void main(String[] args){
//           NumToWord._main();
//    }
//    
    
    static String line = "";
    public static void main(String[] args) {
        // TODO code application logic here
        temp();
                String random = "CHASE\n" +
                "S' MPTON\n" +
                "60 MAIN ST\n" +
                "ATM NUMBER\n" +
                "NY3181\n" +
                "DATE:\n" +
                "08/07/11\n" +
                "CARD NUMBER: ******* ****1453\n" +
                "TIME:\n" +
                "16:23\n" +
                "SEQUENCE NUMBER: 2334\n" +
                "WITHDRAWAL FROM\n" +
                "ACCOUNT ENDING WITH: XXXXXXXXXXx6817\n" +
                "CHECKING\n" +
                "AMOUNT\n" +
                "AVAILAßLE BALANCE:\n" +
                "PRESENT BALANCE:\n" +
                "$500.000\n" +
                "$329,174.91\n" +
                "$329,174.91";
                
//                System.out.println(random);
//                random = random.replaceAll("TIME", " ");
//                System.err.println(random);
    }
    
    private static void xyz(String line){
        String[] wv ;
        do{
            wv = findkeyWord(line);
            if (wv!=null){
               String word = wv[0];
               String value = wv[1];
               String tword = word + " ";
                System.out.println("XYZ: " + word +" = "+ value);
                   
              System.out.println("twmpWord:"  + tword.toUpperCase());
                line = line.replaceAll(tword, "");
                tword = value ;
                System.out.println("twmpWord:"  + tword.toUpperCase());
                line = line.replaceAll(tword, "");
            }
        }while(wv != null);
//                   tword = " " + word;
//                   line.replaceAll(tword, "");
                   
        
    }

    
    private static String abc(String line, int ind){
        String value = "";
       
        for (int i = ind; line.charAt(i) != '\n'; i++) {
            System.out.println("ABC: " + String.valueOf(line.charAt(i)));
            value += line.charAt(i);
        }
//        while(true){
////            Log.d("Found", String.valueOf(line.charAt(ind)));
//            System.out.println("ABC: " + String.valueOf(line.charAt(ind)));
//            if(line.charAt(ind) == '\n'){
//                break;
//            }
//            value += line.charAt(ind);
//            ind++;
//        }
        return value;
    }
     
     private static String[] findkeyWord(String str){
        String line = str.trim();
//        Log.d("Found", line);
//         System.err.println("FOUND: " + line);
        String[] keywords = {"time", "date", "amount", "qty", "quantity", "description", "desc"};
//        char[] cs = line.getChars();

        for(String word: keywords)
        {
            if (line.contains(word.toUpperCase())){
//               Log.d("Found", word);
                System.out.println("WORD: " + word);
                int ind = line.indexOf(word);
                System.out.println("ind: " + ind);
//                Log.d("Found", "line.charAt(ind+1): " + line.charAt(ind + word.length()+2));
//                Log.d("Found", "word.length(): " + ind + " "  + (word.length()+2));
                System.out.println("FOUND: line.charAt(ind + word.length()+1)" + line.charAt(ind + word.length()+1)); 
//               System.out.println("FOUND: word.length():" + ind + " "  + (word.length()+2)); 

                String value = abc(line, ind + word.length()+1);
//                   Log.d("Found", "value: " + value);
//                   Log.d("Found", word +" = "+ value);
                System.out.println("FOUND: value: " + value);
//                   System.out.println("FOUND: " + word +" = "+ value);
                String[] wv = {word, value};
                System.out.println("String[] wv = " + wv);
                return wv;
               
//               if( line.charAt(ind + word.length()+1) == '1') {
//                   
//               }
//                System.out.println("LIILILI: \n" + line);
//                return line;
            }
        }
        return null;
    }

    private static void temp(){
        String temp = "Desc\tQty\tPrice\nsample\t12\t1200";
        String random = "CHASE\n" +
                "S' MPTON\n" +
                "60 MAIN ST\n" +
                "ATM NUMBER\n" +
                "NY3181\n" +
                "DATE:\n" +
                "08/07/11\n" +
                "CARD NUMBER: ******* ****1453\n" +
                "TIME:\n" +
                "16:23\n" +
                "SEQUENCE NUMBER: 2334\n" +
                "WITHDRAWAL FROM\n" +
                "ACCOUNT ENDING WITH: XXXXXXXXXXx6817\n" +
                "CHECKING\n" +
                "AMOUNT\n" +
                "AVAILAßLE BALANCE:\n" +
                "PRESENT BALANCE:\n" +
                "$500.000\n" +
                "$329,174.91\n" +
                "$329,174.91";
//        Log.d("temp,", "/n" + random);
//        System.err.println("temp: \n" + random);
        random = random.replaceAll(":", "");
//        line = random;
        xyz(random);
    }    
}
