import db


def getStudentMatch():
    sqlCommand = """SELECT
                        sp.student_id,
                        concat(u.first_name,' ',u.last_name),
                        GROUP_CONCAT( DISTINCT sp.project_id ) project_id,
                        GROUP_CONCAT( DISTINCT p.project_title ) p_title,
                            GROUP_CONCAT(  sp.will  )as will
                    FROM
                        student_project sp
                        LEFT JOIN project p ON sp.project_id = p.id
                        LEFT JOIN user u ON u.user_id = sp.student_id
                        left JOIN student stu ON u.user_id = stu.id
                        where stu.placement_status = 0
                    GROUP BY
                        sp.student_id """
    id = db.DBOperator(sqlCommand)
    return id

def getMentorMatch():
    sqlCommand = """SELECT
                        ms.project_id,
                        GROUP_CONCAT(ms.student_id ) as student_id,
                        GROUP_CONCAT( DISTINCT concat(u.first_name,' ',u.last_name)  )as student,
                        GROUP_CONCAT(  ms.will  )as will
                    FROM
                        mentor_student ms
                        LEFT JOIN user u ON u.user_id = ms.student_id
                        left JOIN student stu ON u.user_id = stu.id and stu.placement_status != 2
                    GROUP BY
                        ms.project_id """
    id = db.DBOperator(sqlCommand)
    return id


def getStudentMatchList(user_id):
    sqlCommand = """SELECT
                    p.id,
                    p.project_title,
                    type_name,
                    description,
                    CONCAT(u.first_name," ",u.last_name ) as mentor,
                    u.email,
                    com.company_name,
                    com.website,
                    CASE 
                        WHEN intv.interview_status is null THEN
                            "Matched"
                        WHEN intv.interview_status = 0 THEN 
                            "Interviewing"
                         WHEN intv.interview_status = 1 THEN 
                            "Interview Failed"
                         WHEN intv.interview_status = 2 THEN 
                        "Interview Passed" 
                        WHEN intv.interview_status = 3 THEN 
                        "Offer accepted"
                         WHEN intv.interview_status = 4 THEN 
                        "Offer accepted"
                         
                        ELSE
                            intv.interview_status
                    END  as status
                    FROM
                        `match` sp
                        INNER JOIN student stu ON sp.student_id = stu.id 
                        AND stu.placement_status != 2 
                        left JOIN mentor_student ms on ms.student_id = stu.id and ms.project_id = sp.project_id
                        left JOIN `user` u on u.user_id = ms.mentor_id
                        left JOIN project p on p.id = sp.project_id
                        left JOIN mentor m on m.mentor_id = p.mentor_id
                        left JOIN company com on com.id = m.company_id
                        left JOIN project_type tp on tp.type_id = project_type
                        left JOIN interviews intv on intv.project_id = sp.project_id and sp.student_id = intv.student_id
                        where stu.id = %s  and p.remain_number_of_student>0 """ % user_id
    id = db.DBOperator(sqlCommand)
    return id


def getProjectMatchList(mentor):
    sqlCommand = f"""SELECT DISTINCT
                stu.id,
                CONCAT( u.first_name, " ", u.last_name ) AS sNAME,
                GROUP_CONCAT(p.project_title) as project,
                GROUP_CONCAT(p.id) as project_id,
                DATE_FORMAT( stu.dateofbirth, '%M %d %Y' ) AS dateofbirth,
            CASE
                    
                    WHEN stu.preferred_name = "None" 
                    OR stu.preferred_name IS NULL THEN
                        "" ELSE stu.preferred_name 
                        END AS preferred_name,
                    u.email,
                    stu.phone,
                    stu.cv,
                CASE
                        
                        WHEN intv.interview_status IS NULL THEN
                        "Matched" 
                        WHEN intv.interview_status = 0 THEN
                        "Interviewing" 
                        WHEN intv.interview_status = 1 THEN
                        "Interview Failed" 
                        WHEN intv.interview_status = 2 THEN
                        "Interview Passed" 
                        WHEN intv.interview_status = 3 THEN
                        "Offer accepted" 
                        WHEN intv.interview_status = 4 THEN
                        "Offer accepted" ELSE intv.interview_status 
                    END AS status,
                    intv.interview_status AS status_value,
                    intv.id as interview_id
                FROM
                    `match` sp
                    INNER JOIN student stu ON sp.student_id = stu.id 
                    AND (stu.placement_status = 0 or stu.placement_status = 1)
                    INNER JOIN mentor_student ms ON ms.student_id = stu.id 
                    AND ms.project_id = sp.project_id
                    INNER JOIN `user` u ON u.user_id = stu.id
                    INNER JOIN project p ON p.id = sp.project_id
                    LEFT JOIN interviews intv ON intv.project_id = p.id and intv.student_id = stu.id
                WHERE
                    ms.mentor_id ={mentor}
            
                GROUP BY stu.id 
                ORDER BY (CASE WHEN intv.interview_status IS NULL THEN 99 ELSE intv.interview_status END) Desc"""
    id = db.DBOperator(sqlCommand)
    return id



def insert(student_id,project_id):
    sqlCommand = """INSERT into `match` ( student_id,project_id,matched,matched_date) VALUES """
    for val in project_id:
        sqlCommand += """  (%s,%s, 0, NOW()) ,""" % (student_id,val)
    sqlCommand = sqlCommand[:-1]

    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def delete(student_id,project_id):
    for val in project_id:
     sqlCommand = """delete from `match` where student_id = %s and project_id  =%s """ % (student_id,val)
     db.DBOperatorInsertedId(sqlCommand)

