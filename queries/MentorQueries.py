import db


def insert(mentor_id, phone, summary, cid):
    sqlCommand = """INSERT INTO mentor ( mentor_id, phone, summary,company_id)
         VALUES ('%s', '%s', '%s', '%s')""" % (mentor_id, phone, summary, cid)
    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def getAllByStudentIdAndProjectId(student_ids, mentor_id):
    student_ids = ','.join(student_ids)
    sqlCommand = """SELECT student_id FROM mentor_student ms where ms.mentor_id = '%s' and ms.student_id in (%s) """ % (
    mentor_id, student_ids)
    result = db.DBOperator(sqlCommand)
    return result;


def getAll():
    sqlCommand = """
                    SELECT
                        concat(u.first_name," ",u.last_name) as first_name,
                        m.mentor_id as id,
                        u.email as email,
                        m.phone,
                        m.summary,
                        c.company_name
                        
                    FROM
                        mentor m
                        LEFT JOIN company c ON m.company_id = c.id
                        LEFT JOIN user u ON u.user_id = m.mentor_id
                    WHERE
                        u.role =1
                """

    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def update(mentor_id, phone, summary):
    sqlCommand = """UPDATE mentor SET  phone = '%s', summary = '%s' WHERE mentor_id = '%s'""" % (
    phone, summary, mentor_id)

    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def delete(id):
    sqlCommand = """DELETE FROM mentor WHERE mentor_id = '%s'""" % id

    deleteResult = db.DBOperator_update(sqlCommand)
    return deleteResult


def deleteByStudentIds(mentor_id, ids):
    sId= []
    if len(ids.split(',')) >1:
        sId = ",".join(ids)
    else:
        sId= ids
    sqlCommand = """DELETE FROM mentor_student WHERE mentor_id = '%s' and student_id in (%s)""" % (mentor_id, sId)
    deleteResult = db.DBOperator_update(sqlCommand)
    return deleteResult


def updatecompany(company_name, region, city, street, website, companyid):
    sqlCommand = """
        UPDATE company
        SET company_name = '%s', region = '%s',city = '%s', street = '%s',  website = '%s'
        WHERE id = '%s'
        """ % (company_name, region, city, street, website, companyid)
    updateid = db.DBOperator_update(sqlCommand)
    print(updateid)
    return updateid


def getMentorinfo(userid):
    sqlCommand = """ SELECT
                        concat(u.first_name," ",u.last_name) as first_name,
                        u.first_name  as fname,
                        u.last_name as lname,
                        m.mentor_id as id,
                        u.email as email,
                        m.phone,
                        m.summary,
                        c.company_name,
                        m.summary as dsummary,         
                        c.id as company_id            
                        from  mentor m
                        LEFT JOIN company c ON m.company_id = c.id
                        LEFT JOIN user u ON u.user_id = m.mentor_id
                        where u.user_id = %s """ % userid

    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def getMentorListinfo(userIds):
    listUser = ""
    if len(userIds):
        listUser = [str(i) for i in userIds]
        listUser = ",".join(listUser)
    else:
        listUser = userIds
    sqlCommand = """SELECT
                        * 
                    FROM
                        mentor m
                        JOIN user u ON m.mentor_id = u.user_id
                        LEFT JOIN company c ON c.id = m.company_id 
                        LEFT JOIN project p on p.mentor_id = u.user_id
                    WHERE
                        p.id IN (%s) """ % listUser
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def getProjectAll():
    sqlCommand = """SELECT p.id,p.project_title,p.description,
                    p.number_of_student,pt.type_name,  DATE_FORMAT(p.start_date, '%M %d %Y') as start_date,
                    DATE_FORMAT(p.end_date, '%M %d %Y') as end_date,p.remain_number_of_student,co.company_name 
                    FROM
                        project p
                        INNER JOIN mentor ON p.mentor_id = mentor.mentor_id
                        LEFT JOIN company co ON co.id = mentor.company_id
                        LEFT JOIN project_type pt on pt.type_id =p.project_type
                """

    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def batchInsert(id, sidArr):
    sqlCommand = """INSERT INTO mentor_student (mentor_id, student_id,project_id,will) VALUES"""
    for val in sidArr:
        sqlCommand += """  ('%s', '%s', '%s', '%s') ,""" % (id, val['sid'], val['pid'], val['will'])
    sqlCommand = sqlCommand[:-1]

    print(sqlCommand)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result
