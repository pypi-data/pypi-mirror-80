#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2Tools.py'
__create_time__ = '2020/9/23 23:14'

import argparse, os, zipfile

def raw_convert(raw: str = None, is_xiaobaiauto2: int = 0, **kwargs) -> str:
    '''
    转换器
    :param raw:
    :param is_xiaobaiauto2:
    :param kwargs:
    :return:
    '''
    _code_top = '#! /usr/bin/env python\n'
    _code_pytest_import = 'try:\n\timport pytest\n' \
                          '\timport requests\n' \
                          '\tfrom re import findall\n' \
                          'except ImportError as e:\n' \
                          '\timport os\n' \
                          '\tos.popen("pip install pytest")\n\n'
    _code_xiaobaiauto2_import = 'try:\n\timport pytest\n' \
                          '\tfrom xiaobaiauto2.xiaobaiauto2 import api_action, PUBLIC_VARS\n' \
                          'except ImportError as e:\n' \
                          '\timport os\n' \
                          '\tos.popen("pip install pytest")\n\n'
    _code_pytest_end = '\r# 脚本使用须知： ' \
                       '\r# pytest -s -v   运行当前目录所有test_*开头的脚本文件' \
                       '\r# pytest -s -v xxx.py 运行指定脚本文件' \
                       '\r# pytest -s -v --html=report.html  运行并将结果记录到HTML报告中' \
                       '\r# pytest其他运行方式参考https://pypi.org/project/xiaobaiauto2或官网说明'
    _code_requests_import = 'try:\n\timport requests\n' \
                            '\tfrom re import findall\n' \
                            'except ImportError as e:\n' \
                            '\timport os\n' \
                            '\tos.popen("pip install requests")\n\n'
    _code = ''
    if raw:
        raw = raw.strip()
        raw_list = raw.split('\n')
        method_list = [i for i, _ in enumerate(raw_list) if ' HTTP/' in _]
        method_list.append(len(raw_list) - 1)
        for i in range(len(method_list) - 1):
            raw_sub_list = raw_list[method_list[i]:method_list[i+1]+1]
            _method = raw_sub_list[0].split(' ')[0]
            _headers = {}
            _headers_end = 0
            raw_header_data_list = raw_sub_list[1:]
            for _, j in enumerate(raw_header_data_list):
                _headers_end = _
                if '' == j:
                    break
                else:
                    _headers[j.split(': ')[0]] = j.split(': ')[1].strip()
            if raw_header_data_list.__len__() > _headers_end+1:
                _data = raw_header_data_list[_headers_end + 1]
            else:
                _data = ''
            _url = raw_sub_list[0].split(' ')[1]
            if '://' not in _url and '443' in _headers.get('Host'):
                _url = 'https://' + _headers.get('Host') + _url
            elif '://' not in _url and '443' not in _headers.get('Host'):
                _url = 'http://' + _headers.get('Host') + _url
            if is_xiaobaiauto2 == 1:
                _code += f'''\
                \r@pytest.mark.run(order={i+1})\
                \rdef test_xiaobai_api_{i+1}():\
                \r\t# 测试前数据准备
                \r\theaders = {_headers}\
                \r\turl = '{_url}' \
                \r\tdata = '{_data}'\
                \r\tresponse = requests.request(method='{_method}', url=url, data=data, headers=headers, verify=False)\
                \r\t# 测试后时间判断/提取
                \r\t# assert response.status_code == 200\
                \r\t# global var_name\
                \r\tif 'application/json' in response.headers['content-type']:\
                \r\t\t# assert '预期结果' == response.json()[路径]\
                \r\t\t# var_name = response.json()[路径]\
                \r\t\tprint(response.json())\
                \r\telse:\
                \r\t\t# assert '预期结果' in response.text\
                \r\t\t# var_name = findall('正则表达式', response.text)[0]\
                \r\t\tprint(response.text)\n\n\
                '''
            elif is_xiaobaiauto2 == 2:
                _code += f'''\
                \r@pytest.mark.run(order={i+1})\
                \rdef test_xiaobai_api_{i+1}():\
                \r\t# 测试前数据准备
                \r\theaders = {_headers}\
                \r\turl = '{_url}' \
                \r\tdata = '{_data}'\
                \r\tapi_action(\
                \r\t\tmethod='{_method}', url=url, data=data, headers=headers, verify=False,\
                \r\t\tjson_path='code', json_assert=200, contains_assert='结果中包含的字符串',\
                \r\t\t_re='正则表达式', _re_var='保存被提取值的变量名')\n\n\
                '''
            else:
                _code += f'''\
                \r# 测试前数据准备
                \rheaders = {_headers}\
                \rurl = '{_url}' \
                \rdata = '{_data}'\
                \rresponse = requests.request(method='{_method}',url=url,data=data,headers=headers,verify=False)\
                \r# 测试后数据判断/提取
                \r# assert response.status_code == 200\
                \rif 'application/json' in response.headers['content-type']:\
                \r\t# assert '预期结果' == response.json()[路径]\
                \r\t# var_name = response.json()[路径]\
                \r\tprint(response.json())\
                \relse:\
                \r\t# assert '预期结果' in response.text\
                \r\t# var_name = findall('正则表达式', response.text)[0]\
                \r\tprint(response.text)\n\n\
                '''
    if is_xiaobaiauto2 == 1:
        return _code_top + _code_pytest_import + _code + _code_pytest_end
    elif is_xiaobaiauto2 == 2:
        return _code_top + _code_xiaobaiauto2_import + _code + \
               '\n# 使用公共变量的格式：\n# PUBLIC_VARS["变量名"][0][0]  获取响应头中第一个匹配值' \
               '\n# PUBLIC_VARS["变量名"][1][0]  获取响应体中第一个匹配值' + _code_pytest_end
    else:
        return _code_top + _code_requests_import + _code

