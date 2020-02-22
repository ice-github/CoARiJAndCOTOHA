# -*- coding:utf-8 -*-
import os
import time
import configparser
import json
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


def CheckUserAttribute(target_text: str, max_text_length: int) -> (Dict[str, float], Dict[str, float], Dict[str, float], Dict[str, float], Dict[str, float],
                                                                   Dict[str, float], Dict[str, float], Dict[str, float], Dict[str, float],
                                                                   Dict[str, float], Dict[str, float], Dict[str, float]):
    # divide long text
    sub_texts = GetDividedSubstring(target_text, max_text_length)

    age: Dict[str, float] = {}
    civilstatus: Dict[str, float] = {}
    earnings: Dict[str, float] = {}
    gender: Dict[str, float] = {}
    habit: Dict[str, float] = {}
    hobby: Dict[str, float] = {}
    kind_of_business: Dict[str, float] = {}
    kind_of_occupation: Dict[str, float] = {}
    location: Dict[str, float] = {}
    moving: Dict[str, float] = {}
    occupation: Dict[str, float] = {}
    position: Dict[str, float] = {}

    # print(company_name + ': {0}(length: {1})'.format(year, len(target_text)))
    for text in sub_texts:
        user_attribute = cotoha_api.userAttribute(text)
        if 'result' not in user_attribute:
            # print('  {0} => {1}(length: {2})'.format(company_name, year, len(text)))
            continue

        if 'age' in user_attribute['result']:
            age_value: str = user_attribute['result']['age']
            if age_value not in age:
                age[age_value] = 0
            age[age_value] += float(len(text)) / len(target_text)

        if 'civilstatus' in user_attribute['result']:
            civilstatus_value: str = user_attribute['result']['civilstatus']
            if civilstatus_value not in civilstatus:
                civilstatus[civilstatus_value] = 0
            civilstatus[civilstatus_value] += float(len(text)) / len(target_text)

        if 'earnings' in user_attribute['result']:
            earnings_value: str = user_attribute['result']['earnings']
            if earnings_value not in earnings:
                earnings[earnings_value] = 0
            earnings[earnings_value] += float(len(text)) / len(target_text)

        if 'gender' in user_attribute['result']:
            gender_value: str = user_attribute['result']['gender']
            if gender_value not in gender:
                gender[gender_value] = 0
            gender[gender_value] += float(len(text)) / len(target_text)

        if 'habit' in user_attribute['result']:
            habit_values: List[str] = user_attribute['result']['habit']
            for habit_value in habit_values:
                if habit_value not in habit:
                    habit[habit_value] = 0
                habit[habit_value] += float(len(text)) / len(target_text)
        if 'hobby' in user_attribute['result']:
            hobby_values: List[str] = user_attribute['result']['hobby']
            for hobby_value in hobby_values:
                if hobby_value not in hobby:
                    hobby[hobby_value] = 0
                hobby[hobby_value] += float(len(text)) / len(target_text)

        if 'kind_of_business' in user_attribute['result']:
            kind_of_business_value: str = user_attribute['result']['kind_of_business']
            if kind_of_business_value not in kind_of_business:
                kind_of_business[kind_of_business_value] = 0
            kind_of_business[kind_of_business_value] += float(len(text)) / len(target_text)

        if 'kind_of_occupation' in user_attribute['result']:
            kind_of_occupation_value: str = user_attribute['result']['kind_of_occupation']
            if kind_of_occupation_value not in kind_of_occupation:
                kind_of_occupation[kind_of_occupation_value] = 0
            kind_of_occupation[kind_of_occupation_value] += float(len(text)) / len(target_text)

        if 'location' in user_attribute['result']:
            location_value: str = user_attribute['result']['location']
            if location_value not in location:
                location[location_value] = 0
            location[location_value] += float(len(text)) / len(target_text)

        if 'moving' in user_attribute['result']:
            moving_values: List[str] = user_attribute['result']['moving']
            for moving_value in moving_values:
                if moving_value not in moving:
                    moving[moving_value] = 0
                moving[moving_value] += float(len(text)) / len(target_text)

        if 'occupation' in user_attribute['result']:
            occupation_value: str = user_attribute['result']['occupation']
            if occupation_value not in occupation:
                occupation[occupation_value] = 0
            occupation[occupation_value] += float(len(text)) / len(target_text)

        if 'position' in user_attribute['result']:
            position_value: str = user_attribute['result']['position']
            if position_value not in position:
                position[position_value] = 0
            position[position_value] += float(len(text)) / len(target_text)

    # result = ''
    # result += ('age: ' + str(sorted(age.items(), key=lambda x: -x[1])) + '\n')
    # result += ('civilstatus: ' + str(sorted(civilstatus.items(), key=lambda x: -x[1])) + '\n')
    # result += ('earnings' + str(sorted(earnings.items(), key=lambda x: -x[1])) + '\n')
    # result += ('gender' + str(sorted(gender.items(), key=lambda x: -x[1])) + '\n')
    # result += ('habit' + str(sorted(habit.items(), key=lambda x: -x[1])) + '\n')
    # result += ('hobby' + str(sorted(hobby.items(), key=lambda x: -x[1])) + '\n')
    # result += ('kind_of_business' + str(sorted(kind_of_business.items(), key=lambda x: -x[1])) + '\n')
    # result += ('kind_of_occupation' + str(sorted(kind_of_occupation.items(), key=lambda x: -x[1])) + '\n')
    # result += ('location' + str(sorted(location.items(), key=lambda x: -x[1])) + '\n')
    # result += ('moving' + str(sorted(moving.items(), key=lambda x: -x[1])) + '\n')
    # result += ('occupation' + str(sorted(occupation.items(), key=lambda x: -x[1])) + '\n')
    # result += ('position' + str(sorted(position.items(), key=lambda x: -x[1])) + '\n')

    return (age, civilstatus, earnings, gender, habit, hobby, kind_of_business, kind_of_occupation, location, moving, occupation, position)


