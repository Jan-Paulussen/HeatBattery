<html>
<title> Heat Battery</title>



<b>Heat Battery technician page</b> <br>
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


if (isset($_POST['SubmitB1'])) {
        $selected_bank1status = $_POST['bank1'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_bank1status' WHERE setting_name = 'Bank1_LIVE_power'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);
                                };


if (isset($_POST['SubmitB2'])) {
        $selected_bank2status = $_POST['bank2'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_bank2status' WHERE setting_name = 'Bank2_LIVE_power'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);
                                };

if (isset($_POST['SubmitB3'])) {
        $selected_bank3status = $_POST['bank3'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_bank3status' WHERE setting_name = 'Bank3_LIVE_power'";
          $result=mysqli_query($db_link, $query);
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

if (isset($_POST['Submit2'])) {
        $selected_percentage = $_POST['percentage'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE settings SET setting_value='$selected_percentage' WHERE setting_name = 'percentage'";
          $result=mysqli_query($db_link, $query);
          //$query="UPDATE Settings SET Value='$selected_percentage' WHERE Setting = 'HeatResistorC'";
          //$result=mysqli_query($db_link, $query);
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
  if($row["setting_name"] == "Bank1_MAX_power") {$bank1_max_pwr=$row["setting_value"]; };
  if($row["setting_name"] == "Bank2_MAX_power") {$bank2_max_pwr=$row["setting_value"]; };
  if($row["setting_name"] == "Bank3_MAX_power") {$bank3_max_pwr=$row["setting_value"]; };


  echo "</tr>";

$i++;
}

echo "</table>";
echo "<br/>";

// for debug: echo $bank1_max_pwr,$bank2_max_pwr,$bank3_max_pwr ;

// tot hier database uitlezen
?>

<FORM NAME ="form31" METHOD ="POST" ACTION ="technician.php">
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'off'  ><b> Off </b>   :Switch fan off <br />
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'on'  ><b> On</b> :Switch fan on.<br />
<INPUT TYPE = "Submit" Name = "Submit31"  VALUE = "Select a mode for the Fan">
</FORM>


<FORM NAME ="form33" METHOD ="POST" ACTION ="technician.php">
<INPUT TYPE = 'Radio' Name ='afterheating'  value= 'off'  ><b> Off </b>   :Switch afterheating off <br />
<INPUT TYPE = 'Radio' Name ='afterheating'  value= 'on'  ><b> On</b> :Switch afterheating on.<br />
<INPUT TYPE = "Submit" Name = "Submit33"  VALUE = "Select a on/off AfterHeating">
</FORM>


<FORM NAME ="form32" METHOD ="POST" ACTION ="technician.php">
<INPUT TYPE = 'Radio' Name ='modus'  value= 'auto'  ><b> Auto</b>   :Use excessive energy otherwise going to the grid <br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'timed'  ><b> Timed</b> :Charge defined hours.<br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'disabled'  ><b> Disabled</b> :Switch charging off.<br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'manual_percentage'  ><b> Manual %</b> :Switch to manual control of output%.<br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'manual_GPIO'  ><b> Manual GPIO</b> :Switch to manual control of output individually.<br />
<INPUT TYPE = "Submit" Name = "Submit32"  VALUE = "Select a mode for the Battery">
</FORM>

<form NAME ="form1" METHOD ="POST" ACTION ="technician.php">
   <label for="Percentage">Percentage:</label><br>
  <input type="text" id="Percentage" name="percentage">
  <INPUT TYPE = "Submit" Name = "Submit2"  VALUE = "Select a percentage for Heat Battery">
</form>
<br>


<FORM NAME ="formB1" METHOD ="POST" ACTION ="technician.php">
<INPUT TYPE = 'Radio' Name ='bank1'  value= '0'  ><b> Off </b>   :Switch Bank1 off <br />
<INPUT TYPE = 'Radio' Name ='bank1'  value=<?php echo $bank1_max_pwr?>  <b> On</b>  :Switch Bank1 on  <br />
<INPUT TYPE = "Submit" Name = "SubmitB1"  VALUE = "Select a mode for Resistor Bank1">
</FORM>

<FORM NAME ="formB2" METHOD ="POST" ACTION ="technician.php">
<INPUT TYPE = 'Radio' Name ='bank2'  value= '0'  ><b> Off </b>   :Switch Bank2 off <br />
<INPUT TYPE = 'Radio' Name ='bank2'  value=<?php echo $bank2_max_pwr?><b> On</b>  :Switch Bank2 on  <br />
<INPUT TYPE = "Submit" Name = "SubmitB2"  VALUE = "Select a mode for Resistor Bank2">
</FORM>

<FORM NAME ="formB3" METHOD ="POST" ACTION ="technician.php">
<INPUT TYPE = 'Radio' Name ='bank3'  value= '0'  ><b> Off </b>   :Switch Bank3 off <br />
<INPUT TYPE = 'Radio' Name ='bank3'  value= <?php echo $bank3_max_pwr?><b> On</b>  :Switch Bank3 on  <br />
<INPUT TYPE = "Submit" Name = "SubmitB3"  VALUE = "Select a mode for Resistor Bank3">
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
