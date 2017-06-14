$(document).ready(function(){

    var matchHash = "";

    $('#matches_table').DataTable({
        "sScrollY": "50vh",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "bLengthChange": false,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_matches_data",
        "oLanguage": {
          "sSearch": "Фильтр по игроку"
        },
        "fnServerParams": function ( aoData ) {
            //aoData.push( { "name":"mySelect", "value": $('#mySelect').find("option:selected").val()});
            /*
            if ($('#sourceCheckboxes')) {
                var c = $('.source-checkbox:checkbox:checked')
                var sources = ""
                for (i = 0; i < c.length; i++) {
                    sources += c[i].value + ";";
                }
                aoData.push({ "name":"sources", "value": sources});
            }
            */
            aoData.push( { "name":"playerInfo", "value": "0"});
            var filters = $('#matches_filters .kv');
            for (i = 0; i < filters.length; i++) {
                //alert($(filters[i]).attr("key") + " = " + $(filters[i]).attr("value"));
                aoData.push({ "name":$(filters[i]).attr("key"), "value": $(filters[i]).attr("value")});
            }
        },
//        "columnDefs": [
//            {"targets": [1,2,3,4,5,6], "orderable": false}],
        "aoColumnDefs": [{"aTargets": [7], "bVisible": false},{"aTargets": [0,1,2,3,4,5,6], "orderable": false}],
        "order": [[ 0, "desc" ]]
    });

    $('.filter_clear').on('click', function(e) {
        //$(this).parent().html("");
        //alert($(this).attr('id'));
        if ($(this).attr('id').indexOf("compId") != -1) {
            window.location.href = removeParam('compId', document.location.href);
        } else if ($(this).attr('id').indexOf("playerId") != -1) {
                window.location.href = removeParam('playerId', document.location.href);
        } else {
            if ($(this).attr('id').indexOf("sourceId") != -1)
                window.location.href = removeParam('sourceId', document.location.href);
        }
    });

    $('#match_bets_table').DataTable({
        "sScrollY": "300px",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "searching": false,
        "paging": false,
        "sAjaxSource": "/_retrieve_match_bets_data",
        "fnServerParams": function ( aoData ) {
            //alert($("#matchHash"));
            if ($("#matchHash")) {
                matchHash = $("#matchHash").attr("hash");
            }
            aoData.push( { "name":"matchHash", "value": matchHash});
        },
        "aoColumnDefs": [{"aTargets": [0,1,2,3,4,5,6], "orderable": false}],
        "order": [[ 0, "asc" ]]
    });

/*    $('a.playerSearchIcon').click(function(event) {
        alert($this.html());
    });
*/

    $(document).on('click','.matchFilter',function(e){
        var playerId = $(this).attr('playerId');
        var compId = $(this).attr('compId');
        var sourceId = $(this).attr('sourceId');
        if (playerId) {
            var hr = removeParam('playerId', document.location.href);
            if (hr.indexOf('?') == -1)
                hr += "?"
            else
                hr += '&'
            window.location.href = hr + 'playerId=' + playerId;
        }
        if (compId) {
            var hr = removeParam('compId', document.location.href);
            if (hr.indexOf('?') == -1)
                hr += "?"
            else
                hr += '&'
            window.location.href = hr + 'compId=' + compId;
        }
        if (sourceId) {
            var hr = removeParam('sourceId', document.location.href);
            if (hr.indexOf('?') == -1)
                hr += "?"
            else
                hr += '&'
            window.location.href = hr + 'sourceId=' + sourceId;
        }
    });

    $("#matches_table tbody").on('click', 'td', function(event){
        if ($(this).index() == 6) {
            matchHash = $('#matches_table').DataTable().row(this).data()[7];
            //$('#match_bets_table').DataTable().ajax.reload();
        }
        if ($(this).index() == 4) {
            var mHash = $('#matches_table').DataTable().row(this).data()[7];
            window.open(document.location.href.split("?")[0] + "/" + mHash, '_blank');
        }
    });

    $('.source-checkbox:checkbox').on('change', function(){
        $('#matches_table').DataTable().ajax.reload();
    });

    $('#players_table').DataTable({
        "sScrollY": "300px",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "fixedHeader": true,
        "bLengthChange": false,
        "bProcessing": true,
        "bServerSide": true,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_players_data",
        "oLanguage": {
          "sSearch": "Фильтр по игроку"
        },
        "fnServerParams": function ( aoData ) {
            //aoData.push( { "name":"mySelect", "value": $('#mySelect').find("option:selected").val()});
        },
        "order": [[ 2, "desc" ]]
    });

    $('#competitions_table').DataTable({
        "sScrollY": "300px",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "fixedHeader": true,
        "bLengthChange": false,
        "bProcessing": true,
        "bServerSide": true,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_competitions_data",
        "oLanguage": {
          "sSearch": "Фильтр по названию"
        },
        "fnServerParams": function ( aoData ) {
            //aoData.push( { "name":"mySelect", "value": $('#mySelect').find("option:selected").val()});
            var filters = $('#matches_filters .kv');
            for (i = 0; i < filters.length; i++) {
                //alert($(filters[i]).attr("key") + " = " + $(filters[i]).attr("value"));
                aoData.push({ "name":$(filters[i]).attr("key"), "value": $(filters[i]).attr("value")});
            }
        },
        "order": [[ 0, "desc" ]]
    });


    $('#player_matches_table').DataTable({
        "sScrollY": "300px",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "bLengthChange": false,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_matches_data",
        "oLanguage": {
          "sSearch": "Фильтр по игроку"
        },
        "fnServerParams": function ( aoData ) {
            aoData.push( { "name":"playerInfo", "value": "1"});
            if ($('#playerName'))
                aoData.push( { "name":"player0Id", "value": $('#playerName').attr("playerId")});

                var filters = $('#matches_filters .kv');
                for (i = 0; i < filters.length; i++) {
                    //alert($(filters[i]).attr("key") + " = " + $(filters[i]).attr("value"));
                    aoData.push({ "name":$(filters[i]).attr("key"), "value": $(filters[i]).attr("value")});
                }
            /*
            if ($('#sourceCheckboxes')) {
                var c = $('.source-checkbox:checkbox:checked')
                var sources = ""
                for (i = 0; i < c.length; i++) {
                    sources += c[i].value + ";";
                }
                aoData.push({ "name":"sources", "value": sources});
            }
            */
        },
        "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
            if (aData[4][0] > aData[4][2])
                $('td:eq(4)', nRow).addClass('winScore');//css('background-color', '#EFC');
            if (aData[4][0] < aData[4][2])
                $('td:eq(4)', nRow).addClass('loseScore');//css('background-color', '#FDC');
        },
        "aoColumnDefs": [{"aTargets": [7], "bVisible": false},{"aTargets": [0,1,2,3,4,5,6], "orderable": false}],
        "order": [[ 0, "desc" ]]
    });

    $("#player_matches_table tbody").on('click', 'td', function(event){
        if ($(this).index() == 6) {
            var matchHash = $('#player_matches_table').DataTable().row(this).data()[7];
            $('#match_bets_table').DataTable().ajax.reload();
        }
        if ($(this).index() == 4) {
            var matchHash = $('#player_matches_table').DataTable().row(this).data()[7];
            window.open(document.location.href.split("/players")[0] + "/matches/" + matchHash, '_blank');
        }
    });

    $('.source-checkbox:checkbox').on('change', function(){
        $('#player_matches_table').DataTable().ajax.reload();
    });

    $('#player_rankings_table').DataTable({
        "sScrollY": "300px",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_player_rankings_data",
        "fnServerParams": function ( aoData ) {
            if ($('#playerName'))
                aoData.push( { "name":"playerId", "value": $('#playerName').attr("playerId")});
        },
        "order": [[ 0, "desc" ]]
    });

    var date_input=$('input[name="date"]'); //our date input has the name "date"
          var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
          var options={
            format: 'yyyy-mm-dd',
            container: container,
            "setDate": new Date(),
            todayHighlight: true,
            autoclose: true,
            weekStart: 1,
            language: "ru",
            orientation: "top",
            daysOfWeekHighlighted: "6",
          };
    date_input.datepicker(options);
    date_input.datepicker("setDate", new Date());

    $('#date').on('click', function(e){
        $('input[name="date"]').focus();
    });
    $('#calendar').on('click', function(e){
        $('#date').click();
    });

    $('#rankings_table').DataTable({
        "sScrollY": "300px",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_rankings_data",
        "fnServerParams": function ( aoData ) {
            if ($('#playerName'))
                aoData.push( { "name":"playerId", "value": $('#playerName').attr("playerId")});
            if ($('#rankingsSex'))
                aoData.push( { "name":"rankingsSex", "value": $('#rankingsSex').attr("sex")});
            aoData.push( { "name":"rankingDate", "value": $('#date').val()});
        },
        "columnDefs": [
            {"targets": 0, "orderable": false},
            {"orderSequence": [ "desc", "asc"], "targets": [3,4,5,6]}],
        "order": [[ 5, "desc" ]]
    });

    date_input.datepicker().on('changeDate', function (ev) {
        //alert($('#date').val());
        $('#rankings_table').DataTable().ajax.reload();
    });

    $('#players_table').on('click', 'tr', function(e){
        var playerId = $(this).find('td').first().html();
        $.ajax({
            url:'/selectPlayer',
            data: {'playerId': playerId},
            type: 'POST',
            success: function(response) {
                console.log(response);
                rjs = JSON.parse(response);
                if ($('#player1Id').html() == "_") {
                    $('#player1Id').html(rjs.playerId);
                    $('#player1Name').html(rjs.playerName);
                    $('#player1R').html(rjs.playerR);
                } else if ($('#player2Id').html() == "_"){
                    $('#player2Id').html(rjs.playerId);
                    $('#player2Name').html(rjs.playerName);
                    $('#player2R').html(rjs.playerR);
                }
                //alert(rjs.player1Name);
            },
            error: function(error) {
                console.log(error);
            }
        });
//        alert(selected);
//        $('#players').DataTable().ajax.reload();
    });

    $('.player_clear').on('click', function(e) {
        $(this).parent().find('h5').html("_");
        $('#prognosis').html("_");
    });

    $('#prognosis_button').on('click', function(e){
        var playerId1 = $('#player1Id').html();
        var playerId2 = $('#player2Id').html();
        if (playerId1 != "_" & playerId2 != "_") {
            $.ajax({
                url:'/makePrognosis',
                data: {'playerId1': playerId1, 'playerId2': playerId2},
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    rjs = JSON.parse(response);
                    $('#prognosis').html(rjs.pred);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });
//        alert(selected);
//        $('#players').DataTable().ajax.reload();

    function removeParam(key, sourceURL) {
        var rtn = sourceURL.split("?")[0],
            param,
            params_arr = [],
            queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
        if (queryString !== "") {
            params_arr = queryString.split("&");
            for (var i = params_arr.length - 1; i >= 0; i -= 1) {
                param = params_arr[i].split("=")[0];
                if (param === key) {
                    params_arr.splice(i, 1);
                }
            }
            if (params_arr.length > 0) {
                rtn = rtn + "?" + params_arr.join("&");
            }
        }
        return rtn;
    }

    //$("#select-yourself").selectize.on('change', function(){
    //    alert($('#select-yourself').selectize().);
    //});

    var liveTable = $('#live_table').DataTable({
        "sScrollY": "50vh",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "searching": false,
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "bLengthChange": false,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_live_data",
        "aoColumnDefs": [{"aTargets": [7], "bVisible": false}, {"aTargets": [0,1,2,3,4,5,6], "orderable": false}],
        "order": [[ 0, "desc" ]]
    });

    setInterval( function () {
            liveTable.ajax.reload();
        }, 15000);

    $("#live_table tbody").on('click', 'td', function(event){
        if ($(this).index() >= 5) {
            var mHash = $('#live_table').DataTable().row(this).data()[7];
            window.open(document.location.href.split("?")[0] + "/" + mHash, '_blank');
        }
    });


    var liveFinishedTable = $('#live_finished_table').DataTable({
        "sScrollY": "50vh",
        "bScrollCollapse": true,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "scrollCollapse": false,
        "lengthMenu": [[1000], [1000]],
        "searching": false,
        "fixedHeader": true,
        "bProcessing": true,
        "bServerSide": true,
        "bLengthChange": false,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_live_finished_data",
        "aoColumnDefs": [{"aTargets": [7], "bVisible": false}, {"aTargets": [0,1,2,3,4,5,6], "orderable": false}],
        "order": [[ 0, "desc" ]]
    });

    setInterval( function () {
            liveFinishedTable.ajax.reload();
        }, 15000);

    /*
    $('.selectPlayer').selectize({
        valueField: 'name',
        labelField: 'name',
        searchField: 'name',
        allowEmptyOption: true,
        options: [],
        create: false,
        score: function() { return function() { return 1; }; },
        onChange: function(value) {
            if (value.length > 0)
                alert(value);
        },
        load: function(query, callback) {
            if (!query.length) return callback();
            var self = this;
            $.ajax({
                url: '/_retrieve_players_names',
                type: 'GET',
                dataType: 'json',
                data: {
                    name: query,
                },
                error: function() {
                    callback();
                },
                success: function(res) {
                    self.clearOptions();
                    callback(res);
                }
            });
        }
    });
    */
//    $('#selectPlayer1').selectize().setValue("123", true);

});

