<?php

include('index.html');


function updateSQL(){ 
    $link = mysqli_connect("localhost:3306", "root", "root", "panneau");

    if ($link->connect_errno) {
        echo "Echec lors de la connexion à mysqli : (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
    }
    $sql = "SELECT * FROM releves;" ;
    if($result = mysqli_query($link, $sql)){
        if(mysqli_num_rows($result) > 0){
            echo "<script language=\"javascript\" type=\"text/javascript\"> \n";
            echo "// Variables essentielles au fonctionnement des données\n";
            while($row = mysqli_fetch_array($result)){
                    $time[] = $row['date'];
                    $dir[] = $row['dir'];
                    $moy[] = $row['moy'];
                    $raf[] = $row['raf'];
                   
            }
        echo "// Taille de time : ", sizeof($time), "\n";
        echo 'timeStamps=[';
        $coma = 0;
           
            for($da = 0; $da < sizeof($time)-46; $da++){
                echo '"';
                echo $time[$da];
                echo '"';
            
                if($coma<11){
                    echo ",";
                }
                $coma++;
            }
        echo "] \n";
        echo 'dir=';
        echo $dir[1];
        echo "\n";
        echo 'medians=[';
        $coma = 0;
            for($da = 0; $da < sizeof($moy)-46; $da++){
                echo '"';
                echo $moy[$da];
                echo '"';
            
                if($coma<11){
                    echo ",";
                }
                $coma++;
            }
        echo "] \n";
        echo 'raffales=[';
        $coma = 0;
            for($da = 0; $da < sizeof($raf)-46; $da++){
                echo '"';
                echo $raf[$da];
                echo '"';
            
                if($coma<11){
                    echo ",";
                }
                $coma++;
            }
        echo "] \n";
        echo "seuil=[";
        $coma=0;
        for($da = 0; $da < sizeof($raf)-46; $da++){
            echo 57;
            if($coma<11){
                echo ",";
            }
            $coma++;
        }
        echo "]";

        
    }
    }
    
    if ($link->connect_errno) {
        echo "Echec lors de la connexion à mysqli : (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
    }
    $sql = "SELECT * FROM etats;" ;
    if($result = mysqli_query($link, $sql)){

        if(mysqli_num_rows($result) > 0){
            while($row = mysqli_fetch_array($result)){
                echo "\nlet mode = ";
                echo $row['mode'];
                echo ";\nlet current =";
                echo $row['current'];
                echo ';';
                echo "</script>\n";
                
            }
        }
        echo "</script>";
    }

    function securePanel() {
        $link = mysqli_connect("localhost:3306", "root", "root", "panneau");
        if ($link->connect_errno) {
            echo "Echec lors de la connexion à mysqli : (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
        }
        $sql = "UPDATE etats SET current = NOT current;" ;
        mysqli_query($link, $sql);

    }
    function switchModes() {
        $link = mysqli_connect("localhost:3306", "root", "root", "panneau");
        if ($link->connect_errno) {
            echo "Echec lors de la connexion à mysql : (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
        }
        $sql = "UPDATE etats SET mode = NOT mode;" ;
        mysqli_query($link, $sql);

    }
    if (isset($_GET['secure'])) {
        securePanel();
    }
    if (isset($_GET['switch'])) {
        switchModes();
    }
}
updateSQL();

echo "<script src='./scripts/chart.js'></script>\n<script src='./scripts/timeProcessing.js'></script>\n<script src='./scripts/secure.js'></script>    <script src='./scripts/modeswapper.js'></script>";



?>


