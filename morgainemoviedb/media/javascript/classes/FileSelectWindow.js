MorgaineMovieDB.util.FileSelectWindow = Ext.extend(Ext.util.Observable,{
  constructor: function(config){
    this.addEvents('fileSelect');
    this.listeners=config.listeners;
    MorgaineMovieDB.util.FileSelectWindow.superclass.constructor.call(this,config);
    this.tree = new Ext.tree.TreePanel({
        animate:true,
        autoScroll:true,
        root:{
          nodeType: 'async',
          text: '/',
          draggable: false,
          expanded:true,
          id: 'rootnode'
        },
        //rootVisible: false,
        loader: new Ext.tree.TreeLoader({
            dataUrl:'config/filesystemFolderIndex'
        }),
        containerScroll: true,
        border: false,
        border:true,
        autoScroll:true
    });
    
    this.win = new Ext.Window({
			layout:'fit',
			title:'Select a File',
//			autoScroll:true,
			width:400,
			height:500,
			closeAction:'destroy',
			plain: true,
			items:[
			  this.tree
			],
			buttons: [{
				text: 'Select',
				scope:this,
				handler:this.onSelect
			}]
		});
		this.win.show(); 
  },
  
  close: function(){
    this.win.destroy();
  },
  
  onSelect: function(){
    if(this.tree.getSelectionModel().getSelectedNode() == null)
      return;
    this.fireEvent('fileSelect',this.tree.getSelectionModel().getSelectedNode().attributes.id);
    this.close(); 
  }
});