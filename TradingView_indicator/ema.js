
let maSeries;
let maSeries2;




function ma(candleData, maLength) {
    const maData = [];

    for (let i = 0; i < candleData.length; i++) {
        if (i < maLength) {
            // Provide whitespace data points until the MA can be calculated
            maData.push({ time: candleData[i].time });
        } else {
            // Calculate the moving average, slow but simple way
            let sum = 0;
            for (let j = 0; j < maLength; j++) {
                sum += candleData[i - j].close;
            }
            const maValue = sum / maLength;
            maData.push({ time: candleData[i].time, value: maValue });
        }
    }

    return maData;
}

function calculateMovingAverageSeriesData(candleData, maLength) {
    const maData = [];

    for (let i = 0; i < candleData.length; i++) {
        if (i < maLength) {
            // Provide whitespace data points until the MA can be calculated
            maData.push({ time: candleData[i].time });
        } else {
            // Calculate the moving average, slow but simple way
            let sum = 0;
            for (let j = 0; j < maLength; j++) {
                sum += candleData[i - j].close;
            }
            const maValue = sum / maLength;
            maData.push({ time: candleData[i].time, value: maValue });
        }
    }
    return maData;
}

function updateMovingAverageSeries(candleData, period) {
      try {
          if (maSeries) {
              chart.removeSeries(maSeries);
          }
          const maData = calculateMovingAverageSeriesData(candleData, period);

          if (maData.length > 0) {
            maData.pop(); // Remove the last element from the moving average data
        }

          maSeries = chart.addLineSeries({ color: '#CA7B05', lineWidth: 1,
             // disabling built-in price lines
    lastValueVisible: false,
    priceLineVisible: false,
           });
          maSeries.setData(maData);
      } catch (error) {
          console.log(error)
      }
  }

  function updateMovingAverageSeries2(candleData, period) {

      try {

          if (maSeries2) {
              chart.removeSeries(maSeries2);
          }
          const maData = calculateMovingAverageSeriesData(candleData, period);
          maSeries2 = chart.addLineSeries({ color: '#69B90D', lineWidth: 1  ,
            // disabling built-in price lines
            lastValueVisible: false,
            priceLineVisible: false,});
          maSeries2.setData(maData);
      } catch (error) {
          console.log(error)
      }
  }
  document.addEventListener('DOMContentLoaded', function () {


  })
