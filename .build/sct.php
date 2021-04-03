<?php

/**
 *  @author Anthony Lawrence
 */

require_once __DIR__ . "/functions.php";

$template = file_get_contents(__DIR__ . "/sct_template.txt");

$template = explode("\n", $template);

$airportData = sctgen_generate_airport_data_list();
$fileUses = [];
$priorityUses = [];

foreach ($template as $lineNumber => $line) {
    $line = trim($line);

    if (!$line or $line == "") {
        continue;
    }

    if ($line[0] == "=") {
        print ltrim($line, "=")."\n";
        continue;
    }

    if ($line[0] == "[") {
        print trim($line)."\n";
        continue;
    }

    $modifier = null;
    if (preg_match("/^[^;].*?(;(.*?))$/i", $line, $findModifier)) {
        $line = str_replace($findModifier[1], "", $line);
        $modifier = $findModifier[2];
    }

    if (!preg_match("/[A-Za-z_]/i", $line[0])) {
        continue;
    }

    $line = str_replace("\\", "/", $line);

    $isPriority = false;
    $priorityKey = 0;
    $priorityPosition = 0;
    if ($line[0] == "_" && preg_match("/^\_p(?P<key>\d+)\_(?<pos>\d+)\_/i", trim($line), $matches)) {
        $isPriority = true;
        $priorityKey = $matches["key"];
        $priorityPosition = $matches["pos"];
        if (!isset($priorityUses[$priorityKey])) {
            $priorityUses[$priorityKey] = [];
        }
        $line = preg_replace("/^\_p(?P<key>\d+)\_(?<pos>\d+)\_/i", "", $line);
    }


    try {
        $filesToInclude = sctgen_generate_file_list("./", $line);
    } catch (Exception $e) {
        print "Error with line: " . $line . "\n\n\n";
        print $e->getMessage() . "\n\n\n";
    }

    if ($modifier) {
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
            foreach ($filesToIncludeModified as $obj) {
                $obj5 = $obj[5];
                unset($obj[5]);
                $filesToInclude[$obj5] = $obj;
            }
        }

        if ($modifier[0] == "ignore" or $modifier[0] == "remove") {
            $modifier[1] = explode(",", $modifier[1]);
            foreach ($filesToInclude as $key => $file) {
                foreach ($modifier[1] as $mod) {
                    if (preg_match("/".$mod."/", $key)) {
                        unset($filesToInclude[$key]);
                    }
                }
            }
        }
    }

    foreach ($filesToInclude as $fullPath => $fileObject) {
        if (isset($fileUses[$fullPath])) {
            $fileUses[$fullPath]++;
        } else {
            $fileUses[$fullPath] = 1;
        }
        $currentFileUsage = $fileUses[$fullPath];

        preg_match("/[A-Z]{4}/", $fullPath, $matches);
        $icao = isset($matches[0]) ? trim($matches[0]) : null;

        if ($isPriority && $icao) {
            if (isset($priorityUses[$priorityKey][$icao])) {
                continue;
            }

            $priorityUses[$priorityKey][$icao] = $priorityPosition;
        }

        $file_contents = file_get_contents($fullPath);

        $version = isset($_GET['version']) ? $_GET['version'] : "DEV-".exec('git log -n 1 --pretty=format:"%h"');

        $file_contents = str_replace("{YEAR}", gmdate("Y"), $file_contents);
        $file_contents = str_replace("{VERSION}", $version, $file_contents);
        $file_contents = str_replace("{BUILD}", gmdate("Y-m-d"), $file_contents);

        if (preg_match("/Basic.txt/", $fullPath) or preg_match("/Airports\/Other\/\w{4}.txt/", $fullPath)) {
            $file_contents = explode("\n", $file_contents);

            print $icao . " ";
            print trim($file_contents[2]) . " ";
            print trim($file_contents[1]) . " ";
            print "E";
            print " ; ".$airportData[$icao]["name"];

            print "\n";
            continue;
        }

        if (preg_match("/Runway.txt/", $fullPath, $matches)) {
            $file_contents = trim($file_contents);

            if ($file_contents == "") {
                continue;
            }

            $file_contents = explode("\n", $file_contents);
            foreach ($file_contents as $rwy) {
                print trim($rwy)." ".$icao." ".$airportData[$icao]["name"]."\n";
            }

            continue;
        }

        if (preg_match("/Fixes.txt/", $fullPath, $matches) && $icao) {
            print "; ".$airportData[$icao]["name"]. " (".$icao.") Fixes\n";
        }

        if (preg_match("/FIXES_(.*?).txt/", $fullPath, $matches) && $icao) {
            print "; ".$matches[1]." FIXES\n";
        }

        if (preg_match("/Geo.txt/", $fullPath, $matches) && $icao) {
            print "; Start ".$airportData[$icao]["name"]. " (".$icao.") Geo\n";
        }

        if (preg_match("/Centreline.txt/", $fullPath, $matches) && $icao) {
            print "; ".$airportData[$icao]["name"]. " (".$icao.")\n";

            if ($currentFileUsage == 1) {
                $file_contents = explode("\n", $file_contents);
                foreach ($file_contents as $fcl) {
                    print trim($fcl) . " centrelinecolour\n";
                }
                continue;
            }
        }

        if (preg_match("/Airways\/\w+\/(.*?)\.txt/", $fullPath, $matches)) {
            $file_contents = explode("\n", $file_contents);
            foreach ($file_contents as $fcl) {
                if (trim($fcl) == "") {
                    continue;
                }
                $trunc_matches = ltrim(strstr($matches[1], '/'), '/');
                print $trunc_matches . " " . trim($fcl) . "\n";
            }
            continue;
        }

        if (preg_match("/Labels.txt/", $fullPath, $matches) && $icao) {
            print "; Start ".$airportData[$icao]["name"]. " (".$icao.") Labels\n";
        }

        if (preg_match("/Regions.txt/", $fullPath, $matches) && $icao) {
            print "; Start ".$airportData[$icao]["name"]. " (".$icao.") Regions\n";
        }

        if (preg_match("/Regions\_(.*?).txt/", $fullPath, $matches)) {
            print "; Start ".$matches[1]."\n";
        }

        print $file_contents;
        print "\n";

        if (preg_match("/Geo.txt/", $fullPath, $matches) && $icao) {
            print "; End ".$airportData[$icao]["name"]. " (".$icao.") Geo\n";
        }

        if (preg_match("/Labels.txt/", $fullPath, $matches) && $icao) {
            print "; End ".$airportData[$icao]["name"]. " (".$icao.") Labels\n";
        }

        if (preg_match("/Regions.txt/", $fullPath, $matches) && $icao) {
            print "; End ".$airportData[$icao]["name"]. " (".$icao.") Regions\n";
        }
    }

    print "\n";
}
