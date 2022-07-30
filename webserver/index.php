<?php
require_once "classes/helper/Database.php";

header('Content-Type: application/json');

function getData($query,$param,$param_name){
    global $conn;
    $conn->getConnection()->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stm = $conn->getConnection()->prepare($query);
    $stm->bindParam($param_name, $param, PDO::PARAM_STR);
    $stm->execute();
    return $stm;
}

$conn = new Database();
if(isset($_GET['steamId'])) {
    $steamId = $_GET["steamId"];
    $query = "SELECT sb_bans.name, sb_bans.reason, sb_admins.user, sb_bans.length, sb_bans.authid, sb_bans.created FROM sb_bans INNER JOIN sb_admins ON sb_bans.aid = sb_admins.aid WHERE sb_bans.authid = :id ORDER BY sb_bans.created DESC LIMIT 1";
    $param_name = ":id";
    $stm = getData($query, $steamId, $param_name);

    if ($stm->rowCount() == 1) {
        $ban = $stm->fetch();
        http_response_code(200);
        $tmp = array("name"=>$ban["name"], "reason"=>$ban["reason"], "user"=>$ban["user"], "authid"=>$ban["authid"], "length"=>$ban["length"], "created"=>$ban["created"]);
        echo json_encode($tmp, JSON_PRETTY_PRINT);
    }
    else{
        http_response_code(404);
        echo $json = json_encode("not found");
    }
}
elseif(isset($_GET['ip'])) {
    $ip = $_GET["ip"];
    $query = "SELECT sb_bans.name, sb_bans.reason, sb_admins.user, sb_bans.length, sb_bans.authid, sb_bans.created  FROM sb_bans INNER JOIN sb_admins ON sb_bans.aid = sb_admins.aid WHERE sb_bans.ip = :ip ORDER BY sb_bans.created DESC";
    $param_name = ":ip";
    $stm = getData($query, $ip, $param_name);

    if ($stm->rowCount() > 0) {
        $arr = [];
        http_response_code(200);
        foreach($stm as $ban) {
            $tmp = array("name"=>$ban["name"], "reason"=>$ban["reason"], "user"=>$ban["user"], "authid"=>$ban["authid"],"length"=>$ban["length"], "created"=>$ban["created"]);
            array_push($arr, $tmp);
        }
        echo json_encode($arr, JSON_PRETTY_PRINT);
    }
    else{
        http_response_code(404);
        echo $json = json_encode("not found");
    }
}
$conn=null;
?>

