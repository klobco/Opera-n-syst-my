<?php

$int_only = False;
$prase_only = False;
$recursive = False;
$parse = "./parse.php";
$interpret = "./interpret.py";
$path = ".";

$neusp_testy = 0;
$usp_testy = 0;

function err($kod,$text){
	fwrite(STDERR, "$kod: $text\n");
	exit($kod);
}

$tmp  = array(
    "help",
    "directory:",
    "recursive",
    "parse-script:",
    "int-script:",
    "parse-only",
    "int-only"  
);
$args = getopt("", $tmp);

if (array_key_exists("help",$args)) {
	if ($argc > 2){
		err(10,"Nespravny pocet argumentov, zadajte --help!");
	}
	echo("--help 					: Zobrazí nápovedu\n");
	echo("--directory=path 			: Cesta kde má hladať testy(ak nieje zadaná použije sa aktuálny adresár)\n");
	echo("--recusrsive 				: Ak je prepínač aktívny testy bude hladať aj v podadresároch\n");
	echo("--parse-script=file 			: Umiestnenie súboru parse.php(ak nieje zadaný bude ho hladať v aktuálnej zložke)\n");
	echo("--int-script=file 			: Umiestnenie súboru interpret.py(ak nieje zadaný bude ho hladať v aktuálnej zložke)\n");
	echo("--parse-only 				: Ak je prepínač aktívny tak sa budú vykonávať len testy na parse.php\n");
	echo("--int-only 				: Ak je prepínač aktívny tak sa budú vykonávať len testy na interpret.py\n");
}

#var_dump($args);

if (array_key_exists("parse-only",$args) and array_key_exists("int-script",$args)){
	err(10,"Parameter parse-only a int-script sa nesmú kombinovať!");
}
if (array_key_exists("int-only",$args) and array_key_exists("parse-script",$args)){
	err(10,"Parameter int-only a parse-script sa nesmú kombinovať!");
}
if (array_key_exists("int-only",$args) and array_key_exists("parse-only",$args)){
	err(10,"parameter int-only a parse-only sa nesmie kombinovať!");
}
if (array_key_exists("directory",$args)){
	$path=$args["directory"];
}
if (array_key_exists("int-only",$args)){
	$int_only = True;
}
if (array_key_exists("parse-only",$args)){
	$prase_only = True;
}
if (array_key_exists("parse-script",$args)){
	$parse = $args["parse-script"];
}
if (array_key_exists("int-script",$args)){
	$interpret = $args["int-script"];
}
if (array_key_exists("recursive",$args)){
	$recursive = true;
}

echo"<!doctype html>

<html lang=\"cs\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">

    <title>Testy</title>
    <meta name=\"description\" content=\"test.php\">
    <meta name=\"author\" content=\"Martin Klobušický (xklobu03)\">
    <style>
    .green {
        color: green;
    }
    .red {
        color: red;
    }
    table{
        width:100%;
    }
    th{
        width:20%;
        border:none;
        height:40px;
    }
    td{ 
        width:20%;
        border:none;
        text-align:center;
        padding:10px;
    }

    </style>

</head>

<body>
<table border=0>
<tr>
	<th>Názov</th>
	<th>Výsledok</th>
	<th>Návratový kód</th>
</tr>
";

if ($recursive == false){
	$iterator = new DirectoryIterator($path);
}
if ($recursive == true){
	 $iterator=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS),RecursiveIteratorIterator::SELF_FIRST);
}


