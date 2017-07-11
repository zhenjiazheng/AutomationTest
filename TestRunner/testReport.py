import time
import os
from Config import config


class TestReport(object):
    platform = config.platf  # os.environ.get('platform', 'api')
    folder = config.folder  # os.environ.get('projectCaseFolder', "Cases\\API\\POS\\11")
    if "/" in folder:
        folder = folder.replace("/", "_")
    if "\\" in folder:
        folder = folder.replace("\\", "_")
    else:
        pass
    # print(folder)
    if ";" in folder:
        # print(folder.split("; ")[0])
        # print(folder.split("; ")[0].split("_")[-1])
        folder = folder.split(";")[0].replace(folder.split(";")[0].split("_")[-1], "Multiple_Folder")
        # print(folder)

    def __init__(self):
        pass

    @classmethod
    def generate_report(cls, root_dir=None):
        cls.report_conf = cls.make_root_dir(root_dir)
        # print(cls.report_conf)
        report_file = cls.get_report_file(cls.platform + "_" + cls.folder + "_" + cls.get_report_timestamp())
        report_file_full_name = os.path.join(cls.report_conf, report_file)
        return report_file_full_name

    '''
        filename="./TestReport.html"  
        fp=file(filename,'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Report_title',description='Report_description')  
     '''

    @classmethod
    def make_root_dir(cls, root_dir=None):
        cls.report_conf = dict(root_run=os.path.dirname(os.path.abspath(__file__)))

        if not root_dir:
            root_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Report'))

        report_dir = os.path.realpath(os.path.join(root_dir, cls.folder))

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        cls.report_conf = report_dir
        return cls.report_conf

    @classmethod
    def get_report_timestamp(cls):
        return time.strftime("%Y%m%d%H%M")

    @classmethod
    def get_report_format(cls):
        report_format = '%(asctime)s %(levelname)-8s %(message)s'
        return report_format

    @classmethod
    def get_report_file(cls, filename_id):
        report_file = "%s.html" % filename_id
        return report_file

    @classmethod
    def get_report_filename_linux(cls, report_file_fullname):
        return report_file_fullname.replace("\\", "/")

    @classmethod
    def get_log_path(cls):
        cls.root = os.path.curdir
        for root, dirs, files in os.walk(cls.root):
            for each in files:
                if each == "log.txt":
                    path = os.path.join(cls.root, each)
                    return path

# if __name__ == "__main__":
#     a = TestReport
#     print a.get_log_path()
#     report_conf = a.generate_report()
#     print report_conf
#     a = TestReport()
