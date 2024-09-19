const video = document.getElementById("video")
const videoName = document.getElementById("video-name")
const videoContainer = document.getElementById("video-container")
const videoControls = document.getElementById("video-control-bar")

const playpause = document.getElementById("playpause");
const mute = document.getElementById("mute");
const picInPic = document.getElementById("picinpic");
const fullscreen = document.getElementById("fs");
const currentTime = document.getElementById("current-time");
const totalTime = document.getElementById("total-time");

const progress = document.getElementById("progress");
const progressDot = document.getElementById("progress-dot");
const progressBar = document.getElementById("progress-bar");

const volumeValue = document.getElementById("volume-value");
const volumeBar = document.getElementById("volume-bar");
const volumeBarDone = document.getElementById("volume-bar-done");

const multipleSpeedList = document.getElementById("multiple-speed-choices").getElementsByTagName('li');

const videoAlternativeBar = document.getElementById("video-chooser")

var mouseDragForProgress = false;          // 鼠标拖拽进度条
var mouseDragForVolume = false;            // 鼠标拖拽音量条

video.controls = false;         // 禁用自带的controls


// 视频选择列表
let focusAlterOrder = 0
const videoAlternativeList = [
    { src : "./video1.mp4", pic : "./pic1.jpg", title : "《你好，李焕英》", subtitle : "贾玲 张小斐" },
    { src : "./video2.mp4", pic : "./pic2.jpg", title : "流浪地球2 · 先导预告片", subtitle : "郭帆 吴京 王智" },
    { src : "./video3.mp4", pic : "./pic3.jpg", title : "电影版想见你预告片", subtitle : "柯佳嬿 许光汉" },
    { src : "./music1.m4a", pic : "./pic4.jpg", title : "Lavender Haze", subtitle : "Taylor Swift"}
]


// 填充视频列表某元素的Html属性
function fillVideoAlter(item, order){
    const title = "<p class = \"title\">" + item.title + "</p>";
    const subtitle = "<p class = \"subtitle\">" + item.subtitle + "</p>";
    const detail = "<div class = \"detail\">" + title + subtitle + "</div>";
    const videopic = "<img src=\"" + item.pic +"\">";
    videoAlternativeBar.innerHTML += "<div class = \"video-alternative\" id = \"videoAlter"+ String(order) + "\">" + videopic +  detail + "</div>";
}

// 改变视频列表顺序
function changeVideoAlter(){
    videoAlternativeBar.innerHTML = "";
    // 当前选中的视频在列表首位
    fillVideoAlter(videoAlternativeList[focusAlterOrder], focusAlterOrder);
    for(const order in videoAlternativeList){
        if(videoAlternativeList[order] != videoAlternativeList[focusAlterOrder])
            fillVideoAlter(videoAlternativeList[order], order);
    }
    
}

// 加载视频选择列表
function loadVideoAlter(){
    changeVideoAlter();
    for(let order in videoAlternativeList){
        document.getElementById("videoAlter"+ String(order)).addEventListener("click", (e) => {
            video.src = videoAlternativeList[order]['src'];
            videoName.innerHTML = videoAlternativeList[order]['title'];
            focusAlterOrder = order;
            changeVideoAlter();
            totalTime.innerHTML = getFormatTime(video.duration, video.duration);    // 初始化视频长度
            progressDot.style.marginLeft = 0;                                       // 初始化圆点位置
            // 音频用封面图
            if(videoAlternativeList[order]['src'].slice(-4) == ".m4a")
                document.getElementById("video-container").style.backgroundImage = "url(" + videoAlternativeList[order]['pic'] + ")";
            // 其他的为黑色底色（background设置为None的话会影响其他css属性，再次设置图片要重设，因此此处也用Image）
            else
                document.getElementById("video-container").style.backgroundImage = "linear-gradient(to bottom, black, black)";
            loadVideoAlter();
        });
    }
}

loadVideoAlter();

// 释放拖动进度条
document.body.addEventListener("mouseup", (e) => {
    mouseDragForProgress = false;
    mouseDragForVolume = false;
});


// 监听鼠标移动
document.body.addEventListener("mousemove", (e) => {
    if(mouseDragForProgress){
        const barRec = progress.getBoundingClientRect();
        const pos = (e.pageX - barRec.left) / progress.offsetWidth;
        video.currentTime = pos * video.duration;
    }
    else if(mouseDragForVolume){
        const barRec = volumeBar.getBoundingClientRect();
        var pos = (barRec.bottom - e.pageY) / volumeBar.offsetHeight;
        if(pos > 1)
            pos = 1;
        else if(pos < 0)
            pos = 0;
        video.volume = pos;
    }
});

