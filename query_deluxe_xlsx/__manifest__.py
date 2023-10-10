{
        'name': 'PostgreSQL Query Deluxe Excel',
        'description': 'Execute postgreSQL query into Odoo interface',
        'author': 'Yvan Dotet',
        'depends': ['query_deluxe', 'report_xlsx'],
        'auto_install': True,
        'application': False,
        'version': '17.0',
        'license': 'AGPL-3',
        'support': 'yvandotet@yahoo.fr',
        'website': 'https://github.com/YvanDotet/query_deluxe/',
        'installable': True,

        'data': [
            'views/querydeluxe.xml',

            'report/print_xlsx.xml',
            ],
}

