{
        'name': 'PostgreSQL Query Deluxe',
        'description': 'Execute postgreSQL query into Odoo interface',
        'author': 'Yvan Dotet',
        'depends': ['base', 'mail'],
        'application': True,
        'version': '17.0.0.4',
        'license': 'AGPL-3',
        'support': 'yvandotet@yahoo.fr',
        'website': 'https://github.com/YvanDotet/query_deluxe/',
        'installable': True,

        'data': [
            'security/security.xml',
            'security/ir.model.access.csv',

            'views/querydeluxe.xml',

            'wizard/pdforientation.xml',

            'report/print_pdf.xml',

            'datas/data.xml'
            ],

        'images': ['static/description/banner.gif']
}

