from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    context = {
        'stylesheets':[
            'javascript/extjs/resources/css/ext-all.css',
        	'javascript/extjs/resources/css/xtheme-blue.css',
        	'css/silk.css',
        	'css/style.css',
        ],
        'javascripts':[
            'javascript/extjs/adapter/ext/ext-base.js',
            'javascript/extjs/ext-all.js',
            'javascript/extjs/plugins/Ext.ux.RowEditor.js',
            'javascript/extjs/plugins/Ext.ux.DDView.js',
            'javascript/script.js',
            'javascript/templates.js',	
            'javascript/classes/FileSelectWindow.js',
            'javascript/classes/AbstractView.js',
            'javascript/classes/MovieView.js',
            'javascript/classes/MovieViewDetail.js',
            #'javascript/classes/ConfigView.js',
            #'javascript/classes/ConfigViewFolderDetail.js',
            'javascript/classes/BottomToolbarView.js',
            #'javascript/classes/UserView.js',
            'javascript/classes/User.js',
            'javascript/init.js',
        ]
    }
    return render_to_response(
        'app.html',
        context,
        context_instance = RequestContext(request),
    )