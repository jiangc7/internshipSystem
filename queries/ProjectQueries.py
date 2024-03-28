import db



def insert(project_title, description, number_of_student, project_type, start_date, end_date, remain_number_of_student,user_id):
    sqlCommand = """INSERT INTO project ( project_title, description, number_of_student, project_type,
                     start_date, end_date, remain_number_of_student,mentor_id) 
                     VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (project_title, description, number_of_student, project_type, start_date, end_date,remain_number_of_student,user_id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def getAll():
    sqlCommand = """SELECT * FROM project order by id DESC """
     
    result = db.DBOperator(sqlCommand)
    return result;

def getProjectAll(ids,compId,mentorId):
    sqlCommand = """SELECT p.id,p.project_title,p.description,
                    GROUP_CONCAT(tas.skill_name) AS skills,
                    p.number_of_student,pt.type_name,  DATE_FORMAT(p.start_date, '%M %d %Y') as start_date,
                    DATE_FORMAT(p.end_date, '%M %d %Y') as end_date,p.remain_number_of_student,co.company_name,
                    mentor.company_id """
    if mentorId:
        sqlCommand += """, CASE
                            WHEN p.mentor_id = %s 
                            THEN
                            '1' 
                            ELSE 
                            '0' 
                        END AS 'if_current_mentor'  """%mentorId
    sqlCommand+= """ FROM
                        project p
                        LEFT JOIN project_skills ps ON ps.project_id = p.id
                        LEFT JOIN techs_and_skills tas ON  tas.id= ps.skill_id
                        LEFT JOIN project_type pt ON pt.type_id = p.project_type 
                        LEFT JOIN mentor ON p.mentor_id = mentor.mentor_id
                        LEFT JOIN company co ON co.id = mentor.company_id """
    if ids:
        sqlCommand += """ where p.id in (%s)""" % ids
    if compId:
        sqlCommand += """ where co.id  = '%s' """ % compId

    sqlCommand += """ GROUP BY	p.id """

    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def getProjectByCoampny(ids):
    sqlCommand = f"""SELECT p.id,p.project_title,p.description,
                    p.number_of_student,pt.type_name,  DATE_FORMAT(p.start_date, '%M %d %Y') as start_date,
                    DATE_FORMAT(p.end_date, '%M %d %Y') as end_date,p.remain_number_of_student,co.company_name 
                    FROM
                        project p
                        INNER JOIN mentor ON p.mentor_id = mentor.mentor_id
                        LEFT JOIN company co ON co.id = mentor.company_id
                        LEFT JOIN project_type pt on pt.type_id =p.project_type
                    where co.id= {ids}"""

    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def update(id, project_title, description, number_of_student, project_type, start_date, end_date,
           remain_number_of_student):
    sqlCommand = """UPDATE project SET project_title = '%s',
                     description = '%s', number_of_student = '%s', project_type = '%s', 
                     start_date = '%s', end_date = '%s', remain_number_of_student = '%s' 
                     WHERE id = '%s'""" % (project_title, description,
                                         number_of_student, project_type, start_date, end_date,
                                         remain_number_of_student, id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def update_num_of_stu(id):
    sqlCommand = """UPDATE project SET remain_number_of_student = remain_number_of_student -1 
                     WHERE id = '%s' and remain_number_of_student >0 """ % ( id)

    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(id):
    sqlCommand = """DELETE FROM project WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result;

def getAlltype():
    sqlCommand = """
                    SELECT
                        *
                    FROM
                        project_type
                   """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def getProjectinfo(pid):
    sqlCommand = """SELECT * FROM project where id = '%s' """ % pid
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult



def getAllskillJson():
    sqlCommand = """
                    SELECT
                        *
                    FROM
                        techs_and_skills
                   """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult

