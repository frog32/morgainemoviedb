var settings={
  api_url:'/mdb/api/',
  media_url:'/media/',
};

var MorgaineMovieDB = {};
MorgaineMovieDB.model = {};
MorgaineMovieDB.view = {};
MorgaineMovieDB.util = {};

function imdbLinkRenderer(val){
    return '<a href="'+val+'" target="_blank">link</a>';
}

function durationRenderer(val){
    //return new Date(val * 1000).add(Date.SECOND,-new Date().format('Z')).format('G:m:s');
    return Math.round(val/60)+' min';
}

function languageRenderer(lang){
    if(lang=='und')
        return '<img src="'+settings.media_url+'img/silk/world.png" />'
    var lang2fam={bul:'bg',chi:'cn',cze:'cs',dan:'dk',dut:'nl',eng:'gb',est:'et',fin:'fi',fre:'fr',ger:'de',gre:'gr',hun:'hu',ita:'it',nor:'no',pol:'pl',por:'pt',rum:'ro',slv:'sl',spa:'es',swe:'se'};
    var filename=lang2fam[lang];
    if(!filename)
        return lang;
    return '<img src="'+settings.media_url+'img/png/'+filename+'.png" /> ';
}

function bookmarkRenderer(val){
    if(val==1)
        return '<img src="'+settings.media_url+'img/silk/flag_red.png" />';
    return '';
}

function languageListRenderer(list){
    var output='';
    Ext.each(list.split(','),function(lang){
        output+=languageRenderer(lang);
    });
    return output;
}

function arrayRenderer(myArray){
    rArray = [];
    Ext.each(myArray,function(entry){
        rArray.push(entry['name']);
    });
    return rArray.join(', ')
}
