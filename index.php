
<html>
<title>MultiTrack</title>
<body>

<?php

    exec('./multitrack.sh', $lines);
    echo "<ul>";
    array_map(function($l) { echo "<li>$l</li>"; }, $lines);
    echo "</ul>";

?>

</body>
</html>


