var page = require('webpage').create(),system = require('system'),address;
console.log('The default user agent is ' + page.settings.userAgent);
phantom.outputEncoding="gbk";
if (system.args.length == 1){
	phantom.exit(1);
}else{
	address = system.args[1];
	page.open(address, function(status) {
  if (status !== 'success') {
    console.log('Unable to access network');
    phantom.exit();
  } else {
    var ua = page.evaluate(function() {
      return document.getElementById('detail').innerHTML;
    });
    window.setTimeout(function(){
    	console.log(ua);
  		phantom.exit();
    },1000)
  }
});
};
