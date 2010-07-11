MorgaineMovieDB.view.BottomToolbarView = Ext.extend(MorgaineMovieDB.view.AbstractView,{
  constructor: function(config){
    MorgaineMovieDB.view.BottomToolbarView.superclass.constructor.call(this,config);
    
    this.pendingRequestCount=0;

  	this.loginButton=new Ext.Button({
    	text:'Login',
    	iconCls:'silk-key',
    	handler:function(){currentUser.showLoginWindow();}
    });
    this.logoutButton=new Ext.Button({
    	disabled:true,
    	text:'Logout',
    	iconCls:'silk-door',
    	handler:function(){currentUser.deauthenticate();}
    });
    this.busy=new Ext.Toolbar.TextItem('<img src="include/extjs/resources/images/default/grid/loading.gif" />');
    this.statusPanel=new Ext.Toolbar.TextItem('');
    this.countPanel=new Ext.Toolbar.TextItem('');
    this.panel=new Ext.Toolbar({
    	items:[
    		this.busy,
    		this.statusPanel,'->',
    		this.countPanel,{xtype:'spacer',width:100},
    		this.loginButton,' ',
    		this.logoutButton
    	]
    });
  },
  
  addRequest: function(){
    this.pendingRequestCount++;
    this.busy.show();
  },
  
  delRequest: function(){
    if(--this.pendingRequestCount)
      this.busy.hide();
  },
  
  statusPanelMessage: function(message){
    this.statusPanel.setText(message);
    (function(){this.statusPanel.setText('');}).defer(2000, this);
  },
  
  updatePrivileges: function(){
    this.loginButton.setDisabled(currentUser.authenticated);	  
    this.logoutButton.setDisabled(!currentUser.authenticated);	  
  }
	
});