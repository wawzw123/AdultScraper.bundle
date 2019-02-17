<?php
$imageurl = $_GET['url'];
$mode = $_GET['mode'];
$data='';
$xx =$_GET['x'];
$width = $_GET['w'];
$height = $_GET['h'];
$headers = array(
'Accept: image/webp,*/*',
'Accept-Encoding: gzip, deflate, br',
'Accept-Charset: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection: keep-alive',
'Cookie:__utma=217774537.2052325145.1549811165.1549811165.1549811165.1;__utmb=217774537.9.10.1549811165;__utmc=217774537;__utmz=217774537.1549811165.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
'Host: img.arzon.jp',
'Referer: https://www.arzon.jp/item_1502421.html',
'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
);
if ($mode=='M'){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $imageurl); 
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_BINARYTRANSFER, 1);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
	$data = curl_exec($ch);
	curl_close($ch);
}
if ($mode=='A'){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $imageurl); 
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_BINARYTRANSFER, 1);
	$data = curl_exec($ch);
	curl_close($ch);
}
$source = imagecreatefromstring($data);
header('Content-Type: image/jpeg');
$w = imagesx($source);
$h = imagesy($source);
$thumb = imagecreatetruecolor($width, $height);
$source = imagecreatefromstring($data);
imagecopyresampled($thumb, $source, 0, 0, 0, 0, $width, $height, $w, $h);
$thumb2 = imagecreatetruecolor($width-$xx, $height);
imagecopyresampled($thumb2, $thumb, 0, 0, $xx, 0, $width, $height, $width, $height);
imagejpeg($thumb2);
imagedestroy($thumb2);
?>

