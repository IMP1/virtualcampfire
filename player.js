const PROGRESS_BAR_TICK_DURATION = 250; // ms

let progressBarInterval = null;
let queue = [];
let hasAudioSupport = false;
let looping = false;
let shuffle = false;

function play(url) {
    if (!hasAudioSupport) { return; }
    let songName = document.getElementById("player-title");
    songName.textContent = getSongName(url);
    let authorName = document.getElementById("player-author");
    // TODO: Get song info to get author
    authorName.textContent = "Author, Date";
    window.currentAudioElement.src = getSongAudioUrl(url);
    window.currentAudioElement.addEventListener("playing", onStartPlaying);
    window.currentAudioElement.play();
    setPlaying();
}

function onStartPlaying() {
    let songDuration = document.getElementById("player-timeline").getElementsByTagName("span")[1];
    let timeProgress = document.getElementById("player-progress");
    timeProgress.max = window.currentAudioElement.duration;
    timeProgress.value = 0;
    songDuration.textContent = toTimeString(timeProgress.max);
    window.currentAudioElement.removeEventListener("playing", onStartPlaying); // Don't happen on resume
}

function addToQueue(url) {
    queue.push(url);
}

function pause() {
    if (!hasAudioSupport) { return; }
    window.currentAudioElement.pause();
    setPaused();
}

function resume() {
    if (!hasAudioSupport) { return; }
    window.currentAudioElement.play();
    setPlaying();
}

function rewind() {
    if (!hasAudioSupport) { return; }
    window.currentAudioElement.currentTime = 0;
}

function skip() {
    if (!hasAudioSupport) { return; }
    finishSong();
}

function toggleLoop() {
    const btn = document.getElementById("player-loop");
    btn.classList.toggle("inactive");
}

function toggleShuffle() {
    const btn = document.getElementById("player-shuffle");
    btn.classList.toggle("inactive");
}

function showQueue() {

}

function showLyrics() {
    
}

function showSongInfo() {
    
}

function downloadSong(url) {
    const link = document.createElement("a");
    link.download = getSongName(url);
    link.href = getSongAudioUrl(url);
    link.target = "_blank";
    document.body.appendChild(link);
    console.log(link);
    link.click();
    document.body.removeChild(link);
}

function setPlaying() {
    document.getElementById("player-controls").classList.remove("hidden");
    const playButton = document.getElementById("player-play-pause");
    playButton.onclick = pause;
    playButton.title = "Pause";
    const icons = playButton.getElementsByTagName("svg");
    icons[0].style.display = "none";
    icons[1].style.display = "inline-block";

    const timeProgress = document.getElementById("player-progress");
    const timeSpan = document.getElementById("player-timeline").getElementsByTagName("span")[0];
    timeInterval = setInterval(function() {
        timeProgress.value = window.currentAudioElement.currentTime;
        timeSpan.textContent = toTimeString(window.currentAudioElement.currentTime);
    }, PROGRESS_BAR_TICK_DURATION);
}

function setPaused() {
    clearInterval(timeInterval);
    const playButton = document.getElementById("player-play-pause");
    playButton.onclick = resume;
    playButton.title = "Play";
    const icons = playButton.getElementsByTagName("svg");
    icons[0].style.display = "inline-block";
    icons[1].style.display = "none";
}

function skipTo(time) {
    if (!hasAudioSupport) { return; }
    window.currentAudioElement.currentTime = time;
    const timeProgress = document.getElementById("player-progress");
    const timeSpan = document.getElementById("player-timeline").getElementsByTagName("span")[0];
    timeProgress.value = window.currentAudioElement.currentTime;
    timeSpan.textContent = toTimeString(window.currentAudioElement.currentTime);
}

function finishSong() {
    console.log(queue);
    if (queue.length > 0) {
        const nextSong = queue.shift();
        play(nextSong);
    } else {
        pause();
        let timeProgress = document.getElementById("player-progress");
        skipTo(timeProgress.max);
        window.currentAudioElement.currentTime = 0; // This is so pressing play will start the song again
    }
}

function getSongName(url) {
    url = decodeURIComponent(url);
    if (url.indexOf("/") >= 0) {
        url = url.substring(url.lastIndexOf("/") + 1, url.length);
    }
    url = url.substring(0, url.lastIndexOf("."));
    url = url.replaceAll("_", " ");
    return url;
}

function getSongAudioUrl(songUrl) {
    // TODO: Clean this up. What is it doing?
    var plain = new RegExp("^([^\(]+)\.mp3$");
    var m = plain.exec(decodeURI(songUrl));
    if (m != null) { 
        return m[1] + ".mp3";
    } else { 
        var withBrackets = new RegExp(/^([^\(]+?)_\(([^\)]+)\)/);
        var wb = withBrackets.exec(decodeURI(songUrl));
        if (wb != null) { 
            return wb[1] + ".mp3";
        } else { 
            return null;
        }
    }
}

function toTimeString(time) {
    const minutes = Math.floor(time / 60).toString();
    const seconds = Math.floor(time % 60).toLocaleString('en-GB', {
        minimumIntegerDigits: 2,
        useGrouping: false
    });
    return minutes + ":" + seconds;
}


function setup() {

    const bar = document.getElementById("player-progress");
    bar.addEventListener("click", function(e) {
        let x = e.pageX - bar.offsetLeft, // or e.offsetX (less support, though)
            y = e.pageY - bar.offsetTop,  // or e.offsetY
            clickedValue = x * bar.max / bar.offsetWidth;

        console.log(x, y);
        console.log(clickedValue);
        skipTo(clickedValue);
    });

    document.getElementById("player-show-lyrics").addEventListener("click", function() { 
        showLyrics(window.currentAudioElement.src); 
    });

    document.getElementById("player-show-info").addEventListener("click", function() { 
        showLyrics(window.currentAudioElement.src); 
    });

    document.getElementById("player-download").addEventListener("click", function() { 
        downloadSong(window.currentAudioElement.src); 
    });

    window.currentAudioElement = document.getElementById("player");
    if (typeof window.currentAudioElement === 'undefined') { 
        alert('your browser does not like audio.');
    } else {
        hasAudioSupport = true;
    }
    window.currentAudioElement.addEventListener("ended", finishSong);
}

window.addEventListener("load", setup);
