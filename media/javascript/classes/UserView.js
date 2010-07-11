
MorgaineMovieDB.view.UserView = Ext.extend(MorgaineMovieDB.view.AbstractView,{
  
  constructor: function(config){
    MorgaineMovieDB.view.UserView.superclass.constructor.call(this,config);
    this.privilegesNeeded = 'admin';

    // events
    this.proxy=new Ext.data.HttpProxy({
      method:'POST',
  		api:{
  			read: 'user/index',
  			create : 'user/create',
  			update: 'user/update',
  			destroy: 'user/destroy'
  		}
  	});
  	this.writer = new Ext.data.JsonWriter({
  		encode: true,
  		writeAllFields: false
  	});
  	this.reader = new Ext.data.JsonReader({
  		totalProperty: 'total',
  		successProperty: 'success',
  		idProperty: 'id',
  		root: 'data',
  		messageProperty: 'message'  // <-- New "messageProperty" meta-data
  	}, [
  		{name: 'id'},
  		{name: 'name', allowBlank: false},
  		{name: 'password'},
  		{name: 'privileges', allowBlank: false},
  		{name: 'localPath'}
  	]);
  	this.store=new Ext.data.Store({
  		id: 'user',
  		restful:false,
  		batch:false,
  		proxy: this.proxy,
  		reader: this.reader,
  		writer: this.writer,
  		autoSave: true
  	});
  	this.editor = new Ext.ux.grid.RowEditor({
  		saveText: 'Update'
  	});


  	this.panel = new Ext.grid.GridPanel({
  		title: 'Users',
  		disabled:true,
  		anchor:'0,0',
  		store: this.store,
  		proxy: this.proxy,
  		columns: [
  			{header: 'UID', width: 50, sortable: true, dataIndex: 'id', editor: new Ext.form.NumberField({disabled:true})},
  			{header: 'Username', width: 100, sortable: true, dataIndex: 'name', editor: new Ext.form.TextField({})},
  			{header: 'Password', width: 100, dataIndex:'password', editor: new Ext.form.TextField({})},
  			{header: 'Privileges', width: 75, dataIndex:'privileges', editor: new Ext.form.ComboBox({
  				store:['none','read','write','admin'],
  				mode:'local',
  				lazyRender: true,
  				listClass: 'x-combo-list-small',
  				triggerAction:'all',
  				editable:false
  			})},
  			{id:'localPath', header: 'Local Path', width: 150, dataIndex:'localPath', editor: new Ext.form.TextField({})}
  		],
  		plugins:[this.editor],
  		tbar: [{
  			text: 'Add',
  			iconCls: 'silk-add',
  			scope: this,
  			handler: this.onAdd
  		}, '-', {
  			text: 'Delete',
  			iconCls: 'silk-delete',
  			scope: this,
  			handler: this.onDelete
  		}, '-'],
  		sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
  		stripeRows: true,
  		autoExpandColumn:'localPath',
  		listeners:{
  		  'activate':{
  		    fn:this.update,
  		    scope:this
  		  }
  		}
  	});
    
  },
  
	onAdd: function(btn, ev) {
		var u = new this.store.recordType({
		});
		this.editor.stopEditing();
		this.store.insert(0, u);
		this.editor.startEditing(0);
	},
	
	onDelete: function() {
		this.editor.stopEditing();
		var rec = this.panel.getSelectionModel().getSelected();
		if (!rec) {
			return false;
		}
		this.store.remove(rec);
	},
	
	update: function(){
	  this.store.load();
	}			
});