def api_raw():
    arg = argparse.ArgumentParser(
        '小白科技·Python代码转换器raw版'
    )
    arg.add_argument('-f', '--file', help='raw数据文件')
    arg.add_argument('-s', '--save', help='要保存的Py文件名*不需要写.py*，默认生成数据文件同名的.py文件')
    arg.add_argument('-x', '--xiaobai',
                     type=int,
                     choices=(0, 1, 2),
                     default=0,
                     help='0：requests库格式，1：pytest库格式，2：xiaobaiauto2库格式，默认为0')
    params = arg.parse_args()
    raw_data = ''
    if params.file and os.path.isfile(params.file):
        if os.path.splitext(params.file)[1] == '.saz':
            raw_file_path = os.path.splitext(params.file)[0]
            zipfile.ZipFile(params.file).extractall(raw_file_path)
            raw_file_list = [i for i in os.listdir(raw_file_path + '/raw') if '_c.txt' == i[-6:]]
            for i in raw_file_list:
                with open(raw_file_path + '/raw/' + i, 'r') as f:
                    raw_data += f.read() + '\n\n\n'
                    f.close()
            if os.path.isdir(raw_file_path):
                try:
                    os.remove(raw_file_path)
                except PermissionError as e:
                    pass
        elif os.path.splitext(params.file)[1] == '.har':
            pass
        else:
            with open(params.file, 'r', encoding='utf-8') as fr:
                raw_data += fr.read()
                fr.close()
        code = raw_convert(raw=raw_data, is_xiaobaiauto2=params.xiaobai)
        if params.save:
            with open(params.save + '.py', 'w', encoding='utf-8') as fw:
                fw.write(code)
                fw.flush()
                fw.close()
        else:
            with open(os.path.splitext(params.file)[0] + '.py', 'w', encoding='utf-8') as fw:
                fw.write(code)
                fw.flush()
                fw.close()
    else:
        exit(0)