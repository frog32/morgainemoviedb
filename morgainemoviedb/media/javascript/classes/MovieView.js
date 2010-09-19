/*    MovieView
        serverRequests:
            movieView/get -> getContents of the movieView
            
*/
MorgaineMovieDB.view.MovieView = Ext.extend(MorgaineMovieDB.view.AbstractView,{
    constructor: function(config){
        MorgaineMovieDB.view.MovieView.superclass.constructor.call(this,config);
        
        this.grid = new Ext.grid.GridPanel({
            region:'center',
            store: new Ext.data.JsonStore({
                fields: [
                    {name: 'movieID', type: 'int', mapping:'id'},
                    {name: 'titles'},
                    {name: 'year', type: 'string'},
                    {name: 'countries'},
                    {name: 'genres'},
                    {name: 'duration', type: 'int'},
                    {name: 'languages'},
                    {name: 'bookmark', type: 'int'}
                ]
            }),
            columns: [
                {header: ' ', width:25, sortable: true, dataIndex: 'bookmark', renderer:bookmarkRenderer},
                {header: 'ID', sortable: true, hidden:true, dataIndex: 'movieID'},
                {id:'title', header: 'Title', sortable: true, dataIndex: 'titles', renderer:titleRenderer},
                {header: 'Year', width: 50, sortable: true, dataIndex: 'year'},
                {header: 'Country', width: 150, sortable: true, dataIndex: 'countries', renderer: arrayRenderer},
                {header: 'Genre', width: 200, sortable: false, dataIndex: 'genres', renderer: arrayRenderer},
                {header: 'Duration', width: 50, sortable: true, dataIndex: 'duration', renderer:durationRenderer, align:'right'},
                {header: 'Language', width: 100, sortable: false, dataIndex: 'languages', renderer: languageListRenderer}
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
            autoExpandColumn: 'title',
            anchor:'0,0',
            title: 'Movies'

        });
        
        this.detailView= new MorgaineMovieDB.view.MovieViewDetail();
        this.detailView.addListener('changedMovie',this.update,this);
        
        this.panel= new Ext.Panel({
            layout: 'border',
            title: 'Movies',
            listeners:{
                'activate':{
                    fn:this.update,
                    scope:this
                }
            },
            items: [
                this.grid,
                this.detailView.draw()
            ]
        });
        
    },
    
    onGridSelect: function(sm){
        if(sm.getCount()==0 | sm.getCount()>1){
            this.detailView.setBlank();
            return true;
        }
        this.detailView.setMovie(sm.getSelected().data.movieID);
        },

    onUpdateReceived: function(response){
        var data=Ext.decode(response.responseText);
        this.grid.store.loadData(data);
        //bottomToolbar.countPanel.setText(templates.library.apply(obj.movieCount));
    },
    
    update: function(){
        Ext.Ajax.request({
            url:settings.api_url+'movies.json',
            scope: this,
            success: this.onUpdateReceived
        });
    }    
});