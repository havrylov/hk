$(document).ready(function (c) {
    
    $('.fashion2.mainPage').on('click', function(c){       
       var formURL = $('.list_of_members').attr("some_url");
       $.ajax({
            url: formURL,
            type: 'GET',
            dataType: 'text',
            data_outp: content,
            error: function (jqXHR, textStatus, errorThrown){
                sweetAlert(errorThrown, textStatus, "error");
            }
        }).done(function(data_outp) {
            var statistic = JSON.parse(data_outp);
                $('.valueType').html('FAMILY');
                $('#balanceMain').html(statistic.public_balance)
                $('#outcomeMain').html(statistic.public_outcome)
                $('#incomeMain').html(statistic.public_income)
                $('.firstTr').html(statistic.public_transaction_time)
        });
    });
    $('.fashion1.mainPage').on('click', function(c){
       var formURL = $('.list_of_members').attr("some_url");
       $.ajax({
            url: formURL,
            type: 'GET',
            dataType: 'text',
            data_outp: content,
            error: function (jqXHR, textStatus, errorThrown){
                sweetAlert(errorThrown, textStatus, "error");
            },            
        }).done(function(data_outp) {
            var statistic = JSON.parse(data_outp);
                $('.valueType').html('PRIVATE');
                $('#balanceMain').html(statistic.private_balance)
                $('#outcomeMain').html(statistic.private_outcome)
                $('#incomeMain').html(statistic.private_income)
                $('.firstTr').html(statistic.private_transaction_time)            
        });
    });
    var content;    
    $('.alert-close').on('click', function (c) {
        $('.calender-left').fadeOut('slow', function (c) {
            $('.calender-left').remove();
        });
    });

    $('.alert-close1').on('click', function (c) {
        $('.calender-right').fadeOut('slow', function (c) {
            $('.calender-right').remove();
        });
    });

    $('.alert-close2').on('click', function (c) {
        $('.graph').fadeOut('slow', function (c) {
            $('.graph').remove();
        });
    });

    $('.alert-close3').on('click', function (c) {
        $('.site-report').fadeOut('slow', function (c) {
            $('.site-report').remove();
        });
    });
    $('.alert-close4').on('click', function (c) {
        $('.total-sale').fadeOut('slow', function (c) {
            $('.total-sale').remove();
        });
    });

    $('.alert-close5').on('click', function (c) {
        $('.total-sale').fadeOut('slow', function (c) {
            $('.total-sale').remove();
        });
    });

    $('.alert-close7').on('click', function (c) {
        $('.user-trends').fadeOut('slow', function (c) {
            $('.user-trends').remove();
        });
    });

    $('.alert-close6').on('click', function (c) {
        $('.world-map').fadeOut('slow', function (c) {
            $('.world-map').remove();
        });
    });

    $('#horizontalTab,#horizontalTab1,#horizontalTab2').easyResponsiveTabs({
        type: 'default', //Types: default, vertical, accordion           
        width: 'auto', //auto or any width like 600px
        fit: true   // 100% fit in a container
    });

    $(".overlay, .overlay-message").hide();

    $(".verlay, .xClose").click(function () {
        $('.xClose').html("");
        $('.messageBody').html("");
        $(".overlay, .overlay-message").hide();
    });
    $(".overlayShow, .as_link").click(function (e) {
        showClickAsLink(e, this);
    });

    $(".send_confirmation").click(function (e) {
        e.preventDefault();
        //alert(this.href);
        var getData = $(this).serializeArray();
        //var formURL = this.href;
        var formURL = this.href;        
        $.ajax(
                {
                    url: formURL,
                    type: "GET",
                    data: getData,
                    dataType: 'html',
                    data_outp: content,
                    error: function (jqXHR, textStatus, errorThrown)
                    {
                        sweetAlert("Oops...", "Something went wrong!", "error");
                    },
                    success: function (data_outp, textStatus, xhr) {
                        var diagnose = xhr.getResponseHeader('Overflow');
                        if (diagnose == "1") {
                            swal({
                                title: "Success!",
                                text: "Confirmation was successfully resent",
                                type: "success",
                                showCancelButton: false,
                                closeOnConfirm: true
                            })
                        } else if (diagnose == "-6") {
                            sweetAlert("Failed!", "You do it too often, dude! Try tomorrow.", "error");
                        } else {
                            sweetAlert("Failed!", "Something strange has happened!", "error");
                        }
                    }
                });
            });

            $(".ajax_form").submit(function (e)
            {
                var getData = $(this).serializeArray();
                var formURL = $(this).attr("action");
                var formName = $(this).attr('name');
                var requestType = $(this).attr('method');

                var alertTitle = "Success!";
                var alertText = "Operation is successfully completed!";

                if (formName.toLowerCase() == "new_transactions".toLowerCase()) {
                    alertTitle = "Saved!";
                    alertText = "All transactions are succesfully added!";
                } else if (formName.toLowerCase() == "edit_transaction".toLowerCase()) {
                    alertTitle = "Saved!";
                    alertText = "All changes are succesfully saved!";
                } else if (formName.toLowerCase() == "save_personal".toLowerCase()) {
                    alertTitle = "Saved!";
                    alertText = "All changes are succesfully saved!";
                }

                $.ajax(
                        {
                            url: formURL,
                            type: requestType,
                            data: getData,
                            dataType: 'html',
                            data_outp: content,
                            error: function (jqXHR, textStatus, errorThrown)
                            {
                                sweetAlert("Oops...", "Something went wrong!", "error");
                            },
                            success: function () {
                                $(".overlay, .overlay-message").hide();
                                swal({
                                    title: alertTitle,
                                    text: alertText,
                                    type: "success",
                                    showCancelButton: false,
                                    closeOnConfirm: true
                                },
                                function () {
                                    location.reload();
                                });
                            }
                        });
                e.preventDefault(); //STOP default action
                e.unbind(); //unbind. to stop multiple form submit.
            });

            $body = $("body");

            $(document).on({
                ajaxStart: function () {
                    $body.addClass("loading");
                },
                ajaxStop: function () {
                    $body.removeClass("loading");
                }
            });




        });

        function showClickAsLink(eve, form) {
            var content;
            eve.preventDefault();
            //alert(this.href);
            var getData = $(form).serializeArray();
            //var formURL = this.href;
            var formURL = $(form).attr("href");
            $.ajax(
                    {
                        url: formURL,
                        type: "GET",
                        data: getData,
                        dataType: 'html',
                        data_outp: content,
                        error: function (jqXHR, textStatus, errorThrown)
                        {
                            //if fails     
                        }
                    })
                    .done(function (data_outp) {
                        $('.xClose').html("&times;");
                        $('.messageBody').html(data_outp);
                        $(".overlay, .overlay-message").show();
                    });
        }

        function submitAjaxForm(form) {
            var getData = $(form).serializeArray();
            var formURL = $(form).attr("action");
            var formName = $(form).attr('name');
            var requestType = $(form).attr('method');

            var alertTitle = "Success!";
            var alertText = "Operation is successfully completed!";

            if (formName.toLowerCase() == "new_transactions".toLowerCase()) {
                alertTitle = "Saved!";
                alertText = "All transactions are succesfully added!";
            } else if (formName.toLowerCase() == "edit_transaction".toLowerCase()) {
                alertTitle = "Saved!";
                alertText = "All changes are succesfully saved!";
            } else if (formName.toLowerCase() == "save_personal".toLowerCase()) {
                alertTitle = "Saved!";
                alertText = "All changes are succesfully saved!";
            }

            $.ajax(
                    {
                        url: formURL,
                        type: requestType,
                        data: getData,
                        dataType: 'html',
                        data_outp: content,
                        error: function (jqXHR, textStatus, errorThrown)
                        {
                            //if fails     
                        }
                    })
                    .done(function () {
                        $(".overlay, .overlay-message").hide();
                        swal({
                            title: alertTitle,
                            text: alertText,
                            type: "success",
                            showCancelButton: false,
                            closeOnConfirm: true
                        },
                        function () {
                            location.reload();
                        });
                    })
                    .error(function () {
                        sweetAlert("Oops...", "Something went wrong!", "error");
                    });
            event.preventDefault();
            return false;
        }
