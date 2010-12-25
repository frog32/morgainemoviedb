MorgaineMovieDB.view.MovieViewDetail = Ext.extend(MorgaineMovieDB.view.AbstractView,{
  constructor: function(config){
    MorgaineMovieDB.view.MovieViewDetail.superclass.constructor.call(this,config);
    this.addEvents('changedMovie');
    this.movieID=0;

    this.movie=new Ext.Panel({
      title:'Info',
    	layout:'fit',
  		autoScroll:true,
    	width:'100%',
    	border:false
    });
    this.files=new Ext.Panel({
      title:'Files',
    	layout:'fit',
  		autoScroll:true,
    	width:'100%',
    	border:false
    });
    
    this.imagesView = new Ext.ux.DDView({
      store: new Ext.data.JsonStore({
        root: 'posters',
        autoHeight:true,
        fields: [
          {name:'id', type:'int'},
          {name:'order', type:'int'},
          {name:'source_type', type:'string'}
        ]
      }),
      tpl: new Ext.XTemplate(
        '<tpl for=".">',
        '<div id="component_{id}" class="x-combo-list-item">',
        '<img align="top" height="30px" width="30px" src="'+settings.media_url+'{id}" />',
        '</div>',
        '</tpl>'
      ),
      autoHeight:true,
      multiSelect: true,
  		dragGroup:'availComponentDDGroup,subComponentDDGroup',
  		dropGroup:'availComponentDDGroup,subComponentDDGroup',
  		selectedClass: 'asp-selected',
      overClass:'x-view-over',
      itemSelector:'.x-combo-list-item',
      emptyText: 'No images to display'
    });
    
    this.images=new Ext.Panel({
      title:'Images',
    	//layout:'fit',
  		autoScroll:true,
    	border:false,
    	items:[this.imagesView]
    });
    this.findLookup=new Ext.Button({
    	iconCls:'silk-film_link',
    	text:'Lookup movie',
    	handler: this.serachLookupMovie,
    	scope:this
    });	
    /*this.searchOSHashButton=new Ext.Button({
    	iconCls:'silk-film_link',
    	text:'Find imdb',
    	handler: this.searchOSHash,
    	scope:this
    });*/
    /*this.changeImg=new Ext.Button({
    	iconCls:'silk-picture_add',
    	text:'New Picture',
    	handler: function(){addPicture(this.movieID);}
    });*/	
    this.commentText= new Ext.form.TextArea({
    	fieldLabel:'Comment',
    	width:400,
    	height:200		
    });
    this.commentRating=new Ext.form.NumberField({
    	fieldLabel:'Rating',
    	width:400
    });
    this.commentForm=new Ext.FormPanel({
    	title:'Write Comment',
    	items:[this.commentRating,this.commentText],
    	buttons:[{
    		text:'Submit',
    		handler:this.commitComment
    	}],
    	hidden:true
    });
    /*this.bookmark=new Ext.Button({
    	iconCls:'silk-flag_red',
    	text:'Mark',
    	handler: function(){bookmark(this.movieID);}
    });*/
    /*this.comment=new Ext.Button({
    	iconCls:'silk-comment_add',
    	text:'Comment',
    	handler: function(){if(this.movieID)this.commentForm.show();}
    });*/
    this.panel = new Ext.TabPanel({
  		region:'east',
  		title:'DetailView',
  		deferredRender:false,
  		width:550,
  		split:true,
  		margins:0,
  		activeTab:0,
  		items:[this.movie,this.files,this.images,this.commentForm],
  		tbar:[this.findLookup,/*this.searchOSHashButton,this.changeImg,'-',this.bookmark,this.comment*/]
  	});
  },

  commitComment: function (){
  	Ext.Ajax.request({
  		url:'ajax.php',
  		params:{
  			action:'commitComment',
  			movieID:this.movieID,
  			rating:this.commentRating.getValue(),
  			text:this.commentText.getValue()
  		},
  		success:function(response){
  			var obj=Ext.decode(response.responseText);
  			if(!obj.success) return;
  			this.update();
  			this.commentRating.setValue();
  			this.commentText.setValue();
  			this.commentForm.hide();
  		}
  	});
  },
  
  searchOSHash: function(){
		Ext.Ajax.request({
			url:'movie/searchOSHash',
			timeout:60000,
			scope: this,
			params:{movieID:this.movieID},
			success:function(response){
				var obj=Ext.decode(response.responseText);
				if(!obj.success) return;
				this.fireEvent('changedMovie');
			}
		});
    
  },

  serachLookupMovie: function(){
  	var titleSearch=new Ext.form.TextField({
  		width:400,
  		value:'',
  		listeners:{
  			specialkey:function(field,e){
  				if(e.getKey()==e.ENTER)
  					Ext.Ajax.request({
  						url:settings.api_url+'lookup/search/'+encodeURIComponent(titleSearch.getValue())+'.json',
  						success:function(response){
  							var obj=Ext.decode(response.responseText);
  							resultGrid.store.loadData(obj);
  						}
  					});					
  			}
  		}
  	});

  	var resultGrid = new Ext.grid.GridPanel({
  		flex:1,
  		store: new Ext.data.JsonStore({
  			fields: [
  				{name: 'id', type: 'integer'},
  				{name: 'title', type: 'string'},
  				{name: 'year', type: 'int'},
  				{name: 'link', type: 'string'}	
  			]
  		}),
  		columns: [
  			{id:'title', header: 'Title', width: 160, sortable: true, dataIndex: 'title'},
  			{header: 'Year', width: 50, sortable: true, dataIndex: 'year'},
  			{header: 'Link', width: 50, dataIndex:'link', renderer: lookupLinkRenderer}
  		],
  		sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
  		stripeRows: true,
  		autoExpandColumn: 'title',
  		anchor:'0,0',
  		title: 'Movies'
  	});
  	resultGrid.getSelectionModel().on('rowselect',function(sm,index,r){Ext.getCmp('lookupSearchSelect').setDisabled(0);})	

  	var win = new Ext.Window({
  		layout:'vbox',
  		title:'Movie Lookup',
  		layoutConfig: {
  			align : 'stretch',
  			pack  : 'start'
  		},
  		width:500,
  		height:500,
  		closeAction:'destroy',
  		plain: true,
  		items:[
  			titleSearch,
  			resultGrid
  		],
  		buttons: [{
  			text:'Select',
  			id:'lookupSearchSelect',
  			disabled:true,
  			scope:this,
  			handler:function(){
  				Ext.Ajax.request({
  					url: settings.api_url+'movies/'+this.movieID+'.json',
  					timeout:60000,
  					scope: this,
  					method: 'PUT',
  					params:{id:resultGrid.getSelectionModel().getSelected().data.id},
  					success:function(response){
  						win.close();
  						this.fireEvent('changedMovie');
  					}
  				});
  			}
  		}]
  	});
  	win.show();
  },  
    
  addPicture: function(){
  	Ext.MessageBox.show({
  		title: 'New Picture',
  		msg: 'Please enter the image address:',
  		width:300,
  		buttons: Ext.MessageBox.OKCANCEL,
  		multiline: true,
  		fn: function(button, text){
  			Ext.Ajax.request({
  				url:'movie/lookupSet',
  				params:{action:'setMovieImage',movieID:this.movieID,url:text},
  				success:function(response){
  					var obj=Ext.decode(response.responseText);
  					if(!obj.success) return;
  					// todo showMovie(movieGrid.getSelectionModel());
  				}
  			});
  		}
  	});
  },
  
  setMovie: function(movieID){
    this.movieID = movieID;
    this.update();
  },
  
  setBlank: function(){
    this.movieID = 0;
    new Ext.Template('').overwrite(this.movie.body);
  },
  
  update: function(){
  	// todo this.commentForm.hide();
  	Ext.Ajax.request({
  		url:settings.api_url+'movies/'+this.movieID+'.json',
  		scope:this,
  		success: this.onUpdateReceived
  	});
  	return true;
  },
  
  onUpdateReceived: function(response){
		this.data=Ext.decode(response.responseText);
		this.movieID=this.data.id
		this.findLookup.setDisabled(false);
		Ext.each(this.data.comments,function(comment,i){
			this.data.comments[i].stars=new Array();
			for(var j=0;j<Math.ceil(comment.rating);j++){
				this.data.comments[i].stars[j]=1;
			}
		});
		templates.movieDetail.overwrite(this.movie.body,this.data);
		templates.movieDetailFiles.overwrite(this.files.body,this.data);
		this.imagesView.store.loadData(this.data);
	},
    
  bookmark: function bookmark(){
  	Ext.Ajax.request({
  		url:settings.api_url+'movies/'+this.movieID+'/bookmark.json',
  		method:'POST',
  		success:function(response){
  			var obj=Ext.decode(response.responseText);
  			if(!obj.success) return;
  			updateList();
  		}
  	});
  }  
	
});