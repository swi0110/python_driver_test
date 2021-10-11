import CUBRIDdb as cubrid
import Python_driver as pytest
import os

pass_cnt = 0
fail_cnt = 0
tc_path = ""

def find_tc(tc_path):
    tc_list=[]

    exec_shell = os.popen("find " + tc_path + " -name '*.sql'").read()

    for i in range(len(exec_shell.split(".sql"))-1):
        tc_list.append(exec_shell.split(".sql")[i].replace("\n","") + ".sql")

    return tc_list

def diff_answer(tc):
    result = tc.rsplit("/", 1)[0] + "/" + tc.rsplit("/", 1)[1].replace(".sql", ".result")
    answer = tc.replace("/cases/", "/answers/").rsplit("/", 1)[0] + "/" + tc.rsplit("/", 1)[1].replace(".sql", ".answer")

    if os.path.isfile(result):
        diff = os.popen("diff " + result + " " + answer)
        diff_result = diff.read()
        if (diff_result == ""):
            print(tc + " : [OK]")
            return True
        else:
            print(tc + " : [NOK]")
            print("")
            print("")
            return False
    else:
        return False

tc_list = find_tc(tc_path)
tc_list.sort()

conn = cubrid.connect("CUBRID:localhost:33000:testdb:::", "dba", "")

for tc in enumerate(tc_list):
    print("========================================================")
    pytest.PythonDriver.exec_sql_file(conn.cursor(), tc[1])

    if(diff_answer(tc[1])):
        pass_cnt = pass_cnt + 1
    else:
        fail_cnt = fail_cnt + 1

print("pass :", pass_cnt)
print("fail :", fail_cnt)
