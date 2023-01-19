{
        'name': 'PostgreSQL Query Deluxe',
        'description': 'Execute postgreSQL query into Odoo interface',
        'author': 'Yvan Dotet',
        'depends': ['base', 'mail'],
        'application': True,
        'version': '16.0.1.0.6',
        'license': 'AGPL-3',
        'support': 'yvandotet@yahoo.fr',
        'website': 'https://github.com/YvanDotet/query_deluxe/',
        'installable': True,

        'data': [
            'security/security.xml',
            'security/ir.model.access.csv',

            'views/query_deluxe_views.xml',

            'wizard/pdforientation.xml',

            'report/print_pdf.xml',

            'datas/data.xml'
            ],

        'images': ['static/description/banner.gif']
}

