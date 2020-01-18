import requests
from bs4 import BeautifulSoup
import json
import copy
import datetime
import os


def get_module_list():
    response = requests.get("http://python.doc.wonderbits.cn")
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    li = soup.body.ul('li')
    m_list = [m.a.text.split('/')[1] for m in li]
    return m_list


def get_codecells(m_name):
    sample_codecell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": ['']
    }
    sample_mdcell = {
        "cell_type": "markdown",
        "metadata": {
            "CAN_EDIT": "",
            "mfe_cell_key": 10002
        },
        "source": ["<h1>Display</h1>"]
    }

    url = 'http://python.doc.wonderbits.cn/{}.html#'.format(m_name)
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    python_codes = soup.find_all('div', class_='highlight-python notranslate')

    # 加上标题显示
    sample_mdcell['source'] = ["<h1>{}</h1>".format(m_name)]

    cells = [
        sample_mdcell,
    ]
    for c in python_codes:
        sample_codecell['source'] = [c.text]
        # 使用深拷贝，否则只能保存最后一个
        cells.append(copy.deepcopy(sample_codecell))
    return cells


# 读取空白nb
notebook = {
    "cells": [{
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": []
    }],
    "metadata": {
        "cell_last_no": 10001,
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.7.4"
        }
    },
    "nbformat":
    4,
    "nbformat_minor":
    4
}


def auto_gen_nb(mod_name):

    # 在第一个codecell加入更新的时间戳
    notebook['cells'][0]['source'] = [
        '# 更新于{}'.format(datetime.datetime.now())
    ]

    print('更新{}中..'.format(mod_name))
    cells = get_codecells(mod_name)
    print('{}个代码案例,更新完成'.format(len(cells)))
    notebook['cells'] = copy.deepcopy(cells)
    #     print(cells)

    if not os.path.exists('../{}'.format(mod_name)):
        os.mkdir('../{}'.format(mod_name))
    # 写入文件
    with open('../{0}/{0}.ipynb'.format(mod_name), 'w', encoding='utf8') as nb:
        nb.write(json.dumps(notebook))


with open('../sections.wbc2', 'r', encoding='utf8') as f:
    sections_wb2 = json.loads(f.read())

sections_wb2["sections"] = list()
add_content = {
    "name": "更新测试代码",
    "isGroup": False,
    "ext": ".ipynb",
    "path": "",
    "order": 0,
    "desc": ""
}

sections_wb2["sections"].append(add_content.copy())

modules_list = get_module_list()
for module in modules_list:
    auto_gen_nb(module)
    add_content["name"] = module
    add_content["order"] += 1
    #     print(add_content)
    sections_wb2["sections"].append(add_content.copy())

# print(json.dumps(sections_wb2))
with open('../sections.wbc2', 'w', encoding='utf8') as f:
    f.write(json.dumps(sections_wb2))

print('共{}个文件,更新完成，前往测试'.format(len(modules_list)))