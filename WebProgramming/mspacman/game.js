function init() {
	canvas = document.getElementById('game_canvas'); //Initializing the Canvas
	ctx = canvas.getContext('2d');	
	img = new Image(); //Initializing the Image
	img.onload = function(){
		ctx.drawImage(img, 322, 1, 464, 137, 0, 0, 464, 137); //background
		ctx.drawImage(img, 80, 20, 17, 17, 279, 114, 17, 17); //mrs pacman
		ctx.drawImage(img, 22, 120, 19, 19, 264, 52, 19, 19); //blue ghost
		ctx.drawImage(img, 61, 103, 19, 19, 279, 55, 19, 19); //pink ghost
		ctx.drawImage(img, 22, 142, 19, 19, 296, 54, 19, 19); //yellow ghost
		ctx.drawImage(img, 102, 83, 19, 19, 280, 30, 19, 19); //red ghost
	};
	img.src = 'pacman10-hp-sprite.png';
}