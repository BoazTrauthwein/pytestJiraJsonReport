import json

xray_json_report = {}

def get_test_step_name(_str):
    # "RunTests/Test_4_Math_Calc.py::TestCalc::test_step_add[15-15]"
    _start = _str.rfind("::") + 2
    _end = _str.find("[")
    return _str[_start : _end]


def get_steps_with_markers(tmp_report):
    steps = []
    dic_actual_result = {}
    for test_item in tmp_report['tests']:
        test_step_name = get_test_step_name(test_item["nodeid"])
        if test_step_name not in dic_actual_result:
            dic_actual_result[test_step_name] = "" 
        if test_item['outcome'] == 'passed':
            dic_actual_result[test_step_name] += ""
        elif test_item['outcome'] == 'failed':
            dic_actual_result[test_step_name] += test_item['call']['crash']['message'] + " \n "

    for message in dic_actual_result.values():
        _dict = {}
        if len(message) == 0:
            _dict["status"] = "PASS"
            _dict["actualResult"] = ""
        else:
            _dict["status"] = "FAIL"
            _dict["actualResult"] = message
        steps.append(_dict)

    return steps

def get_steps(tmp_report):
    steps = []
    for test_item in tmp_report['tests']:
        _dict = {}
        if test_item['outcome'] == 'passed':
            _dict["status"] = "PASS"
            _dict["actualResult"] = ""
        elif test_item['outcome'] == 'failed':
            _dict["status"] = "FAIL"
            _dict["actualResult"] = test_item['call']['crash']['message']
        steps.append(_dict)

    return steps

def generate_xray_json_info_section(imported_py_test_module, start_time, end_time):
    xray_json_report["info"] = {}
    xray_json_report["info"]["project"] = imported_py_test_module.project
    xray_json_report["info"]["description"] = imported_py_test_module.description
    xray_json_report["info"]["startDate"] = start_time
    xray_json_report["info"]["finishDate"] = end_time
    xray_json_report["info"]["testPlanKey"] = imported_py_test_module.test_plan_key
    xray_json_report["info"]["testEnvironments"] = imported_py_test_module.test_environment

def generate_xray_json_test_section(imported_py_test_module, json_tmp_path, start_time, end_time):
    xray_json_report["tests"] = []
    tests = {}

    tests["testKey"] = imported_py_test_module.test_key
    tests["start"] = start_time
    tests["finish"] = end_time
    tests["comment"] = imported_py_test_module.comment

    with open(json_tmp_path) as json_file:
        tmp_report = json.load(json_file)
        tests["status"] = "FAIL" if "failed" in tmp_report["summary"] else "PASS"
        tests["steps"] = get_steps_with_markers(tmp_report) if imported_py_test_module.pytest_markers else get_steps(tmp_report)

    xray_json_report["tests"].append(tests)


def generate_jira_xray_json_report(imported_py_test_module, json_tmp_path, json_report_path, start_time, end_time):

    generate_xray_json_info_section(imported_py_test_module, start_time, end_time)
    generate_xray_json_test_section(imported_py_test_module, json_tmp_path, start_time, end_time)

    with open(json_report_path, 'w',) as json_report:
        json.dump(xray_json_report, json_report, indent=4)
    
