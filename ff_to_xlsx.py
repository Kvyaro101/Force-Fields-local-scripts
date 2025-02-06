structname = "Sub4"

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

def scan_data_to_xlsx(qm_es: list[float], mm_es: list[float], rel_qm_es: list[float], rel_mm_es: list[float]):
    "Function to get .xlsx file of QM/MM scans from 4 lists: QM/MM energies, QM/MM relative energies of format list[float]"
    import pandas as pd
    excel_file, st_name = 'ff_scan.xlsx', 'Scans result'
    scan_data = {"QM": qm_es, "MM": mm_es, "QM_relative": rel_qm_es, "MM_relative": rel_mm_es}
    x_axis = range(0, 360, 10)
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
    qm_es = file_to_list("qm_e.txt")
    mm_es = file_to_list("mm_e.txt")
    
    qm_es = [float(i) for i in qm_es]
    mm_es = [float(i) for i in mm_es]

    rel_qm_es = [(i-qm_es[0])*627.5 for i in qm_es]
    rel_mm_es = [(i-mm_es[0])*627.5 for i in mm_es]

    scan_data_to_xlsx(qm_es, mm_es, rel_qm_es, rel_mm_es)
