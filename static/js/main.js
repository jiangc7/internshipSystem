jQuery.validator.setDefaults({
    debug: true,
    success: "valid"
});


/**
 *  a function to initial a Datatable by passing
 *      formId:     the pre-required empty <table id="formId" > and with initialed <th>(s)
 *
 *      URL:        the back-end route as datasource to load the data of a datatable
 *
 *      columns:    the columns where each column should be put
 *
 *      flag:       indicate if a set of button is needed or not
 *
 *   checkboxFlag :   indicate if a checkbox is needed in front of each row is needed or not
 *
 *      target:     if button required then target is where the but located in the table.
 *
 *      btns:       an array of object that represent the button name and function to be called on click the button
 *
 **/
function renderDataTable(formId, url, columns, flag, checkboxFlag, target, btns) {
    setTimeout(1000);
    $.ajax({
            url: url,
            type: "get",
            dataType: "JSON",
            success: function (data) {
                var columnDefs = []
                if (flag) {
                    columnDefs.push(
                        {
                            "render": function (data, type, meta, row) {
                                var btn = ""
                                console.log(data)
                                console.log(meta)
                                console.log(type)
                                console.log(row)
                                btns.forEach(button => {
                                    console.log(button.btnName)
                                    if (button.btnName == 'Edit' && meta.if_current_mentor != '1') {
                                        btn += "<input type='button' onclick='" + button['func'] + "(" + (meta.id) + ")' class='hide' value='" + button['btnName'] + "'> "
                                    }
                                    else if (button.btnName == 'Skills' && meta.if_current_mentor != '1') {
                                        btn += "<input type='button' onclick='" + button['func'] + "(" + (meta.id) + ")' class='hide' value='" + button['btnName'] + "'> "
                                      }
                                    else if (button.btnName == 'Interview') {
                                        if (meta.status_value == 0) {
                                            btn += "<input type='button' onclick='manageInterview(" + (meta.interview_id) + ")'  value='Update'> "
                                            btn += "<input type='button' onclick='CancelInter(" + (meta.interview_id) + ")'  value='Cancel'> "
                                        } else if (meta.status_value == 1) {
                                            btn += " "
                                        } else if (meta.status_value == 2) {
                                            btn += "<input type='button' onclick='sendOffer(" + (meta.id) + "," + meta.project_id + " ," + meta.interview_id + ")' value='Send Offer'> "
                                        } else if (meta.status_value == 4) {
                                            btn += " "
                                        } else if (meta.status_value == null) {
                                            var myobj = {
                                                "pj": meta.project,
                                                "stu_id": meta.id,
                                                "pid": meta.project_id
                                            }

                                            btn += "<input type='button' data-pj='" + meta.project + "' data-stu_id='" + meta.id + "' data-pid='" + meta.project_id + "'" +
                                                "onclick='" + button['func'] + "( this )' value='" + button['btnName'] + "'> "
                                        } else {
                                            btn += "<input type='button' onclick='" + button['func'] + "(" + (meta.id) + ")' value='" + button['btnName'] + "'> "
                                        }
                                    } else {
                                        btn += "<input type='button' onclick='" + button['func'] + "(" + (meta.id) + ")' value='" + button['btnName'] + "'> "
                                    }


                                })
                                return btn
                            },
                            "targets": target
                        }
                    )
                }
                if (checkboxFlag) {
                    columnDefs.push(
                        {
                            "render": function (data, type, meta, row) {
                                var btn = "<div align='center'><input type=\"checkbox\" name=\"ckb-jobid\" value=" + (meta.id) + "></div>"
                                return btn;
                            },
                            "targets": 0
                        }
                    )
                }
                if ($.fn.dataTable.isDataTable(formId)) {
                    console.log("dataTable1")
                    let dataTable1 = $(formId).dataTable();
                    dataTable1.fnClearTable()
                    dataTable1.fnAddData(data, true)
                } else {
                    $(formId).dataTable({
                        "autoWidth": false,
                        select: {
                            style: 'os',
                            selector: 'td:first-child'
                        },
                        "dataSrc": "",
                        "order": [[0, "desc"]],  // HERE !! ERROR TRIGGER!
                        "lengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]],
                        "data": data,
                        "columns": columns,
                        "columnDefs": columnDefs
                    });
                }
            },
            error: function (xhr, status, error) {

            }
        }
    );
}

$(function () {
    $("#noti").on("click", function (func) {
        allMembers = []
        $.ajax({
            url: "getAllUserByUserType",
            type: "get",
            data: {"role": "2", "to": "messageBox"}
        }).then(function (response) {
            console.log(response);

            let allMem = response.filter(item => {
                return item[10] == 0
            }).reduce((acc, curr) => {
                console.log(curr[10])
                acc[curr[0]] = curr[1] + ' ' + curr[2];
                return acc;
            }, {});
            console.log(typeof allMem)
            var myObject = {"0": "All", ...allMem};

            const sortedArray = Object.entries(myObject).sort();

            // Convert the sorted array back to an object
            const sortedObject = Object.fromEntries(sortedArray);

            // Multiple inputs of different types
            $.MessageBox({
                message: "<b>Notifications</b>",
                buttonFail: "Cancel",

                input: {
                    text1: {
                        type: "text",
                        label: "Title:",
                        title: "Input some title",
                        required: 'true'
                    },
                    select1: {
                        type: "select",
                        label: "Receiver:",
                        title: "Select one member or all members",
                        options: sortedObject,
                    },
                    text2: {
                        type: "textarea",
                        label: "Content:",
                        title: "Input some other text",
                        maxlength: 200
                    },

                },

                filterDone: function (data) {
                    if (data['text1'] == '' || data['text1'] === null) return "Please fill the title";
                    if (data['text2'] == '' || data['text2'] === null) return "Please fill the content";
                    if (data['select1'] === "" || data['select1'] === null) return "Please choose at least one member";
                    return $.ajax({
                        url: "addMessage",
                        type: "post",
                        dataType: "JSON",
                        data: data
                    }).then(function (response) {
                        if (response == false) return "some thing wrong happened, could you try again later.";
                        else {
                            if (response.code == "MessageSentCode") {
                                $.MessageBox(response.message)
                            }
                        }
                    });
                },

                top: "auto"
            }).then(function (data) {
            });


        });

    })

    $("#notiList").on("click", function (func) {
        allMembers = []
        $.ajax({
            url: "/getAllMyMsg",
            type: "get",
        }).then(function (response) {
            console.log(response);
            if (response.data.length == 0) {
                return $.MessageBox("you don't have any messages!")
            }
            var table = $("<table>", {
                css: {
                    "width": "520px",
                    "margin-top": "1rem"
                }
            });

            var headerRow = $("<tr>");
            $("<th>").text("Title").appendTo(headerRow);
            $("<th>").text("Sent Date").appendTo(headerRow);
            headerRow.appendTo(table);

            $.each(response.data, function (index, item) {
                var dataRow = $('<tr onclick=notiDetail(' + item[0] + ')>');
                $("<td>").text(item[3]).appendTo(dataRow);
                $("<td>").text(item[2]).appendTo(dataRow);
                dataRow.appendTo(table);
            });

            table.appendTo("body");
            $.MessageBox({
                message: "Your Message List:",
                input: table
            }).done(function (data) {
                console.log(data);
            });


        }).then(function (data) {
        });
    });
    $('#memberList th.sortable').click(function () {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(compare($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) {
            rows = rows.reverse();
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i]);
        }
    });
    $('#trainerList th.sortable').click(function () {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(compare($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) {
            rows = rows.reverse();
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i]);
        }
    });

    // Compare function for sorting the table
    function compare(index) {
        return function (a, b) {
            var valA = getCellValue(a, index);
            var valB = getCellValue(b, index);
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB);
        }
    }

    // Get the value of a table cell
    function getCellValue(row, index) {
        return $(row).children('td').eq(index).text();
    }

})

