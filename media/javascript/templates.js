templates=new Object();
templates.movieDetail=new Ext.XTemplate(
	'<table class="movieDetail" width="100%">',
	'<tpl for="titles"><tr><td colspan="2"><h1>{text}</h1></td></tr></tpl>',
	'<tr><td colspan="2"><tpl for="countries">{name}</tpl>',
		'<tpl if="year!=null"> ({year})</tpl></td></tr>',
	'<tr><td colspan="2"><tpl for="genres">{name}</tpl></td></tr>',
	'<tr><td valign="top">',
	'<tpl if="imdbID!=null"><p><a href="http://www.imdb.com/title/tt{imdbID}/" target="_blank">IMDB</a></p></tpl>',
	'<p>Duration:{[durationRenderer(values["duration"])]}</p>',
	'</td><td align="right">',
	'<tpl if="posters.length">',
  	'<a href="'+settings.media_url+'{[values["posters"][0].image_original]}" ',
  			'target="_blank">',
  		'<img src="'+settings.media_url+'{[values["posters"][0].image_thumb]}" />',
  	'</a>',
	'</tpl>',
	'</td></tr>',
	'<tr><td>Cast</td><td>',
	'<tpl for="actors">',
	  '<p>{[values["role"].name]} - {[values["person"].name]}</p>',
	'</tpl>',
	'<tr><td>Writers</td><td>',
	'<tpl for="writers">',
	  '<p>{name}</p>',
	'</tpl>',
	'<tr><td>Directors</td><td>',
	'<tpl for="directors">',
	  '<p>{name}</p>',
	'</tpl>',
/*				'<tpl if="comments.length"><tr><td colspan="2"><h2>Comments</h2></td></tr></tpl>',
	'<tpl for="comments">',
		'<tr><td colspan="2"><tpl for="stars"><img src="'+settings.media_url+'img/silk/star.png"></tpl></td></tr>',
		'<tr><td><h3>{name}</h3></td><td align="right">{created}</td></tr>',
		'<tr><td>{comment}</td></tr>',
	'</tpl>',
*/	
    '</table>',
    {
        imageUrl: function(image){
            return settings.media_url + image;
        }
    });

templates.movieDetailFiles=new Ext.XTemplate(
	'<table class="movieDetail" width="100%">',
  '<tpl for="files">',
    '<tpl if="type == \'movie\'">',
      '<tr><td colspan="2">{name}</td></tr>',
      '<tr><td colspan="2">{hash}</td></tr>',
  		'<tr><td>Size</td><td>{[fm.fileSize(values["size"])]}</td></tr>',
  		'<tpl if="videoTracks.length"><tr><td>Video</td><td></tpl>',
  		'<tpl for="videoTracks">',
  			'<tpl if="name"<p>Name: {name}</p></tpl>',
  			'<p>Codec: {[this.renderCodec(values["codec"])]}</p>',
  			'<p>Resolution: {width}x{height}</p>',
  		'</tpl>',
  		'<tpl if="videoTracks.length"></td></tr></tpl>',
  		'<tpl if="audioTracks.length"><tr><td>Audio</td><td></tpl>',
  		'<tpl for="audioTracks">',
  			'<p><tpl if="name"Name: {name}<br /></tpl>',
  			'{[languageRenderer(values["language"])]} {[this.renderCodec(values["codec"])]} {channels} Channel</p>',
  		'</tpl>',
  		'<tpl if="audioTracks.length"></td></tr></tpl>',
  		'<tpl if="subtitleTracks.length"><tr><td>Subtitles</td><td></tpl>',
  		'<tpl for="subtitleTracks">',
  			'<p>{[languageRenderer(values["language"])]}&nbsp;<tpl if="name">{name}</tpl></p>',
  		'</tpl>',
  		'<tpl if="subtitleTracks.length"></td></tr></tpl>',
  	'</tpl>',
  '</tpl>',
	'</table>',{
	renderCodec:function(code){
		var codecNames={'A_AC3':'AC3','A_DTS':'DTS','A_MPEG/L3':'mpeg Layer III','V_MPEG4/ISO/AVC':'H.264'};
		if(!codecNames[code])
			return code;
		return codecNames[code];
	},
	renderFilename:function(value){
		return value.replace(/\./g,'.\u200B');
	}				
});

templates.movieDetailImages=new Ext.XTemplate(
	'<table class="movieDetail" width="100%">',
  '<tpl for="posters">',
    '<img src="'+settings.media_url+'posters/thumb/{id}.jpg" />',
  '</tpl>',
	'</table>',{
	renderCodec:function(code){
		var codecNames={'A_AC3':'AC3','A_DTS':'DTS','A_MPEG/L3':'mpeg Layer III','V_MPEG4/ISO/AVC':'H.264'};
		if(!codecNames[code])
			return code;
		return codecNames[code];
	},
	renderFilename:function(value){
		return value.replace(/\./g,'.\u200B');
	}				
});

templates.folderDetail= new Ext.XTemplate(
  '<table width="100%">',
  '<colgroup><col width="50%" /><col width="50%" /></colgroup>',
  '<tr><td>Path:</td><td>{path}</td>',
  '<tr><td>Movie Count:</td><td>{movieCount}</td>',
  '</table>'
);

templates.library = new Ext.XTemplate(
	'{count} Movies, {[fm.fileSize(values["size"])]}',
	' {[this.durationRenderer(values["duration"])]}',{
		durationRenderer:function(val){
			var d=Math.floor(val/60/60/24);
			var h=Math.floor((val-d*24*60*60)/60/60);
			var m=Math.floor((val-d*24*60*60-h*60*60)/60);
			var s=Math.round((val-d*24*60*60-h*60*60-m*60));
			return d+' days '+h+':'+m+':'+s;
		}
	}
);

templates.scanResult=new Ext.XTemplate(
	'<p>Scanned {scan} Files.</p>',
	'<h3>{[values["added"].length]} Movies added</h3>',
	'<tpl for="added"><p>{.}</p></tpl>',
	'<h3>{[values["removed"].length]} Movies Deleted</h3>',
	'<tpl for="removed"><p>{.}</p></tpl>'
);


