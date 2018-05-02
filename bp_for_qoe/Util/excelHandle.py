import xlrd
import openpyxl

'''
@Author:xiayifan
@Function:提供excel相关接口功能，包括从excel中获取数据集，向excel写入权值矩阵,从excel读取权值

'''
DataSetPath = './static/1.xlsx'
WidthPath = './static/width.xlsx'
DataSetPathTest = '../static/1.xlsx'



def GetDataSetAndLabelsFormExcel():
    workbook = xlrd.open_workbook(DataSetPathTest)  # 通过xlrd打开excel文件，1.xlsx目前为测试文件
    sheet = workbook.sheet_by_index(0)  # 取excel文件的第一张表
    row = sheet.nrows  # 记录行列数
    casesRaw = []
    labelsRaw = []
    for i in range(row):  # 取每行元素 制作case 与 label
        caseRaw = []
        labelRaw = []
        delayInEx = sheet.row(i)[0].value
        shakeInEx = sheet.row(i)[1].value
        packetInEx = sheet.row(i)[2].value
        bandwidthInEx = sheet.row(i)[3].value
        labelInEx = sheet.row(i)[4].value
        caseRaw.append(delayInEx)
        caseRaw.append(shakeInEx)
        caseRaw.append(packetInEx)
        caseRaw.append(bandwidthInEx)
        casesRaw.append(caseRaw)
        labelRaw.append(labelInEx)
        labelsRaw.append(labelRaw)
    return [casesRaw, labelsRaw]


def GetWidthFromExcel():
    workbook = xlrd.open_workbook(WidthPath)
    sheet = workbook.sheet_by_index(0)
    row = sheet.nrows
    col = sheet.ncols
    mat = []
    for i in range(row):
        hang = []
        for j in range(col):
            hang.append(sheet.row(i)[j])
        mat.append(hang)
    return mat


def InsertWidthToExcel(width):
    workbook = openpyxl.Workbook()
    sheetW = workbook.active
    sheetW.title = 'width'
    for i in range(len(width)):
        for j in range(len(width[0])):
            sheetW.cell(row=i + 1, colum=j + 1, value=width[i][j])
    sheetW.save(WidthPath)