function removeMentorStudent(sid) {

    $.confirm({
        theme: 'dark',
        title: 'Remove project',
        content: 'Are you sure to remove this student from your preference？',
        buttons: {
            Confirm: async function () {
                var formData = serializeData("form#mentorForm")
                $.ajax({
                    url: "/studentMentor/remove",
                    type: "POST",
                    dataType: "JSON",
                    data: {sid: sid}
                }).then(data => {
                    if ($.fn.dataTable.isDataTable("#myTablePreStudent")) {
                        let dataTable1 = $("#myTablePreStudent").dataTable();
                        dataTable1.fnClearTable()
                        dataTable1.fnAddData(data, true)
                    }
                })

            },
            cancel: function () {
            }

        }
    })
}

function removePreproject(pid) {

    $.confirm({
        theme: 'dark',
        title: 'Remove project',
        content: 'Are you sure to remove this project from your preference？',
        buttons: {
            Confirm: async function () {
                var formData = serializeData("form#mentorForm")
                $.ajax({
                    url: "/studentProject/remove",
                    type: "GET",
                    dataType: "JSON",
                    data: {pid: pid}
                }).then(data => {
                    if ($.fn.dataTable.isDataTable("#myTableOne")) {
                        let dataTable1 = $("#myTableOne").dataTable();
                        dataTable1.fnClearTable()
                        dataTable1.fnAddData(data, true)
                    }
                })

            },
            cancel: function () {
            }

        }
    })
}

function checkInterview(thisButn) {
    var pj = thisButn.dataset.pj
    var stu_id = thisButn.dataset.stu_id
    var pid = thisButn.dataset.pid
    let pidArray = pid.split(',');
    selection = ""
    for (let i = 0; i < pidArray.length; i++) {
        selection += "<option value='" + pidArray[i] + "'>" + pj.split(',')[i] + "</option>"
    }
    locationselection = "<option value='0'>Online</option><option value='1'>In site</option>"

    $.confirm({
        theme: 'dark',
        title: 'Arrange Interview',
        content: '' +
            '<form id="mentorForm" class="formName">' +
            '<div class="form-group justify-content-center">' +
            '     <input type="text" class="hide" name="stu_id" id="stu_id" value = "' + thisButn.dataset.stu_id + '"><!--required to check for empty-->\n' +
            '   <div class="inputBox">\n' +
            '     <label for="date" style="margin-right: 45px;padding-top: 5px">Date</label>\n' +
            '     <input type="date" name="startdate" id="startdate" min="2023-06-16" required="required"><!--required to check for empty-->\n' +
            '   </div>\n' +
            '   <div class="inputBox" style="display: flex;padding-top: 5px">\n' +
            '     <label for="date" style="margin-right: 32px">Project</label>\n' +
            "     <select id='menMatchProject'  name=\"menMatchProject\" class=\"menCompany form-control\">'" + selection + "'</select>" +
            '   </div>\n' +
            '   <div class="inputBox" style="display: flex;padding-top: 5px" >\n' +
            '     <label for="date" style="margin-right: 20px">Location</label>\n' +
            "     <select id='location'  name=\"location\" class=\"menCompany form-control\">'" + locationselection + "'</select>" +
            '   </div>\n' +
            '   <div class="inputBox">\n' +
            '    <label for="starttime" style="margin-right: 63px;padding-top: 5px">At </label>\n' +
            '    <input type="text" id="myTimeInput">\n' +
            '   </div>\n' +
            ' </div>' +
            '</form>'

        ,
        onContentReady: function () {
            $('#myTimeInput').timepicker({
                'step': 30,
                'minTime': '9:00am',
                'maxTime': '5:30pm',
                'beforeShow': function () {
                    // 延迟以等待 timepicker 完全初始化
                    setTimeout(function () {
                        // jQuery UI 时间选择器使用 jQuery UI dialog 组件来展示时间选择器
                        // dialog 的 z-index 值设置在其父元素上
                        $('.ui-timepicker-div').parent().css('z-index', 99999999999999);
                    }, 0);
                }
            });

        },
        buttons: {
            Save: async function () {
                var stu_id = this.$content.find('#stu_id').val();
                var startdate = this.$content.find('#startdate').val();
                var pid = this.$content.find('#menMatchProject').val();
                var starttime = this.$content.find('#myTimeInput').val();
                var location = this.$content.find('#location').val();

                var jsonData = {
                    "stu_id": stu_id,
                    "startdate": startdate,
                    "starttime": starttime,
                    "pid": pid,
                    "location": location
                }
                formId = "#myTableProject"
                $.ajax({
                    url: "/interview/addInterview",
                    type: "post",
                    dataType: "JSON",
                    data: jsonData,
                }).then(result => {
                    if ($.fn.dataTable.isDataTable(formId)) {
                        console.log("dataTable1")
                        console.log(result)
                        let dataTable1 = $(formId).dataTable();
                        dataTable1.fnClearTable()
                        dataTable1.fnAddData(result, true)
                    }
                })

            },
            cancel: function () {
            }


        }
    })


}

function CancelInter(student_id) {
    formId = "#myTableProject"
    $.confirm({
        boxWidth: '30%',
        useBootstrap: false,
        title: "Cancel Interview",
        content: "Are you sure to cancel this interview ?",
        buttons: {
            OK: function () {
                $.ajax({
                    url: "/interview/delete",
                    type: "get",
                    dataType: "JSON",
                    data: {"id": student_id},
                }).then(result => {
                    if ($.fn.dataTable.isDataTable(formId)) {
                        console.log("dataTable1")
                        console.log(result)
                        let dataTable1 = $(formId).dataTable();
                        dataTable1.fnClearTable()
                        dataTable1.fnAddData(result, true)
                    }
                })

            }
        },
    })
}

