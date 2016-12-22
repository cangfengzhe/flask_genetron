 $("#snp_indel").kendoGrid({
                        toolbar: ["excel"],
                        excel: {
                            allPages: true
                            },
                        dataSource: {
                            transport: {
                                read:  {
                                url: "{{ url_for('genetron.sample_table') }}",
                                dataType: "json" // "jsonp" is required for cross-domain requests; use "json" for same-domain requests
                                }
                            },
                            schema: {

                            type: 'json',
                            data: "data",
                            total: function(data) {
                                return data.data.length;
                            },
                            model: {
                                 fields: {
                                     id: { type: "string" },
                                     name: { type: "string" },
                                     hospital: { type: "string" },
                                     panel: { type: "string" },
                                     blts: { type: "string" },
                                     tumor: { type: "string" },
                                     tissue: { type: "string" },
                                     collect_time: { type: "date" },
                                     accept_time: { type: "date" },
                                     class_time: { type: "date" },
                                     submit_time: { type: "date" },
                                     bioinfo_time: { type: "date" },
                                     bioinfo_report_time: { type: "date" },
                                     ask_histology_time: { type: "date" },
                                     get_histology_time: { type: "date" },
                                     is_finish_time: { type: "date" },
                                     end_time: { type: "date" },
                                     xj_time: { type: "date" },
                                     note: { type: "string" },
                                     
                                    }
                                }
                            },
                            sort: {
                                field: "class_time",
                                dir: "desc"
                            },
                            pageSize: 20,



                        },
     //                   height: 800,
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
                        columns: [
                            {
                                field:"sample_id",
                                title: "ID",
                                width: 100,
                                filterable: true,

                            },
                            {
                                field:"name",
                                title: "姓名",
                                width: 80,
                                filterable: true,

                            },
                            {
                                field:"panel",
                                title: "panel",
                                width: 120,
                                filterable: true,
                                

                            },
                            {
                                field:"indication",
                                title: "病理提示",
                                width: 160,
                                filterable: true,

                            },
                            {
                                field:"tumor",
                                title: "癌种",
                                width: 100,
                                filterable: true,

                            },
                            {
                                field:"tissue",
                                title: "组织",
                                width: 200,
                                filterable: true,

                            },
                            {
                                field:"collect_time",
                                title: "采样时间",
                                width: 100,
                                filterable: true,
                                format: "{0:yyyy-MM-dd}",

                            },
                            {
                                field:"accept_time",
                                title: "收样时间",
                                width: 100,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field:"xj_time",
                                title: "下机时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field:"class_time",
                                title: "分类时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field:"submit_time",
                                title: "提交时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field: "bioinfo_time",
                                title: "生信完成时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field: "bioinfo_report_time",
                                title: "生信报告时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field: "ask_histology_time",
                                title: "索要病理时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field: "get_histology_time",
                                title: "更新病理时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            },
                            {
                                field: "is_finish_time",
                                title: "完成时间",
                                width: 160,
                                filterable: true,
                                format: "{0:yyyy-MM-dd HH:mm:ss}",

                            }, 
                            {
                                field: "end_time",
                                title: "截止日期",
                                width: 100,
                                filterable: true,
                                format: "{0:yyyy-MM-dd}",

                            }, 
                              {
                                field: "note",
                                title: "备注",
                                width: 130,

                            },
                           
                       ],
                    });

                function titleFilter(element) {
                    element.kendoAutoComplete({
                        dataSource: titles
                    });
                }

                function cityFilter(element) {
                    element.kendoDropDownList({
                        dataSource: cities,
                        optionLabel: "--Select Value--"
                    });
                    
                }