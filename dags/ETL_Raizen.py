from airflow import DAG
from airflow.operators.python import PythonOperator 
import pandas as pd
import pathlib
import win32api
import win32con
import win32com.client
import pandas as pd
from os.path import join
from datetime import datetime as dt

def processo_ETL():
    def enable_vba():
        key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                    "Software\\Microsoft\\Office\\16.0\\Excel"
                                    + "\\Security", 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, "AccessVBOM", 0, win32con.REG_DWORD, 1)

    def load_databases(indexes:list=[0, 2]) -> DataFrame:
        with open (VBA_FILE_PATH, "r") as f: macro = f.read()
        
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(Filename=EXCEL_FILE_PATH)

        # Insert and run macro
        excelModule = workbook.VBProject.VBComponents.Add(1)
        excelModule.CodeModule.AddFromString(macro)
        excel.Application.Run(MACRO_NAME)

        dataframes = []
        for i in indexes:
            sheet = workbook.Sheets(f"PIVOT-TABLE-{i}")
            df = pd.DataFrame(sheet.UsedRange())

            # Using first row as column's names
            df.rename(columns=df.iloc[0], inplace=True)
            df.drop(df.index[0], inplace=True)

            dataframes.append(df)
        df = pd.concat(dataframes)

        # Close without saving
        excel.Workbooks(1).Close(SaveChanges=0)
        excel.Application.Quit()

        return df

    def process_datasets(df:DataFrame) -> DataFrame:
        df = melt_dataset_columns(df)
        df = adjust_dates_columns(df)
        df = ajust_column_names(df)
        return df

    def write_partitioned(df:DataFrame, partitions_path:str, partitions_cols:list) -> DataFrame:
        df.to_parquet(partitions_path,
                    partition_cols=partitions_cols)

    def melt_dataset_columns(df:DataFrame) -> DataFrame:
        columns = list(df.columns)

        values = columns[5:-1]
        ids = columns[:2] + columns[3:5]

        df = df.melt(id_vars=ids, value_vars=values, var_name="MES", value_name="VOLUME")
        return df

    def adjust_dates_columns(df:DataFrame) -> DataFrame:
        # Adjusts year and month columns values
        months = {'Jan': '1', 'Fev': '2', 'Mar': '3', 'Abr': '4',  'Mai': '5',  'Jun': '6',
                'Jul': '7', 'Ago': '8', 'Set': '9', 'Out': '10', 'Nov': '11', 'Dez': '12'}

        df = df.replace({'MES': months})
        df['ANO'] = df['ANO'].astype(int).astype(str)

        # Combines year and month values into one column
        df['year_month'] = pd.to_datetime(df['ANO'] + df['MES'], format='%Y%m').dt.date
        df.drop(columns=['ANO', 'MES'], inplace=True) # Drops original year and month columns

        # Adds column "created_at"
        df['created_at'] = dt.now()

        return df

    def ajust_column_names(df:DataFrame) -> DataFrame:
        # Renames columns
        new_col_names = ['product', 'uf', 'unit', 'volume', 'year_month', 'created_at']
        df.columns = new_col_names

        # Reorders columns
        cols_in_order = ['year_month', 'uf', 'product', 'unit', 'volume', 'created_at']
        df = df.reindex(columns=cols_in_order)

        return df

    def main():
        enable_vba()
        df = load_databases()
        df = process_datasets(df)
        write_partitioned(df, partitions_path='dados_combustiveis/', partitions_cols=['year_month'])

    BASE_PATH = pathlib.Path().resolve()

    EXCEL_FILE_PATH = join(BASE_PATH, 'vendas-combustiveis-m3.xls')
    VBA_FILE_PATH = join(BASE_PATH, 'macro.txt')
    MACRO_NAME = 'ExtractPivotTableData'

    if __name__ == '__main__': main()

with DAG('Teste_ETL_Raízen', start_date = datetime(2022,5,18),
          schedule_interval = '30 * * * *' , catchup = False) as dag:

    processo_ETL = PythonOperator(
        task_id = 'processo_ETL',
        python_callable = processo_ETL        
    )

    