import pytest
import os
import sys
import importlib
import Utils.Generate_Reports as gr
import Utils.utils as util

if __name__ == '__main__':

    dir_path = util.create_directory()

    path_RunTests = os.path.join(os.getcwd(), "RunTests")
    sys.path.append(path_RunTests)
    json_tmp_path = os.path.join(dir_path, "tmp.json")

    # Get a list of all py files in RunTests directory to run pytest.
    lst_py_test_modules = [py_file for py_file in os.listdir(path_RunTests) if py_file.endswith(".py")]
    for py_test_module in lst_py_test_modules:
        # Import module from the py file.
        imported_py_test_module = importlib.import_module(py_test_module[:py_test_module.find('.py')])
        # Generate json file paths with names.
        json_report_path = os.path.join(dir_path, "Report_" + py_test_module[:py_test_module.find('.py')] + ".json")
        # Run tests.
        start_time = util.get_xray_iso_time()
        pytest.main(["-v", "--json-report", '--json-report-file=' + json_tmp_path, "--json-report-indent=4", os.path.join(path_RunTests, py_test_module)])
        end_time = util.get_xray_iso_time()
        # Generate report.
        gr.generate_jira_xray_json_report(imported_py_test_module, json_tmp_path, json_report_path, start_time, end_time)
        # os.remove(json_tmp_path) 