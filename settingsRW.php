<?php
// Connect to the HeatBatt database
$conn = mysqli_connect("localhost", "root", "raspberry", "HeatBatt");

// Check for a successful connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// SELECT query to retrieve the current settings
$query = "SELECT setting_id, setting_name, setting_value FROM settings";
$result = mysqli_query($conn, $query);

// Display the current settings in a table
echo "<table>";
echo "<tr><th>Setting ID</th><th>Setting Name</th><th>Setting Value</th></tr>";
while ($row = mysqli_fetch_assoc($result)) {
    echo "<tr>";
    echo "<td>" . $row["setting_id"] . "</td>";
    echo "<td>" . $row["setting_name"] . "</td>";
    echo "<td>" . $row["setting_value"] . "</td>";
    echo "</tr>";
}
echo "</table>";

// Form to update the settings
echo "<form action='update.php' method='post'>";
echo "<label for='setting_id'>Setting ID:</label>";
echo "<input type='text' id='setting_id' name='setting_id'><br>";
echo "<label for='setting_name'>Setting Name:</label>";
echo "<input type='text' id='setting_name' name='setting_name'><br>";
echo "<label for='setting_value'>Setting Value:</label>";
echo "<input type='text' id='setting_value' name='setting_value'><br>";
echo "<input type='submit' value='Update'>";
echo "</form>";

// Close the database connection
mysqli_close($conn);
?>