function editMentor(mId) {
    $.ajax({
        url: "/mentor/getMentorData",
        type: "get",
        data: {"mId": mId}
    }).then(data => {
        console.log(data.email)
        $.confirm({
            theme: 'dark',
            title: 'Edit mentor information',
            content: '' +
                '<form id="mentorForm" class="formName" xmlns="http://www.w3.org/1999/html">' +
                '<div class="form-group">' +
                '<input type="hidden" name="mentorid" value="' + mId + '" />' +
                '<label>Mentor email address</label>' +
                '<input type="text" value = "' + data.email + '" placeholder="John.Doe@gmail.com" id="mentorEmail" name="email" class="email form-control" ' +
                'required onchange="checkEmail(this.value,this.id)" />' +
                '<label>Phone</label>' +
                '<input type="text" name="phone" value="' + data.phone + '" class=" form-control" required />' +
                '<label>Mentor First Name</label>' +
                '<input type="text" placeholder="Jone" value="' + data.fname + '"  name="firstname" class="fname form-control" required />' +
                '<label>Mentor Last Name</label>' +
                '<input type="text" placeholder="Doe" name="lastname" value="' + data.lname + '"  class="lastname form-control" required />' +
                '<label>Summary</label>' +
                '<textarea placeholder="..." name="summary"   class=" form-control" required />' + data.dsummary + '</textarea>' +
                '</div>' +
                '</form>',

            buttons: {
                Update: async function () {
                    var formData = serializeData("form#mentorForm")
                    $.ajax({
                        url: "/mentor/UpdateJson",
                        type: "POST",
                        dataType: "JSON",
                        data: formData,
                    }).then(data => {
                        if ($.fn.dataTable.isDataTable("#myTableOne")) {
                            let dataTable1 = $("#myTableOne").dataTable();
                            dataTable1.fnClearTable()
                            dataTable1.fnAddData(data, true)
                        }
                    })

                },
                cancel: function () {
                }

            }
        })
    })

}

function checkPassword(inp) {
    let pass1 = $("#password").val();
    let pass2 = $("#compassword").val();
    if (pass1 != pass2 && (pass1 != "" && pass2 != "")) {
        $(inp).addClass("error")
    } else {
        $("#password").removeClass("error")
        $("#compassword").removeClass("error")
    }


}

function deleteMentor(mId) {

    $.confirm({
        theme: 'dark',
        title: 'Edit mentor information',
        content: 'Are you sure to delete this Mentor？',
        buttons: {
            Confirm: async function () {
                var formData = serializeData("form#mentorForm")
                $.ajax({
                    url: "/mentor/deleteJson/" + mId,
                    type: "GET",
                    dataType: "JSON",
                }).then(data => {
                    if(data.code!= 'ok'){
                        $.alert(data.message)
                    }
                    else if($.fn.dataTable.isDataTable("#myTableOne")) {
                        let dataTable1 = $("#myTableOne").dataTable();
                        dataTable1.fnClearTable()
                        dataTable1.fnAddData(data, true)
                    }
                })

            },
            cancel: function () {
            }

        }
    })
}

function manageInterview(intv_id) {

    $.confirm({
        theme: 'dark',
        title: 'Manage Interview',
        content: '' +
            '   <div class="inputBox">\n' +
            "  <input type='radio' id='interviewOP1' name='interviewOP' value='2'>" +
            "  <label for='interviewOP1'>Passed</label>" +
            "  <input type='radio' id='interviewOP2' name='interviewOP' value='1'>" +
            "  <label for='interviewOP2'>Failed</label>" +
            '   </div>\n'

        ,
        buttons: {
            Save: async function () {
                var optionval = $("input[name='interviewOP']:checked").val()

                var jsonData = {
                    "optionval": optionval,
                    "intv_id": intv_id,
                }
                formId = "#myTableProject"
                $.ajax({
                    url: "/interview/update",
                    type: "get",
                    dataType: "JSON",
                    data: jsonData,
                }).then(result => {
                    if ($.fn.dataTable.isDataTable(formId)) {
                        console.log("dataTable1")
                        console.log(result)
                        let dataTable1 = $(formId).dataTable();
                        dataTable1.fnClearTable()
                        dataTable1.fnAddData(result, true)
                    }
                })

            },
            cancel: function () {
            }


        }
    })
}

function sendOffer(student_id, pid, intvid) {

    $.ajax({
        url: "/match/sendOffer",
        type: "get",
        dataType: "JSON",
        data: {"stu_id": student_id, "pid": pid, "intvId": intvid},

        beforeSend: function () {
            // 在 AJAX 请求发送前显示 loading 动画
        },
        complete: function (data) {
            $.alert("Offer are sent successfully!")
        },
    }).then(data => {
             if ($.fn.dataTable.isDataTable("#myTableProject")) {
                    console.log("dataTable1")
                    console.log(data)
                    let dataTable1 = $("#myTableProject").dataTable();
                    dataTable1.fnClearTable()
                    dataTable1.fnAddData(data, true)
            }
        })
}

function notiDetail(id) {
    $.ajax({
        url: "/getAllMyMsg",
        type: "get",
        dataType: "JSON",
        data: {"dataId": id},
    }).then(function (response) {
        console.log(response.data)
        $.confirm({
            boxWidth: '30%',
            useBootstrap: false,
            title: response.data[0][3],
            content: "<br>" + response.data[0][1] + "<br><br><br><br><br><br><br><br><br>" + response.data[0][2] + "<br> Sent By Admin",
            buttons: {
                OK: function () {
                },


            }
        });
    })
}

function sendRequest(url, data, method, ifDirect) {
    $.ajax({
        url: url,
        type: method,
        dataType: "JSON",
        data: data,
        success: function (response) {
            console.log(response)
            if (response.code == "SUCCESS") {
                if (ifDirect != 0) {
                    $.MessageBox(response.message + " success!!")
                }
            } else if (response.code == "DeleteUserSUCCESS") {
                $.MessageBox(response.message)
                location.reload();
            } else if (response.code == "UserUnsubscribe") {
                $.MessageBox(response.message)
                location.href = "/"
            } else {
                $.MessageBox(response.message)
            }


        }, fail: function (response) {
            console.log(response)

        }
    })
}


function deleteMember(data, ifDirect) {
    var formData = {'userId': data}
    console.log(formData)

    sendRequest('/removeUser', formData, "get", ifDirect);
}

// need more work for the ClassBooking confirmation pop up
function bookingClass(classId, userId) {
    $.confirm({
        theme: 'dark',
        title: 'Send Email',
        content: 'Are you sure?',
        buttons: {
            confirm: function () {
                confirmBooking(classId, userId)
                location.href = "/login"
            },
            cancel: function () {
            }

        }
    });
}

function checkEmail(email, id) {
    $.ajax({
        url: "/users/checkEmail",
        type: "get",
        dataType: "JSON",
        data: {"email": email},
    }).then(data => {
        console.log("asdasd")
        if (data.code == "ok") {
            if (id) {
                id = "#" + id
                $(id).addClass("error")
            }
            $.alert("email is already registered")
        } else {
            if (id) {
                id = "#" + id
                $(id).removeClass("error")
            }
        }
    })
}

function addMentor(fromdata) {

    $.ajax({
        url: "/users/addOrUpdate",
        type: "POST",
        dataType: "JSON",
        data: fromdata,
    }).then(data => {
        if (data.code == 'ok') {
            $.alert("Mentor has been added successfully")
            var btn = [
                {
                    "btnName": "editMentor",
                    "func": "alert"
                }, {
                    "btnName": "deleteMentor",
                    "func": "alert"
                }];
            renderDataTable("#myTableOne", "/mentor/getAllJson", [
                {"data": "first_name"},
                {"data": "phone"},
                {"data": "email"},
                {"data": "company_name"},
            ], true, 3, btn)
        }
    })

}

