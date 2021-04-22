<?php

/**
 *  @author Anthony Lawrence
 */

require_once __DIR__ . "/functions.php";

$template = file_get_contents(__DIR__ . "/ese_template.txt");

$template = explode("\n", $template);

$airportData = sctgen_generate_airport_data_list();
$fileUses = [];
$priorityUses = [];
$currentSection = null;
$currentSectionModifier = null;

foreach($template as $lineNumber => $line){
    $line = trim($line);

    if(!$line OR $line == ""){
        continue;
    }

    if($line[0] == "="){
        print ltrim($line, "=")."\n";
        continue;
    }

    if($line[0] == "["){
        $currentSection = preg_replace("/[^A-Za-z0-9 \s:]/i", "", $line);
        $cs_split = explode(":", $currentSection);
        if(count($cs_split) >= 2){
            $currentSection = $cs_split[0];
            $currentSectionModifier = $cs_split[1];
        } else {
            $currentSectionModifier = null;
        }
        print trim($line)."\n";
        continue;
    }

    $modifier = null;
    if(preg_match("/^[^;].*?(;(.*?))$/i", $line, $findModifier)){
        $line = str_replace($findModifier[1], "", $line);
        $modifier = $findModifier[2];
    }

    if(!preg_match("/[A-Za-z_]/i", $line[0])){
        continue;
    }

    $line = str_replace("\\", "/", $line);

    $isPriority = false;
    $priorityKey = 0;
    $priorityPosition = 0;
    if($line[0] == "_" && preg_match("/^\_p(?P<key>\d+)\_(?<pos>\d+)\_/i", trim($line), $matches)){
        $isPriority = true;
        $priorityKey = $matches["key"];
        $priorityPosition = $matches["pos"];
        if(!isset($priorityUses[$priorityKey])){
            $priorityUses[$priorityKey] = [];
        }
        $line = preg_replace("/^\_p(?P<key>\d+)\_(?<pos>\d+)\_/i", "", $line);
    }


    try {
        $filesToInclude = sctgen_generate_file_list("./", $line);
    } catch(Exception $e) {
        print "Error with line: " . $line . "\n\n\n";
        print $e->getMessage() . "\n\n\n";
    }

    if($modifier) {
        $modifier = explode("=", trim($modifier));

        if ($modifier[0] == "sort") {
            $modifier[2] = isset($modifier[2]) ? (int) $modifier[2] : 0;

            $filesToIncludeModified = [];
            foreach ($filesToInclude as $key => $obj) {
                preg_match("/".$modifier[1]."/", $key, $sortMatches);
                $obj[5] = $key;
                $filesToIncludeModified[$sortMatches[$modifier[2]]] = $obj;
            }

            ksort($filesToIncludeModified);

            $filesToInclude = [];
            foreach($filesToIncludeModified as $obj){
                $obj5 = $obj[5];
                unset($obj[5]);
                $filesToInclude[$obj5] = $obj;
            }
        }

        if($modifier[0] == "ignore" OR $modifier[0] == "remove"){
            $modifier[1] = explode(",", $modifier[1]);
            foreach($filesToInclude as $key => $file){
                foreach($modifier[1] as $mod){
                    if(preg_match("/".$mod."/", $key)){
                        unset($filesToInclude[$key]);
                    }
                }
            }
        }
    }

    foreach($filesToInclude as $fullPath => $fileObject){
        if(isset($fileUses[$fullPath])){
            $fileUses[$fullPath]++;
        } else {
            $fileUses[$fullPath] = 1;
        }
        $currentFileUsage = $fileUses[$fullPath];

        preg_match("/[A-Z]{4}/", $fullPath, $matches);
        $icao = isset($matches[0]) ? trim($matches[0]) : null;

        if($isPriority && $icao){
            print $fullPath."\n";
            if(isset($priorityUses[$priorityKey][$icao])){
                continue;
            }

            $priorityUses[$priorityKey][$icao] = $priorityPosition;
        }

        $file_contents = file_get_contents($fullPath);

        $version = isset($_GET['version']) ? $_GET['version'] : "DEV-".exec('git log -n 1 --pretty=format:"%h"');

        $file_contents = str_replace("{YEAR}", gmdate("Y"), $file_contents);
        $file_contents = str_replace("{VERSION}", $version, $file_contents);
        $file_contents = str_replace("{BUILD}", gmdate("Y-m-d"), $file_contents);

        if(preg_match("/VRPs.txt/", $fullPath) && $icao){
            $file_contents = explode("\n", $file_contents);
            foreach($file_contents as $fcl){
                $fcl = explode(":", $fcl);

                if(count($fcl) < 3){ continue; }

                print $fcl[1].":".$fcl[2].":".$icao." VRPs:".$fcl[0]."\n";
            }

            print "\n";
            continue;
        }

        if(strcasecmp($currentSectionModifier, "REMCOMMENTS") == 0){
            $existingFileContents = explode("\n", $file_contents);
            $newFileContents = [];
            foreach($existingFileContents as $key => $line){
                if($line && $line[0] != ";"){
                    $newFileContents[] = $line;
                }
            }
            $file_contents = implode("\n", $newFileContents);
        }

        print $file_contents;
        print "\n";

        if(preg_match("/Positions(_Mentor)?.txt/", $fullPath, $matches)){
            print "\n";
        }

        if(strcasecmp($currentSection, "AIRSPACE") == 0){
            print "\n";
        }

        if(preg_match("/Sids.txt/", $fullPath, $matches) && $icao){
            print "\n";
        }

        if(preg_match("/Stars.txt/", $fullPath, $matches) && $icao){
            print "\n";
        }
    }

    print "\n";
}
