{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Module for managing library books',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
    ],
    'installable': True,
    'application': True,
}
