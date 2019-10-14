const HOURS_DAY = 24;
const HOUR_MIN = 60;
const DAY_MIN = HOUR_MIN * HOURS_DAY;

const DOM = 0;
const SEG = 1;
const TER = 2;
const QUA = 3;
const QUI = 4;
const SEX = 5;
const SAB = 6;

// week_day = int[0..6]
// hour = int[0..23]
// min = int[0..59]
// week_start_on = sunday

function zero_pad(val) {
    return ("00" + val).substr(-2, 2);
}

function get_csv_path() {
    // let domain = window.location.origin;
    // let base_path = window.location.pathname.split("/").slice(0, -1).join("/") + "/";
    // return domain + base_path + 'dataset/test.csv';
    return 'file:///home/matheusjardimb/workspace/VDH-20192/dataset/test.csv';
}