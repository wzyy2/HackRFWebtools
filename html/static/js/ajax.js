  function _$call(method,params,callback){
        for(key in params){
            params[key] = JSON.stringify(params[key])
        }
        params.method = method;
        $.ajax({
            type    : "GET",
            url     : "/do",
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
