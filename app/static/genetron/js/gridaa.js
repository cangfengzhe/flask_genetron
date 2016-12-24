gridaa = function(url){
    var crudServiceBaseUrl = "//demos.telerik.com/kendo-ui/service"
                    $("#gridd").kendoGrid({
                        dataSource: {
                            transport: {
                                read:  {
                                url: url,
                                dataType: "json" // "jsonp" is required for cross-domain requests; use "json" for same-domain requests
                                },
                                update: {
                                   url: "aaa" + "/Products/Update",
                                    dataType: "jsonp",
                                },
                                destroy: {
                                    url: '/api/cnv/aaa',
                                    type: 'delete',
                                    dataType: "jsonp"
                                },
                                create: {
                                    url: '/api/cnv/aaa',
                                    type: 'post',
                                    dataType: "jsonp"
                                },
                            },
                            schema: {

                            type: 'json',
                            data: "data",
                            total: function(data) {
                                return data.data.length;
                            },
                            model: {
                            id: "DT_RowId",
                                 fields: {
                                    DT_RowId: {type: "string",editable: false},
                                     panel: { type: "string",editable: true },
                                     age: { type: "number", editable: true },
                                     collect_time: { type: "date", editable: true }
                                    }
                                }
                            },
                            sort: {
                                field: "age",
                                dir: "desc"
                            },
                            pageSize: 20,



                        },
                        height: 550,
                        toolbar: ["create"],
                        editable: "popup",
                        scrollable: true,
                        filterable: {
                            extra: false,
                            operators: {
                                string: {
                                    startswith: "Starts with",
                                    eq: "Is equal to",
                                    neq: "Is not equal to"
                                }
                            }
                        },
                        filterable:true,
                        sortable:true,
                        pageable: true,
                        editable: "popup",

                        columns: [
                            {
                                field:"panel",
                                title: "panel",
                                width: 160,
                                filterable: false,

                            },
                            {
                                field: "age",
                                title: "age",
                                width: 130,

                            },
                            {
                                field: "DT_RowId",
                                title: "DT_RowId",

                            },
                            {
                                field: "collect_time",
                                title: "collect time",
                                format: "{0:MM/dd/yyyy HH:mm:ss}",

                            },
                            { command: ["edit", "destroy"], title: "&nbsp;", width: "200px" }
                       ],
                    });

                    }

