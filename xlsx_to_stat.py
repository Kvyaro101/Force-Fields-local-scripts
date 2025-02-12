xlsx_name = "for_stat_analyse.xlsx"
start1, end1 = "E2", "E37"
start2, end2 = "F2", "F37"

import openpyxl as op

wb=op.load_workbook(xlsx_name)
sheet = wb["S1"]
qm_e = [sheet[start1[0]+str(i)].value for i in range(int(start1[1:]), int(end1[1:])+1)]
mm_e = [sheet[start2[0]+str(i)].value for i in range(int(start2[1:]), int(end2[1:])+1)]

from stat_functions import get_analysis_for_ff
result = get_analysis_for_ff(qm_e, mm_e)
print(sheet["A1"].value)
print(f"calculated for columns: {sheet[start1[0]+str(int(start1[1:])-1)].value}, {sheet[start2[0]+str(int(start2[1:])-1)].value}")
print(f"mean: {result.mean}, RMSD: {result.sqrt}, QMM sigma: {result.sigmas[0]}, MM sigma: {result.sigmas[1]}, cov: {result.cov}, corr: {result.corr}")
output = f"{round(result.mean, 3)}\t{round(result.sqrt, 3)}\t{round(result.sigmas[0],3)}\t{round(result.sigmas[1], 3)}\t{round(result.cov, 3)}\t{round(result.corr, 3)}"

from tkinter import Tk
r = Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(output)
r.update() # now it stays on the clipboard after the window is closed
r.destroy()