class UserAttribute:
    def __init__(self,
                 age: Dict[str, float], civilstatus: Dict[str, float], earnings: Dict[str, float], gender: Dict[str, float], habit: Dict[str, float],
                 hobby: Dict[str, float], kind_of_business: Dict[str, float], kind_of_occupation: Dict[str, float], location: Dict[str, float],
                 moving: Dict[str, float], occupation: Dict[str, float], position: Dict[str, float]):
        super().__init__()

        self.__age = age
        self.__civilstatus = civilstatus
        self.__earnings = earnings
        self.__gender = gender
        self.__habit = habit
        self.__hobby = hobby
        self.__kind_of_business = kind_of_business
        self.__kind_of_occupation = kind_of_occupation
        self.__location = location
        self.__moving = moving
        self.__occupation = occupation
        self.__position = position

    @staticmethod
    def FromJson(json_data: any, name: str) -> 'UserAttribute':
        if name not in json_data:
            raise Exception('UserAttribute.FromJson()', name + ' isnt in json')

        age = json_data[name]['age']
        civilstatus = json_data[name]['civilstatus']
        earnings = json_data[name]['earnings']
        gender = json_data[name]['gender']
        habit = json_data[name]['habit']
        hobby = json_data[name]['hobby']
        kind_of_business = json_data[name]['kind_of_business']
        kind_of_occupation = json_data[name]['kind_of_occupation']
        location = json_data[name]['location']
        moving = json_data[name]['moving']
        occupation = json_data[name]['occupation']
        position = json_data[name]['position']
        return UserAttribute(age, civilstatus, earnings, gender, habit, hobby, kind_of_business, kind_of_occupation, location, moving, occupation, position)

    @staticmethod
    def SaveJson(json_data: any, file_path: str) -> None:
        json_text = json.dumps(json_data, indent=4, separators=(',', ': '), ensure_ascii=False)
        with open(file_path, mode='w', encoding='UTF-8') as f:
            f.write(json_text)

    def GetJsonAs(self, name: str) -> any:
        json_data = {name: {}}
        json_data[name]['age'] = self.__age
        json_data[name]['civilstatus'] = self.__civilstatus
        json_data[name]['earnings'] = self.__earnings
        json_data[name]['gender'] = self.__gender
        json_data[name]['habit'] = self.__habit
        json_data[name]['hobby'] = self.__hobby
        json_data[name]['kind_of_business'] = self.__kind_of_business
        json_data[name]['kind_of_occupation'] = self.__kind_of_occupation
        json_data[name]['location'] = self.__location
        json_data[name]['moving'] = self.__moving
        json_data[name]['occupation'] = self.__occupation
        json_data[name]['position'] = self.__position

        return json_data

    def GetUserAttributeAge(self) -> str:
        if len(self.age) == 0:
            return ''
        sorted_age = sorted(self.__age.items(), key=lambda x: -x[1])
        return list(sorted_age[0])[0]


