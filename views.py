# morgainemoviedb -- a tool to organize your local movies
# Copyright 2010 Marc Egli
#
# This file is part of morgainemoviedb.
# 
# morgainemoviedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# morgainemoviedb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with morgainemoviedb.  If not, see <http://www.gnu.org/licenses/>.

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