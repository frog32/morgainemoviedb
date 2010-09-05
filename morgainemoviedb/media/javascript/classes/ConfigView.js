
MorgaineMovieDB.view.ConfigView = Ext.extend(MorgaineMovieDB.view.AbstractView,{
  
  constructor: function(config){
    MorgaineMovieDB.view.ConfigView.superclass.constructor.call(this,config);
    this.privilegesNeeded = 'none';
    this.grid = new Ext.grid.GridPanel({
      region:'center',
  		store: new Ext.data.JsonStore({
  			fields: [
  				{name: 'id', type: 'int'},
  				{name: 'path', type: 'string'},
  				{name: 'type', type: 'string'},
  				{name: 'scanMode', type: 'string'}
  			],
  			id:'id'
  		}),
  		columns: [
  			{id:'path', header: 'Path', sortable: true, dataIndex: 'path'},
  			{header: 'type', width: 50, sortable: true, dataIndex: 'type'},
  			{header: 'scanMode', width: 150, sortable: true, dataIndex: 'scanMode'}
  		],
  		sm: new Ext.grid.RowSelectionModel({
  			singleSelect:false,
  			listeners:{
  				selectionchange:{
  				  fn:this.onGridSelect,
  				  scope:this
  				}
  			}
  		}),
  		stripeRows: true,
  		autoExpandColumn: 'path',
  		anchor:'0,0',
  		title: 'Folders',
  		tbar:[{
      	iconCls:'silk-folder_add',
  	    text: 'Add Folder',
  	    scope: this,
  	    handler: this.addFolder
  	  }]
  	});
    
    this.folderDetailView = new MorgaineMovieDB.view.ConfigViewFolderDetail({});

  	this.panel = new Ext.Panel({
  	  title:'Folders',
  	  disabled:'true',
  	  layout:'border',
      listeners:{
        'activate':{
          fn:this.update,
          scope:this
        }
      },
  	  items:[
  	    this.grid,
  	    this.folderDetailView.draw()
  	  ]
  	});
  },
  
  addFolder: function(){
    new MorgaineMovieDB.util.FileSelectWindow({
      listeners:{
        fileSelect:{
          fn:this.onAddFolderSelected,
          scope:this
        }
      }
    });
  },
  
  onAddFolderSelected: function(path){
  	Ext.Ajax.request({
  		url:'config/movieFolderAdd',
  		params:{
  		  dir:path,
  		  type:1
  		},
  		scope:this,
  		success:this.update
  	});
    return false;
  },

  onGridSelect: function(sm){
	  if(sm.getCount()==0 | sm.getCount()>1){
  		this.folderDetailView.setBlank();
  		return true;
  	}
  	this.folderDetailView.setFolder(sm.getSelected().data.id);
	},
    
	onUpdateReceived: function(response){
		var obj=Ext.decode(response.responseText);
		if(!obj.success) return;
		this.grid.store.loadData(obj.data);
	},
	
  update: function(){
  	Ext.Ajax.request({
  		url:'config/movieFolderIndex',
  		method:'post',
  		scope: this,
  		success: this.onUpdateReceived
  	});
  }
});