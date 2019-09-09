using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Protocal
{ 
    /// <summary>
    /// 物品状态
    /// </summary>
    public enum SignState
    { 
        NormalSign, 
        UnSign, 
        RepairSign,//补签 
    }
    
    /// <summary>
    /// 商城主分类
    /// </summary>
    public enum GoodType
    { 
        Furniture,//家具 
        Clothing,//时装 
        Heartbeat,//心动值 
    }
    
    public enum TitleType
    { 
        TitleType1 = 0, 
        TitleType2, 
        TitleType3, 
    }
    
}