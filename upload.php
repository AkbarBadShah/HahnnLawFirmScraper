<?PHP
$wp_dir = "/var/www/html/";
require_once($wp_dir . 'wp-load.php');
$wp_dir = $wp_dir . "wp-admin/includes/";
require_once($wp_dir . "post.php");
require_once($wp_dir . "taxonomy.php");
// function create_posts($name, $file){
$name = 'Scraped';
$file = 'posts.json';
    $categoryID = wp_insert_category(array('cat_name' => $name));
    $data = file_get_contents($file);
    $characters = json_decode($data);
    $count = 1;
    foreach ($characters as $character) {
        $leadTitle = $character->name;
        $leadContent = $character->description;
        $new_post = array(
            'post_title' => $leadTitle,
            'post_content' => $leadContent,
            'post_status' => 'pending',
            'post_author' => 1,
            'post_type' => 'post',
            'post_category' => array($categoryID)
        );
        $post_id = post_exists($leadTitle);
        if ($post_id) {
            echo $leadTitle . '\n' . $post_id;
        }
        else {
            echo 'does not exist<br>';
                $post_id = wp_insert_post($new_post);
                $finaltext = '';
                if ($post_id) {
                    $finaltext .= 'Yay, I made a new post.<br>' . $count;
                }
                else {
                    $finaltext .= 'Something went wrong and I didn\'t insert a new post.<br>';
                }
        }
        echo $finaltext;
        $count = $count+1;
    }


//     }
//create_posts("Practice Areas","practice_areas.json");

?>


