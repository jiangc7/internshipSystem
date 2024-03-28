import db





def getOneByStudentNo(stuNo: object) -> object:
    sqlCommand = """SELECT * FROM external_student where student_id_no ='%s'""" %stuNo
    return db.DBOperator(sqlCommand);

