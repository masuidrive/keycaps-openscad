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
    dome_height = 1.0;

  union() {
    hull() {
      translate([0.0, 2.0, dome_height+head_height])
        rounded_plate(12.0, 5.0, side_r);
      translate([0.0, 0.0, head_height])
        rounded_plate(top_size, top_size, side_r);
    }
    keycap_basic_shape(top_size, head_height, middle_size, skert_height, bottom_size, thickness, side_r);
    kailh_choc_v1_stem();
  }
}
