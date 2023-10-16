include <../../lib/choc.scad>
include <../../lib/utils.scad>

// DEBUG = "y";

$fs = 0.1;
$fa = 0.25;

preview_chocv1_switch(DEBUG) {
  top_size = 12;
  head_height = 1.5;
  middle_size = 14.5;
  skert_height = 1.0; 
  bottom_size = 15.6;
  thickness = 1.0;
  r = 1.0;
  cylindrical_depth = 1.0;
  
  union() {
    difference () {
      keycap_basic_shape(top_size, head_height, middle_size, skert_height, bottom_size, thickness, r);      
      head_cylindrical_depress(top_size, head_height, cylindrical_depth);
    }
    kailh_choc_v1_stem();
  }
}
