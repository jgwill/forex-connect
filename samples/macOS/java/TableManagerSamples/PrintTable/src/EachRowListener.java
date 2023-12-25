package printtable;

import java.text.SimpleDateFormat;
import java.util.Calendar;

import com.fxcore2.*;

public class EachRowListener implements IO2GEachRowListener {
    private SimpleDateFormat mDateFormat = new SimpleDateFormat("MM.dd.yyyy HH:mm:ss");
    private String mAccountID;

    public EachRowListener(String sAccountID) {
        mAccountID = sAccountID;
    }

    @Override
    public void onEachRow(String sRowID, O2GRow rowData) {
         if (rowData.getTableType() == O2GTableType.ORDERS ||
             rowData.getTableType() == O2GTableType.TRADES) {

            String accountID = "";
            if (rowData.getTableType() == O2GTableType.ORDERS)
               accountID = ((O2GOrderTableRow)rowData).getAccountID();
            else
               accountID = ((O2GTradeTableRow)rowData).getAccountID();
            int columnsCount = rowData.getColumns().size();
            for (int i = 0; i < columnsCount; i++) {
                if (mAccountID.isEmpty() || mAccountID.equals(accountID)) {
                    System.out.print(rowData.getColumns().get(i).getId() + "=");
                    if (Calendar.class.isAssignableFrom(rowData.getCell(i).getClass())) {
                        System.out.print(mDateFormat.format(((Calendar)rowData.getCell(i)).getTime()));
                    } else {
                        System.out.print(rowData.getCell(i));
                    }
                    System.out.print("; ");
                }
            }
            System.out.println("");
        }
    }
}