//(function (i, s, o, g, r, a, m) {
//    i['GoogleAnalyticsObject'] = r;
//    i[r] = i[r] || function () {
//        (i[r].q = i[r].q || []).push(arguments)
//    }, i[r].l = 1 * new Date();
//    a = s.createElement(o),
//            m = s.getElementsByTagName(o)[0];
//    a.async = 1;
//    a.src = g;
//    m.parentNode.insertBefore(a, m)
//})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');
//
//ga('create', 'UA-48014931-1', 'codyhouse.co');
//ga('send', 'pageview');
//
//jQuery(document).ready(function ($) {
//    $('.close-carbon-adv').on('click', function () {
//        $('#carbonads-container').hide();
//    });
//});


// note, we have townName field with a name specified for each datapoint and townName2 with only some of the names specified.
// we use townName2 to display town names next to the bullet. And as these names would overlap if displayed next to each bullet,
// we created this townName2 field and set only some of the names for this purpse.
        var chartData = [
            {
                "date": "2012-01-01",
                "distance": 227,
                "townName": "New York",
                "townName2": "New York",
                "townSize": 25,
                "latitude": 40.71,
                "duration": 408
            },
            {
                "date": "2012-01-02",
                "distance": 371,
                "townName": "Washington",
                "townSize": 14,
                "latitude": 38.89,
                "duration": 482
            },
            {
                "date": "2012-01-03",
                "distance": 433,
                "townName": "Wilmington",
                "townSize": 6,
                "latitude": 34.22,
                "duration": 562
            },
            {
                "date": "2012-01-04",
                "distance": 345,
                "townName": "Jacksonville",
                "townSize": 7,
                "latitude": 30.35,
                "duration": 379
            },
            {
                "date": "2012-01-05",
                "distance": 480,
                "townName": "Miami",
                "townName2": "Miami",
                "townSize": 10,
                "latitude": 25.83,
                "duration": 501
            },
            {
                "date": "2012-01-06",
                "distance": 386,
                "townName": "Tallahassee",
                "townSize": 7,
                "latitude": 30.46,
                "duration": 443
            },
            {
                "date": "2012-01-07",
                "distance": 348,
                "townName": "New Orleans",
                "townSize": 10,
                "latitude": 29.94,
                "duration": 405
            },
            {
                "date": "2012-01-08",
                "distance": 238,
                "townName": "Houston",
                "townName2": "Houston",
                "townSize": 16,
                "latitude": 29.76,
                "duration": 309
            },
            {
                "date": "2012-01-09",
                "distance": 218,
                "townName": "Dalas",
                "townSize": 17,
                "latitude": 32.8,
                "duration": 287
            },
            {
                "date": "2012-01-10",
                "distance": 349,
                "townName": "Oklahoma City",
                "townSize": 11,
                "latitude": 35.49,
                "duration": 485
            },
            {
                "date": "2012-01-11",
                "distance": 603,
                "townName": "Kansas City",
                "townSize": 10,
                "latitude": 39.1,
                "duration": 890
            },
            {
                "date": "2012-01-12",
                "distance": 534,
                "townName": "Denver",
                "townName2": "Denver",
                "townSize": 18,
                "latitude": 39.74,
                "duration": 810
            },
            {
                "date": "2012-01-13",
                "townName": "Salt Lake City",
                "townSize": 12,
                "distance": 425,
                "duration": 670,
                "latitude": 40.75,
                "alpha": 0.4
            },
            {
                "date": "2012-01-14",
                "latitude": 36.1,
                "duration": 470,
                "townName": "Las Vegas",
                "townName2": "Las Vegas",
                "bulletClass": "lastBullet"
            },
            {
                "date": "2012-01-15"
            },
            {
                "date": "2012-01-16"
            },
            {
                "date": "2012-01-17"
            },
            {
                "date": "2012-01-18"
            },
            {
                "date": "2012-01-19"
            }
        ];
        var chart;

        AmCharts.ready(function () {
            // SERIAL CHART
            chart = new AmCharts.AmSerialChart();
            chart.addClassNames = true;
            chart.dataProvider = chartData;
            chart.categoryField = "date";
            chart.dataDateFormat = "YYYY-MM-DD";
            chart.startDuration = 1;
            chart.color = "#FFFFFF";
            chart.marginLeft = 0;

            // AXES
            // category
            var categoryAxis = chart.categoryAxis;
            categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
            categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
            categoryAxis.autoGridCount = false;
            categoryAxis.gridCount = 50;
            categoryAxis.gridAlpha = 0.1;
            categoryAxis.gridColor = "#FFFFFF";
            categoryAxis.axisColor = "#555555";
            // we want custom date formatting, so we change it in next line
            categoryAxis.dateFormats = [{
                    period: 'DD',
                    format: 'DD'
                }, {
                    period: 'WW',
                    format: 'MMM DD'
                }, {
                    period: 'MM',
                    format: 'MMM'
                }, {
                    period: 'YYYY',
                    format: 'YYYY'
                }];

            // as we have data of different units, we create three different value axes
            // Distance value axis
            var distanceAxis = new AmCharts.ValueAxis();
            distanceAxis.title = "distance";
            distanceAxis.gridAlpha = 0;
            distanceAxis.axisAlpha = 0;
            chart.addValueAxis(distanceAxis);

            // latitude value axis
            var latitudeAxis = new AmCharts.ValueAxis();
            latitudeAxis.gridAlpha = 0;
            latitudeAxis.axisAlpha = 0;
            latitudeAxis.labelsEnabled = false;
            latitudeAxis.position = "right";
            chart.addValueAxis(latitudeAxis);

            // duration value axis
            var durationAxis = new AmCharts.ValueAxis();
            durationAxis.title = "duration";
            // the following line makes this value axis to convert values to duration
            // it tells the axis what duration unit it should use. mm - minute, hh - hour...
            durationAxis.duration = "mm";
            durationAxis.durationUnits = {
                DD: "d. ",
                hh: "h ",
                mm: "min",
                ss: ""
            };
            durationAxis.gridAlpha = 0;
            durationAxis.axisAlpha = 0;
            durationAxis.inside = true;
            durationAxis.position = "right";
            chart.addValueAxis(durationAxis);

            // GRAPHS
            // distance graph
            var distanceGraph = new AmCharts.AmGraph();
            distanceGraph.valueField = "distance";
            distanceGraph.title = "distance";
            distanceGraph.type = "column";
            distanceGraph.fillAlphas = 0.9;
            distanceGraph.valueAxis = distanceAxis; // indicate which axis should be used
            distanceGraph.balloonText = "[[value]] miles";
            distanceGraph.legendValueText = "[[value]] mi";
            distanceGraph.legendPeriodValueText = "total: [[value.sum]] mi";
            distanceGraph.lineColor = "#263138";
            distanceGraph.alphaField = "alpha";
            chart.addGraph(distanceGraph);

            // latitude graph
            var latitudeGraph = new AmCharts.AmGraph();
            latitudeGraph.valueField = "latitude";
            latitudeGraph.id = "g1";
            latitudeGraph.classNameField = "bulletClass";
            latitudeGraph.title = "latitude/city";
            latitudeGraph.type = "line";
            latitudeGraph.valueAxis = latitudeAxis; // indicate which axis should be used
            latitudeGraph.lineColor = "#786c56";
            latitudeGraph.lineThickness = 1;
            latitudeGraph.legendValueText = "[[description]]/[[value]]";
            latitudeGraph.descriptionField = "townName";
            latitudeGraph.bullet = "round";
            latitudeGraph.bulletSizeField = "townSize"; // indicate which field should be used for bullet size
            latitudeGraph.bulletBorderColor = "#786c56";
            latitudeGraph.bulletBorderAlpha = 1;
            latitudeGraph.bulletBorderThickness = 2;
            latitudeGraph.bulletColor = "#000000";
            latitudeGraph.labelText = "[[townName2]]"; // not all data points has townName2 specified, that's why labels are displayed only near some of the bullets.
            latitudeGraph.labelPosition = "right";
            latitudeGraph.balloonText = "latitude:[[value]]";
            latitudeGraph.showBalloon = true;
            latitudeGraph.animationPlayed = true;
            chart.addGraph(latitudeGraph);

            // duration graph
            var durationGraph = new AmCharts.AmGraph();
            durationGraph.id = "g2";
            durationGraph.title = "duration";
            durationGraph.valueField = "duration";
            durationGraph.type = "line";
            durationGraph.valueAxis = durationAxis; // indicate which axis should be used
            durationGraph.lineColor = "#ff5755";
            durationGraph.balloonText = "[[value]]";
            durationGraph.lineThickness = 1;
            durationGraph.legendValueText = "[[value]]";
            durationGraph.bullet = "square";
            durationGraph.bulletBorderColor = "#ff5755";
            durationGraph.bulletBorderThickness = 1;
            durationGraph.bulletBorderAlpha = 1;
            durationGraph.dashLengthField = "dashLength";
            durationGraph.animationPlayed = true;
            chart.addGraph(durationGraph);

            // CURSOR
            var chartCursor = new AmCharts.ChartCursor();
            chartCursor.zoomable = false;
            chartCursor.categoryBalloonDateFormat = "DD";
            chartCursor.cursorAlpha = 0;
            chartCursor.valueBalloonsEnabled = false;
            chart.addChartCursor(chartCursor);

            // LEGEND
            var legend = new AmCharts.AmLegend();
            legend.bulletType = "round";
            legend.equalWidths = false;
            legend.valueWidth = 120;
            legend.useGraphSettings = true;
            legend.color = "#FFFFFF";
            chart.addLegend(legend);

            // WRITE
            chart.write("chartdiv");
        });

        function DropDown(el) {
            this.dd = el;
            this.initEvents();
        }
        DropDown.prototype = {
            initEvents: function () {
                var obj = this;

                obj.dd.on('click', function (event) {
                    $(this).toggleClass('active');
                    event.stopPropagation();
                });
            }
        }
        $(function () {

            var dd = new DropDown($('#dd'));

            $(document).click(function () {
                // all dropdowns
                $('.wrapper-dropdown-2').removeClass('active');
            });

        });        
        function addRow() {
            if (rowNum < 100) {
                rowNum++;
                var row = '<tr id="rowNum' + rowNum + '">\n';
                row = row + '<td><input autocomplete="on" placeholder="Date or empty for now" type="text" name="date" id="date" title="Date of the transaction"></td>';
                row = row + '<td><input autocomplete="on" placeholder="Purpose" type="text" name="purpose" id="purpose" title="Purpose or Source"></td>';
                row = row + '<td><input autocomplete="on" placeholder="Amount" type="number" step="0.01" name="amount" id="amount" title="Amount of the transaction"></td>';
                row = row + '<td style="text-align:center"><input type="checkbox" name="private" id="private" title="This transaction is not to be shown in public budget"></td>';
                row = row + '<td><textarea placeholder="comment" name="comment" id="comment" title="Free comment" rows="2" maxlength="255" wrap="soft"></textarea></td>';
//            row = row + '<td><input  placeholder="comment" type="text" name="comment" id="comment" title="Free comment"></td>'
                row = row + '<td><input  type="button" name="add" id="add" value="+" class="addButton" onclick="addRow();">';
                row = row + '<td><input type="button" value="X" onclick="removeRow(' + rowNum + ');" class="addButton"></td></tr>';
                jQuery('#itemRows').append(row);
            }
        }

        function removeRow(rnum) {
            jQuery('#rowNum' + rnum).remove();
        }