// 监听全屏
window.addEventListener('fullscreenchange', () => {
    const isFullScreen = document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen
    if(isFullScreen) {
        fullscreen.src = "./icon/fullscreenexit.svg";
    }
    else{
        fullscreen.src = "./icon/fullscreen.svg";
    }

    // 防止进度条圆点错位
    progressDot.style.marginLeft = (progress.value / video.duration) * progress.offsetWidth - progressDot.offsetWidth / 2 + "px";
})


// 播放按钮
playpause.addEventListener("click", (e) => {
    if (video.paused || video.ended) {
        video.play();
        playpause.src = "./icon/pause.svg"
    } 
    else {
        video.pause();
        playpause.src = "./icon/play.svg"
    }
});


// 点击视频本身同理暂停/播放
video.addEventListener("click", (e) => {
    if (video.paused || video.ended) {
        video.play();
        playpause.src = "./icon/pause.svg"
    } 
    else {
        video.pause();
        playpause.src = "./icon/play.svg"
    }
});


// 监听音量变化
video.addEventListener("volumechange", (e)=>{
    volumeValue.innerHTML = Math.floor(video.volume * 100);
    volumeBarDone.style.height = video.volume * volumeBar.offsetHeight + 'px';
});


// 点击音量条
volumeBar.addEventListener("click", (e) => {
    const barRec = volumeBar.getBoundingClientRect();
    var pos = (barRec.bottom - e.pageY) / volumeBar.offsetHeight;
    if(pos > 1)
        pos = 1;
    else if(pos < 0)
        pos = 0;
    video.volume = pos;
});

// 拖动音量条
volumeBar.addEventListener("mousedown", (e) => {
    mouseDragForVolume = true;
})


// 静音键
mute.addEventListener("click", (e) => {
    video.muted = !video.muted;
    if(video.muted)
        mute.src = "./icon/mute.svg";
    else
        mute.src = "./icon/volume.svg";
});

// 画中画
picInPic.addEventListener("click", () => {
    video.requestPictureInPicture();
})


// 同步进度条时间
video.addEventListener("timeupdate", () => {
    progress.setAttribute("max", video.duration);
    progress.value = video.currentTime;

    // 控制圆点
    progressDot.style.marginLeft = (progress.value / video.duration) * progress.offsetWidth - progressDot.offsetWidth / 2 + "px";

    // 时间显示
    currentTime.innerHTML = getFormatTime(video.currentTime, video.duration);
    totalTime.innerHTML = getFormatTime(video.duration, video.duration);
});


// 点击进度条
progress.addEventListener("click", (e) => {
    const barRec = progress.getBoundingClientRect();
    const pos = (e.pageX - barRec.left) / progress.offsetWidth;
    video.currentTime = pos * video.duration;
});


// 拖动进度条
progress.addEventListener("mousedown", (e) => {
    mouseDragForProgress = true;
});


// 全屏
fullscreen.addEventListener("click", (e) => {
    if (document.fullscreenElement !== null) {
        // 当下处于全屏模式
        document.exitFullscreen();
    } 
    else {
        // 当下并非全屏模式
        videoContainer.requestFullscreen();
    }
    videoContainer.setAttribute("data-fullscreen", !!document.fullscreenElement);
});


// 根据总时长格式化为 00:00 或 00:00:00 的格式
function getFormatTime(time, duration) {
    var time = time || 0;         
    
    var h = parseInt(time / 3600),
        m = parseInt(time % 3600 / 60),
        s = parseInt(time % 60);

    s = s < 10 ? "0" + s : s;

    if (duration >= 3600){
        m = m < 10 ? "0" + m : m; 
        h = h < 10 ? "0" + h : h;
        return h + ":" + m + ":" + s;
    }
    else{
        if(m == 0)
            m = "00";
        else
            m = m < 10 ? "0" + m : m; 
        return m + ":" + s;
    }
}   

// 监听倍速列表中的元素
var speedSelected = multipleSpeedList[3];
speedSelected.style.color = "mediumaquamarine";
for(var i = 0; i < multipleSpeedList.length; i++){
    multipleSpeedList[i].addEventListener('click', function() {
        video.playbackRate = parseFloat(this.innerHTML);
        speedSelected.style.color = "white";
        speedSelected = this;
        speedSelected.style.color = "mediumaquamarine";
    })
}


// 开启视频循环
function openVideoCycle(obj){
    if(obj.checked){
        video.loop = true;
    }
    else
        video.loop = false;
}

// 开启视频镜像
function openVideoMirror(obj){
    if(obj.checked){
        video.style.transform = "rotateY(180deg)";
    }
    else
        video.style.transform = "none";
}