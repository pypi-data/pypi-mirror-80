import datetime
from dataclasses import dataclass
from typing import Sequence, Optional, Any, List

import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pldata.courses.main import get_courses
from derobertis_cv.pldata.employment_model import EmploymentModel, AcademicEmploymentModel
from derobertis_cv.pltemplates.academic_employment import AcademicEmployment


def get_professional_jobs(excluded_companies: Optional[Sequence[str]] = None,
                          include_private: bool = False) -> List[EmploymentModel]:
    jobs = [
        EmploymentModel(
            [
                r'Rebuilt Allowance for Loan and Lease Losses (ALLL) models, ultimately saving \$5.4 million '
                r'for the bank',
                'Designed and implemented stress testing methodologies'
            ],
            'Eastern Virginia Bankshares',
            'Portfolio Analyst, Portfolio Management',
            'Atlee, VA',
            datetime.datetime(2012, 8, 15),
            datetime.datetime(2013, 8, 15),
        ),
        EmploymentModel(
            [
                'Analyzed financial information obtained from clients to determine strategies for meeting '
                'their financial objectives',
            ],
            'CNC Partners',
            'Managing Partner',
            'Richmond, VA',
            datetime.datetime(2013, 5, 15),
            datetime.datetime(2014, 8, 15),
        ),
        EmploymentModel(
            [
                "Created a regulatory scale which standardizes the largest banks' internal ratings",
            ],
            'Federal Reserve Board of Governors',
            'Credit Risk Intern, Banking Supervision & Regulation',
            'Washington, D.C.',
            datetime.datetime(2011, 5, 15),
            datetime.datetime(2011, 8, 15),
        )
    ]
    if include_private:
        from private_cv.jobs import get_professional_jobs as get_private_jobs
        jobs.extend(get_private_jobs())
    if excluded_companies:
        jobs = [job for job in jobs if job.company_name not in excluded_companies]
    jobs.sort(key=lambda job: job.sort_key, reverse=True)
    return jobs


def get_academic_jobs() -> List[AcademicEmploymentModel]:

    courses = get_courses()
    uf_courses = [course for course in courses if course.university and course.university.title == UF_NAME]
    vcu_courses = [course for course in courses if course.university and course.university.title == VCU_NAME]

    return [
        AcademicEmploymentModel(
            [
                'Conduct full research projects, including project development, data collection, and '
                'analysis',
                'Analyze billions of data points of panel- and time-series data using econometric models '
                'and techniques such as OLS, Logit, Probit, Fama-Macbeth, '
                'ARIMA, vector autoregression, Granger causality, hazard, quantile, '
                'PCA, LDA, EFA, CFA, SEM, difference-in-difference, and propensity score matching',
                'Predict and classify outcomes using machine learning models such as '
                'deep learning (multilayer perceptron), SVM, '
                'K-nearest neighbors, K-means, decision trees, '
                'ridge, LASSO, naive Bayes, and ensemble methods',
                'Collect data using web-scraping, APIs, and databases',
                'Clean, aggregate, and merge data from multiple sources with outliers and errors '
                'at different frequencies and levels of aggregation',
            ],
            UF_NAME,
            'Graduate Assistant',
            'Gainesville, FL',
            begin_date=datetime.datetime(2014, 8, 15),
            end_date=None,
            courses_taught=uf_courses
        ),
        AcademicEmploymentModel(
            [
                'Conduct research and assist professors in teaching class sections and grading assignments'
            ],
            VCU_NAME,
            'Graduate Assistant',
            'Richmond, FL',
            begin_date=datetime.datetime(2013, 9, 1),
            end_date=datetime.datetime(2014, 8, 15),
            courses_taught=vcu_courses
        ),
    ]