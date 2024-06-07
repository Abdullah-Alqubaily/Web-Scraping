import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import csv


def similar_data(
        timepieces, type_value='', brand_value='Czapek', year_introduced_value='', style_value='', currency_value='CHF',
        made_in_value='Switzerland', case_shape_value='', case_finish_value='', between_lugs_value='',
        lug_to_lug_value='', bezel_material_value='', bezel_color_value='', weight_value='',
        movement_value='', short_description_value=''):
    watch_url_value = timepieces

    image_url_value = (
        dom.xpath('//img[@class="attachment-shop_single size-shop_single wp-post-image"]')[0].attrib)['src']

    case_material_value = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case") or contains(text(), '
        '"Material")]/../../div['
        '2]/ul/li')[0].text.strip()

    caseback_value = '' if not dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case")]/../../div['
        '2]/ul/li[contains(text(), "back")]') else \
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case")]/../../div['
                  '2]/ul/li[contains(text(), "back")]')[0].text.strip()
    print(f'In Def: {timepieces}')
    check_mm = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case")]/../../div['
        '2]/ul/li[contains(text(), "mm")]/text()')
    check_diameter = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case")]/../../div['
        '2]/ul/li[contains(text(), "Diameter")]/text()')

    if check_diameter:
        diameter_value = check_mm[0].split(":")[1].strip()
        diameter_value = re.match(r'\d+.\d+mm|\d+.\d+ mm| \d+.\d+mm| \d+.\d+ mm', diameter_value).group().strip()
        if ' ' in diameter_value:
            diameter_value = diameter_value
        else:
            diameter_value = re.sub(r'(\.\d)', r'\1 ', diameter_value)
    elif check_mm:
        diameter_value = check_mm[0].strip()
        diameter_value = re.match(r'\d+.\d+mm|\d+.\d+ mm| \d+.\d+mm| \d+.\d+ mm', diameter_value).group().strip()
        if ' ' in diameter_value:
            diameter_value = diameter_value
        else:
            diameter_value = re.sub(r'(\.\d)', r'\1 ', diameter_value)
    else:
        diameter_value = ''

    check_thickness = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case")]/../../div['
        '2]/ul/li[contains(text(), "Height")]/text()')
    check_height = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Height")]/../../div['
        '2]/ul/li/text()')
    if check_thickness:
        case_thickness_value = check_thickness[0].split(":")[1].strip()
        if ' ' in case_thickness_value:
            case_thickness_value = case_thickness_value
        else:
            res = re.sub(r'(\.\d)', r'\1 ', case_thickness_value)
            case_thickness_value = res
    elif check_height:
        case_thickness_value = check_height[0].strip()
        if ' ' in case_thickness_value:
            case_thickness_value = case_thickness_value
        else:
            res = re.sub(r'(\.\d)', r'\1 ', case_thickness_value)
            case_thickness_value = res
    else:
        case_thickness_value = ''

    crystal_value = '' if not \
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case") or contains('
                  'text(), "Material")]/../../div['
                  '2]/ul/li[contains(text(), "crystal")]') else \
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case") or contains('
                  'text(), "Material")]/../../div['
                  '2]/ul/li[contains(text(), "crystal")]')[0].text.strip()

    water_resistance_value = '' if not (
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Case")]/../../div['
                  '2]/ul/li[contains(text(), "Water-resistance") or contains(text(), "Water '
                  'resistance") or'
                  'contains('
                  'text(), "Water Resistance")]')) \
        else (dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span['
                        '1][contains(text(), "Case")]/../../div['
                        '2]/ul/li[contains(text(), "Water-resistance") '
                        'or contains(text(), "Water resistance") or'
                        'contains(text(), "Water Resistance")]')[0].text.split(":")[1].strip())
    if water_resistance_value != '':
        if re.match(r'\d+m$|\d+ m$', water_resistance_value):
            water_resistance_value = re.sub(r'(\D)', r' \1', water_resistance_value)

    dial_color_list = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Dial")]/../../div['
        '2]/ul/li/text()')
    if not dial_color_list:
        dial_color_value = ''
    else:
        dial_color_value = listing_items(dial_color_list)

    numerals_value = dial_color_value

    bracelet_material_list = dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), '
                                       '"Bracelet")]/../../div['
                                       '2]/ul/li/text()')
    if not bracelet_material_list:
        bracelet_material_value = ''
    else:
        bracelet_material_value = listing_items(bracelet_material_list)

    bracelet_color_value = bracelet_material_value

    clasp_type_value = bracelet_material_value

    caliber_value = '' if not dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Movement")]/../../div['
        '2]/ul/li') else \
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Movement")]/../../div['
                  '2]/ul/li')[0].text.strip()
    power_reserve_value = '' if not \
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Movement")]/../../div['
                  '2]/ul/li[contains(text(), "Power-reserve:") or contains(text(), "Power-reserve >") or '
                  'contains(text(),"Power reserve")]') else \
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Movement")]/../../div['
                  '2]/ul/li[contains(text(), "Power-reserve:") or contains(text(), "Power-reserve >") or '
                  'contains(text(),"Power reserve")]')[0].text.strip()
    power_reserve_lst = re.split('[>:]', power_reserve_value)
    if power_reserve_lst != [''] and power_reserve_lst:
        power_reserve_value = re.split('[>:]', power_reserve_value)[1].strip()
    else:
        power_reserve_value = power_reserve_value

    frequency_value = '' if not (
        dom.xpath('//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Movement")]/../../div['
                  '2]/ul/li[contains(text(), "Frequency")]')) else \
        dom.xpath('//div[contains(@id, '
                  '"tab-title-")]/div[1]/span[1]['
                  'contains(text(), '
                  '"Movement")]/../../div['
                  '2]/ul/li[contains(text(), '
                  '"Frequency")]')[0].text.split(":")[1].strip()

    jewels_check = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Movement")]/../../div['
        '2]/ul/li[contains(text(), "Jewels")]')
    jewels_value = '' if not jewels_check else jewels_check[0].text.split(":")[1].strip()

    features_list = dom.xpath(
        '//div[contains(@id, "tab-title-")]/div[1]/span[1][contains(text(), "Functions")]/../../div['
        '2]/ul/li/text()')
    if not features_list:
        features_value = ''
    else:
        features_value = listing_items(features_list)

    row = [watch_url_value, type_value, brand_value, year_introduced_value,
           style_value, currency_value, image_url_value, made_in_value,
           case_shape_value, case_material_value,
           case_finish_value,
           caseback_value, diameter_value, between_lugs_value, lug_to_lug_value, case_thickness_value,
           bezel_material_value, bezel_color_value,
           crystal_value,
           water_resistance_value, weight_value, dial_color_value, numerals_value, bracelet_material_value,
           bracelet_color_value, clasp_type_value,
           movement_value, caliber_value, power_reserve_value, frequency_value,
           jewels_value, features_value, short_description_value]
    return row


