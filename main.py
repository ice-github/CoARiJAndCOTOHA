# -*- coding:utf-8 -*-
import os
import time
import configparser
from typing import Dict, List

from TopixCore30 import TopixCore30
from Nikkei255 import Nikkei255

from CompanyInformation import CompanyInformation
from CompanyInformation import CompanyInformationRepository
from cotoha_api_python3 import CotohaApi


def GetCotohaApi() -> CotohaApi:
    APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/'

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + 'config.ini')
    CLIENT_ID = config.get('COTOHA API', 'Developer Client id')
    CLIENT_SECRET = config.get('COTOHA API', 'Developer Client secret')
    DEVELOPER_API_BASE_URL = config.get('COTOHA API', 'Developer API Base URL')
    ACCESS_TOKEN_PUBLISH_URL = config.get('COTOHA API', 'Access Token Publish URL')

    # COTOHA APIインスタンス生成
    return CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)


def IsInvalid(data):
    return data != data


def GetDividedSubstring(text: str, max_length: int) -> List[str]:
    if len(text) < max_length:
        return [text]

    index = text.rfind('。', 0, max_length)
    if index < 0:
        index = text.rfind('\n\n', 0, max_length)  # try to find double newlines
    if index < 0:
        if len(text) < max_length:
            return [text]
        else:
            index = max_length

    head = text[: index + 1]
    tail = text[index + 1:]
    result: List[str] = [head]
    for text in GetDividedSubstring(tail, max_length):
        result.append(text)
    return result


def CheckSimilarity(target_text1: str, target_text2: str, max_text_length: int) -> float:
    # text division
    sub_texts1 = GetDividedSubstring(target_text1, max_text_length)
    sub_texts2 = GetDividedSubstring(target_text2, max_text_length)

    texts_size = len(sub_texts1)
    if len(sub_texts1) != len(sub_texts2):
        # print('  text division failed')
        texts_size = texts_size if len(sub_texts1) < len(sub_texts2) else len(sub_texts2)

    text_length = len(target_text1) if len(target_text1) > len(target_text2) else len(target_text2)

    total_similarity: float = 0

    for text_index in range(texts_size):
        text1 = sub_texts1[text_index]
        text2 = sub_texts2[text_index]

        similarity = cotoha_api.similarity(text1, text2)
        if 'result' not in similarity:
            continue
        total_similarity += similarity['result']['score'] * float(len(text1)) / text_length
        time.sleep(0.1)

    return total_similarity


def CheckSummary(target_text: str, max_text_length: int) -> str:
    # divide long text
    sub_texts = GetDividedSubstring(target_text, max_text_length)

    summary_result: str = ''
    for text in sub_texts:
        summary = cotoha_api.summary(text, max_text_length / 500)
        if 'result' not in summary:
            continue
        summary_result += summary['result']
        time.sleep(0.1)
    return summary_result


def CheckSentiment(target_text: str, max_text_length: int) -> Dict[str, float]:
    # divide long text
    sub_texts = GetDividedSubstring(target_text, max_text_length)

    sentiments: Dict[str, float] = {}
    for text in sub_texts:
        sentiment = cotoha_api.sentiment(text)
        if 'result' not in sentiment:
            continue

        sentiment_value = sentiment['result']['sentiment']
        sentiment_score = sentiment['result']['score']

        if sentiment_value not in sentiments:
            sentiments[sentiment_value] = 0
        sentiments[sentiment_value] += sentiment_score * float(len(text)) / len(target_text)
        time.sleep(0.1)

    return sentiments


def CheckNe(target_text: str, max_text_length: int) -> List[str]:
    # divide long text
    sub_texts = GetDividedSubstring(target_text, max_text_length)

    words: List[str] = []
    for text in sub_texts:
        ne = cotoha_api.ne(text)
        if 'result' not in ne:
            continue

        for dict_index in range(len(ne['result'])):
            word_class = ne['result'][dict_index]['class']
            if word_class == 'ART' or word_class == 'PSN' or word_class == 'LOC':
                word = ne['result'][dict_index]['form']
                if word not in words:  # Unique
                    words.append(ne['result'][dict_index]['form'])
        time.sleep(0.1)

    return words