function validateQueForm() {

    var form = $("#queForm");
    form.validate({
        rules: {
            que_1: {
                required: true,

            },
            que_2: {
                required: true,

            },
            que_3: {
                required: true,

            },
            que_4: {
                required: true,

            },
            que_5: {
                required: true,

            },
            que_5: {
                required: true,

            },
            que_6: {
                required: true,

            },
            que_7: "required",
            que_8: "required",
            que_9: "required",
            que_10: "required"
        }

        ,
        errorPlacement: function (error, element) {
            return true;
        }
    });
    let valid = form.valid();

    if (!valid) {
        $.MessageBox("please fill out all required information in correct format");
    }
    return valid
}


function sendEmailPassword(email) {
    $.ajax({
        url: "/users/checkEmail",
        type: "get",
        dataType: "JSON",
        data: {"email": email},
    }).then(data => {
        if (data.code == 'ok') {
            $.ajax({
                url: "/users/sendPasswordEmail",
                type: "get",
                dataType: "JSON",
                data: {"email": email},
            }).then(data => {
                console.log(data)
            })
        } else {
            $.confirm({
                theme: 'dark',
                title: 'Send Email',
                content: 'Email doesn\'t exist',
                buttons: {
                    confirm: function () {
                    }
                }
            });
        }
    })
}

function validateForm() {
    $.validator.addMethod("greaterThan12Years", function (value, element) {
        var inputDate = new Date(value);
        var currentDate = new Date();
        var twelveYearsAgo = new Date().setFullYear(currentDate.getFullYear() - 12);

        return inputDate < twelveYearsAgo;
    }, "Date should be greater than 12 years from the current date.");

    var form = $("#regiForm");
    form.validate({
        rules: {
            firstname: {
                required: true,
                lettersonly: true
            },
            lastname: {
                required: true,
                lettersonly: true
            },
            preferName: {
                required: true,
                lettersonly: true
            },
            studentNo: {
                required: true,
                digits: true
            },
            password: {
                required: true,
                minlength: 6,
                maxlength: 15
            },
            phone: {
                required: true,
                digits: true
            },
            gender: "required",
            dob: {
                required: true,
                date: true,
                greaterThan12Years: true
            },
            email: {
                required: true,
                email: true
            }

        }, messages: {
            firstname: "please enter a valid first name",
            lastname: "please enter a valid last name",

            password: {
                required: "password is required",
                minlength: "password length should be greater than 6 "
            },
            dob: {
                required: "Please enter a date",
                date: "You must be at least 12 years old"
            },
            email: "please enter a valid email",
        }, errorPlacement: function (error, element) {
            // Custom error placement
            error.insertAfter(element);
            error.css('color', 'red');
            error.css('max-width', '200px !important')// Example: Set error message color to red
        },
        errorElement: "div", // Wrap error messages in a div element
        wrapper: "div",
        submitHandler: function (form) {
            // Handle form submission
            form.submit();
        }
    });
    let valid = form.valid();
    if (!valid) {
        $.MessageBox("please fill out all required information in correct format");
    }
    return valid
}

function processPayment(data, userId) {

    data = {
        "sessionId": data,
        "userId": userId
    }
    sendRequest("/addPayment", data, "post")
}

function updatePassword(role) {
    var formData = serializeData("form#forgotPass");

    $.validator.addMethod("passwordEqual", function (value, element) {
        let forpassword = $('#forpassword').val();
        let conpassword = $('#forconpassword').val();
        console.log(forpassword, conpassword)
        return forpassword == conpassword;
    }, "Passwords must be same");
    var form = $("#forgotPass");
    form.validate({
            rules: {
                forpassword: {
                    required: true,
                    passwordEqual: true
                },
                conpassword: {
                    required: true,
                    passwordEqual: true
                }

            },
            errorPlacement: function (error, element) {
                return true;
            }

        }
    )
    let valid = form.valid();
    if (!valid) {
        $.MessageBox("Passwords must be same");
    } else {
        $.ajax({
            url: "/users/changePassword",
            type: "POST",
            data: formData
        }).then(data => {
            if (data.code == 'ok') {
                $.MessageBox("your password has been changed.")
            } else {
                $.MessageBox(data.message)
            }
        })
    }

}

function checksendEmail() {
    $.confirm({
        theme: 'dark',
        title: 'Enter your email',
        content: '' +
            '<form action="" class="formName">' +
            '<div class="form-group">' +
            '<label>Your email address</label>' +
            '<input type="text" placeholder="John.Doe@gmail.com" class="email form-control" required />' +
            '</div>' +
            '</form>',

        buttons: {
            Send: function () {
                var email = this.$content.find('.email').val();
                if (!email) {
                    $.alert('provide a valid email');
                    return false;
                }
                sendEmailPassword(email)
            },
            cancel: function () {
            }

        }
    });
}

function changeIntention(ele) {
    if (ele.value == 2 || ele.value == 3) {
        $.alert("You can't use our system, please contact with the staff in charge.")
        $("#btnNext").addClass("hide");
    } else {
        $("#btnNext").removeClass("hide");
    }
}

function extraMultipul(selectedOptions, formData) {
    const result = selectedOptions.reduce((acc, {name, value}) => {
        acc[name] = acc[name] || [];
        acc[name].push(value);
        return acc;
    }, {});

    console.log(result);
    for (var objA in formData) {
        for (var objB in result) {
            if (objB === objA) {
                formData[objA] = result[objB]
            }
        }
    }
}

function submitQA() {
    validResult = validateQueForm()
    console.log(validResult)
    var formData = serializeData("form#queForm");
    console.log(formData)

    var selectedOptions = $("#queForm input[name='que_7']:checked").serializeArray();
    var selectedOptionsQ8 = $("#queForm input[name='que_8']:checked").serializeArray();

    extraMultipul(selectedOptions, formData);
    extraMultipul(selectedOptionsQ8, formData);


    let data1 = JSON.stringify(formData);
    let data2 = JSON.parse(data1);
    console.log(data1);
    $.ajax({
        url: "/studentQuestions/addQuestionAnswer",
        type: "POST",
        dateType: 'json',
        data: data2
    }).then(data => {
        if (data.code = 'ok') {
            $.alert("your survey has been updated successfully")
        }
    })

}

function hideQuestions(preOrNext) {
    var elements = $('#queForm .sideContainer');
    console.log(elements.length)
    var displayIndex = -1
    var hideIndex = -1
    if (preOrNext == 'next') {
        for (let i = 0; i < elements.length; i++) {
            if (elements[i].className.indexOf('hide') > 0 && displayIndex > 0) {

                if (i < hideIndex + 2) {
                    $(elements[i]).removeClass("hide")
                }
                if (hideIndex > elements.length - 4) {
                    $('#btnNext').addClass('hide')
                    $('#submitQABtn').removeClass('hide')
                }
            } else if (elements[i].className.indexOf('hide') < 0) {
                if (i >= elements.length - 2) {
                    $('#submitQABtn').removeClass('hide')
                    continue;
                } else {
                    $('#btnPrev').removeClass('hide')

                }
                if (hideIndex < displayIndex + 2) {
                    hideIndex = displayIndex + 2
                    displayIndex = i;
                }

                $(elements[i]).addClass("hide")
            }
        }

    } else {
        for (let i = elements.length - 1; i >= 0; i--) {
            if (elements[i].className.indexOf('hide') > 0 && displayIndex > 0) {

                if (i > hideIndex - 2) {
                    $(elements[i]).removeClass("hide")
                }
                if (hideIndex <= 1) {
                    $('#submitQABtn').addClass('hide')
                    $('#btnPrev').addClass('hide')
                    continue;
                }
                $('#btnNext').removeClass('hide')

            } else if (elements[i].className.indexOf('hide') < 0) {

                if (hideIndex > displayIndex - 2) {
                    displayIndex = i;
                    hideIndex = displayIndex - 2
                }
                $('#submitQABtn').addClass('hide')

                $(elements[i]).addClass("hide")
            }
        }
    }

}


