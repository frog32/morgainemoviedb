
var moviePanel = new MorgaineMovieDB.view.MovieView({});
//var userPanel = new MorgaineMovieDB.view.UserView({});
//var configPanel = new MorgaineMovieDB.view.ConfigView({});
var bottomToolbar = new MorgaineMovieDB.view.BottomToolbarView({});

var currentUser = new MorgaineMovieDB.model.User({});

// register updatePrivileges Callbacks
//currentUser.addListener('authenticationUpdate',userPanel.updatePrivileges, userPanel);
//currentUser.addListener('authenticationUpdate',configPanel.updatePrivileges, configPanel);
currentUser.addListener('authenticationUpdate',bottomToolbar.updatePrivileges, bottomToolbar);

Ext.onReady(function(){
	
	var viewport = new Ext.Viewport({
		layout: 'border',
		items:[/*{
			region:'north',
			height:50,
			title:'Morgaine Movie Database',
			items:[searchPanel.panel]
		},*/{
			region:'south',
			height:28,
			items:[bottomToolbar.draw()]
		},{
  		region:'center',
  		xtype:'tabpanel',
  		activeTab:0,
  		items:[moviePanel.draw()/*,configPanel.draw(),userPanel.draw()*/]		  
		}]
	});
		
	// global listeners
	Ext.Ajax.on('beforerequest',bottomToolbar.addRequest, bottomToolbar);
	Ext.Ajax.on('requestcomplete', bottomToolbar.delRequest, bottomToolbar);
//	Ext.Ajax.on('requestcomplete', function(conn,response){
//		var obj=Ext.decode(response.responseText);
//		if(obj.success!=true & obj.length==null){
//			Ext.MessageBox.alert('Error',obj.message);
//		}else{
//			if(obj.message){
//				bottomToolbar.statusPanelMessage(obj.message);
//			}
//		}
//	}, this);
	Ext.Ajax.on('requestexception', function(){Ext.MessageBox.alert('Error','ERROR: Serverrequest not possible.');}, this);
	
});
