# 二人牛牛消息协议 #

**牌编号:CS_**  
<pre>
方块[A...K]: [1...13]   # CS_DIAMOND
梅花[A...K]: [17...29]  # CS_CLUB
红桃[A...K]: [33...45]  # CS_HEART
黑桃[A...K]: [49...61]  # CS_SPADE
</pre>
**牌型:T_**  
<pre>
T_VALUE0        =  0 # 混合牌型
T_THREE         = 12 # 三条 (×)
T_FOUR          = 13 # 四条 (×)
T_FOURKING      = 14 # 天王1(1张10, 4张(JQK)) 天王--五花牛
T_FIVEKING      = 15 # 天王2(5张都是(JQK)
</pre>
**牛牛:K_**
<pre>
K_NIU0  = 0 # 没牛
K_NIU1  = 1 # 牛一
K_NIU2  = 2
K_NIU3  = 3
K_NIU4  = 4
K_NIU5  = 5
K_NIU6  = 6
K_NIU7  = 7
K_NIU8  = 8
K_NIU9  = 9
K_NIU10 = 10 # 牛牛
</pre>
**牌桌信息:**  
desk_info:
<pre>
{
    // "continue_timeout": integer, # 等待继续超时
    
}
</pre>
**游戏流程**  

=>决定叫庄玩家 **step1**
<pre>
{
    "type": "niuniu",
    "tag": "call_user",
    "body": 
    {
        "forced":0, # 0-非强制指定,1-强制指定庄家(用于庄家不叫,闲家也不叫,强制指定第一个庄家为庄家)
        "uid": uid, # 叫庄用户id
    }
}
</pre>

<=叫庄请求 **step2**
<pre>
{
    "type": "niuniu",
    "tag": "REQ_call",
    "body": 
    {
        "called": 0, # 0-不叫, 1-叫
        "uid": uid, # 叫庄用户id
    }
}
</pre>

=>叫庄响应 **step3**
<pre>
{
    "type": "niuniu",
    "tag": "RESP_call",
    "body": 
    {
        "called": 0, # 0-不叫, 1-叫
        "uid": uid, # 叫庄用户id
    }
}
</pre>
**如果未叫庄,goto-->step1**  

<=用户加注 **step4**  
<pre>
{
    "type": "niuniu",
    "tag": "REQ_bet",
    "body": 
    {
        "bet": integer, # 加注金额
        "uid": uid, # 加注用户id
    }
}
</pre>

=>加注响应 **step5**
<pre>
{
    "type": "niuniu",
    "tag": "RESP_bet",
    "body": 
    {
        "bet": integer, # 加注金额
        "uid": uid, # 加注用户id
    }
}
</pre>

=>发牌 **step6**
<pre>
{
    "type": "niuniu",
    "tag": "deal",
    "body": 
    {
        "players":
        [
            {
                "uid": uid, # 用户id
                "cards": [], # 5张牌
            },
        ]，
    }
}
</pre>

<=摊牌请求 **setp7**  
<pre>
{
    "type": "niuniu",
    "tag": "REQ_show",
    "body": 
    {
        "uid": uid, # 摊牌用户id
    }
}
</pre>

=>摊牌响应 **setp8**
<pre>
{
    "type": "niuniu",
    "tag": "RESP_show",
    "body": 
    {
        "uid": uid, # 摊牌用户id
    }
}
</pre>

<=强退
<pre>
{
    "type": "niuniu",
    "tag": "compel",
    "body": 
    {
    }
}
</pre>

=>结束 **setp9**
<pre>
{
    "type": "niuniu",
    "tag": "over",
    "body": 
    {
        "players":
        [
            {
                "uid": , # 用户id
                "all_turn_money": integer, # 总局得分
                "curr_turn_money": integer, # 本局得分(上局)(游戏得分)
                "cards": [], # 5张, 包括底牌
                "tax": integer, # 税
            },
        ]，
    }
}
</pre>

<=重进请求
<pre>
{
    "type": "niuniu",
    "tag": "REQ_reenter",
    "body": 
    {
    }
}
</pre>
=>重进响应
<pre>
{
    "type": "showhand",
    "tag": "RESP_reenter",
    "body": 
    {
        "players":
        [
            {
                "uid": uid, # 用户id
                "cards": [], # 扑克
                "niuniu": 9, # 牛几(0 - 15)
                "table_money_bet": integer, # 该玩家下注数目
                "all_turn_money": integer, # 总局得分
                "last_turn_money": integer, # 上局得分

            },
        ]

        "max_turn_money": integer, # 下轮最大下注
        "min_turn_money": integer, # 下轮最小下注
        "banker": uid, # 庄家
    }
}
</pre>

<=托管 [×]
<pre>
{
    "type": "game", 
    "tag": "manage", 
    "body": 
    {
        "uid": uid, 
        "managed": 1/0,
    }
}
</pre>

=>托管广播 [×]
<pre>
{
    "type": "game", 
    "tag": "manage", 
    "body": 
    {
        "uid": uid, 
        "managed": 1/0,
    }
}
</pre>

<=结束后点继续[×]
<pre>
{
    "type": "game", 
    "tag": "continue", 
    "body": 
    {
        
    }
}
</pre>

=>继续广播[×]
<pre>
{
    "type": "game", 
    "tag": "ready", 
    "body": 
    {
        "uid": uid, 
    }
}
</pre>

<= 点换桌[×]
<pre>
{
    "type": "game", 
    "tag": "changedesk", 
    "body": 
    {
        
    }
}
</pre>

=>某人离开牌桌[×]
<pre>
{
    "type": "game", 
    "tag": "leave", 
    "body": 
    {
        "uid", uid,
    }
}
</pre>

***注:*** 和代码有区别部分: 用户叫庄/摊牌等的标识字段去掉了,如果收到相应消息,就代表有相应的标识