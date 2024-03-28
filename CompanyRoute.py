from flask import Blueprint, make_response, jsonify
from flask import render_template

from StudentRoute import studentRoute, checkStudentProfileAndSurvey
from UserRoute import login_require
from queries import CompanyQueries

companyRoute = Blueprint('companyRoute', __name__)
companyRoute.register_blueprint(studentRoute)



@companyRoute.route('/company/getAll')
@checkStudentProfileAndSurvey
def getAll():
    companys = CompanyQueries.getAll()
    return render_template("company.html", companys=companys)

@companyRoute.route('/company/getAllJson')
def getCompanys():
    companys = CompanyQueries.getAll()
    return make_response(jsonify(companys),200)



@companyRoute.route('/company/addCompany')
def addCompany():
    companys = CompanyQueries.insert("1", "2", "3", "1", "1", "1")
    return render_template("company.html")


@companyRoute.route('/company/delete')
def deleteCompany():
    companys = CompanyQueries.delete(1)
    return render_template("company.html")


@companyRoute.route('/company/update')
def updateCompany():
    companys = CompanyQueries.update(2, "111", "222", "333", "444", 1, "6666")
    return render_template("company.html")
