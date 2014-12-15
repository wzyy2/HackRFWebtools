var ic_base = {
    init:function(){
    },
	getUrlString:function(name){
	    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	    var r = window.location.search.substr(1).match(reg);
	    if (r != null) {
	    	return r[2]; 
	    }
	    return null;
    },
};
ic_base.init();

