MorgaineMovieDB.view.ConfigViewFolderDetail = Ext.extend(MorgaineMovieDB.view.AbstractView,{
  constructor: function(config){
    MorgaineMovieDB.view.ConfigViewFolderDetail.superclass.constructor.call(this,config);
    this.folderID=0;

    this.panel = new Ext.Panel({
      title:'Folder Details',
      region:'east',
  		width:550,
  		split:true,
      layout:'form',
      buttons:[{
        text:'Delete Folder'
      },{
        text:'Scan Folder',
        scope:this,
        handler: this.scanDir
      },{
        text:'Export',
        scope:this,
        handler:this.exportDir
      }]
  	});
  },
  
  setFolder: function(folderID){
    this.folderID = folderID;
    this.update();
  },
  
  setBlank: function(){
    this.folderID = 0;
    new Ext.Template('').overwrite(this.panel.body);
  },
  
  exportDir: function(){
  	Ext.Ajax.request({
  		url:'export/folder',
  		timeout:300000,
  		params:{
  		  folderID:this.folderID
  		},
  		scope: this,
  		success:this.onExportReceived
  	});
  },
  
  onExportReceived: function(response){
		var obj=Ext.decode(response.responseText);
		if(!obj.success) return;
		Ext.MessageBox.hide();
		var win = new Ext.Window({
			layout:'fit',
			title:'Export',
			autoScroll:true,
			width:500,
			height:300,
			closeAction:'destroy',
			plain: true,
			html:Ext.encode(obj.output),
			buttons: [{
				text: 'OK',
				handler: function(){
					win.destroy();
				}
			}]
		});
		win.show();
	},
  
  scanDir: function(){
  	Ext.MessageBox.show({
  		msg: 'Adding all new movies.',
  		progressText: 'Scanning...',
  		width:300,
  		wait:true,
  		waitConfig: {interval:200}
  	});
  	Ext.Ajax.request({
  		url:'config/movieFolderScan',
  		timeout:300000,
  		params:{
  		  folderID:this.folderID
  		},
  		scope: this,
  		success:this.onScanResultReceived
  	});

  },
  
  onScanResultReceived: function(response){
		var obj=Ext.decode(response.responseText);
		if(!obj.success) return;
		Ext.MessageBox.hide();
		var win = new Ext.Window({
			layout:'fit',
			title:'Scan Result',
			autoScroll:true,
			width:500,
			height:300,
			closeAction:'destroy',
			plain: true,
			html:templates.scanResult.apply(obj.scanresult),
			buttons: [{
				text: 'OK',
				handler: function(){
					win.destroy();
				}
			}]
		});
		win.show();
	},
  
  onUpdateReceived: function(response){
		this.data=Ext.decode(response.responseText);
		this.folderID=this.data.data.id
		if(!this.data.success) return;
		templates.folderDetail.overwrite(this.panel.body,this.data.data);
	},
  
  update: function(){
  	// todo this.commentForm.hide();
  	Ext.Ajax.request({
  		url:'config/movieFolderGet',
  		params:{folderID:this.folderID},
  		scope:this,
  		success:this.onUpdateReceived
  	});
  	return(true);
  }	
});