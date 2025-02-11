from os import environ
number = 4
#number = environ.get("strn")
structname = f"sub{number}"

def file_to_list(filepath:str) -> list:
    "Filepath to list of strings. Exclude empty lines"
    with open(filepath,'r') as file:
        try:
            with open(filepath, 'r') as file:
                column_data = file.readlines()
                # Remove newline characters from each line
                column_data = [line.strip() for line in column_data]
                return column_data
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return []
        except Exception as e:
            print(f"An external error occurred when reading file at {filepath}: {e}")
            return []

def scan_data_to_xlsx(qm_es: list[float], mm_es: list[float], rel_qm_es: list[float], rel_mm_es: list[float], excel_file: str):
    "Function to get .xlsx file of QM/MM scans from 4 lists: QM/MM energies, QM/MM relative energies of format list[float]"
    import pandas as pd
    st_name = 'Scans result'
    scan_data = {"QM": qm_es, "MM": mm_es, "QM_relative": rel_qm_es, "MM_relative": rel_mm_es}
    x_axis = range(0, 10*len(qm_es), 10)
    scan_data_df = pd.DataFrame(data = scan_data, index = x_axis)
    #scan_data_df.to_excel(excel_file, sheet_name = st_name)

    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    scan_data_df.to_excel(writer, sheet_name = st_name)
    chart = writer.book.add_chart({'type': 'line'})
    chart.set_legend({'position': 'bottom'})
    chart.set_title({'name': structname})

    chart.add_series({
    'categories': [st_name, 1, 0, 36, 0],
    'values': [st_name, 1, 3, 36, 3],
    'line': {'color': 'blue'},
    'name': "QMM"
    })
    chart.add_series({
    'categories': [st_name, 1, 0, 36, 0],
    'values': [st_name, 1, 4, 36, 4],
    'line': {'color': 'orange'},
    'name': "MM"
    })

    writer.sheets[st_name].insert_chart('G2', chart)
    writer.close()

if __name__ == "__main__":
    excel_file = 'ff_scan.xlsx'
    qm_es = file_to_list("qm_e.txt")
    mm_es = file_to_list("mm_e.txt")
    
    qm_es = [float(i) for i in qm_es]
    mm_es = [float(i) for i in mm_es]

    if len(qm_es) != len(mm_es):
        raise ValueError("qm_e.txt and mm_e.txt has different amount of energy points")

    rel_qm_es = [(i-qm_es[0])*627.5 for i in qm_es]
    rel_mm_es = [(i-mm_es[0])*627.5 for i in mm_es]

    scan_data_to_xlsx(qm_es, mm_es, rel_qm_es, rel_mm_es, excel_file)

    import openpyxl as op

    wb=op.load_workbook(excel_file)
    sheet = wb["Scans result"]
    from stat_functions import get_analysis_for_ff
    statistics_class = get_analysis_for_ff(rel_qm_es, rel_mm_es)
    sheet["G17"], sheet["H17"] = "mean deviation", statistics_class.mean
    sheet["G18"], sheet["H18"] = "QMM sigma value", statistics_class.sigmas[0]
    sheet["G19"], sheet["H19"] = "MM sigma value", statistics_class.sigmas[1]
    sheet["G20"], sheet["H20"] = "sqrt deviation", statistics_class.sqrt
    sheet["G21"], sheet["H21"] = "correlation", statistics_class.cov
    sheet["G22"], sheet["H22"] = "covariation", statistics_class.corr
    sheet["A1"] = structname
    wb.save(excel_file)
