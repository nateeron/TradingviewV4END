
let ws = new WebSocket('wss://stream.binance.com:9443/ws/xrpusdt@trade')

const showdatastockPrice = document.getElementById('stock-price')

ws.onmessage = (event) => {
    let stockOpject = JSON.parse(event.data)
    console.log(stockOpject.p);
    showdatastockPrice.innerText = parseFloat(stockOpject.p).toFixed(4)
}

let ws2 = new WebSocket('wss://stream.binance.com:9443/ws/bnbusdt@trade')

const showdatastockPrice2 = document.getElementById('stock-price2')

ws2.onmessage = (event) => {
    let stockOpject2 = JSON.parse(event.data)
    console.log(stockOpject2.p);
    showdatastockPrice2.innerText = parseFloat(stockOpject2.p).toFixed(2)
}