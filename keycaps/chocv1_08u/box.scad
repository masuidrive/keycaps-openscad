include <../../lib/choc.scad>
include <../../lib/utils.scad>

// DEBUG = "x";

$fs = 0.1;

preview_chocv1_switch(DEBUG) {
  union() {
    keycap_basic_shape(
      15.6, // top_size
      1.5, // head_height
      0, // middle_size
      1.0, // skert_height
      15.6, // bottom_size
      1.0, // thickness
      2.0 // r
    );
    kailh_choc_v1_stem();
  }
}