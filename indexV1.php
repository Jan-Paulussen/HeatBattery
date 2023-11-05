<html>
<title> Heat Battery</title>

<b>Start page  for Heat Batterij</b> <br>
---------------------------------------------------------<br><br>
<?php


//Vanaf hier uitvoeren  als radiobutton wordt gekozen
if (isset($_POST['Submit1'])) {
        $selected_radio = $_POST['modus'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE Settings SET Value='$selected_radio' WHERE Setting = 'Modus'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);

};

if (isset($_POST['Submit2'])) {
        $selected_percentage = $_POST['Percentage'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE Settings SET Value='$selected_percentage' WHERE Setting = 'Percentage'";
          $result=mysqli_query($db_link, $query);
          $query="UPDATE Settings SET Value='$selected_percentage' WHERE Setting = 'HeatResistorC'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);

};

if (isset($_POST['Submit31'])) {
        $selected_fanstatus = $_POST['fanstatus'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE Settings SET Value='$selected_fanstatus' WHERE Setting = 'FanStatus'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);

};

if (isset($_POST['Submit32'])) {
        $selected_Resistorbank1 = $_POST['Resistorbank1'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE Settings SET Value='$selected_Resistorbank1' WHERE Setting = 'HeatResistor1'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);

};

if (isset($_POST['Submit33'])) {
        $selected_Resistorbank2 = $_POST['Resistorbank2'];
        //Wegschrijven data in de database:
          $db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met my$
          $query="UPDATE Settings SET Value='$selected_Resistorbank2' WHERE Setting = 'HeatResistor2'";
          $result=mysqli_query($db_link, $query);
          mysqli_close($db_link);

};




// Read database and show it---------------------------------------------------------------------------------------------------------------------------------------------------
$db_link = mysqli_connect('localhost','root','raspberry','HeatBatt') or die ('<p><br/>fout: Database-problem opening</p>'); //Connecteren met de database, nu met mysql'i' sin$

$query="SELECT * FROM Settings";
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
 <th>Description</th>
</tr>
";

$i=0;
  while ($i < $num) {
 $row=mysqli_fetch_assoc($result);
  echo "<tr>";
  echo "<td><b>", $row["Value"] , "</b></td>";
  echo "<td>", $row["Setting"] , "</td> ";
  echo "<td>", $row["Description"] , "</td>"; 
  echo "</tr>";

$i++;
}

echo "</table>";
echo "<br/>";


// tot hier database uitlezen
?>
//Here starts the part of the inout fields by the user on the webpage-----------------------------------------------------------------------------------------

<form NAME ="form1" METHOD ="POST" ACTION ="index.php">
   <label for="Percentage">Percentage:</label><br>
  <input type="text" id="Percentage" name="Percentage">
  <INPUT TYPE = "Submit" Name = "Submit2"  VALUE = "Select a percentage for Heat Battery">
</form>
<br>

<FORM NAME ="form2" METHOD ="POST" ACTION ="index.php">
<INPUT TYPE = 'Radio' Name ='modus'  value= 'auto'  ><b> Automatic</b> :Use excessive energy otherwise going to the grid.<br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'timed'  ><b> Timed </b>   :Charge battery at certain fixed hours  <br />
<INPUT TYPE = 'Radio' Name ='modus'  value= 'IO-test'  ><b> IO-test</b> :Manually set the charging. Or control the IO for testing.<br />

<INPUT TYPE = "Submit" Name = "Submit1"  VALUE = "Select a mode for Heat Battery">
</FORM>

<FORM NAME ="form31" METHOD ="POST" ACTION ="index.php">
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'off'  ><b> Off </b>   :Switch fan off <br />
<INPUT TYPE = 'Radio' Name ='fanstatus'  value= 'on'  ><b> On</b> :Switch fan on.<br />
<INPUT TYPE = "Submit" Name = "Submit31"  VALUE = "Select a mode for the Fan">
</FORM>

<FORM NAME ="form32" METHOD ="POST" ACTION ="index.php">
<INPUT TYPE = 'Radio' Name ='Resistorbank1'  value= 'off'  ><b> Off </b>   :Switch Resistorbank1 off <br />
<INPUT TYPE = 'Radio' Name ='Resistorbank1'  value= 'on'  ><b> On</b> :Switch Resistorbank1 on.<br />
<INPUT TYPE = "Submit" Name = "Submit32"  VALUE = "Select a mode for Resistorbank1">
</FORM>

<FORM NAME ="form33" METHOD ="POST" ACTION ="index.php">
<INPUT TYPE = 'Radio' Name ='Resistorbank2'  value= 'off'  ><b> Off </b>   :Switch Resistorbank2 off <br />
<INPUT TYPE = 'Radio' Name ='Resistorbank2'  value= 'on'  ><b> On</b> :Switch Resistorbank2 on.<br />
<INPUT TYPE = "Submit" Name = "Submit33"  VALUE = "Select a mode for Resistorbank2">
</FORM>



<?php
echo "<br><center>Today is ";
echo date ('l jS \of F Y ');
echo (' - ');
echo date ('h:i:sa');
echo "<br> (C) Jan Paulussen";
echo "</center><br><br>";

?>

//Here below starts the explenation on the webpage, of the structure of everything-------------------------------------------------------------------------------------------------------------------
<p style="font-size:30px"><b>Structure:</b></p>
<br>
   <b>LAMP-server</b><br>
    --<i>index.php</i> 	(This page, with settings en current status, and where settings are input)<br><br>

   <b>MQTT-client</b><br>
    --<i></i> Is separate packet must be installed (e.g. with pip, MQTT-server en MQTT-clients installing)<br><br>

  <b><u>Python</u></b><br>
<i><b>--control.py</b></i> Program that controls physical GPIO, the triacs/optocouplers for the resistorbanks only (at fast speed!), <br>
It only reads the status for the 3 resistors from the database, and sets them accordingly on/off or at a percentage. 
(:HeatResistor1/2/C)<br>
It therefore does not matter if the system is manual or not, only the values written in the database for each output matter<br>
It does NOT control the fan (the fan is controlled in the slower control-program<br>
<b> in the sudo crontab!</b><br><br>

<i><b>--slow.py</b></i><b> - in crontab</b><br>
 Controls slow controls like the fan<br> (programmed already)
 Records setup values, every minute, in the SQL table Battery_log (Not programmed yet!)<br>
<br>


    --<i><b>valuesupdate.py</b></i> Program that reads the smart meter via the MQTT server or at 3AM if in timed mode, <br>
and puts values and calculations in the settings table of the SQL (paho-mqtt library install needed)<br>
The percentage etc. is also calculated here, depending of auto/timed mode, and the excessive power that is available in auto.<br>
<b>in crontab!</b><br>
<br>

--<i><b>banktest.py</b></i>
Program that tests the power a resistor bank is using.<br>
It's done by switching on and off the bank and read the difference from the smart metering.<br>
By doing this a number of times, a reasonable measurement is achieved (but it vries depending on the temperature)<br>
It should NOT go in the crontab, but only be run from the command line at startup, to establish the constants.


<br><br>
   <b>Crontab: </b>to start below programs at boot (and with some delays)<br>
		   ---control.py 	Script that reads the modus, and duty-cycle from the database 'HeatBatt' table  'Settings' and controls the output accordingly. It will also need to read the temperatures, and  control the fan<br>
		   ---valuesupdate.py   Script slimme meter uitlezen en in database zetten (MQTT-client)<br>
		   ---slow.py still to be written: Does slow control / Records all values every minute, for graphs and calculations (not programmed yet)<br>
<br><br>
//Here blow the IO pin assignement of the hardware-----------------------------------------------------------------------------------------------------------------------------------------------
<br><br>
<strong>I/O definition</strong><br>
GPIO20 (pin38) = Zero detection input<br>
GPIO21 (pin 40) = Ledpin triac output<br>
GPIO12 (pin32) = Resistorbank1 (orange)<br>
GPIO16 (pin36) = Resistorbank 2 (groen)<br>
GPIO26 (pin37) = Fan (geel)<br>



<br><br>
<strong>Todo/Bugs:</strong><br>
- Berekenen en sturen weerstanden batterij<br>
- Gaat bij volledige overschot niet verder dan 'on/on/30%'?!<br>
- Zelfs bij stroomtekort gaat rode led nog lichtjes knipperen<br>
- Setup tables in database in logging?<br>
 -inbouwen en inlezen thermocouple <br>
 -BACKUPS!!!(HeatBattery)