if ($recursive == false or $recursive == true){
	while($iterator->valid()) {
	    $file = $iterator->current();
	    $test= $file->getFilename();
	    $path = $file->getPath();
	    if(preg_match('/.+.src$/', $test)){
	    	echo("<tr>");
		  	$src = str_replace(".src", "", "$test");
		  	$src2 = ($path."/".$src."."."src");
		  	echo("<td>".$src."</td>");
			$rc = ($path."/".$src."."."rc");
			$in = ($path."/".$src."."."in");
			$out = ($path."/".$src."."."out");
			$vystup2 = ($path."/"."ten_jediny_a_pravy"."."."out");
			$vystup4 = ($path."/"."ten_jediny_a_pravy2"."."."out");
			if (file_exists($rc)) {
			    $rc_file = fopen($rc, 'r');
				$navrat = fgets($rc_file);
				$navrat = trim($navrat);
			} else {
			    $myfile = fopen("$rc", "w");
			    fwrite($myfile, "0");
			    $navrat = 0;
			}
			if (file_exists($in)) {

			} else {
			    $myfile = fopen("$in", "w");
			    fclose($myfile);
			}
			if (file_exists($out)) {

			} else {
			    $out_file = fopen("$out", "w");
			    fclose($out_file);
			}

			if($prase_only == true){
				if(!file_exists($parse)){
					err(10,"Súbor parse.php neexistuje!");
				}
				$vystup = fopen("$vystup2", "w");
				$kod = trim(shell_exec("php7.3 $parse <$src2 >/dev/null; echo $?"));

				if ($kod != $navrat){
					$neusp_testy++;
					echo("<td><b class=red>Neuspel</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					shell_exec("rm $vystup2");
					continue;
				}
				if ($kod != 0){
					if($kod == $navrat){
						$usp_testy++;
						echo("<td><b class=green>USPEL</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup2");
						continue;
					}
					else{
						$neusp_testy++;
						echo("<td><b class=red>Neuspel</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup2");
						continue;
					}
				}
				fwrite($vystup, trim(shell_exec("php7.3 $parse <$src2")));
				fclose($vystup);
				$diff=shell_exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar ".$vystup2 ." ".$out. " delta.xml /pub/courses/ipp/jexamxml/options >/dev/null;echo $?");
				shell_exec("rm $vystup2");
				if ($diff == 0){
					$usp_testy++;
					echo("<td><b class=green>USPEL</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					continue;
				}
				else{
					$neusp_testy++;
					echo("<td><b class=red>Neuspel</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					continue;
				}
			}

			if($int_only == true){
				if(!file_exists($interpret)){
					err(10,"Súbor interpret.py neexistuje!");
				}
				$vystup = fopen("$vystup2", "w");
				$kod = trim(shell_exec("python3.6 $interpret --source=$src2 --input=$in >/dev/null; echo $?"));
				if ($kod != $navrat){
					$neusp_testy++;
					echo("<td><b class=red>Neuspel</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					shell_exec("rm $vystup2");
					continue;
				}
				if ($kod != 0){
					if($kod == $navrat){
						$usp_testy++;
						echo("<td><b class=green>USPEL</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup2");
						continue;
					}
					else{
						$neusp_testy++;
						echo("<td><b class=red>Neuspel</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup2");
						continue;
					}
				}

				fwrite($vystup, trim(shell_exec("python3.6 $interpret --source=$src2 --input=$in")));
				fclose($vystup);
				$diff=trim(shell_exec("diff ".$vystup2." ".$out. "; echo $?"));
				shell_exec("rm $vystup2");
				if ($diff == 0){
					$usp_testy++;
					echo("<td><b class=green>USPEL</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					continue;
				}
				else{
					$neusp_testy++;
					echo("<td><b class=red>Neuspel</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					continue;
				}
			}
			if($int_only == false and $parse_only == false){
				if(!file_exists($interpret) or !file_exists($parse)){
					err(10,"Súbor interpret.py alebo parse.php neexistuje!");
				}
				$vystup = fopen("$vystup2", "w");
				$vystup3 = fopen("$vystup4", "w");
				$kod = trim(shell_exec("php7.3 $parse <$src2 >/dev/null; echo $?"));
				if ($kod != 0){
					if($kod == $navrat){
						$usp_testy++;
						echo("<td><b class=green>USPEL</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup2");
						shell_exec("rm $vystup4");
						continue;
					}
					else{
						$neusp_testy++;
						echo("<td><b class=red>Neuspel</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup4");
						shell_exec("rm $vystup2");
						continue;
					}
				}
				fwrite($vystup, trim(shell_exec("php7.3 $parse <$src2")));
				$kod = trim(shell_exec("python3.6 $interpret --source=$vystup2 --input=$in >/dev/null; echo $?"));
				if ($kod != 0){
					if($kod == $navrat){
						$usp_testy++;
						echo("<td><b class=green>USPEL</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup4");
						shell_exec("rm $vystup2");
						continue;
					}
					else{
						$neusp_testy++;
						echo("<td><b class=red>Neuspel</b></td>");
						echo("<td>".$kod."</td>");
						echo("</tr>");
						$iterator->next();
						shell_exec("rm $vystup4");
						shell_exec("rm $vystup2");
						continue;
					}
				}
				fwrite($vystup3, trim(shell_exec("python3.6 $interpret --source=$vystup2 --input=$in")));
				fclose($vystup);
				fclose($vystup3);
				$diff=trim(shell_exec("diff ".$vystup4." ".$out. "; echo $?"));
				shell_exec("rm $vystup2");
				shell_exec("rm $vystup4");
				if ($diff == 0){
					$usp_testy++;
					echo("<td><b class=green>USPEL</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					continue;
				}
				else{
					$neusp_testy++;
					echo("<td><b class=red>Neuspel</b></td>");
					echo("<td>".$kod."</td>");
					echo("</tr>");
					$iterator->next();
					continue;
				}
			}
		}
	    $iterator->next();
	}
}
$celkom = $neusp_testy+$usp_testy;
echo"<table border=0>
<tr>
	<th>Celkom testov</th>
	<th>Uspesne testy</th>
	<th>Neuspesne testy</th>
</tr>";
echo("<td><b class=green>".$celkom."</b></td>");
echo("<td><b class=green>".$usp_testy."</b></td>");
echo("<td><b class=green>".$neusp_testy."</b></td>");
echo("</table>");
echo("</table>");
echo("</body>");
?>