if __name__ == '__main__':

    cotoha_api = GetCotohaApi()

    years = range(2014, 2018 + 1)

    cir: Dict[int, CompanyInformationRepository] = {}
    data_directory = os.path.join(os.path.dirname(__file__), 'data')
    for year in years:
        cir[year] = CompanyInformationRepository(data_directory, year)

    # codes = TopixCore30.Get()
    codes = Nikkei255.Get()

    for code in codes:
        five_digit_code = code * 10  # 本来は銘柄コードは5桁

        infoDict: Dict[int, CompanyInformation] = {}
        for year in years:
            info: CompanyInformation = cir[year].Get(five_digit_code)
            if info is None:
                continue
            infoDict[year] = info

        # const
        MAX_TEXT_LENGTH = 2000
        TARGET_YEAR = 2018

        # check items
        if TARGET_YEAR not in infoDict:
            continue
        if TARGET_YEAR - 1 not in infoDict:
            continue
        if IsInvalid(infoDict[TARGET_YEAR].net_sales):
            continue
        if IsInvalid(infoDict[TARGET_YEAR].operating_income):
            continue
        if IsInvalid(infoDict[TARGET_YEAR].ordinary_income):
            continue
        if IsInvalid(infoDict[TARGET_YEAR - 1].net_sales):
            continue
        if IsInvalid(infoDict[TARGET_YEAR - 1].operating_income):
            continue
        if IsInvalid(infoDict[TARGET_YEAR - 1].ordinary_income):
            continue
        if len(infoDict[TARGET_YEAR].business_policy_environment_issue_etc_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR - 1].business_policy_environment_issue_etc_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR].business_risks_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR - 1].business_risks_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR].business_analysis_of_finance_text) == 0 and len(infoDict[TARGET_YEAR].business_management_analysis_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR].business_research_and_development_text) == 0:
            continue

        result_text = '---\n'
        result_text += '### [{0}]\n'.format(infoDict[TARGET_YEAR].name)
        result_text += '総売上　: {0:>7.2f}億円({1}) => {2:>7.2f}億円({3})\n'.format(
            infoDict[TARGET_YEAR - 1].net_sales / 100000000, TARGET_YEAR - 1,
            infoDict[TARGET_YEAR].net_sales / 100000000, TARGET_YEAR)
        result_text += '営業利益: {0:>7.2f}億円({1}) => {2:>7.2f}億円({3}), 営業利益率{4:.2f}%({5}) => {6:.2f}%({7})\n'.format(
            infoDict[TARGET_YEAR - 1].operating_income / 100000000, TARGET_YEAR - 1,
            infoDict[TARGET_YEAR].operating_income / 100000000, TARGET_YEAR,
            infoDict[TARGET_YEAR - 1].operating_income / infoDict[TARGET_YEAR - 1].net_sales * 100, TARGET_YEAR - 1,
            infoDict[TARGET_YEAR].operating_income / infoDict[TARGET_YEAR].net_sales * 100, TARGET_YEAR)
        result_text += '経常利益: {0:>7.2f}億円({1}) => {2:>7.2f}億円({3}), 経常利益率{4:.2f}%({5}) => {6:.2f}%({7})\n\n'.format(
            infoDict[TARGET_YEAR - 1].ordinary_income / 100000000, TARGET_YEAR - 1,
            infoDict[TARGET_YEAR].ordinary_income / 100000000, TARGET_YEAR,
            infoDict[TARGET_YEAR - 1].ordinary_income / infoDict[TARGET_YEAR - 1].net_sales * 100, TARGET_YEAR - 1,
            infoDict[TARGET_YEAR].ordinary_income / infoDict[TARGET_YEAR].net_sales * 100, TARGET_YEAR)

        # 類似度
        business_policy_environment_issue_etc_similarity = CheckSimilarity(
            infoDict[TARGET_YEAR - 1].business_policy_environment_issue_etc_text,
            infoDict[TARGET_YEAR].business_policy_environment_issue_etc_text,
            int(MAX_TEXT_LENGTH / 2))
        business_risks_similarity = CheckSimilarity(
            infoDict[TARGET_YEAR - 1].business_risks_text,
            infoDict[TARGET_YEAR].business_risks_text,
            int(MAX_TEXT_LENGTH / 2))

        # 類似度が低い場合に要約を表示
        if business_policy_environment_issue_etc_similarity < 0.8:
            business_policy_environment_issue_etc = CheckSummary(infoDict[TARGET_YEAR].business_policy_environment_issue_etc_text, MAX_TEXT_LENGTH)
            result_text += '#### 経営方針、経営環境及び対処すべき課題等\n'
            result_text += '<details><summary>要約</summary><div>\n{0}\n</div></details>\n'.format(business_policy_environment_issue_etc)
        if business_risks_similarity < 0.8:
            business_risks = CheckSummary(infoDict[TARGET_YEAR].business_risks_text, MAX_TEXT_LENGTH)
            result_text += '#### 事業等のリスク\n'
            result_text += '<details><summary>## 要約</summary><div>\n{0}\n</div></details>\n'.format(business_risks)

        # 感情分析
        result_text += '#### 財政状態、経営成績及びキャッシュ・フローの状況の分析\n'
        sentiment = CheckSentiment(infoDict[TARGET_YEAR].business_analysis_of_finance_text + infoDict[TARGET_YEAR].business_management_analysis_text, MAX_TEXT_LENGTH)
        sorted_sentiment = sorted(sentiment.items(), key=lambda x: -x[1])

        contradicted = False  # 矛盾判定
        if len(sorted_sentiment) > 0:
            contradicted = infoDict[TARGET_YEAR].operating_income > infoDict[TARGET_YEAR - 1].operating_income
            contradicted = contradicted or infoDict[TARGET_YEAR].operating_income > infoDict[TARGET_YEAR - 1].operating_income
            contradicted = contradicted and list(sorted_sentiment[0])[0] == 'Negative'

        # 営業利益/経常利益が増えているにも関わらずネガティブな場合
        if contradicted:
            original = infoDict[TARGET_YEAR].business_analysis_of_finance_text + infoDict[TARGET_YEAR].business_management_analysis_text
            result_text += '<details><summary>原文</summary><div>\n{0}\n</div></details>\n'.format(original)
        else:
            summary = CheckSummary(infoDict[TARGET_YEAR].business_analysis_of_finance_text + infoDict[TARGET_YEAR].business_management_analysis_text, MAX_TEXT_LENGTH)
            result_text += '<details><summary>要約</summary><div>\n{0}\n</div></details>\n'.format(summary)

        # 固有表現抽出
        result_text += '#### 研究開発活動\n'
        ne = CheckNe(infoDict[TARGET_YEAR].business_research_and_development_text, MAX_TEXT_LENGTH)
        result_text += '<details><summary>キーワード</summary><div>\n{0}\n</div></details>\n'.format(ne)
        summary = CheckSummary(infoDict[TARGET_YEAR].business_research_and_development_text, MAX_TEXT_LENGTH)
        result_text += '<details><summary>要約</summary><div>\n{0}\n</div></details>\n'.format(summary)

        result_text += '---\n'

        # with open('main_result.txt', mode='a', encoding='UTF-8') as f:
        #     f.write(result_text)
        print(result_text)
