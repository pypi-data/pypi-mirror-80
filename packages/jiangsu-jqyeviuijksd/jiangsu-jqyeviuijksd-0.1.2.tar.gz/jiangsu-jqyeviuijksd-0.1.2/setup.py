# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jiangsu_jqyeviuijksd']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.1.3,<5.0.0',
 'lxml>=4.5.2,<5.0.0',
 'muggle-ocr>=1.0.3,<2.0.0',
 'pathlib2>=2.3.5,<3.0.0',
 'requests>=2.24.0']

entry_points = \
{'console_scripts': ['js-job = jiangsu_jqyeviuijksd.console:main']}

setup_kwargs = {
    'name': 'jiangsu-jqyeviuijksd',
    'version': '0.1.2',
    'description': '可用于江苏就业知识竞赛的自动答题, 主要用于 Python 和 HTTP 的入门',
    'long_description': '# jiangsu-jqyeviuijksd\nhttp://www.91job.org.cn/default/contest 的自动做题工具\n\n仅供 Python 和 HTTP 相关知识的学习交流只用, 勿用于其他途径, 作者不承担任何连带责任\n\n## 直接使用本项目\n1. 正常安装 Python3.7, 由于用到了`tensorflow`只能固定在此版本. \n2. `python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jiangsu-jqyeviuijksd`\n3. `js-job answer-question -u <your-id> -p <your-password> -s <your-school>`\n\n## 如果用于研究\n1. `git clone https://github.com/myuanz/jiangsu-jqyeviuijksd`\n2. `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple poetry`\n3. `poetry install`\n4. `从 console.py 开始读`\n\n--- \n## 其他使用\n\n## 如何获取所有学校前缀?\n在 http://www.91job.org.cn/default/contest 控制台运行以下代码获取\n```javascript\nJSON.stringify($x(\'//ul/li/a\').map(elem => ({\n    [elem.href.split(\'.\')[0].slice(\'http://\'.length)]: elem.text\n})).reduce((acc, item) => Object.assign(acc, item)))\n```\n<details>\n<summary>所有学校前缀</summary>\n\n```JSON\n{\n    "nju": "南京大学",\n    "seu": "东南大学",\n    "nuaa": "南京航空航天大学",\n    "njust": "南京理工大学",\n    "njtech": "南京工业大学",\n    "njupt": "南京邮电大学",\n    "hhu": "河海大学",\n    "njfu": "南京林业大学",\n    "nuist": "南京信息工程大学",\n    "njau": "南京农业大学",\n    "njmu": "南京医科大学",\n    "njucm": "南京中医药大学",\n    "cpu": "中国药科大学",\n    "njnu": "南京师范大学",\n    "njue": "南京财经大学",\n    "jspi": "江苏警官学院",\n    "nipes": "南京体育学院",\n    "nua": "南京艺术学院",\n    "niit": "南京工业职业技术大学",\n    "sju": "三江学院",\n    "njit": "南京工程学院",\n    "nau": "南京审计大学",\n    "njxzc": "南京晓庄学院",\n    "jvic": "江苏经贸职业技术学院",\n    "njty": "南京特殊教育师范学院",\n    "forestpolice": "南京森林警察学院",\n    "juti": "江苏联合职业技术学院",\n    "jmi": "江苏海事职业技术学院",\n    "ytc": "应天职业技术学院",\n    "cxxy": "东南大学成贤学院",\n    "njci": "南京交通职业技术学院",\n    "njpi": "南京科技职业学院",\n    "zdxy": "正德职业技术学院",\n    "zscollege": "钟山职业技术学院",\n    "jku": "金肯职业技术学院",\n    "nty": "南京铁道职业技术学院",\n    "njcit": "南京信息职业技术学院",\n    "jit": "金陵科技学院",\n    "jlxy": "南京大学金陵学院",\n    "zijin": "南京理工大学紫金学院",\n    "nuaajc": "南京航空航天大学金城学院",\n    "cucn": "中国传媒大学南广学院",\n    "njpji": "南京工业大学浦江学院",\n    "njnuzb": "南京师范大学中北学院",\n    "niva": "南京视觉艺术职业学院",\n    "bjxy": "南京信息工程大学滨江学院",\n    "naujsxy": "南京审计大学金审学院",\n    "jscvc": "江苏城市职业学院",\n    "ncc": "南京城市职业学院",\n    "nimt": "南京机电职业技术学院",\n    "nith": "南京旅游职业学院",\n    "jssmu": "江苏卫生健康职业学院",\n    "jsie": "江苏第二师范学院",\n    "jiangnan": "江南大学",\n    "wxit": "无锡职业技术学院",\n    "wxstc": "无锡科技职业学院",\n    "wxic": "无锡商业职业技术学院",\n    "wsoc": "无锡南洋职业技术学院",\n    "jnys": "江南影视艺术职业学院",\n    "jsit": "江苏信息职业技术学院",\n    "jypc": "江阴职业技术学院",\n    "thxy": "无锡太湖学院",\n    "wxcu": "无锡城市职业技术学院",\n    "wxgy": "无锡工艺职业技术学院",\n    "cumt": "中国矿业大学",\n    "xzhmu": "徐州医科大学",\n    "jsnu": "江苏师范大学",\n    "jsjzi": "江苏建筑职业技术学院",\n    "xzit": "徐州工程学院",\n    "jzp": "九州职业技术学院",\n    "xzcit": "徐州工业职业技术学院",\n    "cumtxhc": "中国矿业大学徐海学院",\n    "xznukwxy": "江苏师范大学科文学院",\n    "xzyz": "徐州幼儿师范高等专科学校",\n    "xzsw": "徐州生物工程职业技术学院",\n    "jsvist": "江苏安全技术职业学院",\n    "cczu": "常州大学",\n    "czu": "常州工学院",\n    "jsut": "江苏理工学院",\n    "ccit": "常州信息职业技术学院",\n    "czwyxx": "常州艺术高等职业学校",\n    "cztgi": "常州纺织服装职业技术学院",\n    "czgyxy": "常州工业职业技术学院",\n    "czie": "常州工程职业技术学院",\n    "czjdu": "建东职业技术学院",\n    "czimt": "常州机电职业技术学院",\n    "js-cj": "江苏城乡建设职业学院",\n    "suda": "苏州大学",\n    "usts": "苏州科技大学",\n    "sgmart": "苏州工艺美术职业技术学院",\n    "jssvc": "苏州市职业大学",\n    "szit": "沙洲职业工学院",\n    "usl": "硅湖职业技术学院",\n    "szjm": "苏州经贸职业技术学院",\n    "siit": "苏州工业职业技术学院",\n    "szetop": "苏州托普信息职业技术学院",\n    "szmtc": "苏州卫生职业技术学院",\n    "szai": "苏州农业职业技术学院",\n    "ivt": "苏州工业园区职业技术学院",\n    "wjxvtc": "苏州健雄职业技术学院",\n    "hkuspace": "苏州百年职业学院",\n    "ksdy": "昆山登云科技职业学院",\n    "sdwz": "苏州大学文正学院",\n    "sudatec": "苏州大学应用技术学院",\n    "uststpxy": "苏州科技大学天平学院",\n    "szlg": "江苏科技大学苏州理工学院",\n    "gist": "苏州高博软件技术职业学院",\n    "szitu": "苏州信息职业技术学院",\n    "siso": "苏州工业园区服务外包职业学院",\n    "szys": "苏州幼儿师范高等专科学校",\n    "cslg": "常熟理工学院",\n    "ntu": "南通大学",\n    "jcet": "江苏工程职业技术学院",\n    "ntvu": "南通职业大学",\n    "ntpc": "南通理工学院",\n    "ntst": "南通科技职业学院",\n    "ntsc": "江苏航运职业技术学院",\n    "xlxy": "南通大学杏林学院",\n    "jsbc": "江苏商贸职业学院",\n    "ntnc": "南通师范高等专科学校",\n    "lygtc": "连云港职业技术学院",\n    "lygsf": "连云港师范高等专科学校",\n    "jou": "江苏海洋大学",\n    "njmukdc": "南京医科大学康达学院",\n    "jscfa": "江苏财会职业学院",\n    "hytc": "淮阴师范学院",\n    "hyit": "淮阴工学院",\n    "jsei": "江苏电子信息职业学院",\n    "jsfsc": "江苏食品药品职业技术学院",\n    "jscjxy": "江苏财经职业技术学院",\n    "jshl": "江苏护理职业学院",\n    "ycit": "盐城工学院",\n    "yctu": "盐城师范学院",\n    "jyzx": "明达职业技术学院",\n    "ycmc": "江苏医药职业学院",\n    "yctei": "盐城工业职业技术学院",\n    "yyz": "盐城幼儿师范高等专科学校",\n    "yzu": "扬州大学",\n    "yzpc": "扬州市职业大学",\n    "yzerc": "扬州环境资源职业技术学院",\n    "jhu": "江海职业技术学院",\n    "ypi": "扬州工业职业技术学院",\n    "yzuglxy": "扬州大学广陵学院",\n    "tdxynjupt": "南京邮电大学通达学院",\n    "jstc": "江苏旅游职业学院",\n    "just": "江苏科技大学",\n    "ujs": "江苏大学",\n    "zjc": "镇江市高等专科学校",\n    "jssfjx": "江苏省司法警官高等职业学校",\n    "jsafc": "江苏农林职业技术学院",\n    "jinshan": "金山职业技术学院",\n    "ujsjjxy": "江苏大学京江学院",\n    "nufehs": "南京财经大学红山学院",\n    "jatc": "江苏航空职业技术学院",\n    "tzpc": "泰州职业技术学院",\n    "jsahvc": "江苏农牧科技职业学院",\n    "tzu": "泰州学院",\n    "nustti": "南京理工大学泰州科技学院",\n    "nnutc": "南京师范大学泰州学院",\n    "hlxy": "南京中医药大学翰林学院",\n    "cczuhdc": "常州大学怀德学院",\n    "cjsiu": "宿迁职业技术学院",\n    "sqc": "宿迁学院"\n}\n```\n</details>\n\n\n## 如何获取题目?\n```shell script\n> js-job get-question-and-save --help\n仅供 Python 和 HTTP 相关知识的学习交流只用, 勿用于其他途径, 作者不承担任何连带责任\n\nUsage: js-job get-question-and-save [OPTIONS]\n\n  获取答案并保存, 需特殊条件, 除研究外勿用\n\nOptions:\n  -u TEXT  学号  [required]\n  -p TEXT  密码  [required]\n  -s TEXT  学校名  [required]\n  --help   Show this message and exit.\n```\n## 如何自动登录?\n```shell script\n> js-job get-sess --help\n仅供 Python 和 HTTP 相关知识的学习交流只用, 勿用于其他途径, 作者不承担任何连带责任\n\nUsage: js-job get-sess [OPTIONS]\n\n  使用用户名和密码获取会话, 自动计算验证码\n\nOptions:\n  -u TEXT  学号  [required]\n  -p TEXT  密码  [required]\n  -s TEXT  学校名  [required]\n  --help   Show this message and exit.\n```',
    'author': 'provefar',
    'author_email': 'provefars@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/myuanz/jiangsu-jqyeviuijksd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
