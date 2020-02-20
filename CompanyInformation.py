# -*- coding:utf-8 -*-
import os
import pandas as pd


class CompanyInformation:
    def __init__(self, name, year, net_sales, operating_income, ordinary_income, profit,
                 operating_income_on_sales, ordinary_income_on_sales, capital_ratio,
                 business_policy_environment_issue_etc_text, business_risks_text, business_management_analysis_text,
                 business_analysis_of_finance_text, business_overview_of_result_text, business_research_and_development_text):
        super().__init__()

        self.name = name
        self.year = year
        self.net_sales = net_sales
        self.operating_income = operating_income
        self.ordinary_income = ordinary_income
        self.profit = profit
        self.operating_income_on_sales = operating_income_on_sales
        self.ordinary_income_on_sales = ordinary_income_on_sales
        self.capital_ratio = capital_ratio
        self.business_policy_environment_issue_etc_text = business_policy_environment_issue_etc_text
        self.business_risks_text = business_risks_text
        self.business_management_analysis_text = business_management_analysis_text
        self.business_analysis_of_finance_text = business_analysis_of_finance_text
        self.business_overview_of_result_text = business_overview_of_result_text
        self.business_research_and_development_text = business_research_and_development_text


class CompanyInformationRepository:
    def __init__(self, data_directory_path: str, year: int):
        super().__init__()

        # ファイルのロード
        csv_path = os.path.join(data_directory_path, 'interim', str(year),
                                'documents.csv')
        self.csv_document = pd.read_csv(filepath_or_buffer=csv_path,
                                        encoding='UTF-8',
                                        sep='\t',
                                        index_col='sec_code')  # use sec_code as index

        # メンバへ保存
        self.year = year
        self.data_directory_path = data_directory_path

    # 個別のファイルをロード
    def __LoadFromFile(self, path: str) -> str:
        with open(path, mode='r', encoding='UTF-8') as f:
            lines = f.readlines()
        return ''.join(lines)

    def Get(self, five_digit_code: int) -> CompanyInformation:

        if five_digit_code not in self.csv_document.index:
            # print(str(fiveDigitCode) + ': company information not exist')
            return

        items = self.csv_document.loc[five_digit_code]
        items = items if isinstance(items, pd.core.series.Series) else items.iloc[0]

        name = items['filer_name']
        year = items['fiscal_year']
        net_sales = items['net_sales']  # 純売上高
        operating_income = items['operating_income']  # 営業利益
        ordinary_income = items['ordinary_income']  # 経常利益
        profit = items['profit']  # 純利益
        operating_income_on_sales = items['operating_income_on_sales']  # 営業利益率
        ordinary_income_on_sales = items['ordinary_income_on_sales']  # 経常利益率
        capital_ratio = items['capital_ratio']  # 自己資本比率

        prefix = items['doc_id']

        business_policy_environment_issue_etc_path = os.path.join(self.data_directory_path, 'interim', str(self.year), 'docs', prefix + '_business_policy_environment_issue_etc.txt')
        business_risks_path = os.path.join(self.data_directory_path, 'interim', str(self.year), 'docs', prefix + '_business_risks.txt')
        business_management_analysis_path = os.path.join(self.data_directory_path, 'interim', str(self.year), 'docs', prefix + '_business_management_analysis.txt')
        business_analysis_of_finance_path = os.path.join(self.data_directory_path, 'interim', str(self.year), 'docs', prefix + '_business_analysis_of_finance.txt')
        business_overview_of_result_path = os.path.join(self.data_directory_path, 'interim', str(self.year), 'docs', prefix + '_business_overview_of_result.txt')
        business_research_and_development_path = os.path.join(self.data_directory_path, 'interim', str(self.year), 'docs', prefix + '_business_research_and_development.txt')

        try:
            business_policy_environment_issue_etc_text = self.__LoadFromFile(business_policy_environment_issue_etc_path)
            business_risks_text = self.__LoadFromFile(business_risks_path)
            business_management_analysis_text = self.__LoadFromFile(business_management_analysis_path)
            business_analysis_of_finance_text = self.__LoadFromFile(business_analysis_of_finance_path)
            business_overview_of_result_text = self.__LoadFromFile(business_overview_of_result_path)
            business_research_and_development_text = self.__LoadFromFile(business_research_and_development_path)
        except Exception:
            print('could not read file. data directory may be broken: ' + self.data_directory_path)
            return

        return CompanyInformation(
            name,
            year,
            net_sales,
            operating_income,
            ordinary_income,
            profit,
            operating_income_on_sales,
            ordinary_income_on_sales,
            capital_ratio,
            business_policy_environment_issue_etc_text,
            business_risks_text,
            business_management_analysis_text,
            business_analysis_of_finance_text,
            business_overview_of_result_text,
            business_research_and_development_text)