function preferStudents() {
    var idArr = []
    $('input:checkbox').each(function () {
        if ($(this).prop('checked') == true) {
            idArr.push($(this).val());
        }
    });

    $.ajax({
        url: "/student/getStudentsByIds?idArr=" + idArr,
        type: "GET",
        data: idArr,
    }).then(data => {
        console.log(data);
        var options = ""
        for (let i = 0; i < data.data.length; i++) {
            selection = ""
            data.projects.forEach(pro => {
                console.log(pro)
                selection += "<option value='" + pro['id'] + "'>" + pro['project_title'] + "</option>"
            })

            let student = data.data[i];
            console.log(student)
            let studentElement = student['skill'];
            if (studentElement == null) studentElement = ""
            options += "<tr>" +
                "<td class='hide' name='stuId' value='" + student['id'] + "'>" + student['id'] + "</td>" +
                "<td>" + student['first_name'] + "\t" + student["last_name"] + "</td>" +
                "<td style=''>" + studentElement + "</td>" +
                "<td  style=\"width:300px;padding-right: 100px\"><select id=\"menProject" + student['id'] + "\" name=\"menProject\" class=\"menCompany form-control\">'" + selection + "'</select></td>" +
                "<td >" +
                "  <input type='radio' id='option" + student['id'] + "' name='option" + student['id'] + "' value='2'>" +
                "  <label for='option1" + student['id'] + "'>Yes</label>" +
                "  <input type='radio' id='option" + student['id'] + "' name='option" + student['id'] + "' value='1'>" +
                "  <label for='option2" + student['id'] + "'>Maybe</label>" +
                "  <input type='radio' id='option" + student['id'] + "' name='option" + student['id'] + "' value='0'>" +
                "  <label for='option3" + student['id'] + "'>No</label>" +
                "</td>" +
                "" +
                "</tr>";

        }

        console.log(options)
        $.confirm({
            theme: 'dark',
            boxWidth: '60%',
            useBootstrap: false,
            title: 'Student Preference',
            content: '' +
                ' <table id="tablePreStudent" class="display">\n' +
                '        <thead>\n' +
                '          <tr class="odd">\n' +
                '           <th width="18%">Student Name</th>\n' +
                '           <th  width="33%">Skills</th>\n' +
                '           <th  width="30%" style="padding-right: 100px">Project Allocation</th>\n' +
                '           <th  width="20%">Willings</th>\n' +
                '          </tr>\n' +
                '        </thead>\n' +
                '        <tbody>' + options +
                '        </tbody>' +
                ' </table>',

            buttons: {
                Save: async function () {
                    var sidList = [];

                    $('#tablePreStudent [name="stuId"]').each(function (eachh) {
                        console.log(eachh)
                        sidList.push({
                            "sid": parseInt(this.innerHTML),
                            "pid": $("#menProject" + this.innerHTML).val() == null ? 0 : $("#menProject" + this.innerHTML).val(),
                            "will": $("input[name='option" + this.innerHTML + "']:checked").val() == null ? 0 : $("input[name='option" + this.innerHTML + "']:checked").val()
                        });
                    });

                    let myJson = JSON.stringify(sidList);

                    $.ajax({
                        url: "/studentMentor/add",
                        type: "POST",
                        dataType: "JSON",
                        data: {sidList: myJson}
                    }).then(data => {
                        if (data.code == 'ok') {
                            $.alert('Student preferences has been updated successfully');

                        }
                    })


                },
                cancel: function () {
                }

            }
        })
    })
}

async function addNewMentor() {
    $.ajax({
        url: "/company/getAllJson",
        type: "GET",

    }).then(data => {
        console.log(data);
        var options = "";
        for (let dataKey in data) {
            options += "<option value='" + data[dataKey]['id'] + "'>" + data[dataKey]['company_name'] + "</option>"
        }
        console.log(options)
        $.confirm({
            theme: 'dark',
            title: 'Enter mentor information',
            content: '' +
                '<form id="mentorForm" class="formName">' +
                '<div class="form-group">' +
                '<input type="hidden" name="role" value="1" />' +
                '<label>Mentor email address</label>' +
                '<input type="text" placeholder="John.Doe@gmail.com" id="mentorEmail" name="email" class="email form-control" ' +
                'required onblur="checkEmail(this.value,this.id)" />' +
                '<label>Password</label>' +
                '<input type="password" name="password" class="password form-control" required />' +
                '<label>Phone</label>' +
                '<input type="text" name="phone" class="password form-control" required />' +
                '<label>Mentor First Name</label>' +
                '<input type="text" placeholder="Jone" name="firstname" class="fname form-control" required />' +
                '<label>Mentor Last Name</label>' +
                '<input type="text" placeholder="Doe" name="lastname" class="lastname form-control" required />' +
                '<label>Mentor Company</label>' +
                '<select id="menCompany" name="menCompany" class="menCompany form-control">' + options + '</select>' +
                '</div>' +
                '</form>',

            buttons: {
                Save: async function () {
                    var email = this.$content.find('.email').val();
                    var fname = this.$content.find('.fname').val();
                    var password = this.$content.find('.password').val();
                    var lastname = this.$content.find('.lastname').val();
                    var menCompany = this.$content.find('.menCompany').val();
                    if (!email) {
                        $.alert('provide a valid email');
                        return false;
                    }
                    var formData = serializeData("form#mentorForm")
                    const checkResult = await ajaxCall("/users/checkEmail", "get", {"email": formData.email})


                    if (checkResult.code == 'ok') {
                        $.alert('email is already registered, please change another email address');
                        return false;
                    } else {
                        addMentor(formData)
                    }

                },
                cancel: function () {
                }

            }
        })
    })
}


function checkUserStatus(id) {
    $.ajax({
        url: "/student/getStudentById",
        type: "get",
        dataType: "JSON",
        data: {"id": id}
    }).then(data => {
        if (data.data == 3) {
            $.alert("Looks like you haven't completed our survey, before you use our system you must complete all of them")
        }
    })
}

