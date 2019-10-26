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

// NOTES
// week_day = int[0..6]
// hour = int[0..23]
// min = int[0..59]
// week_start_on = sunday

function zero_pad(val) {
    return ("00" + val).substr(-2, 2);
}

function week_day_to_str(week_day) {
    if (week_day === DOM) return 'Dom';
    if (week_day === SEG) return 'Seg';
    if (week_day === TER) return 'Ter';
    if (week_day === QUA) return 'Qua';
    if (week_day === QUI) return 'Qui';
    if (week_day === SEX) return 'Sex';
    if (week_day === SAB) return 'Sab';
}

function get_idx(week_day, hour, min) {
    return min + (hour * HOUR_MIN) + (week_day * DAY_MIN);
}

function get_str(idx) {
    if (idx < 0) return '--';

    idx = Math.trunc(idx);

    const week_day = Math.trunc(idx / DAY_MIN);
    if (week_day > SAB) return '--';
    const week_day_str = week_day_to_str(week_day);

    const aux_idx = idx - (week_day * DAY_MIN);
    const hour = Math.trunc(aux_idx / HOUR_MIN);

    const min = aux_idx - (hour * HOUR_MIN);
    return `${week_day_str} ${zero_pad(hour)}:${zero_pad(min)}`;
}

// function marker_options(radius) {
//     return {
//         radius: radius || 10,
//         // states: {
//         //     hover: {
//         //         enabled: true,
//         //         lineColor: 'rgb(100,100,100)'
//         //     }
//         // }
//     }
// }
