<?php

/**
 *  @author Anthony Lawrence
 */

function sctgen_generate_airport_data_list(){
    $airportData = [];

    $airportFilesList = ["Airports/[A-Z]{4}/Basic.txt", "Airports/Other/[A-Z]{4}.txt"];
    foreach($airportFilesList as $afl) {
        $airportFiles = sctgen_generate_file_list("./", $afl);
        foreach ($airportFiles as $af => $afObj) {
            preg_match("/(?<icao>[A-Z]{4})/", $af, $matches);

            if (!isset($matches["icao"])) {
                continue;
            }

            $icao = $matches["icao"];

            $_tmp = file_get_contents($af);
            $_tmp = explode("\n", $_tmp);
            $_tmp = array_map("trim", $_tmp);

            $a = [];
            $a["name"] = $_tmp[0];
            $airportData[ $icao ] = $a;
        }
    }

    return $airportData;
}

function sctgen_generate_regex_safe($regex){
    $regex = str_replace("/", "\/", $regex);
    $regex = str_replace(".", "\.", $regex);
    $regex = str_replace("*", ".*?", $regex);
    $regex = trim($regex);
    return $regex;
}

function sctgen_generate_file_list($dir, $regex){
    $regex = sctgen_generate_regex_safe($regex);

    $dataFilesDirectory = new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS);
    $dataFilesIterator = new RecursiveIteratorIterator($dataFilesDirectory);
    $dataFilesRegex = new RegexIterator($dataFilesIterator, "/".$regex."/", RecursiveRegexIterator::GET_MATCH);

    $dataFiles = [];
    foreach($dataFilesRegex as $key => $object){
        $dataFiles[$key] = $object;
    }

    ksort($dataFiles);

    return $dataFiles;
}
