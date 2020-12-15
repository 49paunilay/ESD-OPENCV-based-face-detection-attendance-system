import xlsxwriter as x
import datetime

namelist=[]
timelist=[]
numberoflines=0

with open('attendance.csv','r') as fhand:
    attendancelist=fhand.readlines()

    for lines in attendancelist:
        if ',' not in lines: # Sanity checking
            continue
        numberoflines=numberoflines+1
        n,t=lines.split(',')
        namelist.append(n)
        timelist.append(t)
dt=str(datetime.datetime.now()).split()[0]
nameofSheet="Attendance"+dt
WorkBook=x.Workbook(nameofSheet+".xlsx")
outsheet = WorkBook.add_worksheet()

totalnames = ''.join(namelist)
print(totalnames)

outsheet.write("A1",namelist[0])
outsheet.write("B1",timelist[0])
for i in range(1,numberoflines):
    place="A"+str(i+1)
    place2="B"+str(i+1)
    outsheet.write(place,namelist[i])
    outsheet.write(place2,timelist[i])

WorkBook.close()
print(f'The Attendance sheet name {nameofSheet} is created')

