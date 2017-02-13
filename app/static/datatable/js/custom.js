
function format(d) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>生信完成时间:</td>'+
            '<td>'+d.bioinfo_time+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>索要病理时间</td>'+
            '<td>'+d.ask_histology_time+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>病理更新时间</td>'+
            '<td>d.get_histology_time</td>'+
        '</tr>'+
           '<tr>'+
            '<td>报告完成时间</td>'+
            '<td>d.</td>'+
        '</tr>'+
    '</table>';
}

var editor; // use a global for the submit and return data rendering in the examples
$(document).ready(function() {
    editor = new $.fn.dataTable.Editor( {
        ajax: "{{ url_for('genetron.patientresponse') }}",
        table: "#example",
        fields: [ {
                label: "patient_id:",
                name: "patient_id"
            },
            {
                label: "name:",
                name: "name"
            },
            {
                label: "hospital:",
                name: "hospital"
            },
            {
                label: "panel:",
                name: "panel"
            },
             {
                label: "bioinfo:",
                name: "bioinfo",
                type:  "radio",
                options: [
                    { label: "未完成", value: '' },
                    { label: "完成",  value: true }
                ],
                def: 0
            },
             {
                label: "索要病理:",
                name: "ask_histology",
                type:  "radio",
                options: [
                    { label: "未要", value: '' },
                    { label: "所要",  value: true }
                ],
                def: 0
            },
            {
                label: "histology:",
                name: "histology"
            },
            {
                label: "tissue:",
                name: "tissue"
            },
            {
                label:'Indication',
                name: "indication"
            },

            {
                label:  'Start date:',
                name:   'start_time',
                type:   'datetime',
                def:    function () { return new Date(); },
                format: 'YYYY-M-D',

            },
             {
                label:  'End date:',
                name:   'dead_line',
                type:   'datetime',
                def:    function () { return new Date(); },
                format: 'YYYY-M-D',

            },
            {
                label: "报告完成:",
                name: "is_finish",
                type:  "radio",
                options: [
                    { label: "未完成", value: '' },
                    { label: "完成",  value: true }
                ],
                def: 0
            },
            {
                label: "note:",
                name: "note"
            }

        ]
    } );

 $('#example').on( 'click', 'tbody td:not(:first-child)', function (e) {

        editor.bubble( this );

    } );

    $('#example').DataTable( {
        dom: "Bfrtip",
        ajax: "{{ url_for('genetron.patient_table') }}",
        "order": [[ 11, 'desc' ],[ 10, 'asc' ], [ 4, 'asc' ]],
        "class": "center",
        "pageLength": 20,
        columns: [
//          {
//                "className": 'details-control',
//                "orderable":  false,
//                "data": null,
//                "defaultContent": ''
//            },
            { data: 'patient_id' },
            { data: "name" },
            { data: "hospital" },
            { data: "panel" },
            {
                "class": "center",
                "data": "bioinfo",
                "render": function (val, type, row) {
                    return val == true ? "完成" : "未完成";
                }
            },
            { data: "histology" },
            { data: "tissue" },
            { data: "indication" },
            { data: "start_time" },
            { data: "dead_line" },
            { data: null,
                "render":function(data,type, row){
                    today = new Date()
                    dead_line = new Date(data.dead_line)
                    return Math.round((dead_line-today)/(24*60*60*1000))
                }
            },
            {
                "class": "center",
                "data": "is_finish",
                "render": function (val, type, row) {
                    return val == true ? "完成" : "未完成";
                }
            },
            { data: "note" }

        ],
        select: true,
        buttons: [
            { extend: "create", editor: editor },
            { extend: "edit",   editor: editor },
            { extend: "remove", editor: editor }
        ]
    } );

       $('#example tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );

} );


