;function click_action_info(id){
    var x=id
    $.get("/weather_code/",
                {
                    city: x,
                    time: "2019-04-05"
                },
                function (result) {
                    alert("返回数据: \n" +x +"\n" + "reason:" + result.reason + "\n" + "weather_name:" + result.weather_name);
                });
    }