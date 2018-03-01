function countdown(time){
	var countTo = new Date();
	countTo.setSeconds(countTo.getSeconds() + time);
	var countDownDate = countTo.getTime();
	var countdown = setInterval(function(){
		var now = new Date().getTime();
		var delta = countDownDate - now;
		var minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((delta % (1000 * 60)) / 1000);
		document.getElementById("countdown").innerHTML = minutes + ":" + seconds;
		if(delta < 0){
			clearInterval(countdown);
			document.getElementById("countdown").innerHTML = "Quelques secondes...";
		}
	}, 1000);
};
