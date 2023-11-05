
<meta http-equiv="refresh" content="3">

<b>Settings in database:</b><br>
--------------------------<br>

<?php
    //connect to the database
    $servername = "localhost";
    $username = "root";
    $password = "raspberry";
    $dbname = "HeatBatt";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    //select all data from the settings table
    $sql = "SELECT * FROM settings";
    $result = $conn->query($sql);

    //check if there are any results
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            echo "ID: " . $row["setting_id"]. " - : " . $row["setting_name"]. " - : <b>" . $row["setting_value"]. "</b><br>";
        }
    } else {
        echo "0 results";
    }
    $conn->close();
?>

<br><br>
<!-- Link to main page -->
<form action="index.html">
    <input type="submit" value="Go to Main page" />
</form>



