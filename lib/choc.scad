// Choc V1の足を作る
module kailh_choc_v1_stem() {
  leg_length = 3.6;
  thin_length = 0.6;

  for (z = [-2.85, 2.85]) {
      translate([z, 0, -leg_length/2])
        hull() {
          cube([1, 2, leg_length], center=true);
          translate([0, 0, -(leg_length/2)-thin_length])
            cube([0.5, 1, 0.001], center=true);
        };
  }
}


module preview_chocv1_switch(DEBUG=true) {
  union() {
    children();

    if(DEBUG == true || DEBUG == "x") {
      translate([20, 20, 0])
      difference() {
        union() {
          children();
          difference() {
            translate([0, 0, -3.35]) import("../lib/choc_v1_switch.stl", convexity=2);
            translate([-10, -10, 0]) cube([20, 20, 20]);
          }
        }
        translate([-10, 0, -10]) cube([20, 20, 20]);
      }
    }

    if(DEBUG == true || DEBUG == "y") {
      translate([-20, -20, 0])
      difference() {
        union() {
          children();
          difference() {
            translate([0, 0, -3.35]) import("../lib/choc_v1_switch.stl", convexity=2);
            translate([-10, -10, 0]) cube([20, 20, 20]);
          }
        }
        translate([0, -10, -10]) cube([20, 20, 20]);
      }
    }
  }
}
