# -*- coding:utf-8 -*-
import os
import time
import configparser
import json
from enum import Enum
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

    return (age, civilstatus, earnings, gender, habit, hobby, kind_of_business, kind_of_occupation, location, moving, occupation, position)


class UserAttributeItem(Enum):
    AGE = 'age'
    CIVILSTATUS = 'civilstatus'
    EARNINGS = 'earnings'
    GENDER = 'gender'
    HABIT = 'habit'
    HOBBY = 'hobby'
    KIND_OF_BUSINESS = 'kind_of_business'
    KIND_OF_OCCUPATION = 'kind_of_occupation'
    LOCATION = 'location'
    MOVING = 'moving'
    OCCUPATION = 'occupation'
    POSITION = 'position'


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

    def __GetTopItem(self, dictionary: Dict[str, float]) -> str:
        if len(dictionary) == 0:
            return ''
        sorted_dictionary = sorted(dictionary.items(), key=lambda x: -x[1])
        return list(sorted_dictionary[0])[0]

    def GetUserAttribute(self, user_attribute_item: UserAttributeItem) -> [str]:

        if user_attribute_item == UserAttributeItem.AGE:
            age = self.__GetTopItem(self.__age)
            return [age] if len(age) != 0 else []

        if user_attribute_item == UserAttributeItem.CIVILSTATUS:
            civilstatus = self.__GetTopItem(self.__civilstatus)
            return [civilstatus] if len(civilstatus) != 0 else []

        if user_attribute_item == UserAttributeItem.EARNINGS:
            earnings = self.__GetTopItem(self.__earnings)
            return [earnings] if len(earnings) != 0 else []

        if user_attribute_item == UserAttributeItem.GENDER:
            gender = self.__GetTopItem(self.__gender)
            return [gender] if len(gender) != 0 else []

        if user_attribute_item == UserAttributeItem.HABIT:
            habit = self.__GetTopItem(self.__habit)
            return [habit] if len(habit) != 0 else []

        if user_attribute_item == UserAttributeItem.HOBBY:
            # top 3を選択
            if len(self.__hobby) == 0:
                return []
            sorted_hobby = sorted(self.__hobby.items(), key=lambda x: -x[1])
            sorted_hobby = sorted_hobby[:3]
            result: List[str] = []
            for hobby in sorted_hobby:
                result.append(hobby[0])
            return result

        if user_attribute_item == UserAttributeItem.KIND_OF_BUSINESS:
            kind_of_business = self.__GetTopItem(self.__kind_of_business)
            return [kind_of_business] if len(kind_of_business) != 0 else []

        if user_attribute_item == UserAttributeItem.KIND_OF_OCCUPATION:
            kind_of_occupation = self.__GetTopItem(self.__kind_of_occupation)
            return [kind_of_occupation] if len(kind_of_occupation) != 0 else []

        if user_attribute_item == UserAttributeItem.LOCATION:
            location = self.__GetTopItem(self.__location)
            return [location] if len(location) != 0 else []

        if user_attribute_item == UserAttributeItem.MOVING:
            moving = self.__GetTopItem(self.__moving)
            return [moving] if len(moving) != 0 else []

        if user_attribute_item == UserAttributeItem.OCCUPATION:
            occupation = self.__GetTopItem(self.__occupation)
            return [occupation] if len(occupation) != 0 else []

        if user_attribute_item == UserAttributeItem.POSITION:
            position = self.__GetTopItem(self.__position)
            return [position] if len(position) != 0 else []


class CompanyAnalysis:
    def __init__(self, name: str, year: int,
                 old_net_sales: float, old_operating_income: float, old_ordinary_income: float,
                 net_sales: float, operating_income: float, ordinary_income: float,
                 user_attribute: UserAttribute):
        super().__init__()
        self.name = name
        self.year = year
        self.old_net_sales = old_net_sales
        self.old_operating_income = old_operating_income
        self.old_ordinary_income = old_ordinary_income
        self.net_sales = net_sales
        self.operating_income = operating_income
        self.ordinary_income = ordinary_income
        self.user_attribute = user_attribute
        self.ordinary_income_diff = ordinary_income - old_ordinary_income

    def ShowOverview(self) -> None:
        result_text = '---\n'
        result_text += '### [{0}]\n'.format(self.name)
        result_text += '総売上　: {0:>7.2f}億円({1}) => {2:>7.2f}億円({3})\n'.format(
            self.old_net_sales / 100000000, self.year - 1,
            self.net_sales / 100000000, self.year)
        result_text += '営業利益: {0:>7.2f}億円({1}) => {2:>7.2f}億円({3}), 営業利益率{4:.2f}%({5}) => {6:.2f}%({7})\n'.format(
            self.operating_income / 100000000, self.year - 1,
            self.operating_income / 100000000, self.year,
            self.old_operating_income / self.old_net_sales * 100, self.year - 1,
            self.operating_income / self.net_sales * 100, self.year)
        result_text += '経常利益: {0:>7.2f}億円({1}) => {2:>7.2f}億円({3}), 経常利益率{4:.2f}%({5}) => {6:.2f}%({7})\n\n'.format(
            self.old_ordinary_income / 100000000, self.year - 1,
            self.ordinary_income / 100000000, self.year,
            self.old_ordinary_income / self.old_net_sales * 100, self.year - 1,
            self.ordinary_income / self.net_sales * 100, self.year)
        print(result_text)


