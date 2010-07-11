/*  MovieView
    serverRequests:
      movieView/get -> getContents of the movieView
      
*/
MorgaineMovieDB.view.AbstractView = Ext.extend(Ext.util.Observable,{
  constructor: function(config){
    MorgaineMovieDB.view.AbstractView.superclass.constructor.call(this,config);
    this.privilegesNeeded = 'none';
  },    
	
  update: function(){
  },
  
  updatePrivileges: function(){
    this.panel.setDisabled(!currentUser.hasPrivilege(this.privilegesNeeded));	  
	},
  
  draw: function(){
    return this.panel;
  }
  
	
});