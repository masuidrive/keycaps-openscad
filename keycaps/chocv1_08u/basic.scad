include <../../lib/choc.scad>
include <../../lib/utils.scad>

// DEBUG = "y";

$fs = 0.1;

preview_chocv1_switch(DEBUG) {
  union() {
    keycap_basic_shape(
      12.5, // top_size
      1.5, // head_height
      14, // middle_size
      1.0, // skert_height
      15, // bottom_size
      1.0, //thickness
      1.0 // r
    );
    kailh_choc_v1_stem();
  }
}
