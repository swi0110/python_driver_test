#import CUBRIDdb as cubrid
import re
import os
import os.path
import _cubrid

#conn = cubrid.connect('CUBRID:localhost:33000:demodb:::','dba','')
#cur = conn.cursor()

class PythonDriver:

    #def __init__(self):


    def exec_sql_file(cursor, sql_file):
        #result = tc.rsplit("/", 1)[0] + "/" + tc.rsplit("/", 1)[1].replace(".sql", ".result")
        out_file_name = sql_file.rsplit("/", 1)[0] + "/" + sql_file.rsplit("/", 1)[1].replace(".sql", ".result")

        if os.path.isfile(out_file_name):
            os.system("rm " + out_file_name) 

        out_file = open(out_file_name, "w")
        statement = ""

        for line in open(sql_file):
            if re.match(r"--", line):  # ignore sql comment lines
                continue
            if not re.search(r";$", line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                try:
                    error_chk = False;
                    word_1st = statement.split(" ")[0].upper().replace("\n","")
                    out_file.write("===================================================\n")

                    try:
                        #print(statement)
                        cursor.execute(statement)
                    except _cubrid.IntegrityError as e:
                        code, msg = e.args
                        out_file.write("Error:" + str(code).replace(" ","") + "\n")
                        error_chk = True;
                    except ProgrammingError as e:
                        # if query statement error
                        continue


                    if not error_chk:
                        if word_1st == "CREATE":
                            out_file.write("0\n");
                        elif word_1st == "DROP":
                            out_file.write("0\n");
                        elif word_1st == "INSERT":
                            out_file.write("1\n");
                        elif word_1st == "ALTER":
                            out_file.write("0\n");
                        elif word_1st == "SET":
                            out_file.write("0\n");
                        elif word_1st == "RENAME":
                            out_file.write("0\n");
                        elif word_1st == "GRANT":
                            out_file.write("1\n")
                        else:
                            # SELECT
                            column_name = ""
                            for col_name in cursor.description:
                                column_name = column_name + col_name[0] + "    "

                            # print the column name
                            out_file.write(column_name+"\n")

                            rows = cursor.fetchall()
                            for row in rows:
                                out_file.write("    ".join(map(str,row))+"     "+"\n")
                            out_file.write("\n")

                except Exception as e:
                    print("check to query:")
                    print(statement)
                    print("Error msg: \n", e,"\n")
                    print("-----------------------------------------------")
                    print("")

                statement = ""

#exec_sql_file(cur,"test.sql")
