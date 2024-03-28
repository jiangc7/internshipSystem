import db

def addwishlist(project_id, userId):
    sqlCommand = """INSERT INTO wishlist ( project_id, student_id) VALUES ('%s', '%s')""" % (project_id, userId)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result

def removewishlist(project_id, userId):
    sqlCommand = """DELETE FROM wishlist WHERE project_id = '%s' and student_id = '%s'""" % (project_id, userId)
     
    result = db.DBOperator_update(sqlCommand)
    return result

def showwishlist(userId):
    sqlCommand ="""SELECT * FROM (project p join wishlist w on w.project_id =p.id) join student s on w.student_id=s.id where s.id='%s'"""% (userId)

    result = db.DBOperator(sqlCommand)
    return result


def preferredProject(id):
    sqlCommand = """SELECT
                        p.id,
                        p.project_title,
                        CONCAT(u.first_name ,' ',u.last_name ) as mentor,
                        p.description,
                        p.number_of_student,
                        pt.type_name,
                        DATE_FORMAT( p.start_date, '%M %d %Y' ) AS start_date,
                        DATE_FORMAT( p.end_date, '%M %d %Y' ) AS end_date,
                        p.remain_number_of_student,
                        co.company_name 
                        FROM
                        student_project sp
                        LEFT JOIN project p ON sp.project_id = p.id
                        INNER JOIN mentor ON p.mentor_id = mentor.mentor_id
                        LEFT JOIN company co ON co.id = mentor.company_id
                        LEFT JOIN project_type pt ON pt.type_id = p.project_type
                        left JOIN user u on mentor.mentor_id = u.user_id
                        where sp.student_id ='%s' """ % (id)
    result = db.DBOperator(sqlCommand)
    return result