// pages/signin/signin.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    radioItems: [
      {name: '软件', value: '软件'},
      {name: '微电子', value: '微电子'},
      {name: '软国', value: '软国'}
  ],
  },radioChange: function (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value);

    var radioItems = this.data.radioItems;
    for (var i = 0, len = radioItems.length; i < len; ++i) {
        radioItems[i].checked = radioItems[i].value == e.detail.value;
    }

    this.setData({
        radioItems: radioItems,
        [`formData.radio`]: e.detail.value,
        radio:e.detail.value
    });
},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  /**
   * 用户提交注册表单
   * 
   */
  formSubmit:function(_content){
    let that =this;
    _content.detail.value['major']=this.data['radio']
    console.log(_content.detail.value);
    wx.request({
      url: 'http://127.0.0.1:5000/api/users',
      data:_content.detail.value,
      header:{"Content-Type":"application/json"},
      method: "POST",
      success: function(res){
        console.log("成功注册");
        console.log(res);
      }
    })
  }
})