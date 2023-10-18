include <../../lib/choc.scad>
include <../../lib/utils.scad>

// DEBUG = "x";

preview_chocv1_switch(DEBUG) {
  top_size = 15.6;
  head_height = 1.5;
  middle_size = 0;
  skert_height = 2.0; 
  bottom_size = 15.6;
  thickness = 1.0;
  side_r = 2.0;
    
  union() {
    difference() {
      keycap_basic_shape(top_size, head_height, middle_size, skert_height, bottom_size, thickness, side_r);      

      // calc r parameter on https://gist.github.com/masuidrive/b34472d82b07d0efead83aedf5579b78
      translate([0, 0, head_height+0.001])
      rotate([0, 180, 0])
        dome(width=12, height=1, r=18.500);

    }
    kailh_choc_v1_stem();
  }
}