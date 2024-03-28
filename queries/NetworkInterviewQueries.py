import db



def getOneByIDAndType(stuNo,type):
    sqlCommand = """SELECT * FROM network_event_participant where participant_id ='%s' and participant_type= %s """ %(stuNo,type)
    return db.DBOperator(sqlCommand);


def insert(stuNo,type,event_id):
    sqlCommand = """insert into network_event_participant  (participant_id,participant_type,event_id)
     values  (%s,%s,%s ) """ %(stuNo,type,event_id)
    return db.DBOperator(sqlCommand);



def get_event():
    sqlCommand = """SELECT event_id, concat(interview_date,' ',time) as interviewDate,location,
                    creator,content FROM speed_network_event order by event_id desc"""
    result = db.DBOperator(sqlCommand)
    return result


def insert_event(date,time,location,creator,content):
    sqlCommand = """insert into speed_network_event  (interview_date
                    ,time,location,
                    creator,content) values  ('%s','%s','%s','%s','%s') """ %(date,time,location,creator,content)
    return db.DBOperator(sqlCommand);

