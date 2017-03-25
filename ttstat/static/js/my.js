$(document).ready(function(){

    var matchHash = "";

    $('#matches_table').DataTable({
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
        "sAjaxSource": "/_retrieve_matches_data",
        "fnServerParams": function ( aoData ) {
            //aoData.push( { "name":"mySelect", "value": $('#mySelect').find("option:selected").val()});
            if ($('#sourceCheckboxes')) {
                var c = $('.source-checkbox:checkbox:checked')
                var sources = ""
                for (i = 0; i < c.length; i++) {
                    sources += c[i].value + ";";
                }
                aoData.push({ "name":"sources", "value": sources});
            }
        },
        "aoColumnDefs": [{ "bVisible": false, "aTargets": [11] }],
        "order": [[ 0, "desc" ]]
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
            aoData.push( { "name":"matchHash", "value": matchHash});
        },
        "order": [[ 0, "desc" ]]
    });

    $("#matches_table tbody").on('click', 'tr', function(event){
        matchHash = $('#matches_table').DataTable().row(this).data()[11];
        $('#match_bets_table').DataTable().ajax.reload();
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
        "bProcessing": true,
        "bServerSide": true,
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_players_data",
        "fnServerParams": function ( aoData ) {
            aoData.push( { "name":"mySelect", "value": $('#mySelect').find("option:selected").val()});
        },
        "order": [[ 2, "desc" ]]
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
        "sPaginationType": "full_numbers",
        "bjQueryUI": true,
        "sAjaxSource": "/_retrieve_matches_data",
        "fnServerParams": function ( aoData ) {
            if ($('#playerName'))
                aoData.push( { "name":"playerId", "value": $('#playerName').attr("playerId")});
            if ($('#sourceCheckboxes')) {
                var c = $('.source-checkbox:checkbox:checked')
                var sources = ""
                for (i = 0; i < c.length; i++) {
                    sources += c[i].value + ";";
                }
                aoData.push({ "name":"sources", "value": sources});
            }
        },
        "order": [[ 0, "desc" ]],
        "aoColumnDefs": [{ "bVisible": false, "aTargets": [11] }],
    });

    $("#player_matches_table tbody").on('click', 'tr', function(event){
        matchHash = $('#player_matches_table').DataTable().row(this).data()[11];
        $('#match_bets_table').DataTable().ajax.reload();
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
        "columnDefs": [{
        "targets": 0,
        "orderable": false
        }],
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

	return;
//    "bLengthChange": false,
//        "bFilter": false,
//        "columns": [null,{"width": "10%"}, {"width": "10%"}
//                   null, null, null, null, null, null, null, null, null, null, null, null, null
//                   ],

    
	var colors = ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', 
		 '#FF9655', '#FFF263', '#6AF9C4'];
			 
	var grid = document.getElementById('queries');
	var grid1 = 0;
	var q = grid.getElementsByTagName('tbody')[0];
	var last_e = 0;
	var fl_e = 0;
	var rowsArray0 = [];
	var trs = [];
	var chart1 = [];
	var chart2 = [];
	var n = 105;
	var startYear = 2013;
	var startMonth = 6;
	var startDay = 1;
    //alert(q.children.length);
	for(var i = 0; i<q.children.length; i++) {
		rowsArray0.push(q.children[i]);
		trs.push($(q.getElementsByTagName("tr")[i]).attr('q'));
	}
    
	$("tr").click(function (e) {
		var target = e && e.target || window.event.srcElement;
		if (target.tagName == 'TH') 
			return;
	
        var iframe = document.createElement('iframe');
        iframe.rowNum = $(this).attr('rowNum');
        iframe.id = 'iframe';
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        iframe.src = $(this).attr('filename');
        iframe.q = $(this).attr('q');
        iframe.onload = function(){
            //var text = iframe.contentDocument.body.firstChild.innerHTML;
            //alert(iframe.contentDocument.body.children[1]['q']);
            var lines = iframe.contentDocument.body.innerHTML.split('\n');
            s = lines[iframe.rowNum].toString().replace(/"/g, "'");
            s = s.toString().replace(/#/g, '"');
            js = JSON.parse(s);
            
            var sv = js.c.split(" ");
            var sv1 = js.c1.split(" "); 
            var bv = js.bind.split(" "); 
            var pv = js.pind.split(" ");

            var v2 = Array.apply(null, Array(n));
            var tsum = 0;
            var WS = 28;
            for (var i = 0; i < sv1.length; i++)
            {
                tsum += parseFloat(sv1[i]);
                if (i >= WS)
                    tsum = tsum - parseFloat(sv1[i - WS]);
                v2[i] = tsum / WS;
            }
            
            var x = Array.apply(null, Array(n));
            x.map(function (x, i) { return i });

            var y = Array.apply(null, Array(n));
            var y1 = Array.apply(null, Array(n));
            var y2 = Array.apply(null, Array(n));
            var plotBands = Array.apply(null, Array(n));
            
            plotBands[0] = {color: '#FFDDDD', from: 1, to: 1};
            for (var i = 1; i < sv.length; i++)
            {
                var tdate = Date.UTC(startYear, startMonth, startDay + i - 1);
                var tdate1 = Date.UTC(startYear, startMonth, startDay + i);
                if (parseFloat(bv[i]) > 0 && parseFloat(bv[i - 1]) > 0)
                    plotBands[i] = {color: '#FFDDDD', from: tdate, to: tdate1};
                else
                    plotBands[i] = {color: '#FFDDDD', from: tdate, to: tdate};
            }

            var pvCnt = 0;
            for (var i = 0; i < sv.length; i++)
                if (pv[i] == '1')
                    pvCnt++;
            var plotLines = Array.apply(null, Array(pvCnt));
            var pvW = 2;
//            if (pvCnt == 3 || pvCnt == 5)
//                pvW = 3;
//            alert(n);
            var j = 0;
            for (var i = 0; i < sv.length; i++)
            {
                var tdate = Date.UTC(startYear, startMonth, startDay +  i);
                if (parseFloat(bv[i]) > 0) {
                    y[i] = {x: tdate, y : parseFloat(sv[i]), marker: {fillColor: '#FF0000', lineColor: '#FF0000', radius: 2, enabled: true}};
                    y1[i] = {x: tdate, y : parseFloat(sv1[i]), color: '#FF0000'};
                    y2[i] = {x: tdate, y : v2[i], marker: {fillColor: '#FF0000', lineColor: '#FF0000', radius: 1, enabled: true}};
                } else {
                    y[i] = {x: tdate, y : parseFloat(sv[i]), marker: {fillColor: '#666666', lineColor: '#666666', radius: 0.1}};
                    y1[i] = {x: tdate, y : parseFloat(sv1[i]), marker: {fillColor: '#FFFFFF', lineColor: '#EEEEEE', radius: 0}};
                    y2[i] = {x: tdate, y : v2[i], marker: {fillColor: '#FFFFFF', lineColor: '#EEEEEE', radius: 0}};
                }
                
                if (pv[i] == '1') {
                    plotLines[j] = {color : '#0000FF', value: tdate, width: pvW};
                    j++;
                }
//                else
//                    plotLines[i] = {color : '#0000FF', value: tdate, width: 0};
            }

            var series = Array.apply(null, Array(3));
            series[0] = {name: '������', type: 'line', data: y, color: '#777', yAxis: 0, showInLegend: false, turboThreshold: 1500};
            series[1] = {name: '������', type: 'column', data: y1, color: '#CCC', yAxis: 1, id: 'Query', turboThreshold: 1500};
            series[2] = {type: 'line', data: y2, color: '#555', yAxis: 1, linkedTo: 'Query', turboThreshold: 1500};
            texts = ['���� �������������', '�������'];
            draw_chart('#chart_container', iframe.q, x, series, plotBands, plotLines, texts);
            
            $("#docs_info", window.parent.document).html(js.docs);
            $("#docs_info th:eq(4)", window.parent.document).addClass("sort");
            $("#docs_info th:eq(4)", window.parent.document).addClass("down");
            $("#docs_info th:eq(4)", window.parent.document).attr("fl", -1);
            
            grid1 = window.parent.document.getElementById('docs_table');
            sortGrid(grid1, 4, -1, 'number');

            grid1.onclick = function(e) {
                var target = e && e.target || window.event.srcElement;
                if (target.tagName != 'TH') return;

                last_e = e;
                var fl = $(target).attr("fl");

                if (fl_e == 0)
                    if (fl == null) {
                        fl = -1;
                    } else fl = -fl;

                $('#docs_table *').removeAttr('fl');
                $(target).attr("fl", fl);

                $("#docs_table .sort").removeClass()
                $(target).addClass("sort");
                if (fl == 1)
                    $(target).addClass("up");
                else
                    $(target).addClass("down");
                
                sortGrid(grid1, target.cellIndex, fl, target.getAttribute('data-type'));
            };
            
            $("#docs_info td", window.parent.document).click(function (e) {
                var tr = $(this).parent();
                var columnCnt = tr.children().length;
                var ind_td = $("#docs_info td").index($(this));
                if (ind_td % columnCnt > 2)
                    return;
                var s = tr.attr('c');
                var sv = s.split(" ");
                var y = Array.apply(null, Array(n));
                var y1 = Array.apply(null, Array(n));
                var tsum = 0;
                for (var i = 0; i < sv.length; i++)
                {
                    tsum += parseFloat(sv[i]);
                    if (i >= WS)
                        tsum = tsum - parseFloat(sv[i - WS]);
                    var tdate = Date.UTC(startYear, startMonth, startDay + i);
                    y[i] = {x: tdate, y: tsum / WS, marker: {fillColor: '#FFFFFF', lineColor: '#EEEEEE', radius: 0}};
                    y1[i] = {x: tdate, y: parseFloat(sv[i]), marker: {fillColor: '#FFFFFF', lineColor: '#EEEEEE', radius: 0}};
                }
                var chart = $('#chart_container').highcharts();
                indDel = -1;
                var cname = tr.find('td:eq(0)').html()
                var foo = tr.find('td:eq(1)').html();
                if (foo.length > 0)
                    cname = cname + '_' + tr.find('td:eq(1)').html();
                for (var i = 0; i < chart.series.length; i++)
                    if (chart.series[i].name == cname)
                    {
                        indDel = i;
                        chart.series[indDel].remove();
                        break;
                    }
                var ind = ($('#docs_info tr').index(tr) - 1) % colors.length;
                
                if (indDel == -1)
                {
                    chart.addSeries({id: cname, name: cname, data: y, color: colors[ind], yAxis: 1, turboThreshold: 1500}, true);
    //				chart.addSeries({id: cname, name: cname, data: y1, color: colors[ind], yAxis: 1, type: 'column', linkedTo: cname}, true);
                    tr.children('td:eq(0),td:eq(1),td:eq(2)').css('color',colors[ind]);
                }
                else
                {
                    tr.children('td:eq(0),td:eq(1),td:eq(2)').css('color','#666');
                }
            });

        };

	});
    
	$("#text_filter").val("");
	$("#tags_filter").val("");
	$("#freq_filter").val("0");
	$('#M1').attr('checked','checked');
	$('#M3').attr('checked','checked');
	$('#M6').attr('checked','checked');
	$('#M12').attr('checked','checked');
	$('#M_OR').attr('checked','checked');
	if ($('#M_OR').length != 0)
	{
		$('#leftG').width("35%");
		$('#right').width("62%");
	}
    $("#tags_type").val('-');


//	alert(rowsArray0[0].cells[0].innerHTML);
	$("#filter_button").click(function(e) 
	{
		var s = $('#text_filter').val().toLowerCase();
		var sm1 = "";
		var sm2 = "";
		if ($('#tags_filter').length != 0) {
			sm1 = $("#tags_type").val();
			sm2 = $('#tags_filter').val().toLowerCase();
		}
        sm1 = sm1.trim();
        sm2 = sm2.trim();
		var freq = $('#freq_filter').val();		
		var rowsArray = [];
		for(var i = 0; i<rowsArray0.length; i++) {
			var s1 = trs[i].toLowerCase();
			var indFreq = 4;
			var s2 = sm1 + ' ' + sm2;
			if ($('#tags_filter').length != 0)
			{
				indFreq = 4;
				s2 = rowsArray0[i].cells[2].title;//innerHTML.toLowerCase();
			}
			if (s1.indexOf(s) != -1 && s2.indexOf(sm1) != -1 && s2.indexOf(sm2) != -1 && (rowsArray0[i].cells[indFreq].innerHTML - freq >= 0 || $('#freq_filter').length == 0))
			{
				pers = rowsArray0[i].cells[3].innerHTML;
				fl = 0;
				if ($('#M_OR').attr('checked') == "checked")
				{
					if (pers.indexOf("�����") != -1 && ($('#M1').attr('checked') == "checked"))
						fl = 1;
					if (pers.indexOf("�������") != -1 && ($('#M3').attr('checked') == "checked"))
						fl = 1;
					if (pers.indexOf("�������") != -1 && ($('#M6').attr('checked') == "checked"))
						fl = 1;
					if (pers.indexOf("���") != -1 && ($('#M12').attr('checked') == "checked"))
						fl = 1;
				}
				if ($('#M_AND').attr('checked') == "checked")
				{
					fl = 1;
					if (pers.indexOf("�����") == -1 && ($('#M1').attr('checked') == "checked"))
						fl = 0;
					if (pers.indexOf("�������") == -1 && ($('#M3').attr('checked') == "checked"))
						fl = 0;
					if (pers.indexOf("�������") == -1 && ($('#M6').attr('checked') == "checked"))
						fl = 0;
					if (pers.indexOf("���") == -1 && ($('#M12').attr('checked') == "checked"))
						fl = 0;
				}
				if (fl == 1 || $('#M_OR').length == 0)
					rowsArray.push(rowsArray0[i]);
			}
		}

//		alert(s);
		
		var tbody = grid.getElementsByTagName('tbody')[0];
		grid.removeChild(tbody);

	// ������ TR �� TBODY.
	// ������������ tbody.innerHTML = '' �� �������� � IE
	// 
	// �� ����� ���� ��� ���� ����� ����� ��������! 
	// ��� ���������� appendChild ��� ���� ����� ���� ���������� �� ���������� �����!
		while(tbody.firstChild) {
			tbody.removeChild(tbody.firstChild);
		}

		// �������� ��������� � ������ ������� � TBODY
		for(var i=0; i<rowsArray.length; i++) {
			tbody.appendChild(rowsArray[i]);
		}

		grid.appendChild(tbody);
		if (last_e != 0)
		{
			fl_e = 1;
			grid.onclick(last_e);
			fl_e = 0;
		}
	});

    $("#text_filter").keydown(function(e) {
        if (e.keyCode == 13) {
			$("#filter_button").click();
        }
    });
    $("#freq_filter").keydown(function(e) {
        if (e.keyCode == 13) {
			$("#filter_button").click();
        }
    });
    $("#tags_filter").keydown(function(e) {
        if (e.keyCode == 13) {
			$("#filter_button").click();
        }
    });
    $("#tags_type").change(function(e) {
        $("#filter_button").click();
    });
    $(".themes").mouseover(function(e) {
    });
	
    /*
	grid.onclick = function(e) {
		var target = e && e.target || window.event.srcElement;
		if (target.tagName != 'TH') return;

		last_e = e;
		var fl = $(target).attr("fl");

		if (fl_e == 0)
			if (fl == null) {
				fl = -1;
			} else fl = -fl;

		$('#queries *').removeAttr('fl');
		$(target).attr("fl", fl);

		$("#queries .sort").removeClass()
		$(target).addClass("sort");
		if (fl == 1)
			$(target).addClass("up");
		else
			$(target).addClass("down");
		
		sortGrid(grid, target.cellIndex, fl, target.getAttribute('data-type'));
	};
	*/
//        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
//        "paging":  false,
    
	function sortGrid(grid, colNum, fl, type) {
		var tbody = grid.getElementsByTagName('tbody')[0];
	// ��������� ������ �� TR
		var rowsArray = [];
		for(var i = 0; i<tbody.children.length; i++) {
			rowsArray.push(tbody.children[i]);
		}
		// ���������� ������� ���������, � ����������� �� ����
		var compare;

		switch(type) {
		  case 'number':
			compare = function(rowA, rowB) {
				if (fl == 1)
					return rowA.cells[colNum].innerHTML - rowB.cells[colNum].innerHTML;
				else
					return rowB.cells[colNum].innerHTML - rowA.cells[colNum].innerHTML;
			};
			break;
		  case 'string':
			compare = function(rowA, rowB) {
			if (fl == 1)
				return rowA.cells[colNum].innerHTML > rowB.cells[colNum].innerHTML ? 1 : -1;
			else
				return rowB.cells[colNum].innerHTML > rowA.cells[colNum].innerHTML ? 1 : -1;
			};
			break;
		}

	// �����������
		rowsArray.sort(compare);

	// ������ tbody �� �������� DOM ��������� ��� ������ ������������������
		grid.removeChild(tbody);

	// ������ TR �� TBODY.
	// ������������ tbody.innerHTML = '' �� �������� � IE
	// 
	// �� ����� ���� ��� ���� ����� ����� ��������! 
	// ��� ���������� appendChild ��� ���� ����� ���� ���������� �� ���������� �����!
		while(tbody.firstChild) {
			tbody.removeChild(tbody.firstChild);
		}

		// �������� ��������� � ������ ������� � TBODY
		for(var i=0; i<rowsArray.length; i++) {
			tbody.appendChild(rowsArray[i]);
		}

		grid.appendChild(tbody);
	}

    $('#queries').DataTable({
        "scrollY": "200px",
        "scrollCollapse": true,
        "scrollX": "99.7%",
        "bFilter": false,
        "bLengthChange": false,
        "fixedHeader": true,
        "lengthMenu": [[100], [100]],
        "columns": [
            { "type": "num"},
            null,
            null,
            { "type": "num"},
            { "type": "num"},
            { "type": "num"},
            { "type": "num"},
            { "type": "num"},
            { "type": "num"},
            { "type": "num"},
            { "type": "num"},
            null,
            { "type": "num"},
        ]
    });
    
});

function draw_chart(container, name, x, seriesY, plotBands, plotLines, text) {
	$(container).highcharts({
		chart: {
			marginRight: 150,
			marginBottom: 50,
			backgroundColor: '#FFF'
		},
		scrollbar: {
			enabled: true,
			haight: 10,
			margin: 0
		},
		navigator: {
			enabled: true,
			haight: 10,
			margin: 0
		},
		title: {
			text: name,
			margin: 1,
			style: {
				fontSize: '14px'
			}
//			x: -20 //center
		},
		subtitle: {
			//text: '',
			x: -20
		},
		xAxis: {
			type: 'datetime',
			gridLineWidth: 1,
//			tickInterval: 30 * 24 * 3600 * 1000,
//			categories: x,
			labels: {
//				step: 10,
				rotation: -25,
				align: 'right'
			},
			title: {
				text: 'Time'
			},
			tickmarkPlacement: 'on',
			plotBands: plotBands,
			plotLines: plotLines
		},
		yAxis: [
			{
				min: 0,
	//			max: maxy,
				title: {
					text: text[0]
				},
				height: '45%',
				plotLines: [{
					value: 0,
					width: 1,
					color: '#000000'
				}]
				
			},
			{
				min: 0,
	//			max: maxy,
				title: {
					text: text[1]
				},
				top: '55%',
				height: '45%',
                offset: 0,
				plotLines: [{
					value: 0,
					width: 1,
					color: '#000000'
				}]
				
			}
		],
//		colors: [
//			'#666666'
//		],
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'top',
			x: 0,
			y: 100,
			borderWidth: 0,
			itemStyle: {
				fontSize: '10px'
			}
		},
		plotOptions: {
			line: {
//				lineColor: '#666666',
				lineWidth: 2,
				marker: {
					lineWidth: 2,
//					lineColor: '#666666'
				}
			}
		},
		series: seriesY
	});
}