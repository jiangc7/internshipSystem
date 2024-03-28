import db


def insert(company_name, street, city, region, mentor_id, website):
    sqlCommand = """INSERT INTO company ( company_name, street, city, region, mentor_id, website)
                    VALUES ( '%s', '%s', '%s', '%s', '%s', '%s')""" % (company_name, street, city, region, mentor_id, website)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result

def getAll():
    sqlCommand = """SELECT * FROM company """
     
    result = db.DBOperator(sqlCommand)
    return result

def update(id, company_name, street, city, region, mentor_id, website):
    sqlCommand = """UPDATE company SET company_name = '%s', street = '%s', city = '%s', region = '%s', mentor_id = '%s', website = '%s' WHERE id = '%s'""" \
                 % (company_name, street, city, region, mentor_id, website, id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result


def delete(id):
    sqlCommand = """DELETE FROM company WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result


def getcompany(userid):
    sqlCommand0 = """SELECT company_id FROM mentor where mentor_id='%s' """%userid
    companyid = db.DBOperator(sqlCommand0)[0]['company_id']
    sqlCommand = """SELECT * FROM company where id='%s' """%companyid
     
    result = db.DBOperator(sqlCommand)
    return result