include <../../lib/choc.scad>
include <../../lib/utils.scad>

// DEBUG = "x";

preview_chocv1_switch(DEBUG) {
  union() {
    difference() {
      head_height = 2.0;
      keycap_basic_shape(
        15.6, // top_size
        head_height, // head_height
        0, // middle_size
        2.0, // skert_height
        15.6, // bottom_size
        1.0, // thickness
        2.0 // side_r
      );
      translate([0, 0, head_height+0.001])
      rotate([0, 180, 0])
        dome(width=12, height=1, r=18.500);

    }
    kailh_choc_v1_stem();
  }
}