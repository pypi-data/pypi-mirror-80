import json
import logging
import time

from selenium.webdriver import Firefox, Chrome

from .configuration import JobConfig, StepConfig, OperatorConfig
from .operation_executor import OperationExecutor
from .web_rpt import HtmlReport, CaseCategory, RptTemplate, ReportSummary

logger = logging.getLogger(__name__)


class WebJobHandler:
    DebugMod = False

    auto_close = True
    _job_id = None
    _job_name = ''
    _job_size = 0
    _cur_step = None
    _cur_step_info = None

    on_job = None
    on_step = None

    enable_html_rpt = False

    rpt_summary = None

    def __init__(self, data):
        logger.info('init web_job_handler')

        if self.DebugMod:
            logger.info('job config data:\n {}'.format(data))
        job_config = json.loads(data)
        self.job_config = job_config

        browser = self.job_config['browser']
        logger.info('use browser:{}'.format(browser))

        if browser == 'Chrome':
            b = Chrome()
        elif browser == 'Firefox':
            b = Firefox()
        else:
            b = Chrome()
        self.be = OperationExecutor(b)

    def run(self, on_job, on_step):
        logger.info('run steps')
        self.on_job = on_job
        self.on_step = on_step
        if self.job_config is None:
            return None
        self._job_id = self.job_config[JobConfig.Id]
        self._job_name = self.job_config[JobConfig.Name]

        logger.info('job id:{}'.format(self._job_id))
        logger.info('job name:{}'.format(self._job_name))

        try:
            self.run_job(self.job_config)
        except Exception as err:
            self.after_job(err)
            raise err
        self.after_job(None)

    def before_job(self):
        self.rpt_summary = ReportSummary(self._job_size)
        self.rpt_summary.set_start_time()
        pass

    def after_job(self, err):
        self.rpt_summary.set_end_time()
        if self.on_job is not None:
            self.on_job(self._job_id, err)
        pass

    def before_step(self):
        pass

    def after_step(self, exp):
        sid = None
        name = ''
        operation = ''
        parameter = ''
        result = ''
        information = ''
        try:
            step = self._cur_step_info
            sid = step[StepConfig.Id]
            name = step[StepConfig.Name]
            operator = step[StepConfig.Operator]
            operation = operator[OperatorConfig.Category]
            parameter = json.dumps(operator[OperatorConfig.Config])
            if exp is None:
                result = 'Passed'
                information = '-'
            else:
                result = 'Failed'
                information = '{}'.format(exp)
        except Exception as e:
            logger.exception(e)

        step_detail = [sid, name, operation, parameter, result, information]
        if exp is None:
            self.rpt_summary.add_case(CaseCategory.Passed, step_detail)
        else:
            self.rpt_summary.add_case(CaseCategory.Failed, step_detail)
        if self.on_step is not None:
            self.on_step(self._job_id, self._cur_step, exp)
        pass

    def run_job(self, job):
        steps = job[JobConfig.Steps]
        self._job_size = len(steps)
        logger.info('steps size: {}'.format(self._job_size))

        self.before_job()

        try:
            self.run_steps(steps)
        except Exception as err:
            raise err
        finally:
            if self.auto_close:
                self.be.close()
            logger.info('all steps completed')

    def run_steps(self, steps):
        for s in steps:
            time.sleep(1)
            self.be.update_step(s)
            self.run_step(s)

    def run_step(self, step):
        if self.DebugMod:
            print(step)
        try:
            self._cur_step = step[StepConfig.Id]
            self._cur_step_info = step
            self._run_step(step)
        except Exception as exp:
            self.after_step(exp)
            raise exp

        # no exception
        self.after_step(None)

    def _run_step(self, step):
        self.before_step()
        sid = step[StepConfig.Id]
        name = step[StepConfig.Name]
        operator = step[StepConfig.Operator]

        operator_category = operator[OperatorConfig.Category]
        operator_config = operator[OperatorConfig.Config]
        logger.info('run step:{}[{}] operator:{}'.format(sid, name, operator_category))
        if operator_category is not None:
            logger.info(operator_config)
        func = getattr(self.be, operator_category)
        if func is not None:
            func(operator_config)

    def gen_html_rpt(self):
        logger.info('generate html report')
        report_title = '测试报告:{}[{}]'.format(self._job_id, self._job_name)
        theme = u'统计'
        report_file = '{}_report.html'.format(self._job_id)

        rpt_detail_title = ['Step ID', 'Step Name', 'Operation', 'Parameter', 'Result', 'Information']

        smr = self.rpt_summary.summary()

        HtmlReport(report_title, theme).set_summary(
            smr
        ).set_detail_title(rpt_detail_title).set_cases(smr.cases_summary).gen_to_file(
            RptTemplate.html_template,
            report_file)
        pass
