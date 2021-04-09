// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: function(res){
        
        if (res.code){
          console.log(res.code);
          wx.getUserInfo({
            success:function(msg){
              //网络请求
              // wx.request({
              //   url: 'http://127.0.0.1:80/login',
              //   method:'POST',
              //   header:{ 
              //     'content-type': 'application/x-www-form-urlencoded'
              //   },
              //   data:{
              //     code: res.code,
              //     encryptedData: msg.encryptedData,
              //     iv: msg.iv              
              //   },
              //   success:
              //   function(data){
              //     console.log(data);
              //   },
    
              // })
            }
          })
        }else{
          console.log('Fail to fetch!'+res.errMsg)
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    shopName: "软院帮帮",
    domain:"http://127.0.0.1:80"	// 本机的地址
  }
})
