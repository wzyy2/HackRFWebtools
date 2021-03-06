/*
* 不关心的非必须参数传递null,（右侧可不传）
*/
var y={
    init:function(){}, 
    
    /*! 获取program列表
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    * @param all,bool: false则隐藏被禁用的program
    * @param keys,str: 逗号（空格）分隔搜索关键字
    */
    programs:function(page,count,all,keys){
        var params = {};
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        if(all!=undefined&&all!=null){
            params.all = all;
        }
        if(keys!=null && keys!=undefined && keys.length>0){
            params.keys = keys;
        }
        return _$call('programs',params);
    },
    
    /*! 获取给定id的program
    * @param id,str: program id
    */
    program:function(id){
        var params = {};
        params.id = id;
        return _$call('program',params);
    },
    
    /*! 开启（禁用）program
    * @param id,str: program id
    * @param enabled,bool: 
    * @return 操作失败返回null，否则返回program的enable状态
    */
    enable_program:function(prgid,enabled){
        var params = {};
        params.prgid = prgid;
        if(enabled!=undefined&&enabled!=null){
            params.enabled = enabled;
        }
        return _$call('enable_program',params);
    },
    
    /*! 获取program的input列表（与input.xml内容对应）
    * @param prgid,str: program id
    * @param required,bool: true则只返回必须设置的input参数
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */
    inputs:function(prgid,required,page,count){
        var params = {};
        params.prgid = prgid;
        if(required!=undefined&&required!=null){
            params.required = required;
        }
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        params.config = false;
        return _$call('inputs',params);
    },
    
    /*! 获取program的config列表（与config.xml内容对应）
    * @param prgid,str: program id
    * @param required bool: true则只返回必须设置的config参数
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */
    configs:function(prgid,required,page,count){
        var params = {};
        params.prgid = prgid;
        params.config = true;
        if(required!=undefined&&required!=null){
            params.required = required;
        }
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('inputs',params);
    },
    
    /*! 获取program的information列表（与information.xml内容对应）
    * @param prgid,str: program id
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */
    informations:function(prgid,page,count){
        var params = {};
        params.prgid = prgid;
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('informations',params);
    },
    
    /*! 获取program的output列表（与output.xml内容对应）
    * @param prgid,str: program id
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */ 
    outputs:function(prgid,page,count){
        var params = {};
        params.prgid = prgid;
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('outputs',params);
    },
    
    /*! 获取program的state列表（与state.xml内容对应）
    * @param prgid,str: program id
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */ 
    states:function(prgid,page,count){
        var params = {};
        params.prgid = prgid;
         if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('states',params);
    },
    
    /*! 将参数加入（移出）活动参数集
    * @param paramid,str: 参数id
    * @param active,bool: true则加入，false则移除
    * @return 操作失败返回None，否则返回参数状态（true已加入活动集，false未加入活动集）
    */
    active_parameter:function(paramid,active){
        var params = {};
        params.paramid = paramid;
        if(active!=undefined&&active!=null){
            params.active = active;
        }
        return _$call('active_parameter',params)
    },
    
    /*! 设置参数
    * @paramid,str: 参数id
    * @param value,*: 参数值
    * @return 成功返回true，失败返回false
    */
    set_parameter:function(paramid,value){
        var params = {};
        if(paramid==''){
            return;
        }
        params.paramid = paramid;
        params.value = value;
        console.debug(paramid,params.value);
        return _$call('set_parameter',params);
    },
    
    /*! 查询活动参数集
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */
    activeset:function(page,count){
        var params = {};
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('activeset',params);
    },
    
    /*! 历史参数集列表
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */
    paramsets:function(page,count){
        var params = {};
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('paramsets',params);
    },
    
    /*! 历史参数集内容
    * @param paramid,str: 参数集id
    * @param page,int: 结果页码，从0开始
    * @param count,int: 每页结果数，置0则返回全部
    */
    paramset:function(psid,page,count){
        var params = {};
        params.psid = psid;
        params.page = page;
        params.count = count;
        return _$call('paramset',params);
    },
    
    /*! 删除历史参数集
    * @param psid,str: 参数集id
    * @return 成功返回true，失败返回false
    */
    del_paramset:function(psid){
        var params = {};
        params.psid = psid;
        return _$call('del_paramset',params);
    },
    
    /*! 将历史参数集加载为活动参数集
    * @param psid,str: 参数集id
    * @return 成功返回true，失败返回false
    */
    pset2aset:function(psid){
        var params = {};
        params.psid = psid;
        return _$call('pset2aset',params);
    },
    
    /*! 清空活动参数集
    *
    */
    clear_aset:function(){
        return _$call('clear_aset',{});
    },
    
    /*! 将活动集保存到历史参数集列表
    * @return 成功返回true，失败返回false
    */
    aset2pset:function(title,author,description,tags){
        var params = {
            title:title,
            author:author,
            description:description,
            tags:tags,
        };
        return _$call('aset2pset',params);
    },
    
      /*! 查询参数（input或config）
    * @param paramid,str: 参数id
    * @return 参数
    */
    get_parameter:function(paramid){
        var params = {
            paramid:paramid,
        };
        return _$call('get_parameter',params); 
    },
    
    /*! 按名查询参数（input或config），prgname必须，idx与name至少设置1个
    * @param prgname,str: 模块名
    * @param idx,int: 参数idx
    * @param name,name: 参数name
    */
    get_parameterx:function(prgname,idx,name){
        var  params = {
            prg_name:prgname,
        }
        if(idx!=undefined&&idx!=null){
            params.param_idx = idx;
        }
        if(name!=undefined&&name!=null){
            params.param_name = name;
        }
        return _$call('get_parameterx',params)
    },
    
     /*! 按名设置参数（input或config），prgname必须，idx与name至少设置1个
    * @param prgname,str: 模块名
    * @param idx,int: 参数idx
    * @param name,name: 参数name
    * @param value,str: 参数值
    */
    set_parameterx:function(prgname,idx,name,value){
        var  params = {
            prg_name:prgname,
        }
        if(idx!=undefined&&idx!=null){
            params.param_idx = idx;
        }
        if(name!=undefined&&name!=null){
            params.param_name = name;
        }
        params.value = value;
        return _$call('set_parameterx',params)
    },
    
    /*! 按名激活参数（input或config），prgname必须，idx与name至少设置1个
    * @param prgname,str: 模块名
    * @param idx,int: 参数idx
    * @param name,name: 参数name
    * @param active,bool: 是否激活，可选，默认为true
    * @return 成功返回激活状态，失败返回null
    */
    active_parameterx:function(prgname,idx,name,active){
        var  params = {
            prg_name:prgname,
        }
        if(idx!=undefined&&idx!=null){
            params.param_idx = idx;
        }
        if(name!=undefined&&name!=null){
            params.param_name = name;
        }
        if(active!=undefined&&active!=null){
            params.active = active;
        }
        return _$call('active_parameterx',params);
    },
    
    /*! 设置历史参数集内参数
    * @param paramid,str: 参数集实例id
    * @param value,*: 
    * @return 成功返回true，失败返回false
    */
    ps_set_parameter:function(paramid,value){
        console.debug(paramid,value);
        var params = {
            paramid:paramid,
            value:value,
        };
        return _$call('ps_set_parameter',params);
    },
    
    worksets:function(page,count){
        var params = {};
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        return _$call('worksets',params);
    },
    
    run_program:function(prgid,psid){
        var params = {prgid:prgid,psid:psid};
        return _$call('run_program',params);
    },
    
    /*! 查询work
    * @param workid,str: work id
    */
    work:function(workid){
        var params = {
            workid:workid,
        };
        return _$call('work',params);
    },
    
    /*! 删除work
    * @param workid,str: work id
    * @return 成功返回true，失败返回false
    */
    del_work:function(workid){
        var params = {};
        params.workid = workid;
        return _$call('del_work',params);
    },
    
    
    results:function(workid,page,count){
        var params = {};
        if(page!=undefined&&page!=null){
            params.page = page;
        }
        if(count!=undefined&&count!=null){
            params.count = count;
        }
        params.workid = workid
        return _$call('results',params);
    },
    
    run_flow:function(path,psid_array){
        var params = {};
        params.path = path;
        params.psid_array = psid_array;
        return _$call('run_flow',params);
   },
   
   flow_state:function(flowid){
        var params = {flowid:flowid};
        return _$call('flow_state',params);
   },
    
   result:function(workid,outputid){
       var params = {workid:workid,outputid:outputid};
       return _$call('result',params);
   },
   
   get_ps_parameter:function(prgid,psid,name){
       var params = {prgid:prgid,psid:psid,name:name};
       return _$call('get_ps_parameter',params);
   },
   
   set_ps_parameter:function(prgid,psid,name,val){
       var params = {prgid:prgid,psid:psid,name:name,value:val};
       return _$call('set_ps_parameter',params);
   },
   
   get_ps_parameter_id:function(psid,inputid){
       var params = {psid:psid,inputid:inputid};
       return _$call('get_ps_parameter_id',params);
   },
   
   set_ps_parameter_id:function(psid,inputid,val){
       var params = {psid:psid,inputid:inputid,value:val};
       return _$call('set_ps_parameter_id',params);
   },
   
  create_paramset:function(title,author,description,tags){
        var params = {title:title,author:author,description:description,tags:tags};
        return _$call('create_paramset',params);
   }

};
y.init();