function addSpeedInterview() {
    $.ajax({
        url: "/speed/getEvent",
        type: "GET",

    }).then(result => {
        console.log(result)
        $.confirm({
            theme: 'dark',
            title: 'Speed Interview',
            content: '' +
                '<form id="mentorForm" class="formName">' +
                '<div class="form-group justify-content-center">' +
                '   <div class="inputBox">\n' +
                '     <label for="date" style="margin-right: 64px;padding-top: 5px">Date</label>\n' +
                '     <input type="date" name="startdate"  value="' + result.interviewDate.split(' ')[0] + '" id="startdate" min="2023-06-16" required="required"><!--required to check for empty-->\n' +
                '   </div>\n' +
                '   <div class="inputBox">\n' +
                '    <label for="starttime" style="margin-right: 83px;padding-top: 5px">At </label>\n' +
                '    <input type="text" id="myTimeInput" value="' + result.interviewDate.split(' ')[1] + '">\n' +
                '   </div>\n' +
                '   <div class="inputBox" style="display: flex;padding-top: 5px" >\n' +
                '     <label for="location" style="margin-right: 40px">Location</label>\n' +
                '     <input type="text" name="location" id="location" value="' + result.location + '" required="required"><!--required to check for empty-->\n' +
                '   </div>\n' +
                '   <div class="inputBox" style="display: flex;padding-top: 5px" >\n' +
                '     <label for="location" style="margin-right: 20px">Description</label>\n' +
                '     <textarea type="text" name="desc" id="desc" value="" required="required">' + result.content + '</textarea>' +
                '   </div>\n' +
                ' </div>' +
                '</form>'
            ,
            onContentReady: function () {
                $('#myTimeInput').timepicker({
                    'step': 30,
                    'minTime': '9:00am',
                    'maxTime': '5:30pm',
                    'beforeShow': function () {
                        // 延迟以等待 timepicker 完全初始化
                        setTimeout(function () {
                            // jQuery UI 时间选择器使用 jQuery UI dialog 组件来展示时间选择器
                            // dialog 的 z-index 值设置在其父元素上
                            $('.ui-timepicker-div').parent().css('z-index', 99999999999999);
                        }, 0);
                    }
                });

            },
            buttons: {
                Save: async function () {
                    var startdate = this.$content.find('#startdate').val();
                    var desc = this.$content.find('#desc').val();
                    var starttime = this.$content.find('#myTimeInput').val();
                    var location = this.$content.find('#location').val();

                    var jsonData = {
                        "startdate": startdate,
                        "starttime": starttime,
                        "desc": desc,
                        "location": location
                    }
                    formId = "#myTableProject"
                    $.ajax({
                        url: "/speed/addEvent",
                        type: "post",
                        dataType: "JSON",
                        data: jsonData,
                    }).then(result => {
                        if ($.fn.dataTable.isDataTable(formId)) {
                            console.log("dataTable1")
                            console.log(result)
                            let dataTable1 = $(formId).dataTable();
                            dataTable1.fnClearTable()
                            dataTable1.fnAddData(result, true)
                        }
                    })

                },
                cancel: function () {
                }


            }
        })
    })


}

function checkStudentProfile(studentId) {
    $.ajax({
        url: "/studentQuestions/getByStudentId",
        type: "get",
        dataType: "JSON",
        data: {"studentId": studentId}
    }).then(data => {
        if (data.code = 'ok') {
            let questionData = data.data;
            console.log(questionData)
            var td = ''
            questionData.forEach(question => {
                td += '<tr  style="width: 100%"><td style="width: 50%; vertical-align: top">'
                console.log(question.question)
                var que = JSON.parse(question.question)
                td += que.title + "</td><td style='width: 50%; vertical-align: top'>"
                if (que.type == "1") {
                    td += que.option[question.question_answer] + "</td>"
                } else if (que.type == "2" && question.question_answer.split(',').length > 0) {
                    for (let i = 0; i < question.question_answer.split(',').length; i++) {
                        td += que.option[question.question_answer.split(',')[i]] + "</br>"
                    }

                } else {
                    td += question.question_answer + "</td>"
                }
                td += "</tr>"
            })
            $.confirm({
                boxWidth: '1200px',
                useBootstrap: false,
                title: 'Survey Answers',
                content: '' +
                    ' <table id="myTableStudent" class="display">' +
                    '      <thead>' +
                    '        <tr>' +
                    '         <th>Question</th>' +
                    '         <th>Answer</th>' +
                    '        </tr>' +
                    '      </thead>' +
                    '      <tbody>' + td + '</tbody>' +
                    ' </table>'
            })

        }
    })
}


async function ajaxCall(url, type, data) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: type,
            dataType: "JSON",
            data: data,
            success: function (data) {
                resolve(data);
            },
            error: function (xhr, status, error) {
                reject(error);
            }
        });
    });
}

async function myFunction() {
    try {
        const myData = await ajaxCall();
        // do something with myData
    } catch (error) {
        console.error(error);
    }
}

function uploadFile() {
    var input = document.getElementById('userCV');
    var file = input.files[0];
    var formData = new FormData();
    if (file == undefined) {
        return
    }
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            if (data.code == 'ok') {
                var span = document.getElementById('text');

                var a = document.createElement('a');
                a.href = "/download/" + data.filename;
                a.textContent = 'Click here to download the file';
                span.innerHTML = a.outerHTML;
            } else {

            }
        });
}


function addOrUpdateUser(type) {

    //add or update a student
    if (type == 2) {
        if (validateForm()) {
            var formData = serializeData("form#regiForm");
            var skills = $("#regiForm input[name='stu_skills']:checked");
            let skillsVale = Array.from(skills).map(input => input.value);
            let $text = $("#text a");
            if ($text != undefined && $text.length > 0) {
                formData['fileLocation'] = $text[0].pathname.replaceAll("/download/", "")
            }

            formData['stu_skills'] = skillsVale;
            console.log(skillsVale)
            console.log(formData)
            // check if a student no is exist
            $.ajax({
                url: "/users/checkStudentExsit",
                type: "POST",
                data: formData
            }).then(data => {
                console.log(data)
                if (data.code != 'ERROR') {
                    $.ajax({
                        url: "/users/addOrUpdate",
                        type: "POST",
                        data: formData
                    }).then(data => {
                        if (data.code == 'ok') {
                            $.MessageBox(data.message);
                        }
                    })

                } else {
                    $.MessageBox(data.message)
                }
            });


        }
    } else {
        if (validateTrainerForm()) {
            var formData = serializeData("form#trainerRegiForm");
            console.log(formData)
            sendRequest('/addOrUpdateMember', formData, "POST", "form#trainerRegiForm");
        }
    }
}

function moveUp(button) {

    var row = $(button).closest('tr');
    var previousRow = row.prev('tr');

    if (previousRow.length !== 0) {
        previousRow.before(row);
    }


}

function moveDown(button) {

    var row = $(button).closest('tr');
    var after = row.next('tr');

    if (after.length !== 0) {
        after.after(row);
    }


}

function checkPreferredStudent(pid) {
    location.href = '/student/getAll?pid=' + pid
}

function goPreferredProject() {
    location.href = '/studentProject/preferProject'

}

