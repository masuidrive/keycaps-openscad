include <../../lib/choc.scad>
include <../../lib/utils.scad>

DEBUG = false;//"x";

preview_chocv1_switch(DEBUG) {
  top_size = 15.6;
  head_height = 1.5;
  middle_size = 0;
  skert_height = 2.0; 
  bottom_size = 15.6;
  thickness = 1.0;
  side_r = 2.0;
  cylindrical_depth = 1.0;

  union() {
    keycap_basic_shape(top_size, head_height, middle_size, skert_height, bottom_size, thickness, side_r);      
    kailh_choc_v1_stem();
  }
}