class CompanyAnalysis:
    def __init__(self, old_ordinary_income: float, new_ordinary_income: float):
        super().__init__()
        self.ordinary_income_diff = new_ordinary_income - old_ordinary_income

    def GetOrdinaryIncomeDiff(self) -> float:
        return self.ordinary_income_diff


plus_companies: List[CompanyAnalysis] = []
minus_companies: List[CompanyAnalysis] = []

if __name__ == '__main__':

    ua1 = UserAttribute(
        {'30-39歳': 0.37100103199174406, '20-29歳': 0.12396800825593396},
        {'既婚': 0.5058049535603716, '未婚': 0.36661506707946334},
        {'3M-5M': 0.36119711042311664, '-1M': 0.12319401444788441},
        {'男性': 0.7381320949432404},
        {'SMOKING': 0.1385448916408669},
        {'COOKING': 0.8817079463364293, 'MOVIE': 0.7549019607843138, 'INTERNET': 0.7381320949432404,
         'FISHING': 0.628482972136223, 'SPORT': 0.6273219814241486, 'GYM': 0.612358101135191,
         'TRAVEL': 0.3691950464396285, 'TVGAME': 0.36906604747162025, 'STUDY': 0.3618421052631579,
         'CAMERA': 0.26986584107327144, 'TVDRAMA': 0.26986584107327144, 'COLLECTION': 0.26044891640866874,
         'FORTUNE': 0.2465170278637771, 'MUSIC': 0.24587203302373584, 'PAINT': 0.24316305469556243,
         'SHOPPING': 0.23787409700722395, 'GAMBLE': 0.11996904024767802, 'SPORTWATCHING': 0.018962848297213623},
        {},
        {},
        {'関東': 0.12319401444788441, '近畿': 0.11829205366357069},
        {'WALKING': 0.26986584107327144, 'CAR': 0.12332301341589268, 'NO': 0.018962848297213623},
        {'会社員': 0.4931630546955625},
        {}
    )

    cotoha_api = GetCotohaApi()

    years = range(2014, 2018 + 1)

    cir: Dict[int, CompanyInformationRepository] = {}
    data_directory = os.path.join(os.path.dirname(__file__), 'data')
    for year in years:
        cir[year] = CompanyInformationRepository(data_directory, year)

    # codes = TopixCore30.Get()
    codes = Nikkei255.Get()

    counter = 0
    ordinary_diff_incomes: List[float] = []
    all_json = json.loads('{}')

    for code in codes:
        five_digit_code = code * 10  # 本来は銘柄コードは5桁

        infoDict: Dict[int, CompanyInformation] = {}
        for year in years:
            info: CompanyInformation = cir[year].Get(five_digit_code)
            if info is None:
                continue
            infoDict[year] = info

        # const
        MAX_TEXT_LENGTH = 1000
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
        # if len(infoDict[TARGET_YEAR].business_policy_environment_issue_etc_text) == 0:
        #     continue
        # if len(infoDict[TARGET_YEAR - 1].business_policy_environment_issue_etc_text) == 0:
        #     continue
        # if len(infoDict[TARGET_YEAR].business_risks_text) == 0:
        #     continue
        # if len(infoDict[TARGET_YEAR - 1].business_risks_text) == 0:
        #     continue
        if len(infoDict[TARGET_YEAR].business_analysis_of_finance_text) == 0 and len(infoDict[TARGET_YEAR].business_management_analysis_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR - 1].business_analysis_of_finance_text) == 0 and len(infoDict[TARGET_YEAR - 1].business_management_analysis_text) == 0:
            continue

        # if len(infoDict[TARGET_YEAR].business_research_and_development_text) == 0:
        #     continue

        # if infoDict[TARGET_YEAR].net_sales < infoDict[TARGET_YEAR - 1].net_sales:
        #     continue
        # if infoDict[TARGET_YEAR].ordinary_income < infoDict[TARGET_YEAR - 1].ordinary_income:
        #     continue

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

        counter += 1
        # print(result_text)

        ordinary_diff_incomes.append(infoDict[TARGET_YEAR].ordinary_income - infoDict[TARGET_YEAR - 1].ordinary_income)

        user_attribute = CheckUserAttribute(infoDict[TARGET_YEAR - 1].business_management_analysis_text + infoDict[TARGET_YEAR - 1].business_analysis_of_finance_text, MAX_TEXT_LENGTH)

        ua = UserAttribute(*user_attribute)
        all_json.update(ua.GetJsonAs(infoDict[TARGET_YEAR].name))

    # print(ordinary_diff_incomes)
    # print(counter)

    UserAttribute.SaveJson(all_json, 'all_json.json')
