import win32com.client as win32


class FileConvert:

    xls_dir = 'E:\\ProgramData\\GitHub\\PyLang\\Crawlers\\BuyBook\\static_files\\excels\\xls\\'
    xlsx_dir = 'E:\\ProgramData\\GitHub\\PyLang\\Crawlers\\BuyBook\\static_files\\excels\\xlsx\\'

    def xlstoxlsx(self, file_list):
        """
        转换xls文件为xlsx
        :param file_list: 列表类型的文件名数组
        :return:
        """
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        for f in file_list:
            try:
                wb = excel.Workbooks.Open(f)
                name = f.split('\\')[-1]
                # FileFormat = 51 is for .xlsx extension, FileFormat = 56 is for .xls extension
                wb.SaveAs(self.xlsx_dir + name + "x", FileFormat=51)
                wb.Close()
                print("\n转换xlsx文件为xls成功：" + name + "x")
            except Exception as e:
                print(e)

        excel.Application.Quit()


    def xlsxtoxls(self, file_list):
        """
        转换xlsx文件为xls
        :param file_list: 列表类型的文件名数组
        :return:
        """
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        for f in file_list:
            try:
                wb = excel.Workbooks.Open(f)
                name = f.split('\\')[-1]
                # FileFormat = 51 is for .xlsx extension, FileFormat = 56 is for .xls extension
                wb.SaveAs(self.xls_dir + name[0:-1], FileFormat=56)
                wb.Close()
                print("\n转换xlsx文件为xls成功：" + name[0:-1])
            except Exception as e:
                print(e)

        excel.Application.Quit()
