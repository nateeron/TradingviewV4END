const SETTING_PERCEN_BUY = 0.45;
const SETTING_PERCEN_SELL = 0.55;

function c_b(p) {
    p_B = p - (p / 100) * SETTING_PERCEN_BUY;
    return p_B;
}
function c_s(p) {
    p_B = p + (p / 100) * SETTING_PERCEN_SELL;
    return p_B;
}

let plotline;

function plotLine(price) {
    try {
        if (plotline) {
            chart.removeSeries(plotline);
        }

        plotline = chart.addLineSeries({
            color: "#910db9",
            lineWidth: 2,
            // disabling built-in price lines
            lastValueVisible: false,
            priceLineVisible: false,
        });
        plotline.setData(price);
    } catch (error) {
        console.log(error);
    }
}

function mark_S(location, c_mark) {
    if (c_mark > 0) {
        return {
            time: location,
            position: "aboveBar",
            color: "#822ee2",
            shape: "arrowDown",
            text: "Sell" + c_mark,
        };
    } else {
        return {
            time: location,
            position: "aboveBar",
            color: "#992FB9",
            shape: "arrowDown",
            text: "Sell",
        };
    }
}
function mark_B(location) {
    return {
        time: location,
        position: "belowBar",
        color: "#3568f3",
        shape: "arrowUp",
        text: "Buy",
    };
}

function cal_NetPorfit(orderval, tp, lowBuy, com, OrderSell) {
    const PercenTP = (orderval / 100) * (tp - com);
    const tp_ = PercenTP * OrderSell;
    console.log(orderval, tp, lowBuy, com, OrderSell);
    console.log(PercenTP);
    console.log(orderval + PercenTP, OrderSell);
    console.log(tp_);

    return tp_.toFixed(2);
}

const txt_Action_B = document.getElementById("Action_B");
const txt_Action_S = document.getElementById("Action_S");
const txt_Action_Day = document.getElementById("Action_D");
const txt_Dxy = document.getElementById("Dxy");

const txt_Order_Val = document.getElementById("Order_Val");
const txt_low_Buy = document.getElementById("low_Buy");
const txt_TP_Val = document.getElementById("TP_Val");
const txt_Net_profit = document.getElementById("Net_profit");
const com = 0.1 * 2; // ค่าคอมมิชั่น
function BotGrid(data, TF) {
    
    txt_Order_Val.value = 16;
    txt_low_Buy.value = 0.45;
    txt_TP_Val.value = 0.55;
    //console.log("BotGrid",data)
    let p = 0;
    let p_buy = [];
    let p_sell = 0;
    let p_Action = 0;
    let last_ACTION = "BUY"; // BUY | SELL

    let markers = [];
    let All_Sell = [];
    let Count_B = 0;
    let Count_S = 0;
    const ss = data.map((x, i) => {
        // console.log(x.close,i)
        const plot = x.time;
        // console.log(i, p_Action, x.close, plot);

        if (p_Action == 0) {
            // Action BUY
            p_Action = x.close;
            last_ACTION = "BUY";
            //console.log("BUY");
            Count_B = Count_B + 1;
            markers = markers.concat(mark_B(plot));
            p_buy = p_buy.concat(x.close);
        }
        let c_mark = 0;
        //แสดงจุดซื้อขาย
        p_buy.forEach((pB, index) => {
            if (x.close > c_s(pB) || x.high > c_s(pB)) {
                // Action Sell
                p_Action = x.close;
                last_ACTION = "SELL";
                //  console.log("SELL");

                markers = markers.concat(mark_S(plot, c_mark));
                c_mark = c_mark + 1;
                Count_S = Count_S + 1;
                // Remove the current element from the array
                p_buy.splice(index, 1);
                for (let index = 0; index < 2; index++) {
                    // console.log("StartNewTime", plot + StartNewTime(TF, index + 1));
                    //All_Sell = All_Sell.concat({time: plot+StartNewTime(TF,index) ,value:null})
                    All_Sell = All_Sell.concat({ time: plot, value: p_Action });
                }

                plotLine(All_Sell);
            }
        });

        if (x.close < c_b(p_Action) || x.low < c_b(p_Action)) {
            // Action BUY
            p_Action = x.close;
            last_ACTION = "BUY";
            // console.log("BUY");
            Count_B = Count_B + 1;
            markers = markers.concat(mark_B(plot));
            p_buy = p_buy.concat(x.close);
        }
        if (p_buy.length == 0) {
            //console.log(plot);
            // Action BUY
            p_Action = x.close;
            last_ACTION = "BUY";
            //console.log("BUY");
            Count_B = Count_B + 1;
            markers = markers.concat(mark_B(plot));
            p_buy = p_buy.concat(x.close);
        }
        // else if (last_ACTION == "BUY" && x.close < c_b(p_Action)) {
        //    // Action BUY
        //    p_Action = x.close;
        //    last_ACTION = "BUY";
        //    console.log("BUY");
        //    markers = markers.concat(mark_B(plot));
        //    Count_B = Count_B + 1;
        //} else if (last_ACTION == "SELL" && x.close > c_s(p_Action)) {
        //    // Action Sell
        //    p_Action = x.close;
        //    last_ACTION = "SELL";
        //    console.log("SELL");
        //    markers = markers.concat(mark_S(plot));
        //    Count_S = Count_S + 1;
        //}
    });

    const day_start = data[0].time;
    const day_end = data[data.length - 1].time;
    txt_Action_B.innerHTML = Count_B;
    txt_Action_S.innerHTML = Count_S;
    txt_Dxy.innerHTML = parseFloat(Count_B) - parseFloat(Count_S);
    txt_Action_Day.innerHTML = cal_days(day_start, day_end);
    const pf = cal_NetPorfit(txt_Order_Val.value, txt_TP_Val.value, txt_low_Buy.value, com, txt_Action_S.innerText);

    txt_Net_profit.innerHTML = pf + "$ THB:" + pf * 35;

    //console.log(markers);
    return markers;
}

txt_Order_Val.addEventListener("change", function () {
    const pf = cal_NetPorfit(txt_Order_Val.value, txt_TP_Val.value, txt_low_Buy.value, com, txt_Action_S.innerText);
    txt_Net_profit.innerHTML = pf + "$ THB:" + pf * 35;
});

txt_TP_Val.addEventListener("change", function () {
    const pf = cal_NetPorfit(txt_Order_Val.value, txt_TP_Val.value, txt_low_Buy.value, com, txt_Action_S.innerText);
    txt_Net_profit.innerHTML = pf + "$ THB:" + pf * 35;
});

txt_low_Buy.addEventListener("change", function () {
    const pf = cal_NetPorfit(txt_Order_Val.value, txt_TP_Val.value, txt_low_Buy.value, com, txt_Action_S.innerText);
    txt_Net_profit.innerHTML = pf + "$ THB:" + pf * 35;
});

function cal_days(t1, t2) {
    const date1 = new Date(t1 * 1000); // Convert to milliseconds
    const date2 = new Date(t2 * 1000);
    const timeDifference = date2 - date1; // Difference in milliseconds
    const dayDifference = (timeDifference / (1000 * 60 * 60 * 24)).toFixed(2); // Convert milliseconds to days

    // console.log(`Difference in days: ${dayDifference}`);
    return dayDifference;
}
