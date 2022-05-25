const Template = require('../../template');

class Main extends Template {
    constructor() {
        super()
        this.title = "京东热爱奇旅组队"
        this.cron = "45 8,15,23 * * *"
        this.help = '2'
        this.task = 'local'
        this.model = 'team'
        this.verify = 1
        this.import = ['jdLog618', 'jdUrl']
    }

    async prepare() {
        this.risk = new this.modules.jdLog618()
        this.funcName = 'promote'
        await this.risk.init({
            type: 3,
            "sceneid": 'RAhomePageh5',
        })
        for (let cookie of this.cookies['help']) {
            let params = {
                'url': `https://api.m.jd.com/client.action`,
                'form': `functionId=${this.funcName}_pk_getHomeData&client=m&clientVersion=-1&appid=signed_wh5&body={}`,
                cookie,
                
            }
            let s = await this.curl(params)
            try {
                let ss = await this.curl({
                    'url': 'https://api.m.jd.com/client.action',
                    'form': 'functionId=getEncryptedPinColor&client=wh5&clientVersion=1.0.0&body={}',
                    cookie,
                    
                })
                this.shareCode.push({mpin: ss.result, 'inviteId': s.data.result.groupInfo.groupJoinInviteId})
                let sss = await this.curl({
                    'url': `https://api.m.jd.com/client.action`,
                    'form': `functionId=${this.funcName}_pk_votForr&client=m&clientVersion=-1&appid=signed_wh5&body={"votFor":"B"}`,
                    'cookie': i
                })
            } catch (e) {
            }
        }
    }

    async main(p) {
        let cookie = p.cookie
        let getHomeData = await this.curl({
                'url': `https://api.m.jd.com/client.action`,
                'form': `functionId=${this.funcName}_getHomeData&client=m&clientVersion=-1&appid=signed_wh5&body={}`,
                cookie,
                
            }
        )
        let secretp = this.haskey(getHomeData, 'data.result.homeMainInfo.secretp')
        let collect = await this.curl({
                'url': `https://api.m.jd.com/client.action`,
                'form': `functionId=collectFriendRecordColor&client=wh5&clientVersion=1.0.0&body={"mpin":"${p.inviter.mpin}","businessCode":"20136","assistType":"2","shareSource":1}`,
                cookie,
                
            }
        )
        let s = await this.curl({
            url: `https://api.m.jd.com/client.action`,
            form: `functionId=${this.funcName}_pk_joinGroup&client=m&clientVersion=-1&appid=signed_wh5&body=${this.dumps(await this.risk.body({
                "inviteId": p.inviter.inviteId,
                "confirmFlag": "1", 'secretp': secretp,
            }))}`,
            cookie,
            
        })
        console.log(s);
        if (new Date().getHours()>=23) {
            await this.curl({
                'url': `https://api.m.jd.com/client.action`,
                form: `functionId=${this.funcName}_pk_divideScores&client=m&clientVersion=-1&appid=signed_wh5&body=${this.dumps(await this.risk.body({}))}`,
                cookie,
                
            })
            await this.curl({
                'url': `https://api.m.jd.com/client.action`,
                form: `functionId=${this.funcName}_pk_getAmountForecast&client=m&clientVersion=-1&appid=signed_wh5&body=${this.dumps(await this.risk.body({}))}`,
                cookie,
                
            })
            let award = await this.curl({
                'url': `https://api.m.jd.com/client.action`,
                form: `functionId=${this.funcName}_pk_receiveAward&client=m&clientVersion=-1&appid=signed_wh5&body=${this.dumps(await this.risk.body({}))}`,
                cookie,
                
            })
            console.log(this.haskey(award, 'data'));
        }
    }
}

module.exports = Main;
