from bottle import template
from .rpt_tpl import RptTemplate
import datetime


class CaseCategory:
    Passed = 'case_passed'
    Failed = 'case_failed'
    Executed = 'case_executed'
    UnExecuted = 'case_un_executed'


class ReportSummary:
    _time_start = None
    _time_end = None
    _time_cost = None

    time_start = None
    time_end = None
    time_cost = None
    case_total = 0  # 总数

    case_passed = 0  # 通过
    case_failed = 0  # 失败

    case_executed = 0  # 执行
    case_not_run = 0  # 未执行

    cases_summary = {}

    def __init__(self, step_size):
        self.case_total = step_size
        self.cases_summary = {CaseCategory.Executed: [],
                              CaseCategory.Passed: [],
                              CaseCategory.Failed: [],
                              CaseCategory.UnExecuted: []
                              }
        pass

    def add_case(self, category, detail):
        group = self.cases_summary[category]
        if group is not None:
            group.append(detail)
        self.cases_summary[CaseCategory.Executed].append(detail)
        pass

    def set_start_time(self):
        self._time_start = datetime.datetime.now()

    def set_end_time(self):
        self._time_end = datetime.datetime.now()

    def summary(self):
        self._time_cost = self._time_end - self._time_start

        self.time_start = self._time_start.strftime('%y-%m-%d %I:%M:%S %p')
        self.time_end = self._time_end.strftime('%y-%m-%d %I:%M:%S %p')
        self.time_cost = '{} Seconds'.format(self._time_cost.total_seconds())
        self.case_passed = len(self.cases_summary[CaseCategory.Passed])
        self.case_failed = len(self.cases_summary[CaseCategory.Failed])
        self.case_executed = self.case_passed + self.case_failed
        self.case_not_run = self.case_total - self.case_executed
        return self


class HtmlReport:
    """

    """

    case_summary = None
    detail_titles = None
    report_cases = None
    pie_sum_number = {}

    html_content = ''

    def __init__(self, html_title, pie_theme):
        """
        """
        self.html_title = html_title
        self.pie_theme = pie_theme

    def packagedCases(self, export_label_title, data_key, class_name, pannel_num):
        cases_num = 1
        cases_packaged = ''
        cases_packaged = ''.join([cases_packaged,
                                  '                   <tr class="{}">\n'.format(class_name),
                                  export_label_title,
                                  '                   </tr>\n'])
        for data_case in self.report_cases[data_key]:
            detail_id = ''.join([pannel_num, '-detail-', str(cases_num)])
            hidden_id = ''.join([pannel_num, '-hidden-', str(cases_num)])
            cases_num += 1
            cases_packaged = ''.join([cases_packaged, '                   <tr class="{}">\n'.format(class_name)])
            for data in data_case[:-1]:
                if '详细' == data:
                    cases_packaged = ''.join(
                        [cases_packaged,
                         RptTemplate.report_table_detail.format(detail_id, hidden_id, 'success', detail_id)])
                else:
                    cases_packaged = ''.join([cases_packaged, RptTemplate.report_table_data.format(data)])
            cases_packaged = ''.join([cases_packaged, '                   </tr>\n'])
            cases_packaged = ''.join(
                [cases_packaged, RptTemplate.report_detail_text.format(hidden_id, len(data_case) - 1, data_case[-1])])
        return cases_packaged

    def genHtmlReport(self, html_tpl):
        export_label_title = ''
        summary = self.case_summary
        for tile in self.detail_titles:
            export_label_title = ''.join([export_label_title, RptTemplate.report_title_label.format(tile)])

        str_passed_cases = ''
        str_not_run_cases = ''
        str_failed_cases = ''
        str_executed_cases = ''

        for data_key in self.report_cases.keys():

            if CaseCategory.Passed == data_key:
                str_passed_cases = self.packagedCases(export_label_title, data_key, 'success', 'panel1')
            elif CaseCategory.UnExecuted == data_key:
                str_not_run_cases = self.packagedCases(export_label_title, data_key, 'untreaded', 'panel3')
            elif CaseCategory.Failed == data_key:
                str_failed_cases = self.packagedCases(export_label_title, data_key, 'error', 'panel2')
            else:
                str_executed_cases = self.packagedCases(export_label_title, data_key, 'all', 'panel0')

        export_label_data = RptTemplate.report_Label.format(summary.case_executed, summary.case_passed,
                                                            summary.case_failed,
                                                            summary.case_not_run,
                                                            str(str_executed_cases[0:-1]),
                                                            str(str_passed_cases[0:-1]),
                                                            str(str_failed_cases[0:-1]),
                                                            str(str_not_run_cases[0:-1]))

        html_tpl = ''.join([html_tpl, export_label_data])

        html_content = template(html_tpl,
                                report_title=self.html_title,
                                theme=self.pie_theme,
                                start_time=self.case_summary.time_start,
                                end_time=self.case_summary.time_end,
                                used_time=self.case_summary.time_cost,
                                sum_all_cases=self.case_summary.case_total,
                                sum_executed_cases=self.case_summary.case_executed,
                                sum_untreaded_cases=self.case_summary.case_not_run,
                                right_sum=self.case_summary.case_passed,
                                error_sum=self.case_summary.case_failed,
                                untreated_sum=self.case_summary.case_not_run)
        return html_content

    def set_summary(self, summary):
        self.case_summary = summary
        self.pie_sum_number = {'right_sum': summary.case_passed,
                               'error_sum': summary.case_failed,
                               'untreated_sum': summary.case_not_run}
        return self

    def set_detail_title(self, titles):
        self.detail_titles = titles
        return self

    def set_cases(self, cases):
        self.report_cases = cases
        return self

    def gen_to_file(self, rpt_tpl, filename):
        """
        输出到文件
        :param rpt_tpl: 模板
        :param filename: xxx.html
        :return:
        """

        self.html_content = self.genHtmlReport(rpt_tpl)
        with open(filename, 'wb') as handler:
            handler.write(self.html_content.encode('utf-8'))
        pass
