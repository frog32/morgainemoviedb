// search panel
searchPanel.namesearch=new Ext.form.TextField({
	enableKeyEvents:true,
	width:200
});
searchPanel.namesearch.on('keyup',function(textfield,e){
	if(textfield.getValue()==''){
		// todo movieGrid.store.clearFilter();
	}else{
		// todo movieGrid.store.filter('title',textfield.getValue());
	}
},{buffer:1000});
searchPanel.panel=new Ext.Panel({
	layout:'column',
	items:[searchPanel.namesearch]
});  