function viewCompanyProject(comId) {

    $.ajax({
        url: "/project/getProjectsByCompanyId",
        type: "GET",
        data: {"comId": comId},
    }).then(data => {
        var options = ""
        if (data.data.length == 0) {
            $.alert("This company haven't got any project !")
            return
        }
        for (let i = 0; i < data.data.length; i++) {
            let item = data.data[i];
            options += "<tr>" +
                "<td class='hide' name='proId' value='" + item['id'] + "'>" + item['id'] + "</td>" +
                "<td style='width: 50%;padding-right: 150px;'>" + item['project_title'] + "</td>" +
                "<td style='width: 25%'>" + item['type_name'] + "</td>" +
                "<td style='width: 25%'>" + item['company_name'] + "</td>"
        }

        console.log(options)
        $.confirm({
            theme: 'dark',
            boxWidth: '900px',
            useBootstrap: false,
            title: 'Projects',
            content: '' +
                ' <table id="tablePreProject" class="display">\n' +
                '        <thead>\n' +
                '          <tr class="odd">\n' +
                '           <th width="33%">Project Name</th>\n' +
                '           <th  width="33%">Project Type</th>\n' +
                '           <th  width="33%">Company</th>\n' +
                '          </tr>\n' +
                '        </thead>\n' +
                '        <tbody>' + options +
                '        </tbody>' +
                ' </table>',

            buttons: {

                cancel: function () {
                }

            }
        })
    })
}

function processMatching() {
    $.ajax({
        url: "/match/processMatch",
        type: "GET",
        beforeSend: function () {
            // 在 AJAX 请求发送前显示 loading 动画
            $("#loading").show();
        },
        complete: function (data) {
            $("#loading").hide();
            if (data.responseJSON.code == 'ok') {

                $.alert("Matches notifications are sent successfully!")
            }
        },
    })
}

function addPreferredProject() {
    var idArr = []
    $('input:checkbox').each(function () {
        console.log($(this))
        if ($(this).prop('checked') == true) {
            idArr.push($(this).val());
        }
    });
    if (idArr.length < 3) {
        $.alert("At least three project need to chosen before your rank them")
        return;
    }

    $.ajax({
        url: "/project/getProjectByIds?idArr=" + idArr,
        type: "GET",
        data: idArr,
    }).then(data => {
        console.log(data);
        var options = ""
        for (let i = 0; i < data.data.length; i++) {
            let item = data.data[i];
            console.log(item)
            options += "<tr>" +
                "<td class='hide' name='proId' value='" + item['id'] + "'>" + item['id'] + "</td>" +
                "<td><button onclick='moveUp(this)' >Up</button><button onclick='moveDown(this)'>Down</button></td>" +
                "<td>" + item['project_title'] + "</td>" +
                "<td>" + item['type_name'] + "</td>" +
                "<td>" + item['company_name'] + "</td>" +
                "<td>" +
                "<input type='radio' id='option" + item['id'] + "' name='option" + item['id'] + "' value='2'>" +
                "  <label for='option1" + item['id'] + "'>Yes</label>" +
                "  <input type='radio' id='option" + item['id'] + "' name='option" + item['id'] + "' value='1'>" +
                "  <label for='option2" + item['id'] + "'>Maybe</label>" +
                "  <input type='radio' id='option" + item['id'] + "' name='option" + item['id'] + "' value='0'>" +
                "  <label for='option3" + item['id'] + "'>No</label>" +
                "</td>" +
                "" +
                "</tr>";

        }

        console.log(options)
        $.confirm({
            theme: 'dark',
            boxWidth: '75%',
            useBootstrap: false,
            title: 'Rank your preference',
            content: '' +
                ' <table id="tablePreProject" class="display">\n' +
                '        <thead>\n' +
                '          <tr class="odd">\n' +
                '           <th width="15%" style="padding-right: 150px">Rank</th>\n' +
                '           <th width="27%">Project Name</th>\n' +
                '           <th  width="19%">Project Type</th>\n' +
                '           <th  width="15%">Company</th>\n' +
                '           <th  width="25%">Willings</th>\n' +
                '          </tr>\n' +
                '        </thead>\n' +
                '        <tbody>' + options +
                '        </tbody>' +
                ' </table>',

            buttons: {
                Save: async function () {
                    var pidList = [];

                    $('#tablePreProject [name="proId"]').each(function (eachh) {
                        console.log(eachh)
                        pidList.push({
                            "pid": parseInt(this.innerHTML),
                            "will": $("input[name='option" + this.innerHTML + "']:checked").val() == null ? 0 : $("input[name='option" + this.innerHTML + "']:checked").val()
                        });
                    });

                    let myJson = JSON.stringify(pidList);

                    $.ajax({
                        url: "/studentProject/add",
                        type: "POST",
                        dataType: "JSON",
                        data: {pidList: myJson}
                    }).then(data => {
                        if (data.code == 'ok') {
                            $.alert('Your project preferences has been updated successfully');

                        }
                    })


                },
                cancel: function () {
                }

            }
        })
    })
}

function serializeData(form, include, exclude) {
    let form2 = $(form);
    var obj = form2.serializeArray();
    include = include || [];
    exclude = exclude || [];
    var holder = {};
    for (var i = 0; i < obj.length; i++) {
        var key = obj[i]['name'];
        var val = obj[i]['value'];
        if (exclude.indexOf(key) > -1) continue;
        if (0 === include.length || include.indexOf(key) > -1) {
            holder[key] = val;
        }
    }
    return holder;
}

// reset password for all user

async function resetPassword(id) {
    $.ajax({
        url: "/company/getAllJson",
        type: "GET",

    }).then(data => {
        console.log(data);
        //  var options = "";
        // for (let dataKey in data) {
        //     options += "<option value='" + data[dataKey]['id'] + "'>" + data[dataKey]['company_name'] + "</option>"
        // }
        // console.log(options)
        $.confirm({
            theme: 'dark',
            title: 'Enter mentor information',
            content: '' +
                '<form id="mentorForm" class="formName">' +
                '<div class="form-group">' +
                '<input type="hidden" name="role" value="1" />' +
                '<label>Old password</label>' +
                '<input type="password" name="oldpassword" class="oldpassword form-control" required />' +
                '<label>Password</label>' +
                '<input type="password" name="password" class="password form-control" required />' +
                '<label>Confirm Password</label>' +
                '<input type="password" name="conpassword" class="conpassword form-control" required />' +
                '</form>',

            buttons: {
                Save: async function () {
                    var oldpassword = this.$content.find('.oldpassword').val();
                    var password = this.$content.find('.password').val();
                    var conpassword = this.$content.find('.conpassword').val();
                    console.log(password, oldpassword, conpassword)
                    if (password != conpassword) {
                        $.alert('Please input the same password');
                        return false;

                    }
                    var formData = serializeData("form#mentorForm")
                    const checkResult = await ajaxCall("/users/checkPassword", "get", {
                        "id": id,
                        "oldpassword": formData.oldpassword
                    })

                    var jsonData = {
                        "userId": id,
                        "password": password
                    }
                    if (checkResult.code == 'error') {
                        $.alert('Password is wrong, please input again');
                        return false;
                    } else {
                        resetPassword2(jsonData)
                        // renderDataTable("#myTable", "/mentor/getAllJson")
                    }

                },
                cancel: function () {
                }

            }
        })
    })
}


function resetPassword2(fromdata) {

    $.ajax({
        url: "/users/resetpassword",
        type: "POST",
        dataType: "JSON",
        data: fromdata,
    }).then(data => {
        if (data.code == 'ok') {
            $.alert("Password has been reset")

        }
    })

}

