{
        'name': 'Addons xlsx Query Deluxe',
        'description': 'Addons for printing SQL queries on XLSX report',
        'author': 'Yvan Dotet',
        'depends': ['query_deluxe', 'report_xlsx'],
        'application': False,
        'version': '15.0.0.0.0',
        'license': 'AGPL-3',
        'support': 'yvandotet@yahoo.fr',
        'website': 'https://github.com/YvanDotet/',
        'installable': True,

        'data': [
            'views/query_deluxe_views.xml',
            'report/print_xlsx.xml',
            ],
}
