// =================================
// ANALYTICS DASHBOARD
// =================================

document.addEventListener("DOMContentLoaded",function(){

    createIssueChart();
    createCategoryChart();
    createAttendanceChart();
    createFineChart();

});

// =================================
// MONTHLY ISSUE CHART
// =================================

function createIssueChart(){

    let ctx =
    document.getElementById("issueChart");

    if(!ctx) return;

    new Chart(ctx,{

        type:"line",

        data:{

            labels:[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug"
            ],

            datasets:[{

                label:"Books Issued",

                data:[
                    100,
                    130,
                    180,
                    210,
                    250,
                    300,
                    340,
                    390
                ],

                borderWidth:3,

                fill:false

            }]

        },

        options:{
            responsive:true
        }

    });

}

// =================================
// CATEGORY CHART
// =================================

function createCategoryChart(){

    let ctx =
    document.getElementById("categoryChart");

    if(!ctx) return;

    new Chart(ctx,{

        type:"pie",

        data:{

            labels:[
                "Programming",
                "AI",
                "Business",
                "Science",
                "Finance"
            ],

            datasets:[{

                data:[
                    40,
                    25,
                    15,
                    10,
                    10
                ]

            }]

        }

    });

}

// =================================
// ATTENDANCE CHART
// =================================

function createAttendanceChart(){

    let ctx =
    document.getElementById("attendanceChart");

    if(!ctx) return;

    new Chart(ctx,{

        type:"bar",

        data:{

            labels:[
                "Week 1",
                "Week 2",
                "Week 3",
                "Week 4"
            ],

            datasets:[{

                label:"Attendance %",

                data:[
                    88,
                    92,
                    90,
                    95
                ]

            }]

        },

        options:{

            scales:{

                y:{

                    beginAtZero:true,
                    max:100

                }

            }

        }

    });

}

// =================================
// FINE CHART
// =================================

function createFineChart(){

    let ctx =
    document.getElementById("fineChart");

    if(!ctx) return;

    new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[
                "Collected",
                "Pending"
            ],

            datasets:[{

                data:[
                    12000,
                    3000
                ]

            }]

        }

    });

}

// =================================
// EXPORT REPORT
// =================================

function exportAnalytics(){

    alert(
        "Analytics Report Download Started"
    );

}

// =================================
// REFRESH DATA
// =================================

function refreshAnalytics(){

    location.reload();

}