async function addNewProjectOrupdate(pid) {


    $.ajax({
        url: "/project/getAllprofileAndtypeJson",
        type: "GET",
        data: {"pid": pid},

    }).then(data => {
        console.log(data);
        var options = "";

        for (let i = 0; i < data.types.length; i++) {
            let item = data.types[i];
            options += "<option value='" + item['type_id'] + "'>" + item['type_name'] + "</option>"
        }
        console.log(options)

        var str = ''
        if (pid == null) {

            str = '' +
                '<form id="projectForm" class="formName">' +
                '<div class="form-group">' +
                '<label>Project Title</label>' +
                '<input type="text" placeholder="Project" name="project_title" class="fname form-control" required />' +
                '<label>Description</label>' +
                '<input type="text" placeholder="Description" name="description" class="fname form-control" required />' +
                '<label>Number of students</label>' +
                '<input type="text" placeholder="10" name="Number_of_student" class="fname form-control" required />' +
                '<label>Project start date</label>' +
                '<input type="date" placeholder="" name="start_date" class="fname form-control" required />' +
                '<label>Project end date</label>' +
                '<input type="date" placeholder="" name="end_date" class="fname form-control" required />' +
                '<label> Company type</label>' +
                '<select id="project type" name="projecttype" class="menCompany form-control">' + options + '</select>' +
                '</div>' +
                '</form>'
        } else {

            let projectitem = data.projects[0];
            str = '' +
                '<form id="projectForm" class="formName">' +
                '<div class="form-group">' +
                '<input type="hidden" name="pid" value="' + pid + '" />' +
                '<label>Project Title</label>' +
                '<input type="text" placeholder="Project" name="project_title" class="fname form-control" value = ' + projectitem['project_title'] + ' required />' +
                '<label>Description</label>' +
                '<input type="text" placeholder="Description" name="description" class="fname form-control" value = ' + projectitem['description'] + ' required />' +
                '<label>Number of students</label>' +
                '<input type="text" placeholder="10" name="Number_of_student" class="fname form-control" value = ' + projectitem['number_of_student'] + ' required />' +
                '<label>Remain Number of students</label>' +
                '<input type="text" placeholder="10" name="remain_number_of_student" class="fname form-control" value = ' + projectitem['remain_number_of_student'] + ' required />' +
                '<label>Project start date</label>' +
                '<input type="text" placeholder="" name="start_date" class="fname form-control" value = ' + projectitem['start_date'] + ' required />' +
                '<label>Project end date</label>' +
                '<input type="text" placeholder="" name="end_date" class="fname form-control" value = ' + projectitem['end_date'] + ' required />' +
                '<label> Company type</label>' +
                '<select id="project type" name="projecttype" class="menCompany form-control">' + options + '</select>' +
                '</div>' +
                '</form>'

        }

        $.confirm({
            theme: 'dark',
            title: 'Enter Project information',

            content: str,

            buttons: {
                Save: async function () {
                    var pid = this.$content.find('.pid').val();
                    var project_title = this.$content.find('.project_title').val();
                    var description = this.$content.find('.description').val();
                    var Number_of_student = this.$content.find('.Number_of_student').val();
                    var start_date = this.$content.find('.start_date').val();
                    var end_date = this.$content.find('.end_date').val();
                    var projecttype = this.$content.find('.projecttype').val();
                    // if (!email) {
                    //     $.alert('provide a valid email');
                    //     return false;
                    // }
                    var formData = serializeData("form#projectForm")
                        // const checkResult = await ajaxCall("/users/checkEmail", "get", {"email": formData.email})


                        // if (checkResult.code == 'ok') {
                        //     $.alert('email is already registered, please change another email address');
                        //     return false;
                        // } else {
                        (formData)

                    // }

                },
                cancel: function () {
                }

            }
        })
    })
}

function addOrUpdateProject(fromdata) {

    $.ajax({
        url: "/Project/addOrUpdate",
        type: "POST",
        dataType: "JSON",
        data: fromdata,

    }).then(data => {
        if (data.code == 'ok') {

            alert("Project has been added or updated successfully")


            $('#myTableOne').delay(2000).slideDown("3000", function () {
                var btn = [{
                    "btnName": "Preferred Students",
                    "func": "alert"
                }
                ];

                renderDataTable('#myTableOne', '/mentor/getProjectAllJson', [
                    {"data": null},
                    {"data": "project_title"},
                    {"data": "description"},
                    {"data": "number_of_student"},
                    {"data": "type_name"},
                    {"data": "start_date"},
                    {"data": "end_date"},
                    {"data": "remain_number_of_student"},
                    {"data": "company_name"},
                ], true, true, 9, btn);


            });


        } else {
            alert("add or update action failed ")
        }
    })


}

function updateSkill(pid) {

    $.ajax({
        url: "/project/getAllskillJson",
        type: "GET",
        data: {"pid": pid},

    }).then(data => {

        console.log(data);
        var options = "";


        var str = ''


        str = '' +
            '<form id="regiForm" class="formName">' +
            '<div class="form-group">' +
            '<input type="hidden" name="pid" value="' + pid + '" />'


        for (let i = 0; i < data.skills.length; i++) {
            let item = data.skills[i];
            if (item['project_id']) {
                str += '<p><div class="text-bg-secondary p-3"><input type="checkbox" id = ' +
                    item['id'] + ' name="projectskill"  checked value= ' + item['id'] + ' >' + '  <label>' +
                    item['skill_name'] + '</label> </div>'
            } else {
                str += '<p><div class="text-bg-secondary p-3"><input type="checkbox" id = ' +
                    item['id'] + ' name="projectskill"  value= ' + item['id'] + ' >' + '  <label>' +
                    item['skill_name'] + '</label> </div>'
            }


        }

        str += '</div>' + '</form>'


        $.confirm({
            theme: 'dark',
            title: 'Select required skills',

            content: str,

            buttons: {
                Save: async function () {
                    var pid = this.$content.find('.pid').val();
                    //var projectskill = this.$content.find('.projectskill').val();
                    // var description = this.$content.find('.description').val();
                    // var Number_of_student = this.$content.find('.Number_of_student').val();
                    // var start_date = this.$content.find('.start_date').val();
                    // var end_date = this.$content.find('.end_date').val();
                    // var projecttype = this.$content.find('.projecttype').val();

                    var formData = serializeData("form#projectForm")

                    addOrUpdateProjectSkill(formData)


                },
                cancel: function () {
                }

            }
        })
    })


}

function addOrUpdateProjectSkill(fromdata) {


    var formData = serializeData("form#regiForm");
    var skills = $("#regiForm input[name='projectskill']:checked");
    let skillsVale = Array.from(skills).map(input => input.value);
    if (skillsVale.length < 1) {
        $.alert("You have to choose at least one skill !")
        return false;
    }
    formData['projectskill'] = skillsVale;
    $.ajax({
        url: "/project/addOrUpdateProjectSkill",
        type: "POST",
        dataType: "JSON",
        data: formData,
    }).then(data => {
        if (data.code == 'ok') {
            $.alert("Project requied skills have been reset")

        } else {
            $.alert(data.message)
        }
    })

}