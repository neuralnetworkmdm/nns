function progress(eta){
	var elem=document.getElementById("progressbar");
	var width=1;
	var id=setInterval(frame, eta*10);
	function frame(){
		if(width>=100){
			clearInterval(id);
		}else{
			width++;
			elem.style.width=width+'%';
		}
	}
}
