$fs = 0.1;

module rounded_cube (size, r) {
  h = 0.0001; // cylinder の高さ (適当な値)
  minkowski () {
    cube([size[0] - r*2, size[1] - r*2, size[2] - h], center = true);
    cylinder(r = r, h = h);
  }
}

module keycap_outer_shape (key_bottom_size, key_top_size, key_top_height) {
    hull () {
        translate([0, 0, key_top_height])
        rounded_cube([key_top_size, key_top_size, 0.01], 1);
        rounded_cube([key_bottom_size, key_bottom_size, 0.01], 1);
    }
}

module keycap_shape () {
  difference () {
    keycap_outer_shape(16.5, 14.5, 3.5);
    // 一回り小さいキーキャップ外形
    keycap_outer_shape(14.5, 12.5, 1.5);
  }
}

keycap_shape();

module kailh_choc_v1_stem() {

    // Latches for switch housing
    translate([-2.85, 0, 0])
    cube([1, 2, 3], center=true);
    translate([2.85, 0, 0])
    cube([1, 2, 3], center=true);
}

kailh_choc_v1_stem();