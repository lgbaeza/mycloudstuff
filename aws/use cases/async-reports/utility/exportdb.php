<?php
    $IdReporte = $argv[1];
    $REMOTE_HOST = $argv[2];
    $PGPASSWORD = $argv[3];

    ini_set('memory_limit', '-1');

    try {
        $USER = "rdsiamuser";
        $DB_NAME = "YOUR_DB_NAME";
        $QUERY = "YOUR_QUERY";
        $dbconn = pg_connect("host=$REMOTE_HOST port=5432 dbname=$DB_NAME user=$USER password=$PGPASSWORD options='--client_encoding=UTF8' sslmode=verify-ca sslrootcert=rds-combined-ca-bundle.pem");
        $resultQuery = pg_query($dbconn, $QUERY);
        $resultSet = pg_fetch_all($resultQuery);

        //Headers
        $headers = array (YOUR_HEADERS_IN_CSV_FORMA);
        $csvExport = fopen("${IdReporte}.csv", 'w');
        fputcsv($csvExport, $headers);
        foreach ($resultSet as $fields) {
            fputcsv($csvExport, $fields);
        }
        fclose($csvExport);
        echo 0;
    }catch(Exception $ex){
        echo $ex;
    }

?>