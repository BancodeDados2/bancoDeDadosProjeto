import java.io.File;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

import java.util.ArrayList;
import java.util.List;

public class interfaceTeste1 {
    public static void main(String[] args) throws Exception {
        List<String> arqsSelec;
        arqsSelec=new ArrayList<>();
        JFileChooser jFileChooser=new JFileChooser();
        FileNameExtensionFilter filtro= new FileNameExtensionFilter("Apenas .pdf", "pdf");
        jFileChooser.setMultiSelectionEnabled(true);
        jFileChooser.setAcceptAllFileFilterUsed(false);
        jFileChooser.addChoosableFileFilter(filtro);
        int respDoExplorador=jFileChooser.showOpenDialog(null);
        if(respDoExplorador==JFileChooser.APPROVE_OPTION){
            File[] selecaoArray = jFileChooser.getSelectedFiles();
            for (File arq : selecaoArray) {
                arqsSelec.add(arq.getAbsolutePath());
            }
            System.out.println("Arquivos selecionados: " + arqsSelec);
        }else{
            System.out.println("Nenhum arquivo selecionado (anta).");
        }
        

    }
}
