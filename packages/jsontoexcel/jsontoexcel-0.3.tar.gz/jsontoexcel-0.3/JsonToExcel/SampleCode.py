from jsontoexcel import JsonToExcel

workbook=JsonToExcel("example_jsontoexcel")

data = json.dumps([
    {
        "name": "Mary",
        "age": 21,
        "subjects": [
            {
                "marks": 80,
                "project": "not submitted"
            },
            {
                "marks": 97,
                "project": "submitted"
            },
            {
                "marks": 88,
                "project": "submitted"
            }
        ],
        "graduated": True
    },
    {
        "name": "Matt",
        "age": 22,
        "subjects": [
            {
                "marks": 69,
                "project": "not submitted"
            },
            {
                "marks": 73,
                "project": "submitted"
            },
            {
                "marks": 75,
                "project": "not submitted"
            }
        ],
        "graduated": False
    }
])


workbook.createSheet("sheet1", data)
workbook.closeWorkbook()
