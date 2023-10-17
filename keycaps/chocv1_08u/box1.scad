include <../../lib/choc.scad>
include <../../lib/utils.scad>

DEBUG = "x";

preview_chocv1_switch(DEBUG) {
  union() {
    keycap_basic_shape(
      15.6, // top_size
      1.5, // head_height
      0, // middle_size
      2.0, // skert_height
      15.6, // bottom_size
      1.0, // thickness
      2.0 // side_r
    );
    kailh_choc_v1_stem();
  }
}
