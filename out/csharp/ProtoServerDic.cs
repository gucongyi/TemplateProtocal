using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Protocal
{

    public class ProxyDic
    {
        public static Dictionary<Type, Type> dicProto = new Dictionary<Type, Type>();
        public static List<Type> listProto = new List<Type>();
        static ProxyDic()
        { 
            //
            AddIfNotContains(typeof(SCSignInfo), typeof(RespSignInfo));
            AddIfNotContains(typeof(CSGetInfo), typeof(RespInfo));
            listProto.Add(typeof(RespInfo));
        }

        private static void AddIfNotContains(Type typeTos, Type typeToc)
        {
            if (!dicProto.ContainsKey(typeTos))
            {
                dicProto.Add(typeTos, typeToc);
            }
        }

        public static Type GetTocByTypeTos(Type typeTos)
        {
            Type typeToc = null;
            if (dicProto.TryGetValue((typeTos), out typeToc))
            {
                return typeToc;
            }
            return null;
        }
        public static string GetTocNameByTypeTos(Type typeTos)
        {
            Type typeToc = null;
            if (dicProto.TryGetValue((typeTos), out typeToc))
            {

            }

            if (typeToc != null)
            {
                return typeToc.Name;
            }
            else
            {
                return string.Empty;
            }
        }
    }

    public class ProxyDicCode
    {
        public static Dictionary<srting, string> codeProto = new Dictionary<srting, string>();
        
        static ProxyDicCode()
        { 
            AddIfNotContains(code, desc);
        }

        private static void AddIfNotContains(srting code, string desc)
        {
            if (!codeProto.ContainsKey(code))
            {
                codeProto.Add(code, desc);
            }
        }
    }
}