def GetDifferences(profittable_companies: List[CompanyAnalysis], unprofittable_companies: List[CompanyAnalysis]):
    # bin-counting
    attribute_items: List[UserAttributeItem] = [
        UserAttributeItem.AGE,
        UserAttributeItem.CIVILSTATUS,
        UserAttributeItem.EARNINGS,
        UserAttributeItem.GENDER,
        UserAttributeItem.HABIT,
        UserAttributeItem.HOBBY,
        UserAttributeItem.KIND_OF_BUSINESS,
        UserAttributeItem.KIND_OF_OCCUPATION,
        UserAttributeItem.LOCATION,
        UserAttributeItem.MOVING,
        UserAttributeItem.OCCUPATION,
        UserAttributeItem.POSITION
    ]

    plus_count: Dict[str, Dict[str, int]] = {}
    minus_count: Dict[str, Dict[str, int]] = {}

    for attribute_item in attribute_items:

        attribute_item_name = attribute_item.value

        for company in profittable_companies:

            if attribute_item_name not in plus_count:
                plus_count[attribute_item_name] = {}

            items = company.user_attribute.GetUserAttribute(attribute_item)

            for item in items:
                if item not in plus_count[attribute_item_name]:
                    plus_count[attribute_item_name][item] = 0
                plus_count[attribute_item_name][item] += 1

        for company in unprofittable_companies:

            if attribute_item_name not in minus_count:
                minus_count[attribute_item_name] = {}

            items = company.user_attribute.GetUserAttribute(attribute_item)

            for item in items:
                if item not in minus_count[attribute_item_name]:
                    minus_count[attribute_item_name][item] = 0
                minus_count[attribute_item_name][item] += 1

    print('Profittable companies: ' + str(len(profittable_companies)))
    print(plus_count)

    print('Unprofitable companies: ' + str(len(unprofittable_companies)))
    print(minus_count)


def CheckFutureOfCompanies():

    print('\nPromising companies for 2019')

    with open('all_json_2018.json', mode='r', encoding='UTF-8') as f:
        json_data_2018 = json.load(f)

    for companyName in json_data_2018:

        try:
            ua2018 = UserAttribute.FromJson(json_data_2018, companyName)
        except Exception:
            continue

        earnings2018 = ua2018.GetUserAttribute(UserAttributeItem.EARNINGS)
        hobby2018 = ua2018.GetUserAttribute(UserAttributeItem.HOBBY)
        location2018 = ua2018.GetUserAttribute(UserAttributeItem.LOCATION)

        flag = False
        if '関東' in location2018:
            if '-1M' in earnings2018 or '1M-3M' in earnings2018:
                if 'FORTUNE' in hobby2018 and 'SPORT' not in hobby2018:
                    flag = True

        if not(flag):
            continue

        print(companyName + ' => ' + str(earnings2018 + hobby2018 + location2018))


if __name__ == '__main__':

    # Mode Flag
    # - Data Save Mode: Save company's user attribute to json file
    # - Data Use Mode:  Use above json file and output the statistics result
    data_save_mode_flag = False

    # check if data save mode
    if data_save_mode_flag:
        companies_json = json.loads('{}')

    # check if data USE mode
    if not data_save_mode_flag:
        with open('all_json_2017.json', mode='r', encoding='UTF-8') as f:
            json_data = json.load(f)
        profittable_companies: List[CompanyAnalysis] = []
        unprofittable_companies: List[CompanyAnalysis] = []

    # Get COTOHA
    cotoha_api = GetCotohaApi()

    # data retrieving
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

        # parameters
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
        if len(infoDict[TARGET_YEAR].business_analysis_of_finance_text) == 0 and len(infoDict[TARGET_YEAR].business_management_analysis_text) == 0:
            continue
        if len(infoDict[TARGET_YEAR - 1].business_analysis_of_finance_text) == 0 and len(infoDict[TARGET_YEAR - 1].business_management_analysis_text) == 0:
            continue

        # save or use
        if data_save_mode_flag:
            user_attribute = CheckUserAttribute(infoDict[TARGET_YEAR - 1].business_management_analysis_text + infoDict[TARGET_YEAR - 1].business_analysis_of_finance_text, MAX_TEXT_LENGTH)
            # user_attribute = CheckUserAttribute(infoDict[TARGET_YEAR].business_management_analysis_text + infoDict[TARGET_YEAR].business_analysis_of_finance_text, MAX_TEXT_LENGTH)
            ua = UserAttribute(*user_attribute)
            companies_json.update(ua.GetJsonAs(infoDict[TARGET_YEAR].name))
        else:
            try:
                ua = UserAttribute.FromJson(json_data, infoDict[TARGET_YEAR].name)
            except Exception:
                continue
            company = CompanyAnalysis(infoDict[TARGET_YEAR].name, TARGET_YEAR,
                                      infoDict[TARGET_YEAR - 1].net_sales, infoDict[TARGET_YEAR - 1].operating_income, infoDict[TARGET_YEAR - 1].ordinary_income,
                                      infoDict[TARGET_YEAR].net_sales, infoDict[TARGET_YEAR].operating_income, infoDict[TARGET_YEAR].ordinary_income, ua)

            earnings = ua.GetUserAttribute(UserAttributeItem.EARNINGS)
            hobby = ua.GetUserAttribute(UserAttributeItem.HOBBY)
            location = ua.GetUserAttribute(UserAttributeItem.LOCATION)

            if company.ordinary_income_diff > 0:
                profittable_companies.append(company)
            else:
                unprofittable_companies.append(company)

            # extra
            # company.ShowOverview()

    if data_save_mode_flag:
        UserAttribute.SaveJson(companies_json, 'all_json.json')
    else:
        GetDifferences(profittable_companies, unprofittable_companies)
        CheckFutureOfCompanies()
