
MorgaineMovieDB.model.User = Ext.extend(Ext.util.Observable,{
  constructor: function(config){
    MorgaineMovieDB.model.User.superclass.constructor.call(this,config);
    this.addEvents('authenticationUpdate');
  	this.authenticated=false;
    this.usergroup='none';
    this.userID = 0;
    this.username='';

  	this.userField=new Ext.form.TextField({
  		fieldLabel:'Username',
  		listeners:{specialkey:{
  		  fn:this.loginBoxOnKeyPress,
  		  scope:this
  		  }
  	  }
  	});
  	this.passwordField=new Ext.form.TextField({
  		fieldLabel:'Password',
  		inputType:'password',
  		listeners:{
  		  specialkey:{
  		    fn: this.loginBoxOnKeyPress,
  		    scope:this
  		  }
  		}
  	});
  	this.win = new Ext.Window({
  		layout:'form',
  		title:'Please enter your Username and Password.',
  		width:300,
  		height:120,
  		closeAction:'hide',
  		plain: true,
  		items:[this.userField,this.passwordField],
  		buttons: [{
  			text:'Login',
  			handler:this.authenticate,
  			scope:this
  		}]
  	});    
    this.getAuthState();
  },
  
  authenticate: function(){
		Ext.Ajax.request({
			url:'user/login',
			params:{
				user:this.userField.getValue(),
				password:this.passwordField.getValue()
			},
			scope:this,
			success:function(response){
				this.win.hide();
				this.userField.setValue('');
				this.passwordField.setValue('');
				var obj=Ext.decode(response.responseText);
				if(!obj.success) return;
				Ext.util.Cookies.set('auth',obj.auth);
				Ext.util.Cookies.set('userID',obj.data.id);
				
				this.updateUser(obj.data);
			}
		});
  },
  
	deauthenticate: function(){
  	Ext.util.Cookies.clear('auth');
  	Ext.util.Cookies.clear('userID');
  	this.updateUser({
  	  name:'',
  	  privileges:'none',
  	  id:0
  	});
	},
  
  updateUser: function(user){
    this.name=user.username;
		this.privileges='admin';
		this.userID = user.id;
		this.authenticated=(user.id)?true:false;
		this.fireEvent('authenticationUpdate',this);		
  },

  getAuthState: function(){
  	Ext.Ajax.request({
  		url:settings.api_url+'users/authstate.json',
  		method:'get',
  		scope:this,
  		success:function(response){
  			var obj=Ext.decode(response.responseText);
  			this.updateUser(obj);
//  			else
//  			  this.deauthenticate();
  		}
  	});
  },
  
  hasPrivilege: function(neededPrivilege){
    if(this.privileges == 'admin')
      return true;
    if(neededPrivilege == 'write' && this.privileges == 'write')
      return true;
    if(neededPrivilege == 'read' && (this.privileges == 'write' || this.privileges == 'read'))
      return true;
    if(neededPrivilege == 'none')
      return true;
    return false;
  },
  
  loginBoxOnKeyPress: function(field,e){
		if(e.getKey()==e.ENTER)
			this.authenticate();
	},
	
  showLoginWindow: function(){
  	this.win.show();
  	this.userField.focus(true,100);
  }  
});
