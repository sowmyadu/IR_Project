<?php
  header('Content-Type:text/html;charset=utf-8');

  $mapping_file = array_map('str_getcsv', file('URLtoHTML_fox_news.csv'));
  $query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
  $results = false;
  $rankingMethod = isset($_REQUEST['ranking_method']) ? $_REQUEST['ranking_method'] : "lucene";
  $limit = 10;
  $total = 0;
  $luceneParameters = array(
    'fl' => 'id,title,og_url,description'
  );
  $pageRankParameters = array(
    'fl' => 'id,title,og_url,description',
    'sort' => 'pageRankFile desc'
  );

  $additionalParameters = $luceneParameters;

  if($query){

    require_once('solr-php-client-master/Apache/Solr/Service.php');
    $solr = new Apache_Solr_Service('localhost',8983,'/solr/hw4core');
    if(get_magic_quotes_gpc()==1){
      $query = stripslashes($query);
    }

    if (strcmp($rankingMethod, "pagerank") == 0) {
        $additionalParameters = $pageRankParameters;
    }

    try{
      $results = $solr->search($query,0,$limit,$additionalParameters);
    }
    catch(Exception $e){
      die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
    }
  }

?>
<html>
<head>
  <title>Comparing Page Rank</title>
</head>
<body>
  <form accept-charset="utf-8" method="get">
    <center><label for="q">Query:</label>
    <input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query,ENT_QUOTES, 'utf-8');?>" />
    <input type="submit" value="Search"/></center><br/>
    <center>Ranking Algorithm:
    <input type="radio" name="ranking_method" value="lucene"
    <?php
    if (strcmp($rankingMethod, "lucene") == 0) {
        echo "checked";
    } ?>>Lucene &nbsp;&nbsp;&nbsp;
    <input type="radio" name="ranking_method" value="pagerank"
    <?php
    if (strcmp($rankingMethod, "lucene") != 0) {
        echo "checked";
    } ?>>External page rank<br/>
  </form><br/>

<?php
//display results
if($results)
{
  $total = (int)$results->response->numFound;
  $start=min(1,$total);
  $end = min($limit,$total);
?>

  <div>Results <?php echo $start;?>-<?php echo $end;?> of <?php echo $total; ?>:</div>
  <ol>
<?php
  //iterate document
  $resultDoc = $results->response->docs;
  foreach($resultDoc as $doc)
  {

?>
  <li style="text-align:center">
    <table style="border: 1px solid black;width:100%;margin-top:4px;text-align:left">

<?php
  //iterate document fields and values
  $value_array = array();
  foreach ($doc as $field => $value)
  {
    $fullid = $doc->id;
    $id = substr($fullid,62);
    $desc = $doc->description;
    if($desc==""){
      $desc = "N/A";
    }
    $title = $doc->title;
    $url = $doc->og_url;
    if($url==""){
      foreach($mapping_file as $file)
		  {
			     if($id == $file[0] )
			     {
				        $url = $file[1];
				        break;
			     }
		   }
    }
  }
?>
    <tr>
      <td>
        <?php
          echo "<b>Title: <a href = '$url'>$title</a> </b><br/>";
          echo "<a href = '$url' style='font-size:16px'>$url</a></br>";
          //echo "<b>Title: $title </b><br/>";
          echo "ID: $id <br/>";
          echo "Description: $desc <br/>";
        ?>
      </td>
    </tr>
</table>
</li>

<?php
  }
?>
</ol>
<?php
}
?>
</body>
</html>
