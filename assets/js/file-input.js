document.getElementById("file").onchange=function(){
	document.getElementById("file-input-label").innerHTML=this.files[0].name;
};
document.getElementById("file_ep").onchange=function(){
	document.getElementById("file-input-label_ep").innerHTML=this.files[0].name;
};
$(function(){
	$("#dynamicSelect").change(function(){
		if($(this).val()!=""){
			$("#rangeOptionsConfig").show();
		} else {
			$("#rangeOptionsConfig").hide();
		}
	});
});
