<html>
<title> Heat Battery</title>

<b>Heat Batterij</b> <br>
---------------------------------------------------------<br><br>
<?php

if (isset($_POST['Submit31'])) {
        $selected_fanstatus = $_POST['fanstatus'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_fanstatus' WHERE setting_name = 'FanStatus'";
          $result=mysqli_query($db_link, $query);
          if ($selected_fanstatus =="off"){
             $query="UPDATE settings SET setting_value='off' WHERE setting_name = 'AfterHeating'";
             $result=mysqli_query($db_link, $query);

                                           };
          mysqli_close($db_link);

};


if (isset($_POST['Submit32'])) {
        $selected_modus = $_POST['modus'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_modus' WHERE setting_name = 'modus'";
          $result=mysqli_query($db_link, $query);

          if($selected_modus==disabled){
            $query="UPDATE settings SET setting_value='0' WHERE setting_name = 'percentage'"; //Reset outputs when set to disabled
            $result=mysqli_query($db_link, $query);
                           }
          mysqli_close($db_link);

};

if (isset($_POST['Submit33'])) {
        $selected_afterheating = $_POST['afterheating'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_afterheating' WHERE setting_name = 'AfterHeating'";
          $result=mysqli_query($db_link, $query);
          if ($selected_afterheating =="on"){
             $query="UPDATE settings SET setting_value='on' WHERE setting_name = 'FanStatus'";
             $result=mysqli_query($db_link, $query);
                                            };
          mysqli_close($db_link);

};




// Read database and show it---------------------------------------------------------------------------------------------------------------------------------------------------
$db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met mysql'i' sin$

$query="SELECT * FROM settings";
$result=mysqli_query($db_link, $query);
$num=mysqli_num_rows($result);

mysqli_close($db_link);

// From here display the all records from database 'HeatBatt', the table 'Settings'
echo "<b>The Heat Battery current Settings : </b><br/>

<style>
table th, td {
 border: 1px solid black
 }

</style>
<table style='width 100%'>
<tr>
 <th>Value</th>
 <th>Setting</th>
</tr>
";

$i=0;
  while ($i < $num) {
 $row=mysqli_fetch_assoc($result);
  echo "<tr>";
  echo "<td><b>", $row["setting_value"] , "</b></td>";
  echo "<td>", $row["setting_name"] , "</td> ";
  echo "</tr>";

$i++;
}

echo "</table>";
echo "<br/>";


// tot hier database uitlezen
?>

<FORM NAME ="form31" METHOD ="POST" ACTION ="user.php">
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'off'  ><b> Off </b>   :Switch fan off <br />
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'on'  ><b> On</b> :Switch fan on.<br />
<INPUT TYPE = "Submit" Name = "Submit31"  VALUE = "Select a mode for the Fan">
</FORM>


<FORM NAME ="form32" METHOD ="POST" ACTION ="user.php">
<INPUT TYPE = 'Radio' Name ='modus'  value= 'auto'  ><b> Auto</b>   :Use excessive energy otherwise going to the grid <br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'timed'  ><b> Timed</b> :Charge defined hours.<br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'disabled'  ><b> Disabled</b> :Switch charging off.<br />
<INPUT TYPE = "Submit" Name = "Submit32"  VALUE = "Select a mode for the Battery">
</FORM>

<FORM NAME ="form33" METHOD ="POST" ACTION ="user.php">
<INPUT TYPE = 'Radio' Name ='afterheating'  value= 'off'  ><b> Off </b>   :Switch afterheating off <br />
<INPUT TYPE = 'Radio' Name ='afterheating'  value= 'on'  ><b> On</b> :Switch afterheating on.<br />
<INPUT TYPE = "Submit" Name = "Submit33"  VALUE = "Select a on/off AfterHeating">
</FORM>



<!-- Link to main page -->
<form action="index.html">
    <input type="submit" value="Go to Main page" />
</form>



<?php
echo "<br><center>Today is ";
echo date ('l jS \of F Y ');
echo (' - ');
echo date ('h:i:sa');
echo "<br> (C) Jan Paulussen";
echo "</center><br><br>";

?>
