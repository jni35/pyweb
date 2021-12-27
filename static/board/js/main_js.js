// 디지털 시계
setInterval(myWatch, 1000);

function myWatch(){
    let date = new Date()
    let now = date.toLocaleTimeString();
    document.getElementById("demo").innerHTML=now;
}