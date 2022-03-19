$fn=30;

translate([80,0])
difference(){
    base();
    union() {
        //translate([(70-45.5)/2,20])
        //square([45.5,35]);
        translate([(70-45.2)/2,20+0.15])
        square([45.2,5]);
        translate([(70-45.2)/2,50-0.15])
        square([45.2,5]);
    }
    translate([15,75])
    poti();
    translate([35,75])
    poti();
    translate([55,75])
    poti();
}

difference(){
    base();
    union() {
        translate([(70-45.5)/2,20])
        square([45.5,35]);
    }
    //translate([15,75])
    //poti();
    //translate([35,75])
    //poti();
    //translate([55,75])
    //poti();
}

//translate([(70-45.2)/2,20+0.15])
//square([45.2,5]);
//translate([(70-45.2)/2,50-0.15])
//square([45.2,5]);

translate([-20,0])
square([10,10]);

translate([-40,5])
difference() {
    circle(5);
    circle(2);
}

translate([-80,20])
difference() {
    union() {
        translate([35,10])
        square([50,10],true);
        translate([10,10])
        circle(5);
        translate([60,10])
        circle(5);
    }
    translate([10,10])
    circle(2);
    translate([60,10])
    circle(2);
}

module base() {
    difference() {
        union() {
            difference() {
                square([70,100]);
                square([10,10]);
                translate([0,90])
                square([10,10]);
                translate([60,90])
                square([10,10]);
                translate([60,0])
                square([10,10]);
            }
            translate([10,10])
            circle(10);
            translate([10,90])
            circle(10);
            translate([60,90])
            circle(10);
            translate([60,10])
            circle(10);
        }
            translate([10,10])
            circle(2);
            translate([10,90])
            circle(2);
            translate([60,90])
            circle(2);
            translate([60,10])
            circle(2);       
    }
}

module poti() {
    circle(6.2/2);
    translate([-11+6.2/2,0])
    square([0.5,2],true);
}
        

