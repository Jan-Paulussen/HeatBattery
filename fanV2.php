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

<FORM NAME ="form31" METHOD ="POST" ACTION ="fanV2.php">
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'off'  ><b> Off </b>   :Switch fan off <br />
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'on'  ><b> On</b> :Switch fan on.<br />
<INPUT TYPE = "Submit" Name = "Submit31"  VALUE = "Select a mode for the Fan">
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
