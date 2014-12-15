var welcomemsg="hello ,this project have not finished,if you have question,please connect me,QQ:1315469509 ,email:zk_michael@qq.com";

console.debug(welcomemsg);

var hostaddr={};
hostaddr.address="0.0.0.0";
hostaddr.port="9999";
  function _$jsonpcall(method,params,callback){
        var ret;
        for(key in params){
            params[key] = JSON.stringify(params[key])
        }
        params.method = method;
        // params.callback = '?';
        //uri="http://"+hostaddr.address+":"+hostaddr.port+"/do";
        uri="/do"; 
        var ret;
        $.ajax({
            type    : "GET",
            url     : uri,
            async   : true,
            data    : params,
            dataType :"json",
            crossDomain: true,
            success : function(data){
                if(callback!=undefined&&callback!=null){
                    callback(data);
                }
                console.debug('ret',data);
            },
            error   : function(xmlHttp,textStatus){
                alert('error');
            }
        });
    }
var com={
    init:function(){}, 

    test:function(callback){
	
      var params = {};
        return _$call('test',params,callback);
    }
	,
	sethostaddress:function(addr,port,callback){
	var params = {};
       hostaddr.address=addr;
	   hostaddr.port=port;
	   _$call = _$jsonpcall;
        return _$call('test',params,callback);
    }

};
function hello(data){
console.debug(data.retmsg);
}
com.init();
