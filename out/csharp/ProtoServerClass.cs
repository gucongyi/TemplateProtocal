using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Protocal
{ 
    
    /**
     * 服务器回给客户端的test
     */
    public class SCSignInfo : ProtoServerBaseClass
    { 
        //物品信息List
        public  listGoodInfoSign;
        public  timeBegin;
        public  timeEnd;
    }
    
    
    /**
     * 客户端向服务器请求的
     */
    public class CSGetInfo : ProtoServerBaseClass
    { 
        public int day;
    }
    
    
    /**
     * 物品信息
     */
    public class GoodInfoSign
    { 
        //物品ID
        public  goodId;
        //签到状态
        public  signState;
        //第几天
        public  whatDay;
    }
    
    
    /**
     * 客户端向服务器请求的
     */
    public class CSInfo : ProtoServerBaseClass
    { 
        public  listGoodInfoSign;
        public  timeBegin;
        public  timeEnd;
    }
    
}