def listing_items(lst):
    string = ""
    for i in lst:
        string += i.strip() + ","
    return string


def get_ordered_data(
        reference_number,
        parent_model,
        specific_model,
        nickname,
        marketing_name,
        price,
        description):
    watches_data = similar_data(timepiece)
    watches_data.insert(0, reference_number)
    watches_data.insert(5, parent_model)
    watches_data.insert(6, specific_model)
    watches_data.insert(7, nickname)
    watches_data.insert(8, marketing_name)
    watches_data.insert(11, price)
    watches_data.insert(-2, description)

    return watches_data


header = ['reference_number', 'watch_URL', 'type', 'brand',
          'year_introduced', 'parent_model', 'specific_model', 'nickname',
          'marketing_name', 'style', 'currency', 'price',
          'image_URL', 'made_in', 'case_shape', 'case_material', 'case_finish',
          'caseback', 'diameter', 'between_lugs',
          'lug_to_lug', 'case_thickness', 'bezel_material', 'bezel_color', 'crystal',
          'water_resistance', 'weight', 'dial_color',
          'numerals', 'bracelet_material', 'bracelet_color', 'clasp_type',
          'movement', 'caliber', 'power_reserve',
          'frequency', 'jewels', 'features', 'description', 'short_description']
data = []

url = 'https://czapek.com/all-timepieces/'
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
dom = etree.HTML(str(soup))

all_timepieces = dom.xpath('//*[@id="main"]/div/div[2]/ul/li/a/@href')

for timepiece in all_timepieces:
    url = timepiece
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    dom = etree.HTML(str(soup))
    is_limited_edition = None if not dom.xpath('//*[@id="masthead"]/div/header/div[3]/a/text()') \
        else dom.xpath('//*[@id="masthead"]/div/header/div[3]/a/text()')[0]
    if is_limited_edition is None:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        dom = etree.HTML(str(soup))

        reference_number_value = dom.xpath('//*[@class="product_title c-product__title entry-title"]')[0].text.strip()

        check_parent_model = dom.xpath('//*[@id="content"]/nav/div/a[last()]')
        parent_model_value = '' if not check_parent_model else check_parent_model[0].text.strip()

        specific_model_value = '' if not parent_model_value \
            else parent_model_value + " " + dom.xpath('//*[@id="content"]/nav/div/text()')[0].strip()

        product_cat_value = dom.xpath('//*[@id="main"]/div[2]/div/div/section/div[2]/h1[1]')[0].text.strip()
        nickname_value = '' if parent_model_value == product_cat_value else product_cat_value

        marketing_name_value = '' if 'Special Edition' not in parent_model_value else 'Special Edition'
        price_value = '' if not dom.xpath('//*[@id="single-product-price"]/span[2]/span/bdi/text()') else \
            dom.xpath('//*[@id="single-product-price"]/span[2]/span/bdi/text()')[0].strip().replace('’', '')
        description_list = dom.xpath('//*[@id="main"]/div[2]/div/div/section/div[2]/div[1]/text()')[:-1]
        description_value = listing_items(description_list)

        data.append(
            get_ordered_data(
                reference_number=reference_number_value,
                parent_model=parent_model_value,
                specific_model=specific_model_value,
                nickname=nickname_value,
                marketing_name=marketing_name_value,
                price=price_value,
                description=description_value
            )
        )
    else:
        reference_number_value = dom.xpath('//*[@id="info"]/p/text()')[0]

        parent_model_value = (
            dom.xpath('//*[@id="product"]/section/div/div[1]/div/div/section/div[2]/h1[2]/text()')[0].strip())
        specific_model_value = parent_model_value + ' ' + reference_number_value
        nickname_value = ''
        marketing_name_value = '' if 'Special Edition' not in parent_model_value else 'Special Edition'
        price_value = '' if not dom.xpath('//*[@id="prices_and_conditions"]/p[2]/text()') else \
            dom.xpath('//*[@id="prices_and_conditions"]/p[2]/text()')[0]
        price_value = re.findall(r'\d+', price_value.replace('’', ''))[-1].strip()
        description_value = dom.xpath('//*[@id="info"]/div[1]/text()')[0].strip()

        data.append(
            get_ordered_data(
                reference_number=reference_number_value,
                parent_model=parent_model_value,
                specific_model=specific_model_value,
                nickname=nickname_value,
                marketing_name=marketing_name_value,
                price=price_value,
                description=description_value
            )
        )

with open('CzapekImproved.csv', 'w', encoding='UTF-8', newline='\n') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)
