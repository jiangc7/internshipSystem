import db


def insert(project_id, student_id, rank):
    sqlCommand = """INSERT INTO student_project (project_id, student_id, rank) VALUES ('%s', '%s', '%s')""" % (
    project_id, student_id, rank)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id;

def getAll():
    sqlCommand = """SELECT * FROM student_project """
     
    result = db.DBOperator(sqlCommand)
    return result;

def update(project_id, student_id, rank):
    sqlCommand = """UPDATE student_project SET rank= '%s' WHERE project_id = '%s' and student_id = '%s' """ \
                 % (rank, project_id, student_id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(sid,pid):
    projectIds = ','.join(pid)
    sqlCommand = """DELETE FROM student_project sp where sp.student_id= '%s' and sp.project_id in (%s)""" % (sid,projectIds)

    result = db.DBOperator_update(sqlCommand)
    return result;


def batchInsert(id, formDatas):
    sqlCommand = """INSERT INTO student_project (student_id, project_id, `rank`, will) VALUES"""
    for idx, val in enumerate(formDatas):
        sqlCommand += """  ('%s', '%s', '%s', '%s') ,""" % (id, val['pid'],idx,val['will'])
    sqlCommand = sqlCommand[:-1]

    print(sqlCommand)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result



def getAllByStudentIdAndProjectId(student_id,project_id):
    projectIds =','.join(project_id)
    sqlCommand = """SELECT project_id FROM student_project sp where sp.student_id= '%s' and sp.project_id in (%s) """%(student_id,projectIds)

    result = db.DBOperator(sqlCommand)
    return result;


def preferredProject(id):
    sqlCommand = f"""SELECT
                       (sp.rank+1) as 'rank',
                        p.id,
                        p.project_title,
                        CONCAT(u.first_name ,' ',u.last_name ) as 'mentor',
                        p.description,
                        p.number_of_student,
                        pt.type_name,
                        DATE_FORMAT( p.start_date, '%m %d %Y' ) AS start_date,
                        DATE_FORMAT( p.end_date, '%m %d %Y' ) AS end_date,
                        p.remain_number_of_student,
                        co.company_name  
                    FROM 
                        student_project sp 
                        LEFT JOIN project p ON sp.project_id = p.id 
                        INNER JOIN mentor ON p.mentor_id = mentor.mentor_id 
                        LEFT JOIN company co ON co.id = mentor.company_id 
                        LEFT JOIN project_type pt ON pt.type_id = p.project_type 
                        left JOIN user u on mentor.mentor_id = u.user_id 
                    WHERE sp.student_id = {id} 
                    order by sp.rank """
    print(sqlCommand)
    result = db.DBOperator(sqlCommand)
    return result